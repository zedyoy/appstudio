let correctCount = 0;
let incorrectCount = 0;
let currentQuestionIndex = 1;
let savedQuestions = [];
let isSavedQuiz = false;

function updateSavedCount() {
    document.getElementById('savedCount').innerText = `Salvate: ${savedQuestions.length}`;
}

function shuffleArray(array) {
    return array.sort(() => Math.random() - 0.5);
}

async function getQuestion() {
    const response = await fetch(`/api/question/${currentQuestionIndex}`);
    const question = await response.json();

    // Visualizza la domanda
    document.getElementById('domanda-id').innerText = `ID Domanda: ${question.id}`;
    const domandaText = document.getElementById('domanda');
    domandaText.innerText = '';  // Resetta il testo della domanda

    if (question.testo) {
        // Poi aggiungi il testo della domanda
        const testo = document.createElement('p');
        testo.textContent = question.testo;
        domandaText.appendChild(testo);
    }

    if (question.immagine) {
        // Se c'è un'immagine nella domanda, la mostra prima del testo
        const img = document.createElement('img');
        img.src = `data:image/jpeg;base64,${question.immagine}`;
        img.alt = 'Immagine della domanda';
        img.style.width = '100%';  // Imposta una larghezza per l'immagine
        domandaText.appendChild(img);  // Aggiungi l'immagine al DOM
    }
    
    

    // Visualizza le risposte
    const answersList = document.getElementById('risposte');
    answersList.innerHTML = '';

    const shuffledAnswers = shuffleArray(question.risposte);
    shuffledAnswers.forEach(risposta => {
        const li = document.createElement('li');

        // Crea un contenitore per la risposta che potrebbe contenere sia testo che immagine
        const rispostaContainer = document.createElement('div');

        if (risposta.immagine) {
            // Se c'è un'immagine per la risposta, aggiungila prima del testo
            const img = document.createElement('img');
            img.src = `data:image/jpeg;base64,${risposta.immagine}`;
            img.alt = 'Immagine risposta';
            img.style.width = '350px';  // Imposta una larghezza per l'immagine (ad esempio 50px)
            rispostaContainer.appendChild(img);
        }

        if (risposta.testo) {
            // Aggiungi il testo della risposta
            const testo = document.createElement('span');
            testo.textContent = risposta.testo;
            rispostaContainer.appendChild(testo);
        }

        // Aggiungi il contenitore della risposta (che include immagine e testo)
        li.appendChild(rispostaContainer);

        // Gestisci il click sulla risposta
        li.onclick = () => checkAnswer(li, risposta.id, question.corretta);
        answersList.appendChild(li);
    });

    document.getElementById('result').innerText = '';
    document.getElementById('nextBtn').style.display = 'inline';
}



function checkAnswer(selectedLi, selectedId, correctId) {
    const result = document.getElementById('result');

    document.querySelectorAll('.answer-list li').forEach(li => {
        li.classList.remove('selected', 'correct', 'wrong');
    });

    if (selectedId === correctId) {
        selectedLi.classList.add('selected', 'correct');
        result.innerText = "Risposta corretta!";
        correctCount++;
    } else {
        selectedLi.classList.add('selected', 'wrong');
        result.innerText = "Risposta errata. Riprova!";
        incorrectCount++;
    }

    document.getElementById('correctCount').innerText = `Corrette: ${correctCount}`;
    document.getElementById('incorrectCount').innerText = `Sbagliate: ${incorrectCount}`;
    document.getElementById('nextBtn').style.display = 'inline';
}

async function saveQuestion() {
    await fetch(`/api/save_question/${currentQuestionIndex}`, { method: 'POST' });
    alert("Domanda salvata per dopo!");

    const response = await fetch('/api/saved_questions');
    savedQuestions = await response.json();
    updateSavedCount();
}

function startQuiz() {
    const startingQuestion = document.getElementById('startingQuestion').value;
    currentQuestionIndex = parseInt(startingQuestion);
    getQuestion();
    document.getElementById('nextBtn').style.display = 'inline';
}

async function startSavedQuiz() {
    const response = await fetch('/api/saved_questions');
    savedQuestions = await response.json();
    if (savedQuestions.length === 0) {
        alert("Nessuna domanda salvata!");
        return;
    }

    isSavedQuiz = true;
    currentQuestionIndex = 0;
    updateSavedCount();
    loadSavedQuestion();
}

function loadSavedQuestion() {
    const question = savedQuestions[currentQuestionIndex];
    document.getElementById('domanda-id').innerText = `ID Domanda: ${question.id}`;
    document.getElementById('domanda').innerText = question.testo;

    const answersList = document.getElementById('risposte');
    answersList.innerHTML = '';

    const shuffledAnswers = shuffleArray(question.risposte);
    shuffledAnswers.forEach(risposta => {
        const li = document.createElement('li');
        li.textContent = risposta.testo;
        li.onclick = () => checkAnswer(li, risposta.id, question.corretta);
        answersList.appendChild(li);
    });

    document.getElementById('result').innerText = '';
    document.getElementById('nextBtn').style.display = 'inline';
}

function nextQuestion() {
    currentQuestionIndex++;
    if (isSavedQuiz) {
        if (currentQuestionIndex < savedQuestions.length) {
            loadSavedQuestion();
        } else {
            alert("Hai completato il quiz delle domande salvate!");
            isSavedQuiz = false;
        }
    } else {
        getQuestion();
    }
    document.getElementById('nextBtn').style.display = 'inline';
}

function prevQuestion() {
    currentQuestionIndex--;
            getQuestion();
    
    document.getElementById('nextBtn').style.display = 'inline';
}

async function clearSavedQuestions() {
    await fetch('/api/clear_saved_questions', { method: 'DELETE' });
    savedQuestions = [];
    updateSavedCount();
    alert("Tutte le domande salvate sono state cancellate.");
}

// Funzione per rimuovere una domanda salvata
async function removeSavedQuestion() {
    // Verifica se stai visualizzando una domanda salvata
    if (isSavedQuiz && savedQuestions.length > 0) {
        const questionId = savedQuestions[currentQuestionIndex].id; // Ottieni l'ID della domanda salvata
        await fetch(`/api/remove_saved_question/${questionId}`, { method: 'DELETE' });
        alert("Domanda rimossa dalle domande salvate.");

        // Ricarica l'elenco delle domande salvate
        const response = await fetch('/api/saved_questions');
        savedQuestions = await response.json();
        updateSavedCount();

        // Se la domanda è stata rimossa e non ci sono più domande salvate, mostra un messaggio
        if (savedQuestions.length === 0) {
            alert("Non ci sono più domande salvate.");
            isSavedQuiz = false; // Torna alla modalità quiz normale
            currentQuestionIndex = 1; // Resetta l'indice per la prossima volta
            document.getElementById('nextBtn').style.display = 'none'; // Nascondi il pulsante "Prossima Domanda"
        } else {
            loadSavedQuestion(); // Carica la prossima domanda salvata
        }
    } else {
        alert("Nessuna domanda salvata da rimuovere.");
    }
}


document.getElementById('startButton').onclick = startQuiz;
