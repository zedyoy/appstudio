import argparse
import re
import sqlite3
from collections import Counter
from pathlib import Path

import pdfplumber


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
SOURCE_DB = DATA_DIR / "study_sources.db"

STOPWORDS = {
    "alla", "allo", "agli", "alle", "che", "con", "dal", "dalla", "dalle",
    "dello", "della", "delle", "degli", "dei", "del", "di", "e", "gli",
    "il", "in", "la", "le", "lo", "ma", "nel", "nella", "nelle", "per",
    "piu", "puo", "quale", "quando", "sono", "sua", "sue", "sui", "sul",
    "sulla", "tra", "un", "una", "uno", "come", "anche", "essere", "viene",
    "vengono", "dopo", "prima", "questo", "questa", "questi", "queste",
    "dunque", "infatti", "quindi", "ai", "al", "ed", "ad", "da", "si",
    "non", "più", "può",
}


def clean_line(line):
    line = re.sub(r"\s+", " ", (line or "").strip())
    if not line:
        return ""
    lower = line.lower()
    if "questo materiale didattico" in lower:
        return ""
    if "ne è severamente vietata" in lower or "ne è severamente vietata" in lower:
        return ""
    if "ai sensi e per gli effetti" in lower:
        return ""
    if re.fullmatch(r"\d+\s+di\s+\d+", lower):
        return ""
    if re.fullmatch(r"\d+", lower):
        return ""
    return line


def normalize_word(word):
    word = word.lower()
    replacements = str.maketrans("àèéìòù", "aeeiou")
    word = word.translate(replacements)
    return re.sub(r"[^a-z0-9_]", "", word)


def keywords_for(text, limit=36):
    words = [normalize_word(w) for w in re.findall(r"\b[\wÀ-ÿ]{4,}\b", text)]
    words = [w for w in words if w and w not in STOPWORDS and not w.isdigit()]
    counts = Counter(words)
    return " ".join(word for word, _ in counts.most_common(limit))


def is_heading(line):
    if len(line) < 4 or len(line) > 140:
        return False
    if re.match(r"^\d+(\.\d+){0,3}\.?\s+[A-ZÀ-ÿ]", line):
        return True
    if re.match(r"^Capitolo\s+\d+", line, re.IGNORECASE):
        return True
    if line.isupper() and len(line.split()) <= 12:
        return True
    return False


def split_long_content(content, max_chars=2600):
    paragraphs = re.split(r"(?<=[.!?])\s+", content)
    chunks = []
    current = []
    current_len = 0

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        if current and current_len + len(paragraph) > max_chars:
            chunks.append(" ".join(current).strip())
            current = []
            current_len = 0
        current.append(paragraph)
        current_len += len(paragraph) + 1

    if current:
        chunks.append(" ".join(current).strip())
    return chunks


def extract_sections(pdf_path, source_title):
    sections = []
    current_title = None
    current_lines = []
    current_start = 1

    with pdfplumber.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf.pages, start=1):
            text = page.extract_text(x_tolerance=1, y_tolerance=3) or ""
            for raw_line in text.splitlines():
                line = clean_line(raw_line)
                if not line:
                    continue

                if is_heading(line):
                    if current_title and current_lines:
                        sections.append(
                            {
                                "topic": current_title,
                                "content": " ".join(current_lines).strip(),
                                "page_start": current_start,
                                "page_end": page_index,
                            }
                        )
                    current_title = line
                    current_lines = []
                    current_start = page_index
                else:
                    if current_title is None:
                        current_title = source_title
                        current_start = page_index
                    current_lines.append(line)

    if current_title and current_lines:
        sections.append(
            {
                "topic": current_title,
                "content": " ".join(current_lines).strip(),
                "page_start": current_start,
                "page_end": current_start,
            }
        )

    cleaned = []
    for section in sections:
        content = re.sub(r"\s+", " ", section["content"]).strip()
        if len(content) < 180:
            continue
        for index, chunk in enumerate(split_long_content(content)):
            if len(chunk) < 180:
                continue
            topic = section["topic"]
            if index:
                topic = f"{topic} ({index + 1})"
            cleaned.append(
                {
                    "topic": topic,
                    "content": chunk,
                    "page_start": section["page_start"],
                    "page_end": section["page_end"],
                }
            )
    return cleaned


def reset_schema(conn):
    conn.execute("DROP TABLE IF EXISTS study_notes")
    conn.execute(
        """
        CREATE TABLE study_notes (
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
        """
        CREATE INDEX IF NOT EXISTS idx_study_notes_subject
        ON study_notes(subject_key)
        """
    )
    conn.commit()


def import_pdf(conn, subject_key, source_title, pdf_path):
    sections = extract_sections(pdf_path, source_title)
    for section in sections:
        blob = f"{section['topic']} {section['content']}"
        conn.execute(
            """
            INSERT INTO study_notes (
                subject_key, source_title, topic, content, keywords,
                page_start, page_end
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                subject_key,
                source_title,
                section["topic"],
                section["content"],
                keywords_for(blob),
                section["page_start"],
                section["page_end"],
            ),
        )
    conn.commit()
    return len(sections)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--diritto", type=Path, required=True)
    parser.add_argument("--prog2", type=Path, required=True)
    args = parser.parse_args()

    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(SOURCE_DB)
    reset_schema(conn)
    diritto_count = import_pdf(
        conn,
        "data/diritto_aziende_digitali.db",
        "Dispensa Diritto Aziende Digitali",
        args.diritto,
    )
    prog2_count = import_pdf(
        conn,
        "data/programmazione_2.db",
        "Dispensa Programmazione 2",
        args.prog2,
    )
    conn.close()

    print(f"Diritto: {diritto_count} note importate")
    print(f"Programmazione 2: {prog2_count} note importate")
    print(f"Database: {SOURCE_DB}")


if __name__ == "__main__":
    main()
