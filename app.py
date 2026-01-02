from flask import Flask, jsonify, render_template, request, session
import base64
import sqlite3
import os

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

IGNORE_DBS = {"dashboard.db"}


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
    return jsonify(questions)


@app.route("/")
def index():
    return render_template("quiz.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
