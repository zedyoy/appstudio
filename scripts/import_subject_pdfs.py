import argparse
import hashlib
import random
import re
import shutil
import sqlite3
from pathlib import Path

import pdfplumber


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
PROG2_HEADER = (
    "DO NOT PAY FOR THIS DOCUMENT - FREE DOCUMENT - NO DOCSITY - "
    "NON PAGARE PER QUESTO DOCUMENTO"
)


def clean_text(value):
    lines = []
    for line in (value or "").splitlines():
        line = line.strip()
        if not line or line == PROG2_HEADER:
            continue
        lines.append(line)
    return re.sub(r"\s+", " ", " ".join(lines)).strip()


def normalized_key(question, answers):
    parts = [question, *(answers.get(letter, "") for letter in "ABCD")]
    blob = "|".join(parts).lower()
    blob = re.sub(r"\W+", "", blob)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()


def extract_pdf_text(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join(
            (page.extract_text(x_tolerance=1, y_tolerance=3) or "")
            for page in pdf.pages
        )


def ensure_quiz_schema(conn):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            testo TEXT NOT NULL,
            immagine BLOB,
            is_saved INTEGER DEFAULT 0
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domanda_id INTEGER NOT NULL,
            testo TEXT NOT NULL,
            immagine BLOB,
            corretta BOOLEAN NOT NULL DEFAULT 0
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )
    conn.commit()


def set_subject(conn, subject):
    conn.execute(
        """
        INSERT INTO meta(key, value) VALUES ('subject', ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """,
        (subject,),
    )
    conn.commit()


def parse_prog2_questions(pdf_path):
    text = extract_pdf_text(pdf_path)
    text = "\n".join(
        line for line in text.splitlines() if line.strip() != PROG2_HEADER
    )
    chunks = re.split(r"(?m)^(?=\d+\.\s+)", text)
    parsed = []
    failures = []

    for chunk in chunks:
        if "Answer:" not in chunk:
            continue

        answer_match = re.search(r"(?m)^Answer:\s*([A-D])\b", chunk)
        if not answer_match:
            failures.append(chunk[:400])
            continue

        answer_letter = answer_match.group(1)
        body = chunk[: answer_match.start()].strip()
        options_match = re.match(
            r"(?ms)^\d+\.\s*(.*?)^A\.\s*(.*?)^B\.\s*(.*?)^C\.\s*(.*?)^D\.\s*(.*)$",
            body,
        )
        if not options_match:
            failures.append(body[:400])
            continue

        question = clean_text(options_match.group(1))
        answers = {
            letter: clean_text(text)
            for letter, text in zip("ABCD", options_match.groups()[1:])
        }

        if question and all(answers.values()):
            parsed.append((question, answers, answer_letter))
        else:
            failures.append(body[:400])

    return parsed, failures


def existing_question_keys(conn):
    cur = conn.cursor()
    keys = set()
    for question_id, question_text in cur.execute(
        "SELECT id, testo FROM questions ORDER BY id"
    ).fetchall():
        rows = cur.execute(
            "SELECT testo FROM answers WHERE domanda_id = ? ORDER BY id",
            (question_id,),
        ).fetchall()
        if len(rows) != 4:
            continue
        answers = {
            letter: clean_text(row[0])
            for letter, row in zip("ABCD", rows)
        }
        keys.add(normalized_key(clean_text(question_text), answers))
    return keys


def append_questions(conn, questions):
    cur = conn.cursor()
    for question, answers, answer_letter in questions:
        cur.execute(
            "INSERT INTO questions(testo, immagine, is_saved) VALUES (?, NULL, 0)",
            (question,),
        )
        question_id = cur.lastrowid
        for letter in "ABCD":
            cur.execute(
                """
                INSERT INTO answers(domanda_id, testo, immagine, corretta)
                VALUES (?, ?, NULL, ?)
                """,
                (question_id, answers[letter], 1 if letter == answer_letter else 0),
            )
    conn.commit()


