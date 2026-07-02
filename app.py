from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
import base64
import html
import json
import math
import sqlite3
import os
import random
import re
import struct
import subprocess
import sys
import tempfile

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

# Cerco i DB qui:
# - ./data (consigliato)

DB_DIRS = [
    os.path.join(app.root_path, "data"),
    app.root_path,
]
for d in DB_DIRS:
    os.makedirs(d, exist_ok=True)

IGNORE_DBS = {"dashboard.db", "study_sources.db"}
APP_PASSWORD = os.environ.get("APP_PASSWORD", "").strip()
PROGRESS_DB_PATH = os.environ.get(
    "PROGRESS_DB_PATH",
    os.path.join(app.instance_path, "user_progress.db"),
)
SOURCE_DB_PATH = os.environ.get(
    "SOURCE_DB_PATH",
    os.path.join(app.root_path, "data", "study_sources.db"),
)
TUTORIAL_PATH = os.environ.get(
    "TUTORIAL_PATH",
    os.path.join(app.root_path, "data", "python_tutorial.json"),
)
ARCHITECTURE_SOURCE_KEY = "architecture"
SUBJECT_PROFILES_STATE_KEY = "subject_study_profiles"
ARCHITECTURE_TRANSCRIPTS_DIR = os.path.join(
    app.root_path,
    "data",
    "architecture_video_transcripts",
)

REVIEW_INTERVALS = {
    0: timedelta(minutes=20),
    1: timedelta(days=1),
    2: timedelta(days=3),
    3: timedelta(days=7),
    4: timedelta(days=14),
    5: timedelta(days=30),
}


def utc_now():
    return datetime.now(timezone.utc)


def iso_now():
    return utc_now().isoformat(timespec="seconds")


def parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def get_progress_connection():
    os.makedirs(os.path.dirname(PROGRESS_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(PROGRESS_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_source_connection():
    conn = sqlite3.connect(SOURCE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_progress_db():
    conn = get_progress_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS question_stats (
            subject_key TEXT NOT NULL,
            question_id INTEGER NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 0,
            correct_count INTEGER NOT NULL DEFAULT 0,
            wrong_count INTEGER NOT NULL DEFAULT 0,
            correct_streak INTEGER NOT NULL DEFAULT 0,
            wrong_streak INTEGER NOT NULL DEFAULT 0,
            confidence INTEGER NOT NULL DEFAULT 0,
            box INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'new',
            last_seen_at TEXT,
            last_wrong_at TEXT,
            due_at TEXT,
            PRIMARY KEY (subject_key, question_id)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_key TEXT NOT NULL,
            question_id INTEGER NOT NULL,
            selected_answer_id INTEGER,
            correct_answer_id INTEGER,
            is_correct INTEGER NOT NULL,
            mode TEXT,
            self_rating TEXT,
            answered_at TEXT NOT NULL
        )
        """
    )
    cur.execute("PRAGMA table_info(attempts)")
    attempt_columns = {row[1] for row in cur.fetchall()}
    if "error_reason" not in attempt_columns:
        cur.execute("ALTER TABLE attempts ADD COLUMN error_reason TEXT")
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS explanations (
            subject_key TEXT NOT NULL,
            question_id INTEGER NOT NULL,
            note TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY (subject_key, question_id)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS app_state (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_question_stats_subject_due "
        "ON question_stats(subject_key, due_at)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_attempts_subject_time "
        "ON attempts(subject_key, answered_at)"
    )
    conn.commit()
    conn.close()


def _title_from_filename(filename: str) -> str:
    name = os.path.splitext(os.path.basename(filename))[0]
    name = name.replace("-", " ").replace("_", " ").strip()
    # rimuove suffissi comuni
    for suffix in (" quiz", " db"):
        if name.lower().endswith(suffix):
            name = name[: -len(suffix)].strip()
    return name.title() if name else "Materia"


def get_subject_label(db_path: str) -> str:
    """Legge il nome materia da meta.subject, fallback sul filename."""
    fallback = _title_from_filename(db_path)
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT value FROM meta WHERE key='subject' LIMIT 1")
        row = cur.fetchone()
        conn.close()
        if row and row[0]:
            return str(row[0]).strip()
    except Exception:
        pass
    return fallback


def scan_databases():
    """Ritorna: {db_key: {path, label}}. db_key = path relativo alla root."""
    dbs = {}
    for base in DB_DIRS:
        if not os.path.isdir(base):
            continue
        for fname in os.listdir(base):
            if not fname.lower().endswith(".db"):
                continue
            if fname in IGNORE_DBS:
                continue
            full = os.path.join(base, fname)
            if not os.path.isfile(full):
                continue
            key = os.path.relpath(full, app.root_path).replace("\\", "/")
            dbs[key] = {"path": full, "label": get_subject_label(full)}
    return dbs


def get_subject_key():
    dbs = scan_databases()
    active = session.get("db_key")
    if not active or active not in dbs:
        return None
    return active


def get_db_path():
    dbs = scan_databases()
    active = session.get("db_key")
    if not active or active not in dbs:
        return None
    return dbs[active]["path"]


def get_connection():
    db_path = get_db_path()
    if not db_path:
        raise RuntimeError("Nessun database selezionato")
    return sqlite3.connect(db_path)


def build_question_payload(cursor, question_id, include_images=True):
    cursor.execute("SELECT id, testo, immagine FROM questions WHERE id = ?", (question_id,))
    row = cursor.fetchone()
    if row is None:
        return None

    q_id, testo, img_blob = row
    image_b64 = (
        base64.b64encode(img_blob).decode("utf-8")
        if img_blob is not None and include_images
        else None
    )

    cursor.execute(
        "SELECT id, testo, corretta, immagine FROM answers WHERE domanda_id = ?",
        (q_id,),
    )

    answers = []
    correct_id = None
    for ans_id, ans_text, corretta, ans_blob in cursor.fetchall():
        ans_img_b64 = (
            base64.b64encode(ans_blob).decode("utf-8")
            if ans_blob is not None and include_images
            else None
        )
        answers.append({"id": ans_id, "testo": ans_text, "immagine": ans_img_b64})
        if corretta:
            correct_id = ans_id

    return {"id": q_id, "testo": testo, "immagine": image_b64, "risposte": answers, "corretta": correct_id}


def require_db_selected():
    if not get_db_path():
        return jsonify({"error": "Seleziona prima una materia"}), 400
    return None


def empty_stats(question_id):
    return {
        "question_id": question_id,
        "attempts": 0,
        "correct_count": 0,
        "wrong_count": 0,
        "correct_streak": 0,
        "wrong_streak": 0,
        "confidence": 0,
        "box": 0,
        "status": "new",
        "last_seen_at": None,
        "last_wrong_at": None,
        "due_at": None,
    }


def row_to_stats(row, question_id=None):
    if not row:
        return empty_stats(question_id)
    data = dict(row)
    data.pop("subject_key", None)
    return data


def classify_status(attempts, wrong_count, correct_streak, wrong_streak, box, rating):
    if attempts <= 0:
        return "new"
    if rating == "dont_know" or wrong_streak > 0:
        return "weak" if wrong_count >= 2 or rating == "dont_know" else "shaky"
    if rating == "unsure":
        return "shaky"
    if box >= 4 and correct_streak >= 3:
        return "mastered"
    if box >= 2:
        return "solid"
    return "learning"


def due_for_box(box):
    return (utc_now() + REVIEW_INTERVALS.get(box, REVIEW_INTERVALS[5])).isoformat(
        timespec="seconds"
    )


def fetch_stats_map(subject_key, question_ids=None):
    conn = get_progress_connection()
    cur = conn.cursor()
    if question_ids:
        placeholders = ",".join("?" for _ in question_ids)
        cur.execute(
            f"""
            SELECT * FROM question_stats
            WHERE subject_key = ? AND question_id IN ({placeholders})
            """,
            [subject_key, *question_ids],
        )
    else:
        cur.execute(
            "SELECT * FROM question_stats WHERE subject_key = ?",
            (subject_key,),
        )
    rows = cur.fetchall()
    conn.close()
    return {row["question_id"]: row_to_stats(row) for row in rows}


def attach_progress(questions):
    subject_key = get_subject_key()
    if not subject_key or not questions:
        return questions
    ids = [q["id"] for q in questions]
    stats = fetch_stats_map(subject_key, ids)
    for q in questions:
        q["progress"] = stats.get(q["id"], empty_stats(q["id"]))
    return questions


def read_app_state(key):
    conn = get_progress_connection()
    cur = conn.cursor()
    cur.execute("SELECT value, updated_at FROM app_state WHERE key = ?", (key,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    try:
        value = json.loads(row["value"])
    except json.JSONDecodeError:
        value = None
    return {"value": value, "updated_at": row["updated_at"]}


def write_app_state(key, value):
    updated_at = iso_now()
    conn = get_progress_connection()
    conn.execute(
        """
        INSERT INTO app_state(key, value, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET
            value = excluded.value,
            updated_at = excluded.updated_at
        """,
        (key, json.dumps(value, ensure_ascii=False), updated_at),
    )
    conn.commit()
    conn.close()
    return updated_at


def delete_app_state(key):
    conn = get_progress_connection()
    conn.execute("DELETE FROM app_state WHERE key = ?", (key,))
    conn.commit()
    conn.close()


def read_subject_profiles():
    stored = read_app_state(SUBJECT_PROFILES_STATE_KEY)
    value = stored["value"] if stored else {}
    return value if isinstance(value, dict) else {}


def write_subject_profiles(profiles):
    return write_app_state(SUBJECT_PROFILES_STATE_KEY, profiles)


def clean_subject_profile(data):
    data = data or {}
    exam_date = str(data.get("exam_date") or "").strip()
    if exam_date:
        try:
            datetime.fromisoformat(exam_date).date()
        except ValueError:
            raise ValueError("Data esame non valida")

    return {
        "exam_date": exam_date,
        "study_minutes": clamp(safe_int(data.get("study_minutes"), 45), 10, 240),
        "target_grade": clamp(safe_int(data.get("target_grade"), 24), 18, 30),
        "updated_at": iso_now(),
    }


def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


SOURCE_STOPWORDS = {
    "alla", "allo", "agli", "alle", "che", "con", "dal", "dalla", "dalle",
    "dello", "della", "delle", "degli", "dei", "del", "di", "e", "gli",
    "il", "in", "la", "le", "lo", "ma", "nel", "nella", "nelle", "per",
    "piu", "puo", "quale", "quando", "sono", "sua", "sue", "sui", "sul",
    "sulla", "tra", "un", "una", "uno", "come", "anche", "essere", "viene",
    "vengono", "dopo", "prima", "questo", "questa", "questi", "queste",
    "dunque", "infatti", "quindi", "ai", "al", "ed", "ad", "da", "si",
    "non", "più", "può",
}

SUBJECT_TOPIC_KEYWORDS = {
    "programmazione": [
        {
            "id": "python_base",
            "label": "Python base",
            "terms": ["python", "print", "input", "variabile", "assegnazione", "operatore", "tipo", "int", "float", "str", "bool"],
        },
        {
            "id": "controllo_flusso",
            "label": "If, cicli e condizioni",
            "terms": ["if", "elif", "else", "for", "while", "range", "break", "continue", "condizione", "iterazione", "ciclo"],
        },
        {
            "id": "funzioni_scope",
            "label": "Funzioni e scope",
            "terms": ["def", "funzione", "return", "parametro", "argomento", "scope", "globale", "locale", "lambda", "ricorsione"],
        },
        {
            "id": "strutture_dati",
            "label": "Liste, tuple, dizionari",
            "terms": ["lista", "liste", "tuple", "tupla", "dizionario", "dict", "set", "insieme", "append", "pop", "chiave", "indice"],
        },
        {
            "id": "oop",
            "label": "Classi e oggetti",
            "terms": ["classe", "oggetto", "metodo", "attributo", "self", "ereditarieta", "polimorfismo", "costruttore", "__init__"],
        },
        {
            "id": "eccezioni_file",
            "label": "Eccezioni e file",
            "terms": ["try", "except", "finally", "raise", "eccezione", "errore", "file", "open", "read", "write"],
        },
        {
            "id": "algoritmi",
            "label": "Algoritmi e complessita",
            "terms": ["algoritmo", "complessita", "ordinamento", "ricerca", "binaria", "lista", "tempo", "o(", "complessità"],
        },
    ],
    "diritto": [
        {
            "id": "privacy_gdpr",
            "label": "Privacy e GDPR",
            "terms": ["gdpr", "privacy", "dato", "dati", "personale", "trattamento", "consenso", "titolare", "responsabile", "interessato"],
        },
        {
            "id": "contratti_digitali",
            "label": "Contratti digitali",
            "terms": ["contratto", "contratti", "firma", "digitale", "elettronica", "validita", "clausola", "obbligazione", "adempimento"],
        },
        {
            "id": "ecommerce_consumatori",
            "label": "E-commerce e consumatori",
            "terms": ["consumatore", "ecommerce", "commercio", "recesso", "vendita", "online", "informativa", "piattaforma", "marketplace"],
        },
        {
            "id": "proprieta_intellettuale",
            "label": "Proprieta intellettuale",
            "terms": ["copyright", "diritto", "autore", "marchio", "brevetto", "licenza", "software", "opera", "proprieta"],
        },
        {
            "id": "responsabilita_sicurezza",
            "label": "Responsabilita e sicurezza",
            "terms": ["responsabilita", "sicurezza", "cybersecurity", "danno", "illecito", "rischio", "misure", "sanzione"],
        },
        {
            "id": "societa_startup",
            "label": "Societa e startup",
            "terms": ["societa", "startup", "impresa", "azienda", "capitale", "socio", "amministratore", "pmi"],
        },
    ],
}


def normalize_source_word(word):
    replacements = str.maketrans("àèéìòù", "aeeiou")
    word = str(word).lower().translate(replacements)
    return re.sub(r"[^a-z0-9_]", "", word)


def source_terms(text):
    import re as _re

    words = [
        normalize_source_word(w)
        for w in _re.findall(r"\b[\wÀ-ÿ]{4,}\b", str(text or ""))
    ]
    return {
        w
        for w in words
        if w and w not in SOURCE_STOPWORDS and not w.isdigit()
    }


def subject_topic_definitions(subject_key):
    subject = str(subject_key or "").lower()
    if "programmazione" in subject:
        return SUBJECT_TOPIC_KEYWORDS["programmazione"]
    if "diritto" in subject:
        return SUBJECT_TOPIC_KEYWORDS["diritto"]
    return []


def topic_keyword_terms(topic):
    terms = set()
    for raw in topic.get("terms", []):
        normalized = normalize_source_word(raw)
        if normalized:
            terms.add(normalized)
        terms.update(source_terms(raw))
    return terms


def text_match_terms(text):
    raw_words = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", str(text or ""))
    terms = source_terms(text)
    terms.update(
        normalize_source_word(word)
        for word in raw_words
        if len(word) >= 2 and normalize_source_word(word) not in SOURCE_STOPWORDS
    )
    return {term for term in terms if term}


def fetch_question_blobs(question_ids):
    ids = [safe_int(qid, 0) for qid in question_ids or [] if safe_int(qid, 0)]
    if not ids:
        return {}

    placeholders = ",".join("?" for _ in ids)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT q.id, q.testo, GROUP_CONCAT(COALESCE(a.testo, ''), ' ') AS answers_text
        FROM questions q
        LEFT JOIN answers a ON a.domanda_id = q.id
        WHERE q.id IN ({placeholders})
        GROUP BY q.id, q.testo
        """,
        ids,
    )
    blobs = {
        row[0]: decode_quiz_text(f"{row[1] or ''} {row[2] or ''}")
        for row in cur.fetchall()
    }
    conn.close()
    return blobs


def match_question_topic(text, definitions):
    if not definitions:
        return None

    normalized_text = " ".join(sorted(text_match_terms(text)))
    words = set(normalized_text.split())
    best_topic = None
    best_score = 0
    for topic in definitions:
        score = 0
        for term in topic_keyword_terms(topic):
            if not term:
                continue
            if term in words:
                score += 4
            elif len(term) >= 4 and term in normalized_text:
                score += 1
        if score > best_score:
            best_topic = topic.get("id")
            best_score = score
    return best_topic if best_score > 0 else None


def filter_question_ids_by_topic(subject_key, question_ids, topic_id):
    topic_id = normalize_source_word(topic_id)
    if not topic_id or topic_id in {"all", "mixed", "general"}:
        return list(question_ids or [])

    definitions = subject_topic_definitions(subject_key)
    valid_ids = {topic.get("id") for topic in definitions}
    if not definitions or topic_id not in valid_ids:
        return list(question_ids or [])

    blobs = fetch_question_blobs(question_ids)
    return [
        qid
        for qid in question_ids
        if match_question_topic(blobs.get(qid, ""), definitions) == topic_id
    ]


def compact_excerpt(text, max_chars=620):
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars].rsplit(" ", 1)[0]
    return f"{cut}..."


def find_study_sources(subject_key, query_text, limit=3):
    if not os.path.exists(SOURCE_DB_PATH):
        return []

    query_terms = source_terms(query_text)
    if not query_terms:
        return []

    conn = get_source_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT id, source_title, topic, content, keywords, page_start, page_end
            FROM study_notes
            WHERE subject_key = ?
            """,
            (subject_key,),
        )
    except sqlite3.Error:
        conn.close()
        return []
    scored = []
    for row in cur.fetchall():
        keyword_terms = set(str(row["keywords"] or "").split())
        topic_terms = source_terms(row["topic"])
        overlap = len(query_terms & keyword_terms)
        topic_overlap = len(query_terms & topic_terms)
        if overlap == 0 and topic_overlap == 0:
            continue
        score = overlap + topic_overlap * 2
        scored.append((score, row))
    conn.close()

    scored.sort(key=lambda item: item[0], reverse=True)
    notes = []
    for score, row in scored[:limit]:
        notes.append(
            {
                "source_title": row["source_title"],
                "topic": row["topic"],
                "excerpt": compact_excerpt(row["content"]),
                "full_text": repair_text(row["content"]).strip(),
                "page_start": row["page_start"],
                "page_end": row["page_end"],
                "score": score,
            }
        )
    return notes


def is_programming_subject(subject_key):
    return "programmazione" in str(subject_key or "").lower()


def decode_quiz_text(value):
    text = html.unescape(str(value or ""))
    text = text.replace("\xa0", " ")
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in text.split("\n")).strip()


def looks_like_python_line(line):
    stripped = str(line or "").strip()
    if not stripped:
        return False
    starters = (
        "if ", "elif ", "else", "for ", "while ", "def ", "class ", "try",
        "except", "finally", "with ", "print", "return", "import ", "from ",
        "break", "continue", "pass", "raise ",
    )
    if stripped.startswith(starters):
        return True
    if re.match(r"^[A-Za-z_]\w*\s*(=|\+=|-=|\*=|/=|//=|%=)", stripped):
        return True
    return bool(
        re.search(r"\b(range|len|int|float|str|set|list|dict|format)\s*\(", stripped)
        and any(char in stripped for char in ("(", ")", "=", ":"))
    )


def split_inline_python(line):
    text = str(line or "").strip()
    lower = text.lower()
    italian_prefixes = (
        "in python",
        "il codice",
        "se dal codice",
        "nel codice",
        "nell'istruzione",
        "nella funzione",
        "nell'ambito",
    )
    if looks_like_python_line(text) and not lower.startswith(italian_prefixes):
        return "", text

    markers = (
        "istruzione",
        "istruzioni",
        "funzione",
        "blocco di istruzioni",
        "codice",
    )
    lower = text.lower()
    candidates = []
    for marker in markers:
        index = lower.find(marker)
        if index >= 0:
            candidates.append(index + len(marker))

    for index in sorted(candidates):
        tail = text[index:].lstrip(" :")
        if looks_like_python_line(tail):
            return text[:index].strip(" :"), tail

    match = re.search(
        r"\b(if|elif|else|for|while|def|class|print|return|[A-Za-z_]\w*\s*=)\b",
        text,
    )
    if match:
        tail = text[match.start():].strip()
        if looks_like_python_line(tail):
            return text[: match.start()].strip(" :"), tail

    return text, ""


def normalize_code_lines(lines):
    cleaned = [line.rstrip() for line in lines if str(line or "").strip()]
    if not cleaned:
        return ""

    indents = [
        len(re.match(r"^\s*", line).group(0))
        for line in cleaned
        if line.strip()
    ]
    common_indent = min(indents) if indents else 0
    if common_indent:
        cleaned = [line[common_indent:] for line in cleaned]
    return "\n".join(cleaned).strip()


def extract_python_code(*texts):
    code_lines = []
    for value in texts:
        text = decode_quiz_text(value)
        if not text:
            continue

        in_code = False
        for raw_line in text.split("\n"):
            line = raw_line.replace("\t", "    ")
            stripped = line.strip()
            if not stripped:
                if in_code and code_lines:
                    code_lines.append("")
                continue

            _, inline_code = split_inline_python(stripped)
            candidate = inline_code or line
            if inline_code and inline_code == stripped and line != stripped:
                candidate = line
            if looks_like_python_line(candidate):
                in_code = True
                code_lines.append(candidate)
                continue

            if in_code:
                end_markers = (
                    "visualizza",
                    "produce",
                    "e:",
                    "risulta",
                    "serve",
                    "calcola",
                    "quale",
                )
                if any(stripped.lower().startswith(marker) for marker in end_markers):
                    in_code = False
                    continue
                if any(token in stripped for token in ("=", ":", "(", ")")):
                    code_lines.append(line)

    return normalize_code_lines(code_lines)


def unsafe_python_reason(code):
    lowered = code.lower()
    blocked_terms = (
        "__",
        "import ",
        "from ",
        "open(",
        "input(",
        "eval(",
        "exec(",
        "compile(",
        "globals(",
        "locals(",
        "vars(",
        "breakpoint(",
        "subprocess",
        "socket",
        "requests",
        "urllib",
        "pathlib",
        "shutil",
        "os.",
        "sys.",
    )
    for term in blocked_terms:
        if term in lowered:
            return "Questo frammento non viene eseguito per sicurezza: contiene accesso a file, rete, input o import."
    if len(code) > 1200:
        return "Questo frammento e troppo lungo per il laboratorio rapido."
    return None


def last_assigned_name(code):
    matches = re.findall(
        r"^\s*([A-Za-z_]\w*)\s*(?:=|\+=|-=|\*=|/=|//=|%=)",
        code,
        flags=re.MULTILINE,
    )
    if not matches:
        return ""
    return matches[-1]


def add_python_example_setup(code):
    assigned_names = set(re.findall(r"^\s*([A-Za-z_]\w*)\s*=", code, flags=re.MULTILINE))
    setup_lines = []
    if " a" in f" {code}" and "a" not in assigned_names and re.search(r"\bin\s+a\b", code):
        setup_lines.append("a = [1, 2, 3]")
    setup = "\n".join(setup_lines)
    runnable_lines = [*setup_lines, code]
    inspection = ""
    if "print(" not in code and not re.search(r"^\s*def\s+", code, flags=re.MULTILINE):
        inspection = last_assigned_name(code)
        if inspection:
            runnable_lines.append(f'print("{inspection} =", {inspection})')
    return setup, "\n".join(runnable_lines), inspection


def explain_python_result(code, stdout, stderr, returncode, setup="", inspection=""):
    error_line = ""
    if stderr:
        error_line = stderr.strip().splitlines()[-1]

    if "SyntaxError" in stderr:
        if re.search(r"\bif\b.+(?<![=!<>])=(?!=).+:", code):
            return "Python non lo esegue: dentro un if il confronto si fa con ==, mentre = prova ad assegnare un valore e crea un errore di sintassi."
        return "Python non lo esegue: c'e un errore di sintassi, quindi il programma si ferma prima di produrre output."

    if "NameError" in stderr:
        return f"Il frammento e incompleto da solo: manca una variabile o un valore iniziale. Errore mostrato da Python: {error_line}."

    if returncode != 0:
        return f"Python avvia il codice ma si ferma con errore: {error_line or 'errore di esecuzione'}."

    if stdout.strip():
        if inspection:
            return f"Per rendere visibile il risultato, stampo il valore finale di {inspection}: l'output e quello mostrato qui sotto."
        prefix = "Con i valori di esempio aggiunti, " if setup else ""
        return f"{prefix}Python esegue il codice e stampa l'output mostrato qui sotto."

    if re.search(r"^\s*def\s+", code, flags=re.MULTILINE):
        return "Python definisce la funzione, ma non stampa nulla finche la funzione non viene chiamata."

    return "Python esegue il codice senza errori, ma non stampa nulla perche non c'e una print o un risultato visualizzato."


def run_python_lab(code):
    if not code:
        return None

    reason = unsafe_python_reason(code)
    if reason:
        return {
            "code": code,
            "status": "blocked",
            "stdout": "",
            "stderr": "",
            "returncode": None,
            "explanation": reason,
            "setup": "",
            "runnable_code": code,
        }

    setup, runnable_code, inspection = add_python_example_setup(code)
    env = {"PYTHONIOENCODING": "utf-8"}
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            proc = subprocess.run(
                [sys.executable, "-I", "-c", runnable_code],
                cwd=temp_dir,
                env=env,
                capture_output=True,
                text=True,
                timeout=2,
            )
    except subprocess.TimeoutExpired:
        return {
            "code": code,
            "status": "timeout",
            "stdout": "",
            "stderr": "",
            "returncode": None,
            "explanation": "Il codice non termina entro 2 secondi: probabilmente c'e un ciclo che non si chiude o un'operazione troppo lunga.",
            "setup": setup,
            "inspection": inspection,
            "runnable_code": runnable_code,
        }

    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()
    if len(stdout) > 1200:
        stdout = f"{stdout[:1200].rstrip()}\n..."
    if len(stderr) > 1200:
        stderr = f"{stderr[:1200].rstrip()}\n..."

    return {
        "code": code,
        "status": "ok" if proc.returncode == 0 else "error",
        "stdout": stdout,
        "stderr": stderr,
        "returncode": proc.returncode,
        "explanation": explain_python_result(
            code, stdout, stderr, proc.returncode, setup=setup, inspection=inspection
        ),
        "setup": setup,
        "inspection": inspection,
        "runnable_code": runnable_code,
    }


def build_python_lab(subject_key, question_text, correct_text, selected_text=""):
    if not is_programming_subject(subject_key):
        return None

    code = extract_python_code(question_text)
    label = "Codice nella domanda"
    if not code:
        code = extract_python_code(selected_text)
        label = "Codice scelto"
    if not code:
        code = extract_python_code(correct_text)
        label = "Codice della risposta corretta"
    if not code:
        return None

    lab = run_python_lab(code)
    if lab:
        lab["label"] = label
    return lab


TUTORIAL_RUNNER = r"""
import contextlib
import io
import json
import re
import sys
import traceback

payload = json.loads(sys.stdin.read() or "{}")
code = payload.get("code") or ""
checks = payload.get("checks") or []

allowed_builtins = {
    "print": print,
    "range": range,
    "len": len,
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,
    "sum": sum,
    "min": min,
    "max": max,
    "abs": abs,
    "round": round,
    "sorted": sorted,
    "enumerate": enumerate,
    "zip": zip,
    "any": any,
    "all": all,
}

namespace = {"__builtins__": allowed_builtins}
stdout_buffer = io.StringIO()
error = ""
error_info = None

def same_value(actual, expected):
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        return abs(actual - expected) < 0.000001
    return actual == expected

def printable(value):
    try:
        json.dumps(value)
        return value
    except TypeError:
        return repr(value)

try:
    with contextlib.redirect_stdout(stdout_buffer):
        compiled = compile(code, "<tutorial>", "exec")
        exec(compiled, namespace, namespace)
except Exception as exc:
    error = traceback.format_exc(limit=4)
    line_match = re.search(r'File "<tutorial>", line (\d+)', error)
    extracted = traceback.extract_tb(exc.__traceback__)
    user_frame = next((frame for frame in reversed(extracted) if frame.filename == "<tutorial>"), None)
    error_info = {
        "type": type(exc).__name__,
        "message": str(exc),
        "line": (
            getattr(exc, "lineno", None)
            or (user_frame.lineno if user_frame else None)
            or (int(line_match.group(1)) if line_match else None)
        ),
    }

stdout = stdout_buffer.getvalue()
if len(stdout) > 1600:
    stdout = stdout[:1600].rstrip() + "\n..."

results = []
if not error:
    for check in checks:
        label = check.get("label") or "Controllo"
        check_type = check.get("type")
        expected = check.get("value")
        actual = None
        passed = False
        detail = ""
        try:
            if check_type == "stdout_contains":
                actual = stdout
                passed = str(expected) in stdout
            elif check_type == "variable_equals":
                actual = namespace.get(check.get("name"))
                passed = same_value(actual, expected)
            elif check_type == "expression_equals":
                actual = eval(check.get("expression") or "", namespace, namespace)
                passed = same_value(actual, expected)
            elif check_type == "function_equals":
                actual = eval(check.get("call") or "", namespace, namespace)
                passed = same_value(actual, expected)
            else:
                detail = "Tipo di controllo non supportato."
        except Exception as exc:
            detail = f"{type(exc).__name__}: {exc}"
        if passed:
            feedback = "OK."
        elif check_type == "stdout_contains":
            feedback = f"Nel testo stampato non trovo {expected!r}."
        elif check_type == "variable_equals":
            feedback = f"La variabile {check.get('name')} non ha ancora il valore richiesto."
        elif check_type in {"expression_equals", "function_equals"}:
            feedback = "Il risultato calcolato non coincide con quello atteso."
        else:
            feedback = detail or "Questo controllo non e passato."

        results.append({
            "label": label,
            "passed": passed,
            "expected": printable(expected),
            "actual": printable(actual),
            "detail": detail,
            "feedback": feedback,
        })

success = bool(results) and all(item["passed"] for item in results) and not error
failed = [item for item in results if not item["passed"]]
if error_info:
    retry_message = "Correggi l'errore Python indicato e premi di nuovo Esegui e verifica."
elif failed:
    retry_message = "Correggi i controlli segnati come Da correggere e ritenta."
elif success:
    retry_message = "Perfetto: puoi passare alla prossima lezione."
else:
    retry_message = "Scrivi la soluzione e premi Esegui e verifica."

print(json.dumps({
    "stdout": stdout,
    "error": error,
    "error_info": error_info,
    "checks": results,
    "success": success,
    "retry_message": retry_message,
}, ensure_ascii=False))
"""


def load_python_tutorial_lessons():
    if not os.path.exists(TUTORIAL_PATH):
        return []
    with open(TUTORIAL_PATH, "r", encoding="utf-8") as handle:
        lessons = json.load(handle)
    for index, lesson in enumerate(lessons):
        lesson["index"] = index
    return lessons


def get_tutorial_state():
    stored = read_app_state("python_tutorial_progress")
    state = stored["value"] if stored and isinstance(stored.get("value"), dict) else {}
    completed = state.get("completed_lesson_ids") or []
    code_by_lesson = state.get("code_by_lesson") or {}
    return {
        "completed_lesson_ids": [
            str(item) for item in completed if isinstance(item, str)
        ],
        "active_lesson_id": state.get("active_lesson_id"),
        "code_by_lesson": {
            str(key): str(value)
            for key, value in code_by_lesson.items()
            if isinstance(key, str)
        },
        "updated_at": state.get("updated_at"),
    }


def save_tutorial_state(state):
    clean_state = {
        "completed_lesson_ids": sorted(set(state.get("completed_lesson_ids") or [])),
        "active_lesson_id": state.get("active_lesson_id"),
        "code_by_lesson": state.get("code_by_lesson") or {},
        "updated_at": iso_now(),
    }
    updated_at = write_app_state("python_tutorial_progress", clean_state)
    clean_state["updated_at"] = updated_at
    return clean_state


def tutorial_unlocked_ids(lessons, state):
    completed = set(state.get("completed_lesson_ids") or [])
    unlocked = []
    for lesson in lessons:
        unlocked.append(lesson["id"])
        if lesson["id"] not in completed:
            break
    return set(unlocked)


def find_tutorial_lesson(lessons, lesson_id):
    return next((lesson for lesson in lessons if lesson["id"] == lesson_id), None)


def public_tutorial_lesson(lesson, state, unlocked_ids, include_details=False):
    completed = set(state.get("completed_lesson_ids") or [])
    public = {
        "id": lesson["id"],
        "index": lesson["index"],
        "module": lesson.get("module", "Python"),
        "title": lesson.get("title", "Lezione"),
        "level": lesson.get("level", "base"),
        "goal": lesson.get("goal", ""),
        "completed": lesson["id"] in completed,
        "locked": lesson["id"] not in unlocked_ids,
    }
    if include_details:
        saved_code = state.get("code_by_lesson", {}).get(lesson["id"])
        public.update(
            {
                "concept": lesson.get("concept", ""),
                "task": lesson.get("task", ""),
                "starter_code": lesson.get("starter_code", ""),
                "code": saved_code if saved_code is not None else lesson.get("starter_code", ""),
                "hint": lesson.get("hint", ""),
                "success_message": lesson.get("success_message", "Lezione completata."),
            }
        )
    return public


def build_tutorial_payload(lessons, state, include_lessons=True):
    unlocked_ids = tutorial_unlocked_ids(lessons, state)
    active_id = state.get("active_lesson_id")
    if active_id not in unlocked_ids:
        active_id = lessons[0]["id"] if lessons else None
        state["active_lesson_id"] = active_id

    completed_count = len(set(state.get("completed_lesson_ids") or []))
    payload = {
        "active_lesson_id": active_id,
        "completed_count": completed_count,
        "total_count": len(lessons),
        "percent": round((completed_count / len(lessons)) * 100) if lessons else 0,
        "updated_at": state.get("updated_at"),
    }
    if include_lessons:
        payload["lessons"] = [
            public_tutorial_lesson(lesson, state, unlocked_ids)
            for lesson in lessons
        ]
    return payload


def run_tutorial_code(code, checks):
    reason = unsafe_python_reason(code)
    if reason:
        return {
            "stdout": "",
            "error": reason,
            "checks": [],
            "success": False,
            "blocked": True,
        }

    payload = {"code": code, "checks": checks}
    try:
        proc = subprocess.run(
            [sys.executable, "-I", "-c", TUTORIAL_RUNNER],
            input=json.dumps(payload, ensure_ascii=False),
            capture_output=True,
            text=True,
            timeout=3,
            env={"PYTHONIOENCODING": "utf-8"},
        )
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "error": "Il codice non termina entro 3 secondi. Controlla cicli while/for e condizioni di uscita.",
            "checks": [],
            "success": False,
            "timeout": True,
        }

    if proc.returncode != 0:
        return {
            "stdout": proc.stdout.strip(),
            "error": proc.stderr.strip() or "Errore durante la verifica del codice.",
            "checks": [],
            "success": False,
        }

    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {
            "stdout": proc.stdout.strip(),
            "error": "Risultato della verifica non leggibile.",
            "checks": [],
            "success": False,
        }


ARCHITECTURE_TOPICS = [
    {"id": "mixed", "label": "Misto esame"},
    {"id": "conversions", "label": "Conversioni basi"},
    {"id": "binary_arithmetic", "label": "Somme/sottrazioni binarie"},
    {"id": "twos", "label": "Complemento a 2"},
    {"id": "ieee754", "label": "IEEE 754"},
    {"id": "logic", "label": "Porte logiche e Boole"},
    {"id": "core", "label": "Fondamenti e registri"},
    {"id": "mips", "label": "MIPS / Assembly"},
    {"id": "memory_bus", "label": "Memoria e bus"},
    {"id": "microarchitecture", "label": "Microarchitettura / IJVM"},
    {"id": "clock", "label": "Clock e prestazioni"},
    {"id": "video_review", "label": "Dai video"},
]


def clean_arch_answer(value):
    text = str(value or "").strip().lower()
    text = text.replace(",", ".")
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"^\((.+)\)(?:_\d+|\d+|\(\d+\))?$", r"\1", text)
    text = re.sub(r"(?:_\d+|\(\d+\))$", "", text)
    text = text.replace("_", "")
    for token in ("0b", "₂", "(2)", "_2"):
        text = text.replace(token, "")
    return text


def to_base(value, base):
    digits = "0123456789ABCDEF"
    if value == 0:
        return "0"
    out = ""
    n = abs(value)
    while n:
        n, rem = divmod(n, base)
        out = digits[rem] + out
    return f"-{out}" if value < 0 else out


def parse_base_digits(digits, base):
    total = 0
    for char in str(digits).upper():
        total = total * base + int(char, 16)
    return total


def base_fraction_to_decimal(text, base):
    raw = str(text).replace(",", ".")
    integer, _, fraction = raw.partition(".")
    total = parse_base_digits(integer or "0", base)
    for index, char in enumerate(fraction, start=1):
        total += int(char, 16) * (base ** -index)
    return total


def twos_complement_bits(value, bits):
    if value < 0:
        value = (1 << bits) + value
    return format(value & ((1 << bits) - 1), f"0{bits}b")


def ieee754_single(value):
    packed = struct.pack(">f", float(value))
    raw = "".join(f"{byte:08b}" for byte in packed)
    return f"{raw[0]} {raw[1:9]} {raw[9:]}"


def arch_public_exercise(exercise):
    return {
        key: exercise[key]
        for key in (
            "id",
            "topic",
            "topic_label",
            "title",
            "prompt",
            "answer_type",
            "options",
            "placeholder",
            "hint",
            "guide",
            "example",
        )
        if key in exercise
    }


def arch_exercise_id():
    return f"arch-{random.randint(100000, 999999)}"


def architecture_default_guide(topic, title):
    guides = {
        "conversions": [
            "Prima leggi bene la base scritta in basso: (1011)_2 significa numero 1011 in base 2, non milleundici.",
            "Se devi andare in decimale, dai un peso a ogni cifra: da destra 2^0, 2^1, 2^2, ... oppure base^0, base^1, ...",
            "Se devi partire dal decimale, dividi per la base di arrivo e leggi i resti dal basso verso l'alto.",
        ],
        "binary_arithmetic": [
            "Allinea i numeri a destra come nelle operazioni in colonna delle elementari.",
            "In binario esistono solo 0 e 1: 1 + 1 non fa 2, fa 10, cioe scrivi 0 e porti 1.",
            "Dopo aver fatto i riporti, controlla convertendo in decimale: serve solo per verificare che non hai perso un riporto.",
        ],
        "twos": [
            "Guarda quanti bit chiede l'esercizio: 4 bit e 8 bit danno risposte diverse.",
            "Scrivi il numero positivo con zeri davanti fino ad arrivare a quei bit.",
            "Per il negativo: inverti tutti i bit, aggiungi 1 e tieni solo il numero di bit richiesto.",
        ],
        "ieee754": [
            "IEEE 754 singola precisione ha sempre tre pezzi: 1 bit di segno, 8 bit di esponente, 23 bit di mantissa.",
            "Prima converti il numero in binario, poi sposti la virgola fino alla forma 1.x * 2^e.",
            "Il segno vale 0 se positivo e 1 se negativo; l'esponente salvato e e + 127; la mantissa e la parte dopo 1.",
        ],
        "logic": [
            "Pensa alle porte come regole semplici: AND vuole tutto vero, OR vuole almeno un vero, NOT ribalta.",
            "Quando vedi una negazione fuori da AND/OR, usa De Morgan: cambi AND con OR e neghi gli ingressi.",
            "Se non sei sicuro, fai una mini tabella di verita con A e B: 00, 01, 10, 11.",
        ],
        "core": [
            "Prima capisci di quale pezzo del calcolatore parla la domanda: memoria, registri, PC, istruzione o modello di Von Neumann.",
            "Associa ogni parola al suo ruolo: il PC punta alla prossima istruzione, i registri sono piccoli e veloci, la memoria contiene dati e istruzioni.",
            "Scarta risposte di altri modelli: per esempio il nastro infinito richiama Turing, non Von Neumann.",
        ],
        "mips": [
            "Prima traduci il nome: load = carica, store = salva, branch = salto condizionato.",
            "Load va da memoria a registro; store va da registro a memoria.",
            "beq significa branch if equal, bne significa branch if not equal; addi somma un immediato.",
        ],
        "memory_bus": [
            "Se la domanda parla di memoria, separa sempre tre idee: dove sono i dati, come li indirizzi, come li trasferisci.",
            "L'ampiezza del bus indirizzi riguarda quante locazioni puoi selezionare; l'ampiezza del bus dati riguarda quanti bit trasferisci alla volta.",
            "Quando compare la temporizzazione, chiediti se i passaggi sono scanditi dal clock o da segnali di richiesta/risposta.",
        ],
        "microarchitecture": [
            "Parti dalla differenza tra ISA e microarchitettura: l'ISA dice quali istruzioni esistono, la microarchitettura dice come vengono eseguite.",
            "Una microistruzione attiva segnali di controllo sul datapath: registri, ALU, bus interni e memoria.",
            "Per velocizzare, spesso si riduce il numero di cicli o il percorso necessario per eseguire una istruzione.",
        ],
        "clock": [
            "Scrivi sempre la formula prima: tempo CPU = numero istruzioni x CPI / frequenza.",
            "Attenzione alle unita: MHz significa milioni di cicli al secondo, quindi moltiplica per 1.000.000.",
            "Se vuoi microsecondi, prima trovi i secondi e poi moltiplichi per 1.000.000.",
        ],
        "video_review": [
            "Queste domande sono generate dagli argomenti ricorrenti nei video, ma devi rispondere come in un esercizio normale.",
            "Prima riconosci il tema: memoria, bus, microarchitettura, MIPS, porte logiche o clock.",
            "Dopo la verifica puoi guardare la fonte video collegata per rinforzare il concetto.",
        ],
    }
    return guides.get(topic, ["Riconosci l'argomento, applica la regola chiave e controlla il risultato."])


def architecture_default_example(topic):
    examples = {
        "conversions": {
            "title": "Esempio: convertire (1011)_2 in decimale",
            "lines": [
                "Scrivi i pesi da destra: 2^0, 2^1, 2^2, 2^3.",
                "1011 significa: 1*2^3 + 0*2^2 + 1*2^1 + 1*2^0.",
                "Calcolo: 8 + 0 + 2 + 1 = 11. Quindi (1011)_2 = 11.",
            ],
        },
        "binary_arithmetic": {
            "title": "Esempio: 1011 + 111",
            "lines": [
                "Allinea a destra: 1011 + 0111.",
                "Da destra: 1+1=10, scrivi 0 e porti 1. Continua gestendo i riporti.",
                "Risultato: 10010. Controllo: 11 + 7 = 18, e 18 in binario e 10010.",
            ],
        },
        "twos": {
            "title": "Esempio: rappresentare -5 su 4 bit",
            "lines": [
                "+5 su 4 bit e 0101.",
                "Inverti i bit: 1010.",
                "Aggiungi 1: 1011. Quindi -5 in complemento a 2 su 4 bit e 1011.",
            ],
        },
        "ieee754": {
            "title": "Esempio: idea base per 8,25 in IEEE 754",
            "lines": [
                "8,25 in binario e 1000,01.",
                "Normalizzi: 1,00001 * 2^3.",
                "Segno 0; esponente salvato 3 + 127 = 130, cioe 10000010; mantissa 00001000000000000000000.",
            ],
        },
        "logic": {
            "title": "Esempio: negazione di AND",
            "lines": [
                "La frase NOT(A AND B) significa: non e vero che A e B sono entrambi veri.",
                "Per De Morgan diventa NOT A OR NOT B.",
                "Quindi se vedi la negazione di una congiunzione, passi a OR delle negazioni.",
            ],
        },
        "core": {
            "title": "Esempio: cosa fa il PC",
            "lines": [
                "Il PC non contiene il risultato di un calcolo.",
                "Il PC contiene l'indirizzo della prossima istruzione da leggere.",
                "Dopo il fetch viene aggiornato: di solito va avanti, oppure cambia se c'e un salto.",
            ],
        },
        "mips": {
            "title": "Esempio: capire lw e sw",
            "lines": [
                "lw $t0, 12($s1) significa: carica una word dalla memoria nel registro $t0.",
                "L'indirizzo di memoria e $s1 + 12.",
                "sw fa il contrario: prende il valore da un registro e lo salva in memoria.",
            ],
        },
        "memory_bus": {
            "title": "Esempio: bus indirizzi e bus dati",
            "lines": [
                "Con 16 linee di indirizzo puoi selezionare 2^16 indirizzi diversi.",
                "Con un bus dati da 32 bit puoi trasferire 32 bit per operazione di bus.",
                "Quindi indirizzi e dati rispondono a due domande diverse: dove vado e quanto trasferisco.",
            ],
        },
        "microarchitecture": {
            "title": "Esempio: microistruzione",
            "lines": [
                "Una istruzione ISA, per esempio una somma, puo richiedere piu passi interni.",
                "Ogni passo interno e controllato da una microistruzione.",
                "La microistruzione dice quali registri leggere, cosa fa l'ALU e dove salvare il risultato.",
            ],
        },
        "clock": {
            "title": "Esempio: tempo CPU",
            "lines": [
                "Hai 1000 istruzioni, CPI = 2, clock = 500 MHz.",
                "Cicli totali = 1000 * 2 = 2000 cicli.",
                "Tempo = 2000 / 500.000.000 secondi = 0,000004 s = 4 microsecondi.",
            ],
        },
        "video_review": {
            "title": "Esempio: domanda dai video",
            "lines": [
                "Se il tema e bus indirizzi, pensa subito a quante locazioni puoi selezionare.",
                "Se il tema e microistruzioni, pensa ai segnali interni che controllano il datapath.",
                "Se il tema e clock, scrivi prima la formula e poi controlla le unita.",
            ],
        },
    }
    return examples.get(topic, {
        "title": "Esempio guidato",
        "lines": ["Leggi la domanda, riconosci l'argomento, applica la regola e controlla il risultato."],
    })


def architecture_default_explanation(topic, steps):
    intro = {
        "conversions": "Nelle conversioni non conviene memorizzare la risposta: devi riconoscere il peso di ogni cifra. Ogni posizione vale una potenza della base.",
        "binary_arithmetic": "Nell'aritmetica binaria il trucco e gestire bene i riporti. Il controllo in decimale serve solo a verificare, non sostituisce il procedimento.",
        "twos": "Il complemento a 2 rappresenta i negativi invertendo il positivo e aggiungendo 1. Il numero di bit e parte della risposta.",
        "ieee754": "IEEE 754 singola precisione usa 1 bit di segno, 8 bit di esponente con bias 127 e 23 bit di mantissa.",
        "logic": "Le porte logiche si studiano meglio collegando formule e tabella di verita. De Morgan e NOR completo tornano spesso all'esame.",
        "core": "I fondamenti di Architettura dei Calcolatori vanno legati ai componenti: memoria, registri, PC, formato istruzione e modello di Von Neumann.",
        "mips": "In MIPS il nome dell'istruzione dice quasi sempre il movimento: load carica, store salva, branch decide se saltare.",
        "memory_bus": "Memoria e bus vanno letti come un flusso: la CPU seleziona un indirizzo, trasferisce dati e rispetta una temporizzazione.",
        "microarchitecture": "La microarchitettura traduce le istruzioni visibili al programmatore in passi interni controllati da segnali e microistruzioni.",
        "clock": "Le domande sul clock sono esercizi di unita di misura: formula corretta, frequenza convertita, tempo finale nell'unita richiesta.",
        "video_review": "Gli esercizi dai video nascono dalle trascrizioni, ma si risolvono come domande normali: riconosci il concetto e applica la regola.",
    }.get(topic, "Applica la regola dell'argomento e verifica il risultato con un controllo breve.")
    detail = " ".join(str(step) for step in steps)
    return f"{intro} {detail}".strip()


def make_arch_exercise(
    topic,
    title,
    prompt,
    answer,
    steps,
    answer_type="text",
    options=None,
    placeholder="Risposta",
    hint=None,
    guide=None,
    explanation=None,
    example=None,
    study_note=None,
):
    labels = {item["id"]: item["label"] for item in ARCHITECTURE_TOPICS}
    payload = {
        "id": arch_exercise_id(),
        "topic": topic,
        "topic_label": labels.get(topic, "Architettura"),
        "title": title,
        "prompt": prompt,
        "answer": str(answer),
        "answer_type": answer_type,
        "options": options or [],
        "placeholder": placeholder,
        "hint": hint or "Risolvi prima senza guardare: se sbagli, vedrai i passaggi essenziali.",
        "guide": guide or architecture_default_guide(topic, title),
        "example": example or architecture_default_example(topic),
        "steps": steps,
        "explanation": explanation or architecture_default_explanation(topic, steps),
    }
    if study_note:
        payload["study_note"] = study_note
    return payload


def generate_conversion_exercise():
    variant = random.choice(["to_decimal", "from_decimal", "fraction"])
    if variant == "to_decimal":
        base = random.choice([3, 4, 7, 8, 16])
        value = random.randint(12, 800)
        digits = to_base(value, base)
        steps = [
            f"Scomponi {digits} in potenze di {base}.",
            "Moltiplica ogni cifra per il suo peso posizionale.",
            f"Risultato: {value}.",
        ]
        return make_arch_exercise(
            "conversions",
            "Conversione in decimale",
            f"Converti ({digits})_{base} in decimale.",
            value,
            steps,
            placeholder="Es. 45",
        )
    if variant == "fraction":
        base = random.choice([2, 4, 8])
        examples = [("110.01", 2), ("30.2", 4), ("10.5", 8), ("11100.1", 2)]
        digits, base = random.choice(examples)
        value = base_fraction_to_decimal(digits, base)
        shown = str(value).rstrip("0").rstrip(".")
        steps = [
            "Parte intera: usa le potenze positive della base.",
            "Parte frazionaria: usa b^-1, b^-2, ...",
            f"Risultato: {shown}.",
        ]
        return make_arch_exercise(
            "conversions",
            "Conversione con virgola",
            f"Converti ({digits.replace('.', ',')})_{base} in decimale.",
            shown,
            steps,
            placeholder="Es. 6,25",
        )
    base = random.choice([2, 8, 16])
    value = random.choice([45, 66, 225, 549, 255, 127, 128])
    answer = to_base(value, base)
    steps = [
        f"Dividi {value} ripetutamente per {base}.",
        "Leggi i resti dal basso verso l'alto.",
        f"Risultato: ({answer})_{base}.",
    ]
    return make_arch_exercise(
        "conversions",
        "Conversione da decimale",
        f"Converti {value} in base {base}.",
        answer,
        steps,
        placeholder="Es. 225",
    )


def generate_binary_arithmetic_exercise():
    variant = random.choice(["add", "sub", "mul"])
    if variant == "add":
        a, b, a_label, b_label = random.choice(
            [
                (0b1011, 0b111, "1011", "111"),
                (0b0101, 0b0011, "0101", "0011"),
                (random.randint(5, 31), random.randint(3, 15), None, None),
            ]
        )
        a_label = a_label or format(a, "b")
        b_label = b_label or format(b, "b")
        answer = format(a + b, "b")
        steps = [
            f"({a_label})_2 = {a}, ({b_label})_2 = {b}.",
            f"Somma decimale di controllo: {a} + {b} = {a + b}.",
            f"Risultato binario: {answer}.",
        ]
        return make_arch_exercise(
            "binary_arithmetic",
            "Somma binaria",
            f"Calcola ({a_label})_2 + ({b_label})_2.",
            answer,
            steps,
            placeholder="Es. 10010",
        )
    if variant == "sub":
        a, b, a_label, b_label = random.choice(
            [
                (0b11101, 0b1110, "11101", "1110"),
                (random.randint(18, 63), 0, None, None),
            ]
        )
        if b == 0:
            b = random.randint(3, min(20, a - 1))
        a_label = a_label or format(a, "b")
        b_label = b_label or format(b, "b")
        answer = format(a - b, "b")
        steps = [
            f"({a_label})_2 = {a}, ({b_label})_2 = {b}.",
            f"Sottrazione decimale di controllo: {a} - {b} = {a - b}.",
            f"Risultato binario: {answer}.",
        ]
        return make_arch_exercise(
            "binary_arithmetic",
            "Sottrazione binaria",
            f"Calcola ({a_label})_2 - ({b_label})_2.",
            answer,
            steps,
            placeholder="Es. 1111",
        )
    a, b = random.choice([(0b1011, 0b110), (0b1010, 0b110), (0b111, 0b101)])
    answer = format(a * b, "b")
    steps = [
        f"({format(a, 'b')})_2 = {a}, ({format(b, 'b')})_2 = {b}.",
        "Moltiplica e somma i prodotti parziali spostati a sinistra.",
        f"Controllo: {a} x {b} = {a * b}; in binario {answer}.",
    ]
    return make_arch_exercise(
        "binary_arithmetic",
        "Prodotto binario",
        f"Calcola ({format(a, 'b')})_2 x ({format(b, 'b')})_2.",
        answer,
        steps,
        placeholder="Es. 1000010",
    )


def generate_twos_exercise():
    bits = random.choice([4, 8])
    minimum = -(2 ** (bits - 1))
    value = random.randint(minimum + 1, -1)
    positive = format(abs(value), f"0{bits}b")
    inverted = "".join("1" if bit == "0" else "0" for bit in positive)
    answer = twos_complement_bits(value, bits)
    steps = [
        f"Scrivi +{abs(value)} su {bits} bit: {positive}.",
        f"Inverti i bit: {inverted}.",
        f"Aggiungi 1: {answer}.",
    ]
    return make_arch_exercise(
        "twos",
        "Complemento a 2",
        f"Rappresenta {value} in complemento a 2 su {bits} bit.",
        answer,
        steps,
        placeholder="Es. 1011",
    )


def generate_ieee_exercise():
    value = random.choice([-67.25, 67.25, 8.25, -5.5, 0.5, 28.5])
    answer = ieee754_single(value)
    sign = "1" if value < 0 else "0"
    steps = [
        f"Segno: {sign} ({'negativo' if value < 0 else 'positivo'}).",
        "Normalizza il valore in forma 1.x * 2^e.",
        "Esponente memorizzato = e + 127; mantissa = parte dopo il primo 1.",
        f"Risultato IEEE 754 singola precisione: {answer}.",
    ]
    return make_arch_exercise(
        "ieee754",
        "IEEE 754 singola precisione",
        f"Scrivi {str(value).replace('.', ',')} in IEEE 754 singola precisione.",
        answer,
        steps,
        placeholder="Es. 1 10000101 00001101000000000000000",
    )


def generate_logic_exercise():
    bank = [
        (
            "Una porta AND e equivalente a:",
            "NOR con input invertiti",
            ["NOR con input invertiti", "OR con output invertito", "XOR con input duplicati", "NAND con output diretto"],
            ["Per De Morgan: A AND B = NOT(NOT A OR NOT B).", "Una NOR riceve gli input invertiti e produce AND."],
        ),
        (
            "La negazione di una congiunzione AND di due variabili e equivalente a:",
            "OR delle negazioni",
            ["OR delle negazioni", "AND delle negazioni", "XOR delle variabili", "NOR delle variabili"],
            ["De Morgan: NOT(A AND B) = NOT A OR NOT B."],
        ),
        (
            "La forma canonica SOP usa:",
            "Somma dei mintermini in cui la funzione vale 1",
            ["Somma dei mintermini in cui la funzione vale 1", "Somma dei maxtermini a 0", "Prodotto dei mintermini a 1", "Solo porte XOR"],
            ["SOP = Sum Of Products.", "Si sommano i prodotti/mintermini associati alle righe con uscita 1."],
        ),
        (
            "Perche le porte NOR sono logicamente complete?",
            "Con sole NOR si possono costruire NOT, OR e AND",
            ["Con sole NOR si possono costruire NOT, OR e AND", "Perche consumano meno memoria", "Perche hanno sempre due input", "Perche eliminano il clock"],
            ["NOR puo fare NOT collegando insieme gli ingressi.", "Da NOT e NOR ricavi OR e AND, quindi puoi costruire qualunque funzione booleana."],
        ),
        (
            "Una porta AND restituisce 1 quando:",
            "Entrambi gli ingressi valgono 1",
            ["Entrambi gli ingressi valgono 1", "Almeno un ingresso vale 1", "Gli ingressi sono diversi", "Entrambi gli ingressi valgono 0"],
            ["AND e vera solo nel caso 1 AND 1."],
        ),
    ]
    prompt, answer, options, steps = random.choice(bank)
    random.shuffle(options)
    return make_arch_exercise(
        "logic",
        "Porte logiche e algebra di Boole",
        prompt,
        answer,
        steps,
        answer_type="choice",
        options=options,
    )


def generate_core_arch_exercise():
    bank = [
        (
            "Nella macchina di Von Neumann:",
            "istruzioni e dati condividono la memoria",
            ["istruzioni e dati condividono la memoria", "esiste un nastro infinito", "la memoria contiene solo dati", "ogni registro e una ALU"],
            ["Il modello di Von Neumann conserva programma e dati nella stessa memoria.", "Il nastro infinito e associato alla macchina di Turing, non a Von Neumann."],
        ),
        (
            "Il PC (Program Counter) contiene:",
            "l'indirizzo dell'istruzione da prelevare",
            ["l'indirizzo dell'istruzione da prelevare", "il risultato dell'ALU", "solo il codice operativo", "il numero di cicli del programma"],
            ["Il PC punta alla prossima istruzione da leggere.", "Dopo il fetch viene aggiornato per proseguire o saltare."],
        ),
        (
            "In un'istruzione MIPS a 32 bit, il formato R usa campi:",
            "op, rs, rt, rd, shamt, funct",
            ["op, rs, rt, rd, shamt, funct", "segno, esponente, mantissa", "opcode e target da 26 bit soltanto", "base, limite, offset, flag"],
            ["Il formato R e diviso in campi fissi.", "I campi principali sono opcode, registri sorgente/destinazione, shift amount e funct."],
        ),
        (
            "In una domanda sul valore immediato MIPS, la dimensione corretta e:",
            "16 bit",
            ["32 bit", "16 bit", "6 bit", "5 bit"],
            ["Nel formato I, l'immediato occupa 16 bit.", "Gli altri campi sono opcode e registri rs/rt."],
        ),
        (
            "I registri servono principalmente a:",
            "contenere temporaneamente valori vicini alla CPU",
            ["contenere temporaneamente valori vicini alla CPU", "sostituire tutta la memoria centrale", "memorizzare solo immagini", "definire la frequenza del clock"],
            ["I registri sono piccoli e veloci.", "La CPU li usa per operandi, risultati temporanei e indirizzi."],
        ),
    ]
    prompt, answer, options, steps = random.choice(bank)
    random.shuffle(options)
    return make_arch_exercise(
        "core",
        "Fondamenti e registri",
        prompt,
        answer,
        steps,
        answer_type="choice",
        options=options,
    )


def generate_mips_exercise():
    bank = [
        ("Quale istruzione carica una word da memoria?", "lw", ["lw", "sw", "lb", "sb"], ["lw = load word: carica 32 bit dalla memoria in un registro."]),
        ("Quale istruzione salva una word in memoria?", "sw", ["lw", "sw", "lb", "sb"], ["sw = store word: scrive 32 bit dal registro alla memoria."]),
        ("Quale istruzione salva un byte in memoria?", "sb", ["lw", "sw", "lb", "sb"], ["sb = store byte: scrive 8 bit dal registro alla memoria."]),
        ("Quale istruzione carica un byte da memoria?", "lb", ["lw", "sw", "lb", "beq"], ["lb = load byte; lbu e la variante unsigned."]),
        ("Quale istruzione effettua un branch se due registri sono uguali?", "beq", ["beq", "bne", "j", "addi"], ["beq = branch if equal. L'ALU sottrae e usa il segnale Zero."]),
        ("Quale istruzione effettua un branch se due registri sono diversi?", "bne", ["beq", "bne", "j", "addi"], ["bne = branch if not equal. Salta quando il confronto non produce uguaglianza."]),
        ("Nel formato I MIPS, il campo immediato ha:", "16 bit", ["32 bit", "16 bit", "6 bit", "5 bit"], ["Le istruzioni I-type hanno op, rs, rt e immediato da 16 bit."]),
        ("Per tradurre x = y - 5 con immediato si usa:", "addi", ["addi", "sub", "lw", "beq"], ["Sottrarre una costante significa sommare il suo opposto: addi dest, sorgente, -5."]),
        ("L'istruzione MIPS j Nome usa indirizzamento:", "pseudodiretto", ["pseudodiretto", "immediato", "base + offset", "registro indiretto"], ["j e di tipo J: conserva opcode e target, ricostruendo l'indirizzo di salto."]),
    ]
    prompt, answer, options, steps = random.choice(bank)
    random.shuffle(options)
    return make_arch_exercise(
        "mips",
        "MIPS / Assembly",
        prompt,
        answer,
        steps,
        answer_type="choice",
        options=options,
    )


def generate_memory_bus_exercise():
    bank = [
        (
            "L'ampiezza del bus indirizzi determina:",
            "quante locazioni di memoria possono essere indirizzate",
            ["quante locazioni di memoria possono essere indirizzate", "quanti bit contiene l'ALU", "la frequenza massima del clock", "il numero di registri MIPS"],
            ["Con n linee di indirizzo puoi selezionare 2^n indirizzi.", "Il bus dati invece indica quanti bit vengono trasferiti alla volta."],
        ),
        (
            "L'ampiezza del bus dati indica:",
            "quanti bit possono essere trasferiti in una operazione",
            ["quanti bit possono essere trasferiti in una operazione", "quanti indirizzi esistono in memoria", "la dimensione del Program Counter", "il numero di istruzioni del programma"],
            ["Il bus dati trasporta il valore letto o scritto.", "Piu linee dati significano piu bit trasferiti nello stesso ciclo di bus."],
        ),
        (
            "La cache serve principalmente a:",
            "ridurre il tempo medio di accesso alla memoria",
            ["ridurre il tempo medio di accesso alla memoria", "aumentare il numero di opcode", "sostituire il clock", "memorizzare solo istruzioni MIPS"],
            ["La cache e piccola e veloce.", "Funziona bene quando il programma riusa dati o istruzioni vicine nel tempo o nello spazio."],
        ),
        (
            "In un bus sincrono, le operazioni sono coordinate da:",
            "un clock comune",
            ["un clock comune", "un nastro infinito", "solo interrupt software", "il valore della mantissa"],
            ["Sincrono significa che i passaggi sono scanditi dal clock.", "Nel bus asincrono invece contano segnali di richiesta e risposta."],
        ),
    ]
    prompt, answer, options, steps = random.choice(bank)
    random.shuffle(options)
    return make_arch_exercise(
        "memory_bus",
        "Memoria e bus",
        prompt,
        answer,
        steps,
        answer_type="choice",
        options=options,
    )


def generate_microarchitecture_exercise():
    bank = [
        (
            "Una microistruzione serve a:",
            "controllare i segnali interni del datapath",
            ["controllare i segnali interni del datapath", "rappresentare un numero in IEEE 754", "convertire decimale in binario", "sostituire la memoria RAM"],
            ["La microistruzione non e una istruzione Python o MIPS visibile al programmatore.", "Serve alla CPU per attivare registri, ALU, bus interni e memoria."],
        ),
        (
            "Una unita di controllo microprogrammata usa principalmente:",
            "una memoria di controllo con microistruzioni",
            ["una memoria di controllo con microistruzioni", "solo porte XOR", "un bus dati esterno", "una tabella IEEE 754"],
            ["La memoria di controllo contiene sequenze di microistruzioni.", "Ogni microistruzione produce segnali per un passo di esecuzione."],
        ),
        (
            "Nella microarchitettura, ridurre il numero di microistruzioni per una istruzione ISA serve a:",
            "ridurre i cicli necessari per eseguirla",
            ["ridurre i cicli necessari per eseguirla", "aumentare la dimensione della mantissa", "cambiare il complemento a 2", "eliminare il Program Counter"],
            ["Meno microistruzioni di solito significa meno cicli di clock.", "Questo puo velocizzare l'esecuzione, ma spesso richiede piu hardware."],
        ),
        (
            "Mic-1 e collegata allo studio di:",
            "una microarchitettura che implementa IJVM",
            ["una microarchitettura che implementa IJVM", "una codifica IEEE 754", "una porta NOR", "una somma binaria"],
            ["IJVM e il livello ISA didattico.", "Mic-1 e una microarchitettura usata per mostrare come quelle istruzioni vengono eseguite."],
        ),
    ]
    prompt, answer, options, steps = random.choice(bank)
    random.shuffle(options)
    return make_arch_exercise(
        "microarchitecture",
        "Microarchitettura / IJVM",
        prompt,
        answer,
        steps,
        answer_type="choice",
        options=options,
    )


def generate_clock_exercise():
    instructions = random.choice([1000, 2000, 5000, 10000])
    cpi = random.choice([1, 2, 4])
    freq_mhz = random.choice([100, 500, 1000])
    seconds = instructions * cpi / (freq_mhz * 1_000_000)
    microseconds = seconds * 1_000_000
    answer = f"{microseconds:g}"
    steps = [
        "Formula: tempo CPU = numero istruzioni x CPI / frequenza.",
        f"Cicli totali = {instructions} x {cpi} = {instructions * cpi}.",
        f"Frequenza = {freq_mhz} MHz = {freq_mhz * 1_000_000} Hz.",
        f"Tempo = {answer} microsecondi.",
    ]
    return make_arch_exercise(
        "clock",
        "Clock e tempo CPU",
        f"Un programma esegue {instructions} istruzioni, CPI medio {cpi}, clock {freq_mhz} MHz. Quanto dura in microsecondi?",
        answer,
        steps,
        placeholder="Es. 4",
    )


def generate_min_bits_exercise():
    m = random.choice([8, 16, 32, 64, 100, 256, 1000])
    answer = math.ceil(math.log2(m))
    steps = [
        "Con n bit rappresenti 2^n valori diversi.",
        f"Serve il minimo n tale che 2^n >= {m}.",
        f"n = ceil(log2({m})) = {answer}.",
    ]
    return make_arch_exercise(
        "conversions",
        "Bit minimi per m valori",
        f"Qual e il numero minimo di bit per rappresentare {m} valori diversi?",
        answer,
        steps,
        placeholder="Es. 7",
    )


ARCH_GENERATORS = {
    "conversions": [generate_conversion_exercise, generate_min_bits_exercise],
    "binary_arithmetic": [generate_binary_arithmetic_exercise],
    "twos": [generate_twos_exercise],
    "ieee754": [generate_ieee_exercise],
    "logic": [generate_logic_exercise],
    "core": [generate_core_arch_exercise],
    "mips": [generate_mips_exercise],
    "memory_bus": [generate_memory_bus_exercise],
    "microarchitecture": [generate_microarchitecture_exercise],
    "clock": [generate_clock_exercise],
}


def generate_architecture_exercise(topic="mixed", lesson_slug=None):
    if topic == "video_review":
        return generate_video_review_exercise(lesson_slug=lesson_slug)

    topic = topic if topic in ARCH_GENERATORS else "mixed"
    if topic == "mixed":
        topic = random.choice(list(ARCH_GENERATORS.keys()))
    generator = random.choice(ARCH_GENERATORS[topic])
    return generator()


ARCHITECTURE_SOURCE_TERMS = {
    "conversions": "conversione binario ottale esadecimale base complemento due ieee floating virgola",
    "binary_arithmetic": "somma sottrazione prodotto binario riporto operazione",
    "twos": "complemento due rappresentazione negativo bit segno",
    "ieee754": "ieee 754 floating virgola mobile mantissa esponente segno",
    "logic": "porte logiche and or not nor nand boole de morgan sop mintermini",
    "core": "von neumann memoria dati istruzioni registri program counter pc alu",
    "mips": "mips assembly lw sw lb sb beq bne addi immediato registro branch",
    "memory_bus": "memoria cache bus indirizzo dati ampiezza temporizzazione ram rom word",
    "microarchitecture": "microarchitettura microistruzione microistruzioni datapath alu controllo mic ijvm microprogrammata",
    "clock": "clock ciclo cicli frequenza cpi prestazioni tempo latenza",
    "video_review": "lezione video architettura memoria bus microarchitettura mips clock porte logiche registri",
}

ARCHITECTURE_VIDEO_TOPIC_LABELS = {
    "conversioni": "Conversioni basi",
    "porte_logiche": "Porte logiche e Boole",
    "mips_assembly": "MIPS / Assembly",
    "memoria_bus": "Memoria e bus",
    "microarchitettura": "Microarchitettura / IJVM",
    "clock_prestazioni": "Clock e prestazioni",
    "registri_flip_flop": "Registri e flip-flop",
}

ARCHITECTURE_VIDEO_TOPIC_TO_EXERCISE = {
    "conversioni": "conversions",
    "porte_logiche": "logic",
    "mips_assembly": "mips",
    "memoria_bus": "memory_bus",
    "microarchitettura": "microarchitecture",
    "clock_prestazioni": "clock",
    "registri_flip_flop": "core",
}


def repair_text(value):
    text = str(value or "")
    if "Ã" not in text and "â" not in text:
        return text
    try:
        return text.encode("latin1").decode("utf-8")
    except UnicodeError:
        return text


def fmt_arch_duration(seconds):
    seconds = safe_int(seconds, 0)
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def architecture_manifest_payload():
    manifest_path = os.path.join(ARCHITECTURE_TRANSCRIPTS_DIR, "manifest.json")
    if not os.path.exists(manifest_path):
        return {"status": "missing", "updated_at": None, "lessons": []}
    try:
        with open(manifest_path, "r", encoding="utf-8") as handle:
            manifest = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {"status": "unreadable", "updated_at": None, "lessons": []}

    lessons = []
    for lesson in manifest.get("lessons") or []:
        topics = []
        for item in lesson.get("topics") or []:
            topic_id = item.get("topic")
            topics.append(
                {
                    "id": topic_id,
                    "label": ARCHITECTURE_VIDEO_TOPIC_LABELS.get(topic_id, topic_id or "Architettura"),
                    "score": safe_int(item.get("score"), 0),
                    "hits": item.get("hits") or [],
                }
            )
        lessons.append(
            {
                "slug": lesson.get("slug"),
                "title": repair_text(lesson.get("title")),
                "duration": fmt_arch_duration(lesson.get("duration_seconds")),
                "duration_seconds": lesson.get("duration_seconds"),
                "topics": topics,
                "segments": safe_int(lesson.get("segments"), 0),
                "updated_at": lesson.get("updated_at"),
            }
        )
    return {
        "status": manifest.get("status") or "unknown",
        "updated_at": manifest.get("updated_at"),
        "lessons": lessons,
    }


def architecture_note_row_to_payload(row):
    full_text = repair_text(row["content"])
    return {
        "source_title": repair_text(row["source_title"]),
        "topic": repair_text(row["topic"]),
        "excerpt": compact_excerpt(full_text, max_chars=520),
        "full_text": full_text.strip(),
        "page_start": row["page_start"],
        "page_end": row["page_end"],
        "score": row["score"] if "score" in row.keys() else 0,
    }


def architecture_lesson_note_rows(lesson_title, limit=8):
    if not os.path.exists(SOURCE_DB_PATH):
        return []
    conn = get_source_connection()
    try:
        rows = conn.execute(
            """
            SELECT id, source_title, topic, content, keywords, page_start, page_end
            FROM study_notes
            WHERE subject_key = ? AND topic LIKE ?
            ORDER BY id
            LIMIT ?
            """,
            (ARCHITECTURE_SOURCE_KEY, f"{lesson_title} -%", limit),
        ).fetchall()
    except sqlite3.Error:
        rows = []
    finally:
        conn.close()
    return rows


def architecture_lesson_note_count(lesson_title):
    if not os.path.exists(SOURCE_DB_PATH):
        return 0
    conn = get_source_connection()
    try:
        row = conn.execute(
            """
            SELECT COUNT(*) AS count
            FROM study_notes
            WHERE subject_key = ? AND topic LIKE ?
            """,
            (ARCHITECTURE_SOURCE_KEY, f"{lesson_title} -%"),
        ).fetchone()
        return safe_int(row["count"] if row else 0, 0)
    except sqlite3.Error:
        return 0
    finally:
        conn.close()


def architecture_lesson_sheet(slug):
    manifest = architecture_manifest_payload()
    lesson = next((item for item in manifest["lessons"] if item.get("slug") == slug), None)
    if not lesson:
        return None

    rows = architecture_lesson_note_rows(lesson["title"], limit=10)
    notes = [architecture_note_row_to_payload(row) for row in rows[:6]]
    key_points = []
    seen = set()
    for note in notes:
        topic = note["topic"]
        label = topic.split(" - ")[-1] if " - " in topic else topic
        label = re.sub(r"\s+\(\d\d:\d\d:\d\d\)$", "", label)
        if label in seen:
            continue
        seen.add(label)
        key_points.append(
            {
                "label": label,
                "text": note["excerpt"],
            }
        )
        if len(key_points) >= 4:
            break

    return {
        "lesson": {
            **lesson,
            "note_count": architecture_lesson_note_count(lesson["title"]),
        },
        "key_points": key_points,
        "notes": notes,
    }


def architecture_lessons_payload():
    manifest = architecture_manifest_payload()
    lessons = []
    for lesson in manifest["lessons"]:
        lessons.append(
            {
                **lesson,
                "note_count": architecture_lesson_note_count(lesson["title"]),
            }
        )
    return {
        "status": manifest["status"],
        "updated_at": manifest["updated_at"],
        "lessons": lessons,
    }


def architecture_video_topic_from_note(row):
    blob = f"{row['topic']} {row['keywords']} {row['content']}"
    scores = []
    for source_topic, exercise_topic in ARCHITECTURE_VIDEO_TOPIC_TO_EXERCISE.items():
        terms = ARCHITECTURE_SOURCE_TERMS.get(exercise_topic, "").split()
        score = 0
        normalized_blob = normalize_source_word(blob)
        for term in terms:
            normalized = normalize_source_word(term)
            if normalized and normalized in normalized_blob:
                score += 1
        if source_topic in str(row["topic"]).lower():
            score += 4
        if score:
            scores.append((score, exercise_topic))
    scores.sort(reverse=True)
    return scores[0][1] if scores else "core"


def architecture_video_note_candidates(lesson_slug=None, topic=None, limit=30):
    if not os.path.exists(SOURCE_DB_PATH):
        return []

    lesson_title = None
    if lesson_slug:
        manifest = architecture_manifest_payload()
        lesson = next((item for item in manifest["lessons"] if item.get("slug") == lesson_slug), None)
        lesson_title = lesson["title"] if lesson else None

    conn = get_source_connection()
    params = [ARCHITECTURE_SOURCE_KEY]
    where = ["subject_key = ?"]
    if lesson_title:
        where.append("topic LIKE ?")
        params.append(f"{lesson_title} -%")
    if topic and topic in ARCHITECTURE_SOURCE_TERMS:
        terms = ARCHITECTURE_SOURCE_TERMS[topic].split()[:8]
        if terms:
            where.append("(" + " OR ".join("keywords LIKE ?" for _ in terms) + ")")
            params.extend(f"%{normalize_source_word(term)}%" for term in terms)

    params.append(limit)
    try:
        rows = conn.execute(
            f"""
            SELECT id, source_title, topic, content, keywords, page_start, page_end
            FROM study_notes
            WHERE {' AND '.join(where)}
            ORDER BY RANDOM()
            LIMIT ?
            """,
            params,
        ).fetchall()
    except sqlite3.Error:
        rows = []
    finally:
        conn.close()
    return rows


def architecture_video_source_payload(row):
    payload = architecture_note_row_to_payload(row)
    payload["excerpt"] = compact_excerpt(repair_text(row["content"]), max_chars=760)
    return payload


def generate_video_review_exercise(lesson_slug=None):
    rows = architecture_video_note_candidates(lesson_slug=lesson_slug, limit=40)
    if not rows:
        return generate_microarchitecture_exercise()

    row = random.choice(rows)
    detected_topic = architecture_video_topic_from_note(row)
    source_note = architecture_video_source_payload(row)
    topic_label = {item["id"]: item["label"] for item in ARCHITECTURE_TOPICS}.get(
        detected_topic,
        "Architettura",
    )

    drills = {
        "conversions": (
            "Quando compare una rappresentazione binaria o in altra base, qual e il primo controllo da fare?",
            "capire la base e il peso delle cifre",
            [
                "capire la base e il peso delle cifre",
                "scegliere sempre il complemento a 2",
                "trasformare tutto in MIPS",
                "ignorare gli zeri a sinistra in ogni caso",
            ],
            ["Prima identifichi la base.", "Poi usi le potenze della base per dare peso alle cifre."],
        ),
        "logic": (
            "Con le porte logiche, qual e il modo piu sicuro per verificare una equivalenza?",
            "costruire o ragionare sulla tabella di verita",
            [
                "costruire o ragionare sulla tabella di verita",
                "contare solo il numero di porte",
                "guardare la frequenza del clock",
                "convertire il risultato in IEEE 754",
            ],
            ["Le equivalenze booleane devono dare la stessa uscita per gli stessi ingressi.", "La tabella di verita rende questo controllo esplicito."],
        ),
        "mips": (
            "In MIPS, qual e la distinzione centrale tra load e store?",
            "load carica da memoria a registro, store salva da registro a memoria",
            [
                "load carica da memoria a registro, store salva da registro a memoria",
                "load e store sono entrambi salti condizionati",
                "store legge sempre un byte, load scrive sempre una word",
                "load modifica solo il Program Counter",
            ],
            ["Load significa caricare in un registro.", "Store significa scrivere il valore del registro in memoria."],
        ),
        "memory_bus": (
            "Quando studi bus e memoria, quale coppia devi distinguere subito?",
            "bus indirizzi per selezionare, bus dati per trasferire",
            [
                "bus indirizzi per selezionare, bus dati per trasferire",
                "mantissa per selezionare, esponente per trasferire",
                "AND per selezionare, OR per trasferire",
                "beq per selezionare, bne per trasferire",
            ],
            ["Il bus indirizzi dice quale locazione vuoi raggiungere.", "Il bus dati porta il valore letto o scritto."],
        ),
        "microarchitecture": (
            "La microarchitettura che cosa descrive rispetto all'ISA?",
            "come le istruzioni vengono eseguite internamente dal datapath",
            [
                "come le istruzioni vengono eseguite internamente dal datapath",
                "solo la sintassi Python delle istruzioni",
                "solo la conversione dei numeri in base 8",
                "solo il risultato visibile a schermo",
            ],
            ["L'ISA definisce le istruzioni viste dal programmatore.", "La microarchitettura mostra registri, ALU, bus interni e segnali che le realizzano."],
        ),
        "clock": (
            "Quando studi prestazioni e clock, qual e la relazione da tenere a mente?",
            "il tempo dipende da istruzioni, CPI e frequenza",
            [
                "il tempo dipende da istruzioni, CPI e frequenza",
                "il tempo dipende solo dalla mantissa",
                "il tempo dipende solo dal numero di porte NOR",
                "il tempo non cambia mai con il clock",
            ],
            ["La formula base e tempo CPU = istruzioni x CPI / frequenza.", "Aumentare la frequenza puo ridurre il tempo, ma non elimina gli altri fattori."],
        ),
        "core": (
            "Con registri e componenti della CPU, qual e l'idea piu importante?",
            "ogni componente ha un ruolo preciso nel ciclo di esecuzione",
            [
                "ogni componente ha un ruolo preciso nel ciclo di esecuzione",
                "tutti i componenti memorizzano solo immagini",
                "i registri sostituiscono sempre tutta la RAM",
                "il PC contiene sempre il risultato dell'ALU",
            ],
            ["Il PC punta alle istruzioni.", "Registri, ALU e memoria collaborano durante fetch, decode ed execute."],
        ),
    }

    prompt, answer, options, steps = drills.get(detected_topic, drills["core"])
    random.shuffle(options)
    return make_arch_exercise(
        "video_review",
        f"Dai video: {topic_label}",
        prompt,
        answer,
        steps,
        answer_type="choice",
        options=options,
        hint="Domanda creata dai video: scegli il concetto chiave.",
        study_note=source_note,
        explanation=(
            f"Questo esercizio nasce da un estratto video classificato come {topic_label}. "
            + architecture_default_explanation(detected_topic, steps)
        ),
    )


def architecture_source_summary():
    summary = {
        "status": "missing",
        "lesson_count": 0,
        "note_count": 0,
        "updated_at": None,
    }

    manifest_path = os.path.join(ARCHITECTURE_TRANSCRIPTS_DIR, "manifest.json")
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as handle:
                manifest = json.load(handle)
            summary["status"] = manifest.get("status") or "unknown"
            summary["lesson_count"] = safe_int(manifest.get("lesson_count"), 0)
            summary["updated_at"] = manifest.get("updated_at")
        except (OSError, json.JSONDecodeError):
            summary["status"] = "unreadable"

    if os.path.exists(SOURCE_DB_PATH):
        conn = get_source_connection()
        try:
            row = conn.execute(
                "SELECT COUNT(*) AS count FROM study_notes WHERE subject_key = ?",
                (ARCHITECTURE_SOURCE_KEY,),
            ).fetchone()
            summary["note_count"] = safe_int(row["count"] if row else 0, 0)
        except sqlite3.Error:
            summary["note_count"] = 0
        finally:
            conn.close()

    return summary


def architecture_source_notes(exercise, limit=2):
    primary_note = exercise.get("study_note")
    if primary_note:
        extra_limit = max(limit - 1, 0)
    else:
        extra_limit = limit

    topic = exercise.get("topic", "")
    query = " ".join(
        [
            str(exercise.get("topic_label", "")),
            str(exercise.get("title", "")),
            str(exercise.get("prompt", "")),
            str(exercise.get("answer", "")),
            " ".join(str(step) for step in exercise.get("steps") or []),
            ARCHITECTURE_SOURCE_TERMS.get(topic, ""),
        ]
    )
    notes = find_study_sources(ARCHITECTURE_SOURCE_KEY, query, limit=extra_limit)
    if primary_note:
        primary_topic = primary_note.get("topic")
        notes = [note for note in notes if note.get("topic") != primary_topic]
        return [primary_note, *notes][:limit]
    return notes


def get_architecture_stats():
    stored = read_app_state("architecture_practice_stats")
    value = stored["value"] if stored and isinstance(stored.get("value"), dict) else {}
    return {
        "attempts": safe_int(value.get("attempts"), 0),
        "correct": safe_int(value.get("correct"), 0),
        "by_topic": value.get("by_topic") if isinstance(value.get("by_topic"), dict) else {},
    }


def save_architecture_stats(stats):
    stats["updated_at"] = iso_now()
    write_app_state("architecture_practice_stats", stats)
    return stats


def update_architecture_stats(topic, is_correct):
    stats = get_architecture_stats()
    stats["attempts"] += 1
    if is_correct:
        stats["correct"] += 1
    by_topic = stats.setdefault("by_topic", {})
    item = by_topic.setdefault(topic, {"attempts": 0, "correct": 0})
    item["attempts"] = safe_int(item.get("attempts"), 0) + 1
    item["correct"] = safe_int(item.get("correct"), 0) + (1 if is_correct else 0)
    return save_architecture_stats(stats)


def check_architecture_answer(exercise, answer):
    expected = str(exercise.get("answer", ""))
    submitted = str(answer or "")
    answer_type = exercise.get("answer_type", "text")
    if answer_type == "choice":
        return submitted.strip().lower() == expected.strip().lower()

    expected_clean = clean_arch_answer(expected)
    submitted_clean = clean_arch_answer(submitted)
    if expected_clean == submitted_clean:
        return True

    try:
        return abs(float(expected_clean) - float(submitted_clean)) < 0.000001
    except ValueError:
        return False


def remember_architecture_exercise(exercise):
    stored = read_app_state("architecture_recent_exercises")
    value = stored["value"] if stored and isinstance(stored.get("value"), dict) else {}
    exercises = value.get("exercises") if isinstance(value.get("exercises"), dict) else {}
    order = value.get("order") if isinstance(value.get("order"), list) else []

    exercise_id = exercise.get("id")
    if not exercise_id:
        return

    exercises[exercise_id] = exercise
    order = [item for item in order if item != exercise_id]
    order.append(exercise_id)

    while len(order) > 20:
        old_id = order.pop(0)
        exercises.pop(old_id, None)

    write_app_state(
        "architecture_recent_exercises",
        {
            "exercises": exercises,
            "order": order,
        },
    )


def find_architecture_exercise(exercise_id):
    stored = read_app_state("architecture_recent_exercises")
    value = stored["value"] if stored and isinstance(stored.get("value"), dict) else {}
    exercises = value.get("exercises") if isinstance(value.get("exercises"), dict) else {}
    exercise = exercises.get(str(exercise_id or ""))
    return exercise if isinstance(exercise, dict) else None


def architecture_stats_payload(stats=None):
    stats = stats or get_architecture_stats()
    attempts = safe_int(stats.get("attempts"), 0)
    correct = safe_int(stats.get("correct"), 0)
    by_topic = stats.get("by_topic") if isinstance(stats.get("by_topic"), dict) else {}
    accuracy = round((correct / attempts) * 100) if attempts else 0
    topic_payload = {}
    for topic in ARCHITECTURE_TOPICS:
        item = by_topic.get(topic["id"], {})
        item_attempts = safe_int(item.get("attempts"), 0)
        item_correct = safe_int(item.get("correct"), 0)
        topic_payload[topic["id"]] = {
            "attempts": item_attempts,
            "correct": item_correct,
            "accuracy": round((item_correct / item_attempts) * 100) if item_attempts else 0,
        }
    return {
        "attempts": attempts,
        "correct": correct,
        "accuracy": accuracy,
        "by_topic": topic_payload,
        "updated_at": stats.get("updated_at"),
    }


def get_all_question_ids():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM questions ORDER BY id")
    ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return ids


def get_correct_answer_id(question_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM answers WHERE domanda_id = ? AND corretta = 1 LIMIT 1",
        (question_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def update_question_stats(subject_key, question_id, is_correct, rating=None):
    rating = rating or ("know" if is_correct else "dont_know")
    now = iso_now()

    conn = get_progress_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM question_stats
        WHERE subject_key = ? AND question_id = ?
        """,
        (subject_key, question_id),
    )
    current = row_to_stats(cur.fetchone(), question_id)

    attempts = current["attempts"] + 1
    correct_count = current["correct_count"] + (1 if is_correct else 0)
    wrong_count = current["wrong_count"] + (0 if is_correct else 1)
    correct_streak = current["correct_streak"] + 1 if is_correct else 0
    wrong_streak = 0 if is_correct else current["wrong_streak"] + 1
    box = current["box"]
    confidence = current["confidence"]

    if is_correct and rating == "know":
        box = clamp(box + 1, 1, 5)
        confidence = clamp(confidence + 2, -10, 10)
    elif is_correct and rating == "unsure":
        box = clamp(max(box, 1), 0, 2)
        confidence = clamp(confidence, -10, 10)
    else:
        box = 0
        confidence = clamp(confidence - 2, -10, 10)

    status = classify_status(
        attempts, wrong_count, correct_streak, wrong_streak, box, rating
    )
    due_at = due_for_box(box)
    last_wrong_at = current["last_wrong_at"]
    if not is_correct or rating == "dont_know":
        last_wrong_at = now

    cur.execute(
        """
        INSERT INTO question_stats (
            subject_key, question_id, attempts, correct_count, wrong_count,
            correct_streak, wrong_streak, confidence, box, status,
            last_seen_at, last_wrong_at, due_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(subject_key, question_id) DO UPDATE SET
            attempts = excluded.attempts,
            correct_count = excluded.correct_count,
            wrong_count = excluded.wrong_count,
            correct_streak = excluded.correct_streak,
            wrong_streak = excluded.wrong_streak,
            confidence = excluded.confidence,
            box = excluded.box,
            status = excluded.status,
            last_seen_at = excluded.last_seen_at,
            last_wrong_at = excluded.last_wrong_at,
            due_at = excluded.due_at
        """,
        (
            subject_key,
            question_id,
            attempts,
            correct_count,
            wrong_count,
            correct_streak,
            wrong_streak,
            confidence,
            box,
            status,
            now,
            last_wrong_at,
            due_at,
        ),
    )
    conn.commit()
    cur.execute(
        "SELECT * FROM question_stats WHERE subject_key = ? AND question_id = ?",
        (subject_key, question_id),
    )
    updated = row_to_stats(cur.fetchone(), question_id)
    conn.close()
    return updated


def apply_confidence(subject_key, question_id, rating):
    now = utc_now()
    conn = get_progress_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM question_stats WHERE subject_key = ? AND question_id = ?",
        (subject_key, question_id),
    )
    current = row_to_stats(cur.fetchone(), question_id)
    if current["attempts"] == 0:
        conn.close()
        return None

    confidence = current["confidence"]
    box = current["box"]
    status = current["status"]
    due_at = current["due_at"]
    last_wrong_at = current["last_wrong_at"]

    if rating == "know":
        confidence = clamp(confidence + 1, -10, 10)
        box = clamp(max(box, 2), 0, 5)
        status = classify_status(
            current["attempts"],
            current["wrong_count"],
            current["correct_streak"],
            current["wrong_streak"],
            box,
            rating,
        )
        due_at = (now + REVIEW_INTERVALS[box]).isoformat(timespec="seconds")
    elif rating == "unsure":
        confidence = clamp(confidence - 1, -10, 10)
        box = clamp(min(max(box, 1), 2), 0, 5)
        status = "shaky"
        due_at = (now + timedelta(days=1)).isoformat(timespec="seconds")
    elif rating == "dont_know":
        confidence = clamp(confidence - 2, -10, 10)
        box = 0
        status = "weak"
        last_wrong_at = now.isoformat(timespec="seconds")
        due_at = (now + timedelta(minutes=20)).isoformat(timespec="seconds")
    else:
        conn.close()
        return None

    cur.execute(
        """
        UPDATE question_stats
        SET confidence = ?, box = ?, status = ?, due_at = ?, last_wrong_at = ?
        WHERE subject_key = ? AND question_id = ?
        """,
        (confidence, box, status, due_at, last_wrong_at, subject_key, question_id),
    )
    conn.commit()
    cur.execute(
        "SELECT * FROM question_stats WHERE subject_key = ? AND question_id = ?",
        (subject_key, question_id),
    )
    updated = row_to_stats(cur.fetchone(), question_id)
    conn.close()
    return updated


def priority_score(stats):
    if not stats or stats["attempts"] <= 0:
        return 0

    attempts = max(stats["attempts"], 1)
    wrong_rate = stats["wrong_count"] / attempts
    due_at = parse_dt(stats.get("due_at"))
    overdue = 0
    if due_at and due_at <= utc_now():
        overdue = max(1, int((utc_now() - due_at).total_seconds() // 3600) + 1)

    return (
        stats["wrong_count"] * 8
        + wrong_rate * 25
        + stats["wrong_streak"] * 10
        + overdue * 2
        - stats["correct_streak"] * 4
        - stats["box"] * 5
        - stats["confidence"]
    )


def sort_by_priority(question_ids, stats_map, reverse=True):
    return sorted(
        question_ids,
        key=lambda qid: priority_score(stats_map.get(qid, empty_stats(qid))),
        reverse=reverse,
    )


def unique_take(target, source, limit):
    for qid in source:
        if len(target) >= limit:
            break
        if qid not in target:
            target.append(qid)
    return target


def select_review_question_ids(subject_key, preset, limit, topic_id=None):
    all_ids = filter_question_ids_by_topic(
        subject_key,
        get_all_question_ids(),
        topic_id,
    )
    stats_map = fetch_stats_map(subject_key)
    now = utc_now()

    seen = [
        qid
        for qid in all_ids
        if stats_map.get(qid, empty_stats(qid))["attempts"] > 0
    ]
    new_ids = [qid for qid in all_ids if qid not in seen]
    random_ids = all_ids[:]
    random.shuffle(random_ids)

    due_ids = [
        qid
        for qid in seen
        if (parse_dt(stats_map[qid].get("due_at")) or now + timedelta(days=1)) <= now
    ]
    weak_ids = [
        qid
        for qid in seen
        if stats_map[qid]["status"] in {"weak", "shaky"}
        or stats_map[qid]["wrong_count"] > 0
    ]
    easy_ids = [
        qid
        for qid in seen
        if stats_map[qid]["status"] in {"solid", "mastered"}
        or stats_map[qid]["correct_streak"] >= 2
    ]
    mastered_ids = [
        qid for qid in seen if stats_map[qid]["status"] == "mastered"
    ]

    due_ids = sort_by_priority(due_ids, stats_map)
    weak_ids = sort_by_priority(weak_ids, stats_map)
    easy_ids = sort_by_priority(easy_ids, stats_map, reverse=False)
    mastered_ids = sort_by_priority(mastered_ids, stats_map, reverse=False)

    if preset == "new":
        return new_ids[:limit]
    if preset == "weak":
        return unique_take([], weak_ids + due_ids + random_ids, limit)
    if preset == "due":
        return unique_take([], due_ids + weak_ids + random_ids, limit)
    if preset == "easy":
        return unique_take([], easy_ids + mastered_ids + random_ids, limit)
    if preset == "mastered":
        return unique_take([], mastered_ids + easy_ids + random_ids, limit)
    if preset == "random":
        return random_ids[:limit]

    selected = []
    unique_take(selected, due_ids, round(limit * 0.35))
    unique_take(selected, weak_ids, round(limit * 0.70))
    unique_take(selected, sort_by_priority(seen, stats_map), round(limit * 0.90))
    unique_take(selected, new_ids, limit)
    unique_take(selected, random_ids, limit)
    return selected[:limit]


@app.before_request
def require_login():
    if not APP_PASSWORD:
        return None
    if request.endpoint in {"login", "static"}:
        return None
    if session.get("authenticated"):
        return None
    if request.path.startswith("/api/"):
        return jsonify({"error": "Autenticazione richiesta"}), 401
    return redirect(url_for("login", next=request.path))


@app.route("/login", methods=["GET", "POST"])
def login():
    if not APP_PASSWORD:
        return redirect(url_for("index"))

    error = None
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == APP_PASSWORD:
            session["authenticated"] = True
            return redirect(request.args.get("next") or url_for("index"))
        error = "Password non corretta"

    return render_template("login.html", error=error)


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("authenticated", None)
    return redirect(url_for("login"))


# ------------------------
#   API: Materie
# ------------------------

@app.route("/api/databases", methods=["GET"])
def list_databases():
    dbs = scan_databases()
    active = session.get("db_key")
    if active not in dbs:
        active = None

    options = [{"key": k, "label": v["label"]} for k, v in dbs.items()]
    options.sort(key=lambda x: x["label"].lower())
    return jsonify({"active": active, "options": options})


@app.route("/api/set_database", methods=["POST"])
def set_database():
    dbs = scan_databases()
    data = request.get_json(silent=True) or {}
    db_key = data.get("db_key")

    if not db_key or db_key not in dbs:
        return jsonify({"error": "Materia/Database non valido"}), 400

    session["db_key"] = db_key
    return jsonify({"message": "Materia impostata", "active": db_key})


@app.route("/api/subject_profile", methods=["GET", "POST"])
def subject_profile():
    guard = require_db_selected()
    if guard:
        return guard

    subject_key = get_subject_key()
    dbs = scan_databases()
    subject_label = dbs.get(subject_key, {}).get("label", "Materia")
    profiles = read_subject_profiles()

    if request.method == "GET":
        profile = profiles.get(subject_key)
        return jsonify(
            {
                "subject_key": subject_key,
                "subject_label": subject_label,
                "profile": profile,
                "is_configured": bool(profile),
            }
        )

    data = request.get_json(silent=True) or {}
    try:
        profile = clean_subject_profile(data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    profile["subject_label"] = subject_label
    profile.setdefault("created_at", iso_now())
    if subject_key in profiles and isinstance(profiles[subject_key], dict):
        profile["created_at"] = profiles[subject_key].get("created_at") or profile["created_at"]
    profiles[subject_key] = profile
    updated_at = write_subject_profiles(profiles)
    return jsonify(
        {
            "message": "Profilo materia salvato",
            "subject_key": subject_key,
            "subject_label": subject_label,
            "profile": profile,
            "updated_at": updated_at,
        }
    )


# ------------------------
#   API: Quiz
# ------------------------

@app.route("/api/question/<int:id>", methods=["GET"])
def get_question_by_id(id):
    guard = require_db_selected()
    if guard:
        return guard

    conn = get_connection()
    cursor = conn.cursor()
    payload = build_question_payload(cursor, id, include_images=True)
    conn.close()

    if payload is None:
        return jsonify({"error": "Domanda non trovata"}), 404

    attach_progress([payload])
    return jsonify(payload)


@app.route("/api/save_question/<int:id>", methods=["POST"])
def save_question(id):
    guard = require_db_selected()
    if guard:
        return guard

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE questions SET is_saved = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Domanda salvata", "id": id})


@app.route("/api/saved_questions", methods=["GET"])
def get_saved_questions():
    guard = require_db_selected()
    if guard:
        return guard

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM questions WHERE is_saved = 1 ORDER BY id")
    rows = cursor.fetchall()

    questions = []
    for (q_id,) in rows:
        payload = build_question_payload(cursor, q_id, include_images=False)
        if payload:
            questions.append(payload)

    conn.close()
    attach_progress(questions)
    return jsonify(questions)


@app.route("/api/remove_saved_question/<int:id>", methods=["DELETE"])
def remove_saved_question(id):
    guard = require_db_selected()
    if guard:
        return guard

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE questions SET is_saved = 0 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Domanda salvata rimossa", "id": id})


@app.route("/api/clear_saved_questions", methods=["DELETE"])
def clear_saved_questions():
    guard = require_db_selected()
    if guard:
        return guard

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE questions SET is_saved = 0")
    conn.commit()
    conn.close()

    return jsonify({"message": "Tutte le domande salvate sono state rimosse"})


@app.route("/api/random_questions", methods=["GET"])
def random_questions():
    guard = require_db_selected()
    if guard:
        return guard

    limit = request.args.get("limit", default=30, type=int)
    if limit <= 0:
        limit = 30

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM questions ORDER BY RANDOM() LIMIT ?", (limit,))
    rows = cursor.fetchall()

    questions = []
    for (q_id,) in rows:
        payload = build_question_payload(cursor, q_id, include_images=True)
        if payload:
            questions.append(payload)

    conn.close()
    attach_progress(questions)
    return jsonify(questions)


@app.route("/api/review_questions", methods=["GET"])
def review_questions():
    guard = require_db_selected()
    if guard:
        return guard

    subject_key = get_subject_key()
    preset = request.args.get("mode", default="mixed", type=str)
    topic_id = request.args.get("topic", default="", type=str)
    limit = request.args.get("limit", default=30, type=int)
    limit = clamp(limit or 30, 1, 300)

    allowed = {"mixed", "new", "weak", "due", "easy", "mastered", "random"}
    if preset not in allowed:
        preset = "mixed"

    ids = select_review_question_ids(subject_key, preset, limit, topic_id)

    conn = get_connection()
    cursor = conn.cursor()
    questions = []
    for q_id in ids:
        payload = build_question_payload(cursor, q_id, include_images=True)
        if payload:
            questions.append(payload)
    conn.close()

    attach_progress(questions)
    return jsonify(
        {
            "mode": preset,
            "topic": normalize_source_word(topic_id),
            "count": len(questions),
            "questions": questions,
        }
    )


@app.route("/api/questions_by_ids", methods=["POST"])
def questions_by_ids():
    guard = require_db_selected()
    if guard:
        return guard

    data = request.get_json(silent=True) or {}
    raw_ids = data.get("ids") or []
    if not isinstance(raw_ids, list):
        return jsonify({"error": "Lista domande non valida"}), 400

    ids = []
    for raw_id in raw_ids[:300]:
        try:
            ids.append(int(raw_id))
        except (TypeError, ValueError):
            continue

    conn = get_connection()
    cursor = conn.cursor()
    questions = []
    for q_id in ids:
        payload = build_question_payload(cursor, q_id, include_images=True)
        if payload:
            questions.append(payload)
    conn.close()

    attach_progress(questions)
    return jsonify({"count": len(questions), "questions": questions})


@app.route("/api/architecture_practice", methods=["GET"])
def architecture_practice():
    return jsonify(
        {
            "topics": ARCHITECTURE_TOPICS,
            "stats": architecture_stats_payload(),
            "focus": [
                "Conversioni tra basi, complemento a 2 e IEEE 754.",
                "Somme, sottrazioni e prodotti binari con controllo decimale.",
                "MIPS: lw, sw, lb, sb, beq, bne, addi e formato I.",
                "Algebra di Boole, De Morgan, SOP, NOR e AND.",
                "Memoria, bus, microarchitettura, microistruzioni e IJVM.",
                "Clock: tempo CPU = istruzioni x CPI / frequenza.",
            ],
            "source_summary": architecture_source_summary(),
        }
    )


@app.route("/api/architecture_lessons", methods=["GET"])
def architecture_lessons():
    payload = architecture_lessons_payload()
    return jsonify(
        {
            **payload,
            "source_summary": architecture_source_summary(),
        }
    )


@app.route("/api/architecture_lessons/<slug>", methods=["GET"])
def architecture_lesson(slug):
    sheet = architecture_lesson_sheet(slug)
    if not sheet:
        return jsonify({"error": "Lezione non trovata"}), 404
    return jsonify(sheet)


@app.route("/api/architecture_exercise", methods=["GET"])
def architecture_exercise():
    topic = request.args.get("topic", default="mixed", type=str)
    lesson_slug = request.args.get("lesson", default="", type=str)
    allowed_topics = {item["id"] for item in ARCHITECTURE_TOPICS}
    if topic not in allowed_topics:
        topic = "mixed"

    exercise = generate_architecture_exercise(topic, lesson_slug=lesson_slug)
    remember_architecture_exercise(exercise)
    return jsonify(
        {
            "exercise": arch_public_exercise(exercise),
            "stats": architecture_stats_payload(),
        }
    )


@app.route("/api/architecture_exercise/check", methods=["POST"])
def architecture_exercise_check():
    data = request.get_json(silent=True) or {}
    exercise_id = data.get("exercise_id")
    exercise = find_architecture_exercise(exercise_id)
    if not exercise:
        return jsonify({"error": "Esercizio non trovato. Generane uno nuovo."}), 404

    answer = str(data.get("answer") or "")[:500]
    is_correct = check_architecture_answer(exercise, answer)
    stats = update_architecture_stats(exercise.get("topic", "mixed"), is_correct)
    expected = exercise.get("answer", "")
    retry_message = (
        "Giusto. Ora cambia esercizio oppure fanne un altro dello stesso argomento."
        if is_correct
        else "Ritenta subito: riscrivi la risposta corretta senza guardare i passaggi."
    )

    return jsonify(
        {
            "exercise_id": exercise.get("id"),
            "is_correct": is_correct,
            "expected": expected,
            "submitted": answer,
            "explanation": exercise.get("explanation") or "",
            "steps": exercise.get("steps") or [],
            "source_notes": architecture_source_notes(exercise),
            "retry_message": retry_message,
            "stats": architecture_stats_payload(stats),
        }
    )


@app.route("/api/study_session", methods=["GET", "POST", "DELETE"])
def study_session():
    if request.method == "DELETE":
        delete_app_state("active_study_session")
        return jsonify({"message": "Sessione cancellata"})

    if request.method == "GET":
        stored = read_app_state("active_study_session")
        if not stored or not stored["value"]:
            return jsonify({"session": None})

        value = stored["value"]
        db_key = value.get("db_key")
        dbs = scan_databases()
        if db_key in dbs:
            session["db_key"] = db_key
        else:
            value["db_key"] = None

        return jsonify(
            {
                "session": value,
                "updated_at": stored["updated_at"],
            }
        )

    data = request.get_json(silent=True) or {}
    db_key = data.get("db_key")
    dbs = scan_databases()
    if db_key and db_key not in dbs:
        return jsonify({"error": "Materia/Database non valido"}), 400

    if db_key:
        session["db_key"] = db_key

    allowed_modes = {
        "training",
        "plan",
        "daily",
        "review",
        "tutor",
        "sprint",
        "tutorial",
        "architecture",
        "exam",
        "saved",
    }
    mode_value = data.get("mode") if data.get("mode") in allowed_modes else "training"

    state = {
        "db_key": db_key,
        "mode": mode_value,
        "current_question_index": clamp(
            safe_int(data.get("current_question_index"), 1), 0, 100000
        ),
        "study_index": clamp(safe_int(data.get("study_index"), 0), 0, 100000),
        "study_question_ids": [
            int(qid)
            for qid in (data.get("study_question_ids") or [])[:300]
            if isinstance(qid, int) or str(qid).isdigit()
        ],
        "plan_settings": data.get("plan_settings") or {},
        "review_settings": data.get("review_settings") or {},
        "architecture_settings": data.get("architecture_settings") or {},
        "playlist_state": data.get("playlist_state") or None,
        "session_stats": data.get("session_stats") or {},
        "updated_at": iso_now(),
    }
    updated_at = write_app_state("active_study_session", state)
    return jsonify({"message": "Sessione salvata", "updated_at": updated_at, "session": state})


@app.route("/api/attempt", methods=["POST"])
def record_attempt():
    guard = require_db_selected()
    if guard:
        return guard

    data = request.get_json(silent=True) or {}
    subject_key = get_subject_key()
    question_id = data.get("question_id")
    selected_answer_id = data.get("selected_answer_id")
    mode = data.get("mode", "training")
    rating = data.get("self_rating")
    error_reason = data.get("error_reason")

    try:
        question_id = int(question_id)
        selected_answer_id = int(selected_answer_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Tentativo non valido"}), 400

    correct_answer_id = get_correct_answer_id(question_id)
    if correct_answer_id is None:
        return jsonify({"error": "Domanda non trovata"}), 404

    is_correct = selected_answer_id == correct_answer_id
    if rating not in {"know", "unsure", "dont_know", None}:
        rating = None
    if error_reason not in {
        "confused_concept",
        "distraction",
        "forgot_definition",
        "calculation",
        None,
    }:
        error_reason = None
    if is_correct:
        error_reason = None

    stats = update_question_stats(subject_key, question_id, is_correct, rating)
    conn = get_progress_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO attempts (
            subject_key, question_id, selected_answer_id, correct_answer_id,
            is_correct, mode, self_rating, error_reason, answered_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            subject_key,
            question_id,
            selected_answer_id,
            correct_answer_id,
            1 if is_correct else 0,
            mode,
            rating,
            error_reason,
            iso_now(),
        ),
    )
    conn.commit()
    conn.close()

    return jsonify(
        {
            "question_id": question_id,
            "selected_answer_id": selected_answer_id,
            "correct_answer_id": correct_answer_id,
            "is_correct": is_correct,
            "progress": stats,
        }
    )


@app.route("/api/confidence", methods=["POST"])
def update_confidence():
    guard = require_db_selected()
    if guard:
        return guard

    data = request.get_json(silent=True) or {}
    subject_key = get_subject_key()
    question_id = data.get("question_id")
    rating = data.get("self_rating")

    try:
        question_id = int(question_id)
    except (TypeError, ValueError):
        return jsonify({"error": "Domanda non valida"}), 400

    if rating not in {"know", "unsure", "dont_know"}:
        return jsonify({"error": "Autovalutazione non valida"}), 400

    stats = apply_confidence(subject_key, question_id, rating)
    if not stats:
        return jsonify({"error": "Prima rispondi alla domanda"}), 400

    return jsonify({"question_id": question_id, "progress": stats})


@app.route("/api/progress_summary", methods=["GET"])
def progress_summary():
    guard = require_db_selected()
    if guard:
        return guard

    subject_key = get_subject_key()
    all_ids = get_all_question_ids()
    total_questions = len(all_ids)
    stats_map = fetch_stats_map(subject_key)
    now = utc_now()

    summary = {
        "total_questions": total_questions,
        "seen": 0,
        "new": 0,
        "due": 0,
        "weak": 0,
        "shaky": 0,
        "learning": 0,
        "solid": 0,
        "mastered": 0,
        "attempts": 0,
        "correct": 0,
        "wrong": 0,
        "accuracy": 0,
        "answered_today": 0,
        "new_seen_today": 0,
    }

    for q_id in all_ids:
        stats = stats_map.get(q_id, empty_stats(q_id))
        if stats["attempts"] <= 0:
            continue
        summary["seen"] += 1
        status = stats.get("status") or "learning"
        if status in summary:
            summary[status] += 1
        if (parse_dt(stats.get("due_at")) or now + timedelta(days=1)) <= now:
            summary["due"] += 1
        summary["attempts"] += stats["attempts"]
        summary["correct"] += stats["correct_count"]
        summary["wrong"] += stats["wrong_count"]

    summary["new"] = max(total_questions - summary["seen"], 0)
    if summary["attempts"]:
        summary["accuracy"] = round((summary["correct"] / summary["attempts"]) * 100)

    today = utc_now().date().isoformat()
    conn = get_progress_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT COUNT(*) AS answered, COUNT(DISTINCT question_id) AS unique_questions
        FROM attempts
        WHERE subject_key = ? AND substr(answered_at, 1, 10) = ?
        """,
        (subject_key, today),
    )
    row = cur.fetchone()
    conn.close()
    summary["answered_today"] = row["answered"] or 0
    summary["new_seen_today"] = row["unique_questions"] or 0

    return jsonify(summary)


def build_progress_summary(subject_key):
    all_ids = get_all_question_ids()
    total_questions = len(all_ids)
    stats_map = fetch_stats_map(subject_key)
    now = utc_now()

    summary = {
        "total_questions": total_questions,
        "seen": 0,
        "new": 0,
        "due": 0,
        "weak": 0,
        "shaky": 0,
        "learning": 0,
        "solid": 0,
        "mastered": 0,
        "attempts": 0,
        "correct": 0,
        "wrong": 0,
        "accuracy": 0,
        "answered_today": 0,
        "new_seen_today": 0,
    }

    for q_id in all_ids:
        stats = stats_map.get(q_id, empty_stats(q_id))
        if stats["attempts"] <= 0:
            continue
        summary["seen"] += 1
        status = stats.get("status") or "learning"
        if status in summary:
            summary[status] += 1
        if (parse_dt(stats.get("due_at")) or now + timedelta(days=1)) <= now:
            summary["due"] += 1
        summary["attempts"] += stats["attempts"]
        summary["correct"] += stats["correct_count"]
        summary["wrong"] += stats["wrong_count"]

    summary["new"] = max(total_questions - summary["seen"], 0)
    if summary["attempts"]:
        summary["accuracy"] = round((summary["correct"] / summary["attempts"]) * 100)

    today = utc_now().date().isoformat()
    conn = get_progress_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT COUNT(*) AS answered, COUNT(DISTINCT question_id) AS unique_questions
        FROM attempts
        WHERE subject_key = ? AND substr(answered_at, 1, 10) = ?
        """,
        (subject_key, today),
    )
    row = cur.fetchone()
    conn.close()
    summary["answered_today"] = row["answered"] or 0
    summary["new_seen_today"] = row["unique_questions"] or 0
    return summary


def estimate_exam_grade(coverage, accuracy, stability, weak_ratio):
    coverage = clamp(float(coverage or 0), 0, 1)
    accuracy = clamp(float(accuracy or 0), 0, 1)
    stability = clamp(float(stability or 0), 0, 1)
    weak_ratio = clamp(float(weak_ratio or 0), 0, 1)
    readiness = (
        coverage * 0.50
        + accuracy * 0.34
        + stability * 0.16
        - weak_ratio * 0.10
    )
    readiness = clamp(readiness, 0, 1)
    grade = round(readiness * 30)
    if grade >= 18:
        label = f"{grade}/30"
    elif grade >= 15:
        label = f"{grade}/30, borderline"
    else:
        label = f"{grade}/30, sotto soglia"
    return {
        "grade": grade,
        "label": label,
        "readiness": round(readiness * 100),
    }


def build_study_plan_payload(subject_key, exam_date_raw="", minutes=45, target_grade=24, days=None):
    summary = build_progress_summary(subject_key)
    minutes = clamp(safe_int(minutes, 45), 10, 240)
    target_grade = clamp(safe_int(target_grade, 24), 18, 30)

    today = datetime.now().date()
    exam_date = None
    days_left = safe_int(days, 10) if days is not None else 10
    if exam_date_raw:
        try:
            exam_date = datetime.fromisoformat(str(exam_date_raw)).date()
            days_left = max((exam_date - today).days + 1, 1)
        except ValueError:
            days_left = max(days_left, 1)

    capacity = max(8, minutes // 2)
    total_capacity = capacity * days_left
    new_needed = summary["new"]
    weak_count = summary["weak"] + summary["shaky"]
    review_backlog = max(summary["due"], weak_count)
    extra_weak_passes = weak_count
    total_work = new_needed + review_backlog + extra_weak_passes
    feasible = total_capacity >= total_work

    required_minutes_total = total_work * 2
    required_minutes_per_day = math.ceil(required_minutes_total / max(days_left, 1)) if total_work else 0

    review_today_min = math.ceil((review_backlog + extra_weak_passes) / max(days_left, 1)) if review_backlog or extra_weak_passes else 0
    review_today = min(
        review_backlog + extra_weak_passes,
        max(review_today_min, round(capacity * 0.30)) if review_backlog or extra_weak_passes else 0,
        capacity,
    )
    new_today_min = math.ceil(new_needed / max(days_left, 1)) if new_needed else 0
    new_today = min(new_needed, max(new_today_min, capacity - review_today))

    if new_today + review_today > capacity:
        overflow = new_today + review_today - capacity
        new_today = max(0, new_today - overflow)

    total_today = new_today + review_today
    estimated_minutes = total_today * 2

    total_questions = max(summary["total_questions"], 1)
    seen = summary["seen"]
    accuracy_now = (summary["accuracy"] or 0) / 100 if summary["attempts"] else 0.45
    coverage_now = seen / total_questions
    stability_now = (summary["solid"] + summary["mastered"]) / max(seen, 1) if seen else 0
    weak_ratio_now = weak_count / max(seen, 1) if seen else 0
    grade_now = estimate_exam_grade(
        coverage_now,
        accuracy_now,
        stability_now,
        weak_ratio_now,
    )

    def project_with_capacity(capacity_until_exam):
        completed_capacity_for_new = max(
            capacity_until_exam - min(review_backlog + extra_weak_passes, capacity_until_exam),
            0,
        )
        projected_new_completed = min(new_needed, completed_capacity_for_new)
        projected_seen = min(
            summary["total_questions"],
            summary["seen"] + projected_new_completed,
        )
        work_ratio = min(capacity_until_exam / max(total_work, 1), 1) if total_work else 1
        review_done_ratio = min(
            capacity_until_exam / max(review_backlog + extra_weak_passes, 1),
            1,
        ) if (review_backlog + extra_weak_passes) else 1
        projected_coverage = projected_seen / total_questions
        projected_accuracy = clamp(
            accuracy_now + 0.16 * review_done_ratio + 0.06 * work_ratio,
            0,
            0.94,
        )
        projected_stability = clamp(
            (
                summary["solid"]
                + summary["mastered"]
                + weak_count * review_done_ratio
                + projected_new_completed * 0.35
            )
            / total_questions,
            0,
            1,
        )
        projected_weak_ratio = clamp(
            (weak_count * (1 - review_done_ratio)) / total_questions,
            0,
            1,
        )
        return {
            "projected_new_completed": projected_new_completed,
            "coverage_projected": round(projected_coverage * 100),
            "accuracy_projected": round(projected_accuracy * 100),
            "stability_projected": round(projected_stability * 100),
            "weak_projected": round(projected_weak_ratio * 100),
            "grade": estimate_exam_grade(
                projected_coverage,
                projected_accuracy,
                projected_stability,
                projected_weak_ratio,
            ),
        }

    projected = project_with_capacity(total_capacity)
    target_reached = projected["grade"]["grade"] >= target_grade

    if not total_work:
        feasibility_label = "Sei in manutenzione: oggi basta tenere calde le domande."
    elif feasible:
        feasibility_label = "Piano sostenibile con il tempo inserito."
    else:
        feasibility_label = "Piano stretto: aumenta i minuti o parti dagli errori piu pesanti."

    if target_reached:
        target_label = f"Obiettivo {target_grade}/30 raggiungibile seguendo il piano."
    else:
        target_label = f"Per puntare a {target_grade}/30 serve piu volume o piu recupero errori."

    return {
        "today": today.isoformat(),
        "exam_date": exam_date.isoformat() if exam_date else "",
        "days_left": days_left,
        "minutes": minutes,
        "capacity": capacity,
        "total_capacity": total_capacity,
        "total_work": total_work,
        "new_today": new_today,
        "review_today": review_today,
        "total_today": total_today,
        "estimated_minutes": estimated_minutes,
        "feasible": feasible,
        "feasibility_label": feasibility_label,
        "required_daily_minutes": required_minutes_per_day,
        "missing_minutes": max(required_minutes_total - total_capacity * 2, 0),
        "missing_daily_minutes": max(required_minutes_per_day - minutes, 0),
        "forecast": {
            "target_grade": target_grade,
            "target_reached": target_reached,
            "target_label": target_label,
            "grade_now": grade_now,
            "grade_projected": projected["grade"],
            "coverage_projected": projected["coverage_projected"],
            "accuracy_projected": projected["accuracy_projected"],
            "stability_projected": projected["stability_projected"],
            "weak_projected": projected["weak_projected"],
        },
        "summary": summary,
    }


def get_subject_profile(subject_key):
    profiles = read_subject_profiles()
    profile = profiles.get(subject_key)
    return profile if isinstance(profile, dict) else {}


def recommended_flow_from_summary(summary):
    weak_total = summary.get("weak", 0) + summary.get("shaky", 0)
    if weak_total > 0:
        return {
            "flow": "sprint_recover",
            "label": "Recupera errori",
            "reason": "Parto dagli errori e dalle incerte: sono quelle che ti fanno salire piu velocemente.",
        }
    if summary.get("due", 0) > 0:
        return {
            "flow": "smart",
            "preset": "due",
            "label": "Ripasso scadute",
            "reason": "Ci sono domande da ripassare oggi: meglio chiuderle prima delle nuove.",
        }
    if summary.get("new", 0) > 0:
        return {
            "flow": "new",
            "label": "Nuove domande",
            "reason": "Non hai arretrato critico: conviene coprire nuovo programma.",
        }
    return {
        "flow": "tutor",
        "label": "Misto casuale",
        "reason": "Hai coperto molto: facciamo mantenimento con domande casuali e spiegazione.",
    }


def subject_source_key(subject_key):
    if "architettura" in str(subject_key or "").lower():
        return ARCHITECTURE_SOURCE_KEY
    return subject_key


def clean_topic_label(topic):
    label = re.sub(r"\s*\(\d{2}:\d{2}:\d{2}\)\s*$", "", str(topic or "Argomento"))
    if " - " in label:
        label = label.split(" - ", 1)[1]
    label = re.sub(r"\s+\(\d+\)$", "", label).strip(" .")
    return label[:70] or "Argomento"


def build_keyword_topic_map(subject_key, summary):
    definitions = subject_topic_definitions(subject_key)
    if not definitions:
        return []

    all_ids = get_all_question_ids()
    if not all_ids:
        return []

    blobs = fetch_question_blobs(all_ids)
    buckets = {topic["id"]: [] for topic in definitions}
    for qid, blob in blobs.items():
        topic_id = match_question_topic(blob, definitions)
        if topic_id in buckets:
            buckets[topic_id].append(qid)

    stats_map = fetch_stats_map(subject_key, all_ids)
    now = utc_now()
    topics = []
    for topic in definitions:
        ids = buckets.get(topic["id"], [])
        total = len(ids)
        if not total:
            continue

        seen = 0
        solid = 0
        weak = 0
        due = 0
        for qid in ids:
            stats = stats_map.get(qid, empty_stats(qid))
            if stats["attempts"] > 0:
                seen += 1
            if stats["status"] in {"solid", "mastered"}:
                solid += 1
            if stats["status"] in {"weak", "shaky"} or stats["wrong_count"] > 0:
                weak += 1
            due_at = parse_dt(stats.get("due_at"))
            if stats["attempts"] > 0 and due_at and due_at <= now:
                due += 1

        seen_pct = round((seen / total) * 100)
        solid_pct = round((solid / total) * 100)
        detail_parts = [f"{seen}/{total} viste"]
        if weak:
            detail_parts.append(f"{weak} deboli")
        if due:
            detail_parts.append(f"{due} scadute")
        if not weak and not due:
            remaining = max(total - seen, 0)
            detail_parts.append(f"{remaining} nuove" if remaining else "stabile")

        topics.append(
            {
                "id": topic["id"],
                "label": topic["label"],
                "seen_pct": seen_pct,
                "solid_pct": solid_pct,
                "detail": ", ".join(detail_parts),
                "weak_count": weak,
                "due_count": due,
                "total": total,
                "action": "review_topic",
            }
        )

    topics.sort(
        key=lambda item: (
            item["weak_count"],
            item["due_count"],
            -item["solid_pct"],
            -item["seen_pct"],
            item["total"],
        ),
        reverse=True,
    )
    return topics[:8]


def build_subject_topic_map(subject_key, summary):
    if "architettura" in str(subject_key or "").lower():
        arch_stats = architecture_stats_payload()
        topics = []
        for topic in ARCHITECTURE_TOPICS:
            if topic["id"] == "mixed":
                continue
            item = arch_stats["by_topic"].get(topic["id"], {})
            attempts = safe_int(item.get("attempts"), 0)
            accuracy = safe_int(item.get("accuracy"), 0)
            topics.append(
                {
                    "id": topic["id"],
                    "label": topic["label"],
                    "seen_pct": min(100, attempts * 10),
                    "solid_pct": accuracy if attempts else 0,
                    "detail": f"{attempts} esercizi",
                    "action": "architecture",
                }
            )
        return topics[:8]

    keyword_topics = build_keyword_topic_map(subject_key, summary)
    if keyword_topics:
        return keyword_topics

    source_key = subject_source_key(subject_key)
    conn = get_source_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT topic, COUNT(*) AS count
            FROM study_notes
            WHERE subject_key = ?
            GROUP BY topic
            ORDER BY count DESC
            LIMIT 12
            """,
            (source_key,),
        )
        rows = cur.fetchall()
    except sqlite3.Error:
        rows = []
    finally:
        conn.close()

    total_seen_pct = round((summary.get("seen", 0) / max(summary.get("total_questions", 1), 1)) * 100)
    solid_pct = round(((summary.get("solid", 0) + summary.get("mastered", 0)) / max(summary.get("seen", 1), 1)) * 100) if summary.get("seen") else 0
    topics = []
    used = set()
    for row in rows:
        label = clean_topic_label(row["topic"])
        if label.lower() in used:
            continue
        used.add(label.lower())
        topics.append(
            {
                "id": normalize_source_word(label) or f"topic_{len(topics) + 1}",
                "label": label,
                "seen_pct": total_seen_pct,
                "solid_pct": solid_pct,
                "detail": f"{row['count']} appunti",
                "action": "review_weak",
            }
        )
        if len(topics) >= 6:
            break
    if topics:
        return topics
    return [
        {
            "id": "general",
            "label": "Copertura generale",
            "seen_pct": total_seen_pct,
            "solid_pct": solid_pct,
            "detail": f"{summary.get('seen', 0)}/{summary.get('total_questions', 0)} viste",
            "action": "review_weak",
        }
    ]


def build_streak_payload(subject_key, summary):
    conn = get_progress_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT DISTINCT substr(answered_at, 1, 10) AS day
        FROM attempts
        WHERE subject_key = ?
        ORDER BY day DESC
        """,
        (subject_key,),
    )
    days = [row["day"] for row in cur.fetchall() if row["day"]]
    today = utc_now().date()
    streak = 0
    cursor_day = today
    day_set = set(days)
    while cursor_day.isoformat() in day_set:
        streak += 1
        cursor_day -= timedelta(days=1)

    cur.execute(
        """
        SELECT COUNT(DISTINCT a.question_id) AS recovered
        FROM attempts a
        JOIN question_stats qs
          ON qs.subject_key = a.subject_key AND qs.question_id = a.question_id
        WHERE a.subject_key = ?
          AND substr(a.answered_at, 1, 10) = ?
          AND a.is_correct = 1
          AND qs.wrong_count > 0
        """,
        (subject_key, today.isoformat()),
    )
    recovered = cur.fetchone()["recovered"] or 0
    conn.close()
    return {
        "streak_days": streak,
        "answered_today": summary.get("answered_today", 0),
        "recovered_today": recovered,
        "energy": min(100, summary.get("answered_today", 0) * 5 + recovered * 10),
    }


def error_reason_label(reason):
    return {
        "confused_concept": "concetto confuso",
        "distraction": "distrazione",
        "forgot_definition": "definizione da fissare",
        "calculation": "calcolo",
    }.get(reason or "", "errore da rivedere")


def build_error_diary(subject_key, limit=5):
    stats_map = fetch_stats_map(subject_key)
    candidates = [
        (qid, stats)
        for qid, stats in stats_map.items()
        if stats.get("wrong_count", 0) > 0
        or stats.get("status") in {"weak", "shaky"}
    ]
    candidates.sort(key=lambda item: priority_score(item[1]), reverse=True)
    ids = [qid for qid, _ in candidates[:limit]]

    latest_reasons = {}
    reason_counts = {}
    conn = get_progress_connection()
    cur = conn.cursor()
    if ids:
        placeholders = ",".join("?" for _ in ids)
        cur.execute(
            f"""
            SELECT question_id, error_reason, answered_at
            FROM attempts
            WHERE subject_key = ?
              AND is_correct = 0
              AND question_id IN ({placeholders})
            ORDER BY answered_at DESC
            """,
            [subject_key, *ids],
        )
        for row in cur.fetchall():
            if row["question_id"] not in latest_reasons and row["error_reason"]:
                latest_reasons[row["question_id"]] = row["error_reason"]

    cur.execute(
        """
        SELECT error_reason, COUNT(*) AS count
        FROM attempts
        WHERE subject_key = ? AND is_correct = 0 AND error_reason IS NOT NULL
        GROUP BY error_reason
        ORDER BY count DESC
        LIMIT 3
        """,
        (subject_key,),
    )
    for row in cur.fetchall():
        reason_counts[row["error_reason"]] = row["count"]
    conn.close()

    question_texts = {}
    if ids:
        conn = get_connection()
        cur = conn.cursor()
        placeholders = ",".join("?" for _ in ids)
        cur.execute(
            f"SELECT id, testo FROM questions WHERE id IN ({placeholders})",
            ids,
        )
        for row in cur.fetchall():
            question_texts[row[0]] = compact_excerpt(decode_quiz_text(row[1]), 118)
        conn.close()

    items = []
    for qid, stats in candidates[:limit]:
        reason = latest_reasons.get(qid)
        wrong_count = safe_int(stats.get("wrong_count"), 0)
        status = stats.get("status") or "learning"
        items.append(
            {
                "question_id": qid,
                "text": question_texts.get(qid, f"Domanda {qid}"),
                "wrong_count": wrong_count,
                "status": status,
                "reason": error_reason_label(reason),
                "action": "Ritentala oggi" if status in {"weak", "shaky"} else "Richiamo veloce",
            }
        )

    top_reason = None
    if reason_counts:
        top_reason = max(reason_counts.items(), key=lambda item: item[1])[0]

    return {
        "items": items,
        "top_reason": error_reason_label(top_reason) if top_reason else "",
        "summary": (
            f"Priorita: {error_reason_label(top_reason)}."
            if top_reason
            else "Nessun errore classificato: fai nuove domande o un misto leggero."
        ),
    }


@app.route("/api/today_dashboard", methods=["GET"])
def today_dashboard():
    guard = require_db_selected()
    if guard:
        return guard

    subject_key = get_subject_key()
    dbs = scan_databases()
    profile = get_subject_profile(subject_key)
    plan = build_study_plan_payload(
        subject_key,
        profile.get("exam_date") or request.args.get("exam_date") or "",
        profile.get("study_minutes") or request.args.get("minutes", default=45, type=int) or 45,
        profile.get("target_grade") or request.args.get("target_grade", default=24, type=int) or 24,
        request.args.get("days", default=10, type=int),
    )
    summary = plan["summary"]
    recommendation = recommended_flow_from_summary(summary)
    weak_total = summary.get("weak", 0) + summary.get("shaky", 0)
    errors_today = min(max(weak_total, summary.get("due", 0)), plan.get("review_today", 0))
    focus_count = max(6, min(10, 15 // 2 + min(weak_total, 3)))
    focus_flow = recommendation.get("flow", "smart")
    daily_load = math.ceil(plan.get("total_work", 0) / max(plan.get("days_left", 1), 1)) if plan.get("total_work", 0) else 0

    return jsonify(
        {
            "subject_key": subject_key,
            "subject_label": dbs.get(subject_key, {}).get("label", "Materia"),
            "profile": profile,
            "summary": summary,
            "today": {
                "new": plan.get("new_today", 0),
                "review": plan.get("review_today", 0),
                "errors": errors_today,
                "estimated_minutes": plan.get("estimated_minutes", 0),
                "projected_grade": plan.get("forecast", {}).get("grade_projected", {}),
                "target_grade": plan.get("forecast", {}).get("target_grade", 24),
                "feasibility_label": plan.get("feasibility_label", ""),
                "days_left": plan.get("days_left", 0),
                "daily_questions_required": daily_load,
                "required_daily_minutes": plan.get("required_daily_minutes", 0),
            },
            "recommendation": {
                **recommendation,
                "count": max(plan.get("total_today", 0), 10 if summary.get("new", 0) else 6),
            },
            "focus": {
                "minutes": 15,
                "count": focus_count,
                "flow": focus_flow,
                "label": "Focus 15 minuti",
                "goal": "Una sessione corta: errori prima, poi ripasso o nuove.",
            },
            "topics": build_subject_topic_map(subject_key, summary),
            "streak": build_streak_payload(subject_key, summary),
            "diary": build_error_diary(subject_key),
        }
    )


@app.route("/api/study_plan", methods=["GET"])
def study_plan():
    guard = require_db_selected()
    if guard:
        return guard

    subject_key = get_subject_key()
    return jsonify(
        build_study_plan_payload(
            subject_key,
            request.args.get("exam_date"),
            request.args.get("minutes", default=45, type=int) or 45,
            request.args.get("target_grade", default=24, type=int) or 24,
            request.args.get("days", default=10, type=int),
        )
    )

    summary = build_progress_summary(subject_key)
    exam_date_raw = request.args.get("exam_date")
    minutes = clamp(request.args.get("minutes", default=45, type=int) or 45, 10, 240)
    target_grade = clamp(request.args.get("target_grade", default=24, type=int) or 24, 18, 30)

    today = datetime.now().date()
    exam_date = None
    days_left = request.args.get("days", default=10, type=int) or 10
    if exam_date_raw:
        try:
            exam_date = datetime.fromisoformat(exam_date_raw).date()
            days_left = max((exam_date - today).days + 1, 1)
        except ValueError:
            days_left = max(days_left, 1)

    capacity = max(8, minutes // 2)
    total_capacity = capacity * days_left
    new_needed = summary["new"]
    weak_count = summary["weak"] + summary["shaky"]
    review_backlog = max(summary["due"], weak_count)
    extra_weak_passes = weak_count
    total_work = new_needed + review_backlog + extra_weak_passes
    feasible = total_capacity >= total_work

    daily_required_questions = math.ceil(total_work / max(days_left, 1)) if total_work else 0
    required_minutes_total = total_work * 2
    required_minutes_per_day = math.ceil(required_minutes_total / max(days_left, 1)) if total_work else 0

    review_today_min = math.ceil((review_backlog + extra_weak_passes) / max(days_left, 1)) if review_backlog or extra_weak_passes else 0
    review_today = min(
        review_backlog + extra_weak_passes,
        max(review_today_min, round(capacity * 0.30)) if review_backlog or extra_weak_passes else 0,
        capacity,
    )
    new_today_min = math.ceil(new_needed / max(days_left, 1)) if new_needed else 0
    new_today = min(new_needed, max(new_today_min, capacity - review_today))

    if new_today + review_today > capacity:
        overflow = new_today + review_today - capacity
        new_today = max(0, new_today - overflow)

    total_today = new_today + review_today
    estimated_minutes = total_today * 2

    total_questions = max(summary["total_questions"], 1)
    seen = summary["seen"]
    accuracy_now = (summary["accuracy"] or 0) / 100 if summary["attempts"] else 0.45
    coverage_now = seen / total_questions
    stability_now = (summary["solid"] + summary["mastered"]) / max(seen, 1) if seen else 0
    weak_ratio_now = weak_count / max(seen, 1) if seen else 0
    grade_now = estimate_exam_grade(
        coverage_now,
        accuracy_now,
        stability_now,
        weak_ratio_now,
    )

    def project_with_capacity(capacity_until_exam):
        completed_capacity_for_new = max(
            capacity_until_exam - min(review_backlog + extra_weak_passes, capacity_until_exam),
            0,
        )
        projected_new_completed = min(new_needed, completed_capacity_for_new)
        projected_seen = min(
            summary["total_questions"],
            summary["seen"] + projected_new_completed,
        )
        work_ratio = min(capacity_until_exam / max(total_work, 1), 1) if total_work else 1
        review_done_ratio = min(
            capacity_until_exam / max(review_backlog + extra_weak_passes, 1),
            1,
        ) if (review_backlog + extra_weak_passes) else 1
        projected_coverage = projected_seen / total_questions
        projected_accuracy = clamp(
            accuracy_now + 0.16 * review_done_ratio + 0.06 * work_ratio,
            0,
            0.94,
        )
        projected_stability = clamp(
            (
                summary["solid"]
                + summary["mastered"]
                + weak_count * review_done_ratio
                + projected_new_completed * 0.35
            )
            / total_questions,
            0,
            1,
        )
        projected_weak_ratio = clamp(
            (weak_count * (1 - review_done_ratio)) / total_questions,
            0,
            1,
        )
        return {
            "projected_new_completed": projected_new_completed,
            "projected_seen": projected_seen,
            "coverage": projected_coverage,
            "accuracy": projected_accuracy,
            "stability": projected_stability,
            "weak_ratio": projected_weak_ratio,
            "grade": estimate_exam_grade(
                projected_coverage,
                projected_accuracy,
                projected_stability,
                projected_weak_ratio,
            ),
        }

    projection = project_with_capacity(total_capacity)
    projected_seen = projection["projected_seen"]
    missing_work = max(total_work - total_capacity, 0)
    missing_minutes = missing_work * 2
    missing_daily_minutes = math.ceil(missing_minutes / max(days_left, 1)) if missing_minutes else 0
    missing_questions_by_exam = max(summary["total_questions"] - projected_seen, 0)
    projected_coverage = projection["coverage"]
    projected_accuracy = projection["accuracy"]
    grade_projected = projection["grade"]

    target_reached = grade_projected["grade"] >= target_grade
    target_required_minutes_per_day = None
    target_required_grade = None
    for candidate_minutes in range(10, 481):
        candidate_capacity = max(8, candidate_minutes // 2) * days_left
        candidate_projection = project_with_capacity(candidate_capacity)
        if candidate_projection["grade"]["grade"] >= target_grade:
            target_required_minutes_per_day = candidate_minutes
            target_required_grade = candidate_projection["grade"]
            break

    if target_reached:
        target_label = f"Obiettivo {target_grade}/30 raggiungibile con il ritmo attuale."
    elif target_required_minutes_per_day:
        target_label = (
            f"Per puntare a {target_grade}/30 servono circa "
            f"{target_required_minutes_per_day} min/giorno."
        )
    else:
        target_label = (
            f"Obiettivo {target_grade}/30 troppo alto con i dati attuali: "
            "serve piu tempo o piu accuratezza."
        )

    if not exam_date_raw:
        feasibility_label = "Inserisci la data esame per una stima precisa."
    elif feasible:
        feasibility_label = "Fattibile con il ritmo impostato."
    else:
        feasibility_label = (
            f"Non fattibile con {minutes} min/giorno: servono circa "
            f"{required_minutes_per_day} min/giorno."
        )

    return jsonify(
        {
            "today": today.isoformat(),
            "exam_date": exam_date.isoformat() if exam_date else None,
            "days_left": days_left,
            "minutes": minutes,
            "capacity": capacity,
            "total_capacity": total_capacity,
            "total_work": total_work,
            "daily_required_questions": daily_required_questions,
            "required_minutes_total": required_minutes_total,
            "required_minutes_per_day": required_minutes_per_day,
            "feasible": feasible,
            "feasibility_label": feasibility_label,
            "missing_work": missing_work,
            "missing_minutes": missing_minutes,
            "missing_daily_minutes": missing_daily_minutes,
            "missing_questions_by_exam": missing_questions_by_exam,
            "new_today": new_today,
            "review_today": review_today,
            "total_today": total_today,
            "estimated_minutes": estimated_minutes,
            "forecast": {
                "target_grade": target_grade,
                "target_reached": target_reached,
                "target_label": target_label,
                "target_required_minutes_per_day": target_required_minutes_per_day,
                "target_required_grade": target_required_grade,
                "coverage_now": round(coverage_now * 100),
                "coverage_projected": round(projected_coverage * 100),
                "accuracy_now": round(accuracy_now * 100),
                "accuracy_projected": round(projected_accuracy * 100),
                "grade_now": grade_now,
                "grade_projected": grade_projected,
            },
            "summary": summary,
        }
    )


@app.route("/api/python_tutorial", methods=["GET", "DELETE"])
def python_tutorial():
    lessons = load_python_tutorial_lessons()
    if not lessons:
        return jsonify({"error": "Tutorial Python non configurato"}), 404

    if request.method == "DELETE":
        delete_app_state("python_tutorial_progress")
        state = get_tutorial_state()
        payload = build_tutorial_payload(lessons, state)
        return jsonify({"message": "Tutorial azzerato", **payload})

    state = get_tutorial_state()
    payload = build_tutorial_payload(lessons, state)
    return jsonify(payload)


@app.route("/api/python_tutorial/<lesson_id>", methods=["GET", "POST"])
def python_tutorial_lesson(lesson_id):
    lessons = load_python_tutorial_lessons()
    lesson = find_tutorial_lesson(lessons, lesson_id)
    if not lesson:
        return jsonify({"error": "Lezione non trovata"}), 404

    state = get_tutorial_state()
    unlocked_ids = tutorial_unlocked_ids(lessons, state)
    if lesson_id not in unlocked_ids:
        return jsonify({"error": "Completa prima la lezione precedente"}), 403

    data = request.get_json(silent=True) or {}
    if request.method == "POST":
        state["active_lesson_id"] = lesson_id
        if "code" in data:
            code = str(data.get("code") or "")[:6000]
            state.setdefault("code_by_lesson", {})[lesson_id] = code
        state = save_tutorial_state(state)

    public = public_tutorial_lesson(lesson, state, unlocked_ids, include_details=True)
    payload = build_tutorial_payload(lessons, state, include_lessons=False)
    return jsonify({"lesson": public, "progress": payload})


@app.route("/api/python_tutorial/run", methods=["POST"])
def python_tutorial_run():
    lessons = load_python_tutorial_lessons()
    data = request.get_json(silent=True) or {}
    lesson_id = data.get("lesson_id")
    code = str(data.get("code") or "")[:6000]

    lesson = find_tutorial_lesson(lessons, lesson_id)
    if not lesson:
        return jsonify({"error": "Lezione non trovata"}), 404

    state = get_tutorial_state()
    unlocked_ids = tutorial_unlocked_ids(lessons, state)
    if lesson_id not in unlocked_ids:
        return jsonify({"error": "Completa prima la lezione precedente"}), 403

    result = run_tutorial_code(code, lesson.get("checks") or [])
    state["active_lesson_id"] = lesson_id
    state.setdefault("code_by_lesson", {})[lesson_id] = code
    if result.get("success"):
        completed = set(state.get("completed_lesson_ids") or [])
        completed.add(lesson_id)
        state["completed_lesson_ids"] = sorted(completed)
    state = save_tutorial_state(state)

    payload = build_tutorial_payload(lessons, state)
    next_lesson = None
    if result.get("success"):
        current_index = lesson["index"]
        if current_index + 1 < len(lessons):
            next_lesson = public_tutorial_lesson(
                lessons[current_index + 1],
                state,
                tutorial_unlocked_ids(lessons, state),
            )

    return jsonify(
        {
            "result": result,
            "lesson": public_tutorial_lesson(
                lesson,
                state,
                tutorial_unlocked_ids(lessons, state),
                include_details=True,
            ),
            "progress": payload,
            "next_lesson": next_lesson,
        }
    )


@app.route("/api/study_note/<int:id>", methods=["GET"])
def study_note(id):
    guard = require_db_selected()
    if guard:
        return guard

    subject_key = get_subject_key()
    conn = get_connection()
    cursor = conn.cursor()
    payload = build_question_payload(cursor, id, include_images=False)
    conn.close()
    if not payload:
        return jsonify({"error": "Domanda non trovata"}), 404

    correct_text = ""
    selected_text = ""
    selected_answer_id = safe_int(request.args.get("selected_answer_id"), 0)
    wrong_texts = []
    for answer in payload["risposte"]:
        if answer["id"] == payload["corretta"]:
            correct_text = answer.get("testo") or "Risposta corretta"
        else:
            wrong_texts.append(answer.get("testo") or "Distrattore")
        if selected_answer_id and answer["id"] == selected_answer_id:
            selected_text = answer.get("testo") or ""

    progress = fetch_stats_map(subject_key, [id]).get(id, empty_stats(id))
    if progress["status"] in {"weak", "shaky"}:
        focus = "Questa domanda va rivista: falla tornare nel ripasso finche non la riconosci senza esitazione."
    elif progress["status"] in {"solid", "mastered"}:
        focus = "Questa sembra stabile: usala come controllo rapido, non come priorita principale."
    else:
        focus = "Prima esposizione: leggi bene domanda e risposta corretta, poi prova a richiamarla senza guardare."

    source_query = f"{payload.get('testo', '')} {correct_text}"
    source_notes = find_study_sources(subject_key, source_query, limit=1)
    source_excerpt = source_notes[0]["excerpt"] if source_notes else ""
    python_lab = build_python_lab(
        subject_key,
        payload.get("testo", ""),
        correct_text,
        selected_text,
    )

    clean_question = decode_quiz_text(payload.get("testo", ""))
    selected_short = compact_excerpt(decode_quiz_text(selected_text), 150)
    focus_terms = [
        term
        for term in sorted(
            source_terms(f"{clean_question} {correct_text}"),
            key=lambda item: (-len(item), item),
        )
        if len(term) >= 5
    ]
    focus_word = focus_terms[0] if focus_terms else "concetto"

    mistake = ""
    why = f"Il punto da riconoscere e '{focus_word}': richiama la regola collegata prima di leggere le opzioni."
    if selected_text:
        mistake = (
            f"Hai scelto: {selected_short}. Il tranello era riconoscere il concetto '{focus_word}' "
            "prima di confrontare le opzioni."
        )
        why = (
            f"La differenza da fissare e il concetto '{focus_word}'. "
            "Quando la domanda cambia una parola o un simbolo, quella parola decide la risposta."
        )

    if source_excerpt:
        example = f"Esempio dalla dispensa: {compact_excerpt(source_excerpt, 280)}"
    elif is_programming_subject(subject_key):
        example = "Esempio: scrivi un caso minimo in Python, eseguilo mentalmente riga per riga e controlla quale valore cambia."
    else:
        example = "Esempio: copri le opzioni, richiama la regola in una frase e poi scegli la risposta che la rispetta meglio."

    if is_programming_subject(subject_key):
        memory_tip = (
            f"Domande simili: cerca la parola-spia '{focus_word}', poi esegui il codice riga per riga. "
            "Se cambiano valori, operatori o indentazione, cambia anche il ramo che viene eseguito."
        )
    else:
        memory_tip = (
            f"Domande simili: cerca la parola-spia '{focus_word}'. "
            "Se cambiano simboli, percentuali, variabili o definizioni, non rispondere a memoria: "
            "prima chiediti cosa rappresenta quel dato nella domanda."
        )

    return jsonify(
        {
            "question_id": id,
            "correct_text": correct_text,
            "selected_text": selected_text,
            "distractors": wrong_texts,
            "mistake": mistake,
            "why": why,
            "example": example,
            "memory_tip": memory_tip,
            "focus": focus,
            "hint": "Fissa l'idea chiave, poi prova a richiamarla senza guardare.",
            "source_notes": source_notes,
            "python_lab": python_lab,
        }
    )


@app.route("/")
def index():
    return render_template("quiz.html")


init_progress_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
