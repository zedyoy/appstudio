from flask import Flask, jsonify, render_template, request, session
import base64
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")  # necessario per sessione

AVAILABLE_DBS = {
    "Architettura dei Calcolatori": "architettura_calcolatori.db",
    "Programmazione 2": "programmazione_2.db",
}

def get_db_path():
    db_key = session.get("db_key", "quiz")  # default
    if db_key not in AVAILABLE_DBS:
        db_key = "quiz"
        session["db_key"] = db_key
    return os.path.join(app.root_path, AVAILABLE_DBS[db_key])


def get_connection():
    conn = sqlite3.connect(get_db_path())
    return conn



def build_question_payload(cursor, question_id, include_images=True):
    """
    Restituisce un dizionario con:
    - id
    - testo
    - immagine (base64 o None)
    - risposte: lista di {id, testo, immagine}
    - corretta: id della risposta corretta
    """
    cursor.execute(
        "SELECT id, testo, immagine FROM questions WHERE id = ?",
        (question_id,),
    )
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
        answers.append(
            {
                "id": ans_id,
                "testo": ans_text,
                "immagine": ans_img_b64,
            }
        )
        if corretta:
            correct_id = ans_id

    return {
        "id": q_id,
        "testo": testo,
        "immagine": image_b64,
        "risposte": answers,
        "corretta": correct_id,
    }


@app.route("/api/databases", methods=["GET"])
def list_databases():
    # restituisco anche quale è attivo
    active = session.get("db_key", "quiz")
    return jsonify({
        "active": active,
        "options": [{"key": k, "label": AVAILABLE_DBS[k]} for k in AVAILABLE_DBS]
    })

@app.route("/api/set_database", methods=["POST"])
def set_database():
    data = request.get_json(silent=True) or {}
    db_key = data.get("db_key")

    if db_key not in AVAILABLE_DBS:
        return jsonify({"error": "Database non valido"}), 400

    session["db_key"] = db_key
    return jsonify({"message": "Database impostato", "active": db_key})


# --------- API DOMANDA SINGOLA (allenamento) ---------


@app.route("/api/question/<int:id>", methods=["GET"])
def get_question_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()

    payload = build_question_payload(cursor, id, include_images=True)
    conn.close()

    if payload is None:
        return jsonify({"error": "Domanda non trovata"}), 404

    return jsonify(payload)


# --------- API SALVATAGGIO DOMANDE ---------


@app.route("/api/save_question/<int:id>", methods=["POST"])
def save_question(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE questions SET is_saved = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Domanda salvata", "id": id})


@app.route("/api/saved_questions", methods=["GET"])
def get_saved_questions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM questions WHERE is_saved = 1 ORDER BY id"
    )
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
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE questions SET is_saved = 0 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Domanda salvata rimossa", "id": id})


@app.route("/api/clear_saved_questions", methods=["DELETE"])
def clear_saved_questions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE questions SET is_saved = 0")
    conn.commit()
    conn.close()

    return jsonify({"message": "Tutte le domande salvate sono state rimosse"})


# --------- NUOVA API: DOMANDE CASUALI (SIMULAZIONE) ---------


@app.route("/api/random_questions", methods=["GET"])
def random_questions():
    """
    Restituisce un elenco di domande casuali
    con la stessa struttura di /api/question/<id>.
    Parametro opzionale: ?limit=30
    """
    limit = request.args.get("limit", default=30, type=int)
    if limit <= 0:
        limit = 30

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM questions ORDER BY RANDOM() LIMIT ?",
        (limit,),
    )
    rows = cursor.fetchall()

    questions = []
    for (q_id,) in rows:
        payload = build_question_payload(cursor, q_id, include_images=True)
        if payload:
            questions.append(payload)

    conn.close()
    return jsonify(questions)


# --------- PAGINA HTML ---------


@app.route("/")
def index():
    return render_template("quiz.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
