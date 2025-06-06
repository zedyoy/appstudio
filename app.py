from flask import Flask, jsonify, render_template, request
import base64
import sqlite3

app = Flask(__name__)

# Funzione per ottenere una domanda casuale
@app.route('/api/question/<int:id>', methods=['GET'])
def get_question_by_id(id):
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    
    # Recupera i dati della domanda
    cursor.execute("SELECT * FROM questions WHERE id = ?", (id,))
    question = cursor.fetchone()
    
    if question:
        # Recupera le risposte associate alla domanda
        cursor.execute("SELECT id, testo, corretta, immagine FROM answers WHERE domanda_id = ?", (question[0],))
        answers = cursor.fetchall()

        # Recupera l'immagine associata alla domanda (se esiste)
        cursor.execute("SELECT immagine FROM questions WHERE id = ?", (id,))
        image_data = cursor.fetchone()
        
        # Codifica l'immagine della domanda in base64, se presente
        image_base64 = None
        if image_data and image_data[0]:
            image_base64 = base64.b64encode(image_data[0]).decode('utf-8')
        
        # Codifica le immagini delle risposte in base64
        formatted_answers = []
        for a in answers:
            answer_image_base64 = None
            if a[3]:  # Se esiste un'immagine associata alla risposta
                answer_image_base64 = base64.b64encode(a[3]).decode('utf-8')
            formatted_answers.append({
                "id": a[0],
                "testo": a[1],
                "immagine": answer_image_base64  # Aggiungi l'immagine della risposta
            })

        conn.close()
        
        # Ritorna la domanda e le risposte (con immagini)
        return jsonify({
            "id": question[0],
            "testo": question[1],
            "risposte": formatted_answers,
            "corretta": [a[0] for a in answers if a[2] == 1][0],
            "immagine": image_base64  # Aggiungi l'immagine della domanda
        })
    else:
        conn.close()
        return jsonify({"error": "Domanda non trovata"}), 404

# Endpoint API per salvare una domanda
@app.route('/api/save_question/<int:id>', methods=['POST'])
def save_question(id):
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    
    cursor.execute("UPDATE questions SET is_saved = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Domanda salvata"})

# Endpoint API per ottenere tutte le domande salvate
@app.route('/api/saved_questions', methods=['GET'])
def get_saved_questions():
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM questions WHERE is_saved = 1")
    questions = cursor.fetchall()
    
    saved_questions = []
    for question in questions:
        cursor.execute("SELECT id, testo, corretta FROM answers WHERE domanda_id = ?", (question[0],))
        answers = cursor.fetchall()
        saved_questions.append({
            "id": question[0],
            "testo": question[1],
            "risposte": [{"id": a[0], "testo": a[1]} for a in answers],
            "corretta": [a[0] for a in answers if a[2] == 1][0]
        })
    
    conn.close()
    return jsonify(saved_questions)

# Endpoint API per eliminare una domanda salvata
@app.route('/api/remove_saved_question/<int:id>', methods=['DELETE'])
def remove_saved_question(id):
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    
    cursor.execute("UPDATE questions SET is_saved = 0 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Domanda rimossa"})

# Endpoint API per eliminare tutte le domande salvate
@app.route('/api/clear_saved_questions', methods=['DELETE'])
def clear_saved_questions():
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    
    cursor.execute("UPDATE questions SET is_saved = 0")
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Tutte le domande salvate sono state rimosse"})

# Endpoint per la pagina del quiz
@app.route('/')
def index():
    return render_template('quiz.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
