import json
import re
import sqlite3
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPTS_DIR = REPO_ROOT / "data" / "architecture_video_transcripts"
SOURCE_DB = REPO_ROOT / "data" / "study_sources.db"
SUBJECT_KEY = "architecture"

STOPWORDS = {
    "alla", "allo", "agli", "alle", "che", "con", "dal", "dalla", "dalle",
    "dello", "della", "delle", "degli", "dei", "del", "di", "gli", "nel",
    "nella", "nelle", "per", "quale", "quando", "sono", "sulla", "questo",
    "questa", "questi", "queste", "anche", "essere", "viene", "vengono",
    "dopo", "prima", "quindi", "diciamo", "appunto", "ovviamente", "cioe",
    "abbiamo", "detto", "puo", "piu", "fare", "come", "delle", "degli",
}

TOPIC_KEYWORDS = {
    "conversioni": {
        "label": "Conversioni basi",
        "terms": [
            "binario", "ottale", "esadecimale", "conversione", "base",
            "complemento", "virgola", "floating", "ieee",
        ],
    },
    "porte_logiche": {
        "label": "Porte logiche e Boole",
        "terms": [
            "and", "or", "not", "nor", "nand", "xor", "boole", "karnaugh",
            "mintermini", "sop", "porta", "porte",
        ],
    },
    "mips_assembly": {
        "label": "MIPS / Assembly",
        "terms": [
            "mips", "assembly", "load", "store", "branch", "beq", "bne",
            "lw", "sw", "lb", "sb", "addi", "registro", "registri",
        ],
    },
    "memoria_bus": {
        "label": "Memoria e bus",
        "terms": [
            "memoria", "cache", "bus", "indirizzo", "temporizzazione", "ram",
            "rom", "word", "ampiezza", "lettura", "scrittura",
        ],
    },
    "microarchitettura": {
        "label": "Microarchitettura e IJVM",
        "terms": [
            "microarchitettura", "microistruzione", "microistruzioni", "mic",
            "mic-1", "ijvm", "datapath", "alu", "controllo", "microprogrammata",
        ],
    },
    "clock_prestazioni": {
        "label": "Clock e prestazioni",
        "terms": [
            "clock", "ciclo", "cicli", "frequenza", "cpi", "prestazioni",
            "tempo", "latenza", "velocita",
        ],
    },
    "registri_flip_flop": {
        "label": "Registri e flip-flop",
        "terms": ["flip flop", "latch", "registro", "registri", "propagazione"],
    },
}


def fix_mojibake(text):
    if "Ã" not in text and "â" not in text:
        return text
    try:
        return text.encode("latin1").decode("utf-8")
    except UnicodeError:
        return text


def normalize_word(word):
    text = fix_mojibake(str(word)).lower()
    text = text.translate(str.maketrans("àèéìòù", "aeeiou"))
    return re.sub(r"[^a-z0-9_]", "", text)


def keywords_for(text, extra_terms=None, limit=48):
    words = [normalize_word(w) for w in re.findall(r"\b[\wÀ-ÿ]{3,}\b", fix_mojibake(text))]
    words = [w for w in words if w and w not in STOPWORDS and not w.isdigit()]
    if extra_terms:
        words.extend(normalize_word(term) for term in extra_terms)
    counts = Counter(words)
    return " ".join(word for word, _ in counts.most_common(limit))


def parse_transcript_line(line):
    match = re.match(r"^\[(\d\d:\d\d:\d\d)\s+-\s+(\d\d:\d\d:\d\d)\]\s*(.*)$", line)
    if not match:
        return None
    start, end, text = match.groups()
    text = re.sub(r"\s+", " ", fix_mojibake(text)).strip()
    if not text:
        return None
    return {"start": start, "end": end, "text": text}


def score_topics(text):
    lowered = normalize_word(text)
    original = fix_mojibake(text).lower()
    scored = []
    for topic, data in TOPIC_KEYWORDS.items():
        score = 0
        hits = []
        for term in data["terms"]:
            normalized = normalize_word(term)
            count = lowered.count(normalized) if normalized else 0
            if " " in term:
                count += original.count(term)
            if count:
                score += count
                hits.append(term)
        if score:
            scored.append((score, topic, hits))
    scored.sort(reverse=True)
    return scored


def chunk_segments(segments, max_chars=1500, min_chars=520):
    chunks = []
    current = []
    current_len = 0

    for segment in segments:
        current.append(segment)
        current_len += len(segment["text"]) + 1
        if current_len >= max_chars:
            chunks.append(current)
            current = []
            current_len = 0

    if current:
        if chunks and current_len < min_chars:
            chunks[-1].extend(current)
        else:
            chunks.append(current)
    return chunks


def ensure_schema(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS study_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_key TEXT NOT NULL,
            source_title TEXT NOT NULL,
            topic TEXT NOT NULL,
            content TEXT NOT NULL,
            keywords TEXT NOT NULL,
            page_start INTEGER,
            page_end INTEGER
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_study_notes_subject ON study_notes(subject_key)"
    )
    conn.commit()


def import_transcripts():
    manifest_path = TRANSCRIPTS_DIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    lessons = manifest.get("lessons") or []

    SOURCE_DB.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(SOURCE_DB)
    ensure_schema(conn)
    conn.execute("DELETE FROM study_notes WHERE subject_key = ?", (SUBJECT_KEY,))

    inserted = 0
    for lesson in lessons:
        text_path = REPO_ROOT / lesson["text"]
        if not text_path.exists():
            continue
        lines = text_path.read_text(encoding="utf-8").splitlines()
        segments = [item for item in (parse_transcript_line(line) for line in lines) if item]
        for chunk in chunk_segments(segments):
            content = " ".join(item["text"] for item in chunk)
            scored = score_topics(content)
            if scored:
                _, topic_id, hits = scored[0]
                label = TOPIC_KEYWORDS[topic_id]["label"]
            else:
                topic_id, hits = "architettura", []
                label = "Architettura"

            topic = f"{fix_mojibake(lesson['title'])} - {label} ({chunk[0]['start']})"
            blob = f"{topic} {content}"
            conn.execute(
                """
                INSERT INTO study_notes (
                    subject_key, source_title, topic, content, keywords,
                    page_start, page_end
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    SUBJECT_KEY,
                    "Video Architettura dei Calcolatori",
                    topic,
                    content,
                    keywords_for(blob, hits),
                    None,
                    None,
                ),
            )
            inserted += 1

    conn.commit()
    conn.close()
    return len(lessons), inserted


def main():
    lessons, notes = import_transcripts()
    print(f"Video importati: {lessons}")
    print(f"Note create: {notes}")
    print(f"Database: {SOURCE_DB}")


if __name__ == "__main__":
    main()