def import_prog2(pdf_path):
    db_path = DATA_DIR / "programmazione_2.db"
    backup_path = DATA_DIR / "programmazione_2.before_pdf_import.db.bak"
    if db_path.exists() and not backup_path.exists():
        shutil.copy2(db_path, backup_path)

    conn = sqlite3.connect(db_path)
    ensure_quiz_schema(conn)
    set_subject(conn, "Programmazione 2")
    existing = existing_question_keys(conn)
    parsed, failures = parse_prog2_questions(pdf_path)
    fresh = [
        item
        for item in parsed
        if normalized_key(item[0], item[1]) not in existing
    ]
    append_questions(conn, fresh)
    total = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    conn.close()

    return {
        "parsed": len(parsed),
        "added": len(fresh),
        "failures": len(failures),
        "total": total,
        "backup": str(backup_path),
    }


def parse_diritto_sections(pdf_path):
    text = extract_pdf_text(pdf_path)
    matches = list(re.finditer(r"(?m)^(\d+\.\d+)\s+(.+)$", text))
    sections = []

    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        heading = clean_text(match.group(2))
        body = clean_text(text[start:end])
        if len(body) < 80:
            continue
        sections.append((match.group(1), heading, body))

    return sections


def sentence_candidates(body):
    sentences = re.split(r"(?<=[.!?])\s+", body)
    candidates = []
    for sentence in sentences:
        sentence = clean_text(sentence)
        if len(sentence) < 55:
            continue
        if sentence.startswith("Capitolo "):
            continue
        if sentence.count(" ") < 7:
            continue
        if len(sentence) > 260:
            sentence = sentence[:257].rsplit(" ", 1)[0] + "..."
        candidates.append(sentence)
    return candidates


def build_diritto_questions(pdf_path):
    sections = parse_diritto_sections(pdf_path)
    seeds = []
    for number, heading, body in sections:
        candidates = sentence_candidates(body)
        if candidates:
            seeds.append(
                {
                    "number": number,
                    "heading": heading,
                    "answer": candidates[0],
                }
            )

    questions = []
    rng = random.Random(42)

    for index, seed in enumerate(seeds):
        distractor_pool = [
            other["answer"]
            for pos, other in enumerate(seeds)
            if pos != index and other["answer"] != seed["answer"]
        ]
        if len(distractor_pool) < 3:
            continue
        distractors = rng.sample(distractor_pool, 3)
        options = distractors + [seed["answer"]]
        rng.shuffle(options)
        letters = dict(zip("ABCD", options))
        correct = next(letter for letter, value in letters.items() if value == seed["answer"])
        question = f"Nel contesto di {seed['heading']}, quale affermazione e corretta?"
        questions.append((question, letters, correct))

    return questions, len(sections)


def import_diritto(pdf_path):
    db_path = DATA_DIR / "diritto_aziende_digitali.db"
    backup_path = DATA_DIR / "diritto_aziende_digitali.before_pdf_import.db.bak"
    if db_path.exists() and not backup_path.exists():
        shutil.copy2(db_path, backup_path)

    questions, section_count = build_diritto_questions(pdf_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS answers")
    cur.execute("DROP TABLE IF EXISTS questions")
    cur.execute("DROP TABLE IF EXISTS meta")
    ensure_quiz_schema(conn)
    set_subject(conn, "Diritto per le aziende digitali")
    append_questions(conn, questions)
    total = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    conn.close()

    return {
        "sections": section_count,
        "added": len(questions),
        "total": total,
        "backup": str(backup_path) if backup_path.exists() else None,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prog2", type=Path, required=True)
    parser.add_argument("--diritto", type=Path, required=True)
    args = parser.parse_args()

    DATA_DIR.mkdir(exist_ok=True)
    prog2_result = import_prog2(args.prog2)
    diritto_result = import_diritto(args.diritto)

    print("Programmazione 2:", prog2_result)
    print("Diritto per le aziende digitali:", diritto_result)


if __name__ == "__main__":
    main()
