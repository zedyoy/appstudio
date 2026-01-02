// --- STATI GLOBALI ---
let correctCount = 0;
let incorrectCount = 0;
let answeredCount = 0;

let currentQuestionIndex = 1;   // allenamento
let savedQuestions = [];
let isSavedQuiz = false;

let hasAnsweredCurrent = false; // evita doppi conteggi in allenamento

async function loadDbOptions() {
    const sel = document.getElementById("dbSelect");
    if (!sel) return;

    const res = await fetch("/api/databases");
    const data = await res.json();

    sel.innerHTML = "";

    // placeholder
    const ph = document.createElement("option");
    ph.value = "";
    ph.textContent = "Seleziona una materia";
    ph.disabled = true;
    ph.selected = true;
    sel.appendChild(ph);

    (data.options || []).forEach((opt) => {
        const o = document.createElement("option");
        o.value = opt.key;       // db_key (relpath)
        o.textContent = opt.label; // nome materia
        sel.appendChild(o);
    });

    // se c'è una materia già attiva, selezionala
    if (data.active) {
        sel.value = data.active;
    }
}

async function setDatabase(dbKey) {
    const res = await fetch("/api/set_database", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ db_key: dbKey })
    });

    const data = await res.json();
    if (!res.ok) {
        alert(data.error || "Errore nel cambio database");
        return false;
    }

    // reset UI locale (per evitare incongruenze con domande salvate del db precedente)
    resetSession();
    savedQuestions = [];
    updateSavedCount();

    // torna a stato iniziale
    mode = "training";
    setMode("training");

    // nascondo nav
    const nextBtn = document.getElementById("nextBtn");
    const prevBtn = document.getElementById("prevBtn");
    if (nextBtn) nextBtn.style.display = "none";
    if (prevBtn) prevBtn.style.display = "none";

    // pulizia card
    const domandaIdEl = document.getElementById("domanda-id");
    const domandaText = document.getElementById("domanda");
    const answersList = document.getElementById("risposte");
    const resultEl = document.getElementById("result");
    if (domandaIdEl) domandaIdEl.innerText = "ID Domanda: -";
    if (domandaText) domandaText.innerText = "Seleziona modalità e premi Inizia.";
    if (answersList) answersList.innerHTML = "";
    if (resultEl) resultEl.innerText = "";

    return true;
}


// modalità: 'training' | 'exam'
let mode = "training";
let isExamMode = false;

// dati simulazione
let examQuestions = [];
let examIndex = 0;
let examAnswers = [];
let examFinished = false;

// timer simulazione
let examTimerId = null;
let examTimeRemaining = 0; // secondi
let examStartTimestamp = null;

// --------- UTILITA' BASE ---------

function updateSavedCount() {
    const savedCountEl = document.getElementById("savedCount");
    if (savedCountEl) {
        savedCountEl.innerText = `Salvate: ${savedQuestions.length}`;
    }
}

function updateSessionStats() {
    const answeredEl = document.getElementById("answeredCount");
    const accEl = document.getElementById("accuracy");
    const perfEl = document.getElementById("performanceLabel");
    const perfContainer = document.querySelector(".session-item.session-performance");

    if (answeredEl) answeredEl.innerText = answeredCount;

    const total = correctCount + incorrectCount;

    // % di accuratezza (già ti torna utile, la manteniamo)
    let accuracy = 0;
    if (total > 0) {
        accuracy = Math.round((correctCount / total) * 100);
    }
    if (accuracy < 0) accuracy = 0;
    if (accuracy > 100) accuracy = 100;
    if (accEl) accEl.innerText = `${accuracy}%`;

    // voto in 30esimi, arrotondato per difetto
    let score30 = 0;
    if (total > 0) {
        score30 = Math.floor((correctCount / total) * 30);
    }

    // Testo della valutazione (es: 20/30)
    if (perfEl) {
        perfEl.innerText = total === 0 ? "-/30" : `${score30}/30`;
    }

    // Colori in base al voto
    if (perfContainer) {
        perfContainer.classList.remove("perf-bad", "perf-medium", "perf-good");
        if (total > 0) {
            if (score30 < 18) {
                perfContainer.classList.add("perf-bad");      // rosso
            } else if (score30 <= 24) {
                perfContainer.classList.add("perf-medium");   // giallo
            } else {
                perfContainer.classList.add("perf-good");     // verde
            }
        }
    }
}



function resetSession() {
    correctCount = 0;
    incorrectCount = 0;
    answeredCount = 0;
    hasAnsweredCurrent = false;

    const correctCountEl = document.getElementById("correctCount");
    const incorrectCountEl = document.getElementById("incorrectCount");
    if (correctCountEl) correctCountEl.innerText = "0";
    if (incorrectCountEl) incorrectCountEl.innerText = "0";

    updateSessionStats();

    const resultEl = document.getElementById("result");
    if (resultEl) resultEl.innerText = "";
}

function shuffleArray(array) {
    return array.sort(() => Math.random() - 0.5);
}

function showNavButtons() {
    const nextBtn = document.getElementById("nextBtn");
    const prevBtn = document.getElementById("prevBtn");
    if (nextBtn) nextBtn.style.display = "inline-flex";
    if (prevBtn) prevBtn.style.display = "inline-flex";
}

function hideExamSummary() {
    const summary = document.getElementById("examSummary");
    if (summary) {
        summary.style.display = "none";
        summary.innerHTML = "";
    }
}

// progress bar per simulazione
function updateProgress() {
    const wrapper = document.getElementById("progressBarWrapper");
    const label = document.getElementById("progressLabel");
    const fill = document.getElementById("progressFill");

    if (!wrapper || !label || !fill) return;

    if (!isExamMode || !examQuestions.length) {
        wrapper.style.display = "none";
        return;
    }

    const current = examIndex + 1;
    const total = examQuestions.length;
    wrapper.style.display = "block";
    label.innerText = `Domanda ${current}/${total}`;
    const perc = Math.round((current / total) * 100);
    fill.style.width = `${perc}%`;
}

// sidebar simulazione
function renderExamSidebar() {
    const sidebar = document.getElementById("examSidebar");
    const list = document.getElementById("examQuestionList");
    if (!sidebar || !list) return;

    if (!isExamMode || !examQuestions.length) {
        sidebar.style.display = "none";
        list.innerHTML = "";
        return;
    }

    sidebar.style.display = "block";
    list.innerHTML = "";

    examQuestions.forEach((_, idx) => {
        const btn = document.createElement("div");
        btn.className = "sidebar-item";
        btn.innerText = (idx + 1).toString();

        if (idx === examIndex) {
            btn.classList.add("current");
        }

        if (examAnswers[idx] != null) {
            btn.classList.add("answered");
        }

        btn.onclick = () => {
            examIndex = idx;
            renderExamQuestion();
        };

        list.appendChild(btn);
    });
}

// timer
function stopExamTimer() {
    if (examTimerId) {
        clearInterval(examTimerId);
        examTimerId = null;
    }
    const timerDisplay = document.getElementById("timerDisplay");
    if (timerDisplay) timerDisplay.style.display = "none";
}

function startExamTimer(seconds) {
    stopExamTimer();
    examTimeRemaining = seconds;

    const timerDisplay = document.getElementById("timerDisplay");
    if (!timerDisplay) return;
    timerDisplay.style.display = "inline";

    function update() {
        const m = Math.floor(examTimeRemaining / 60);
        const s = examTimeRemaining % 60;
        const mm = m.toString().padStart(2, "0");
        const ss = s.toString().padStart(2, "0");
        timerDisplay.innerText = `${mm}:${ss}`;

        if (examTimeRemaining <= 0) {
            stopExamTimer();
            if (!examFinished && isExamMode) {
                finishExam();
            }
        } else {
            examTimeRemaining--;
        }
    }

    update();
    examTimerId = setInterval(update, 1000);
}

// animazione card
function applyCardAnimation() {
    const card = document.querySelector(".question-card");
    if (!card) return;
    card.classList.remove("fade-in");
    void card.offsetWidth; // force reflow
    card.classList.add("fade-in");
}

// --------- RENDER DOMANDA GENERICA ---------

function renderQuestionPayload(question, forExam) {
    const domandaIdEl = document.getElementById("domanda-id");
    const domandaText = document.getElementById("domanda");
    const answersList = document.getElementById("risposte");
    const resultEl = document.getElementById("result");

    if (domandaIdEl) domandaIdEl.innerText = `ID Domanda: ${question.id}`;

    if (domandaText) {
        domandaText.innerHTML = "";
        if (question.immagine) {
            const img = document.createElement("img");
            img.src = `data:image/jpeg;base64,${question.immagine}`;
            img.alt = "Immagine della domanda";
            domandaText.appendChild(img);
        }
        if (question.testo) {
            const p = document.createElement("p");
            p.textContent = question.testo;
            domandaText.appendChild(p);
        }
    }

    if (answersList) answersList.innerHTML = "";
    if (resultEl) resultEl.innerText = "";

    if (!answersList) return;

    const shuffledAnswers = shuffleArray(question.risposte.slice());

    shuffledAnswers.forEach((risposta) => {
        const li = document.createElement("li");
        const container = document.createElement("div");

        if (risposta.immagine) {
            const img = document.createElement("img");
            img.src = `data:image/jpeg;base64,${risposta.immagine}`;
            img.alt = "Immagine risposta";
            container.appendChild(img);
        }

        if (risposta.testo) {
            const span = document.createElement("span");
            span.textContent = risposta.testo;
            container.appendChild(span);
        }

        li.appendChild(container);
        li.dataset.answerId = risposta.id;

        if (forExam) {
            li.onclick = () => selectExamAnswer(li, risposta.id);
        } else {
            li.onclick = () =>
                checkAnswerTraining(li, risposta.id, question.corretta);
        }

        answersList.appendChild(li);
    });

    applyCardAnimation();
}

// --------- MODALITÀ ALLENAMENTO ---------

async function getTrainingQuestion() {
    const response = await fetch(`/api/question/${currentQuestionIndex}`);
    const question = await response.json();

    hasAnsweredCurrent = false;
    hideExamSummary();
    renderExamSidebar();
    updateProgress();
    stopExamTimer();

    if (question.error) {
        const domandaIdEl = document.getElementById("domanda-id");
        const domandaText = document.getElementById("domanda");
        const answersList = document.getElementById("risposte");
        const resultEl = document.getElementById("result");

        if (domandaIdEl) domandaIdEl.innerText = "ID Domanda: -";
        if (domandaText) domandaText.innerText = "Domanda non trovata.";
        if (answersList) answersList.innerHTML = "";
        if (resultEl) resultEl.innerText = "";
        return;
    }

    renderQuestionPayload(question, false);
    showNavButtons();
}

function checkAnswerTraining(selectedLi, selectedId, correctId) {
    const result = document.getElementById("result");

    if (hasAnsweredCurrent) {
        return;
    }
    hasAnsweredCurrent = true;

    const allLis = document.querySelectorAll(".answer-list li");
    allLis.forEach((li) => {
        li.classList.remove("selected", "correct", "wrong");
    });

    answeredCount++;
    if (selectedId === correctId) {
        selectedLi.classList.add("selected", "correct");
        if (result) result.innerText = "Risposta corretta.";
        correctCount++;
    } else {
        selectedLi.classList.add("selected", "wrong");
        if (result) result.innerText = "Risposta errata.";
        incorrectCount++;
    }

    const correctLi = Array.from(allLis).find(
        (li) => Number(li.dataset.answerId) === Number(correctId)
    );
    if (correctLi) {
        correctLi.classList.add("correct");
    }

    const correctCountEl = document.getElementById("correctCount");
    const incorrectCountEl = document.getElementById("incorrectCount");
    if (correctCountEl) correctCountEl.innerText = correctCount;
    if (incorrectCountEl) incorrectCountEl.innerText = incorrectCount;

    updateSessionStats();
    showNavButtons();
}

function startTrainingMode() {
    mode = "training";
    isExamMode = false;
    isSavedQuiz = false;

    hideExamSummary();
    stopExamTimer();

    const startingQuestion =
        document.getElementById("startingQuestion").value || "1";
    currentQuestionIndex = parseInt(startingQuestion, 10);

    getTrainingQuestion();
    showNavButtons();
}

// --------- MODALITÀ SIMULAZIONE ---------

async function startExamMode() {
    mode = "exam";
    isExamMode = true;
    isSavedQuiz = false;
    examFinished = false;

    hideExamSummary();
    resetSession();

    examStartTimestamp = Date.now();

    let limit = 30;
    const examInput = document.getElementById("examQuestionCount");
    if (examInput) {
        const parsed = parseInt(examInput.value, 10);
        if (!isNaN(parsed) && parsed > 0) {
            limit = parsed;
        }
    }

    const response = await fetch(`/api/random_questions?limit=${limit}`);
    examQuestions = await response.json();

    if (!Array.isArray(examQuestions) || examQuestions.length === 0) {
        alert("Non è stato possibile caricare le domande casuali.");
        isExamMode = false;
        return;
    }

    examIndex = 0;
    examAnswers = new Array(examQuestions.length).fill(null);

    // timer opzionale
    const timerEnabled = document.getElementById("examTimerEnabled").checked;
    if (timerEnabled) {
        let minutes = parseInt(
            document.getElementById("examTimerMinutes").value,
            10
        );
        if (isNaN(minutes) || minutes <= 0) minutes = 30;
        startExamTimer(minutes * 60);
    } else {
        stopExamTimer();
    }

    renderExamQuestion();
    showNavButtons();
}

function renderExamQuestion() {
    const question = examQuestions[examIndex];
    if (!question) return;

    renderQuestionPayload(question, true);
    renderExamSidebar();
    updateProgress();

    const resultEl = document.getElementById("result");
    if (resultEl) resultEl.innerText = "";
}

function selectExamAnswer(selectedLi, answerId) {
    const allLis = document.querySelectorAll(".answer-list li");
    allLis.forEach((li) => {
        li.classList.remove("selected", "correct", "wrong");
    });

    selectedLi.classList.add("selected");
    examAnswers[examIndex] = answerId;
    renderExamSidebar();
}

function finishExam() {
    isExamMode = false;
    examFinished = true;
    stopExamTimer();

    let localCorrect = 0;
    let localWrong = 0;

    const summary = document.getElementById("examSummary");
    if (!summary) return;

    summary.innerHTML = "";
    const title = document.createElement("h2");
    title.textContent = `Riepilogo simulazione (${examQuestions.length} domande)`;
    summary.appendChild(title);

    // Calcolo corrette/errate
    examQuestions.forEach((q, idx) => {
        const chosenId = examAnswers[idx];
        const correctId = q.corretta;

        const answersMap = {};
        q.risposte.forEach((r) => {
            answersMap[r.id] = r.testo;
        });

        const chosenText =
            chosenId != null ? answersMap[chosenId] || "(non risposto)" : "(non risposto)";
        const correctText = answersMap[correctId] || "";

        const isCorrect = chosenId === correctId;

        if (isCorrect) {
            localCorrect++;
        } else {
            localWrong++;
        }

        const item = document.createElement("div");
        item.className = "summary-item " + (isCorrect ? "correct" : "wrong");

        const qText = document.createElement("div");
        qText.textContent = `${idx + 1}. ${q.testo}`;
        item.appendChild(qText);

        const chosenP = document.createElement("div");
        chosenP.textContent = `Tua risposta: ${chosenText}`;
        item.appendChild(chosenP);

        const correctP = document.createElement("div");
        correctP.textContent = `Risposta corretta: ${correctText}`;
        item.appendChild(correctP);

        summary.appendChild(item);
    });

    // --- RIEPILOGO GLOBALE IN 30ESIMI + TEMPO ---

    const total = localCorrect + localWrong;
    let score30 = 0;
    if (total > 0) {
        score30 = Math.floor((localCorrect / total) * 30);
    }

    // tempo impiegato
    let elapsedSec = 0;
    if (examStartTimestamp) {
        elapsedSec = Math.round((Date.now() - examStartTimestamp) / 1000);
    }
    const mm = String(Math.floor(elapsedSec / 60)).padStart(2, "0");
    const ss = String(elapsedSec % 60).padStart(2, "0");

    const overview = document.createElement("div");
    overview.className = "exam-overview";

    if (total > 0) {
        if (score30 < 18) {
            overview.classList.add("perf-bad");
        } else if (score30 <= 24) {
            overview.classList.add("perf-medium");
        } else {
            overview.classList.add("perf-good");
        }
    }

    overview.innerHTML = `
        <div class="exam-overview-main">
            Punteggio: <strong>${total === 0 ? "-/30" : `${score30}/30`}</strong>
        </div>
        <div class="exam-overview-sub">
            Corrette: <strong>${localCorrect}</strong> ·
            Errate: <strong>${localWrong}</strong> ·
            Tempo: <strong>${mm}:${ss}</strong>
        </div>
    `;

    // metto il riepilogo globale subito dopo il titolo
    summary.insertBefore(overview, title.nextSibling);

    summary.style.display = "block";

    // Aggiorno i contatori globali e la valutazione in alto
    correctCount = localCorrect;
    incorrectCount = localWrong;
    answeredCount = localCorrect + localWrong;

    const correctCountEl = document.getElementById("correctCount");
    const incorrectCountEl = document.getElementById("incorrectCount");
    if (correctCountEl) correctCountEl.innerText = correctCount;
    if (incorrectCountEl) incorrectCountEl.innerText = incorrectCount;

    updateSessionStats();
    summary.scrollIntoView({ behavior: "smooth" });

    // aggiorna sidebar (verde/rosso)
    const list = document.getElementById("examQuestionList");
    if (list) {
        const items = list.querySelectorAll(".sidebar-item");
        items.forEach((el, idx) => {
            const chosenId = examAnswers[idx];
            const correctId = examQuestions[idx].corretta;
            if (chosenId === correctId) {
                el.classList.add("answered");
            } else {
                el.classList.add("wrong");
            }
        });
    }
}


// --------- NAVIGAZIONE ---------

function nextQuestion() {
    if (mode === "exam" && isExamMode) {
        if (examIndex < examQuestions.length - 1) {
            examIndex++;
            renderExamQuestion();
        } else if (!examFinished) {
            finishExam();
        }
        return;
    }

    // allenamento / salvate
    if (isSavedQuiz) {
        if (currentQuestionIndex < savedQuestions.length - 1) {
            currentQuestionIndex++;
            loadSavedQuestion();
        } else {
            alert("Hai completato il quiz delle domande salvate.");
            isSavedQuiz = false;
        }
    } else {
        currentQuestionIndex++;
        getTrainingQuestion();
    }
    showNavButtons();
}

function prevQuestion() {
    if (mode === "exam" && isExamMode) {
        if (examIndex > 0) {
            examIndex--;
            renderExamQuestion();
        }
        return;
    }

    if (isSavedQuiz) {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            loadSavedQuestion();
        }
    } else {
        if (currentQuestionIndex > 1) {
            currentQuestionIndex--;
            getTrainingQuestion();
        }
    }
    showNavButtons();
}

// --------- DOMANDE SALVATE ---------

async function saveQuestion() {
    if (mode === "exam" && isExamMode) {
        alert("Salvataggio non disponibile in modalità simulazione.");
        return;
    }

    await fetch(`/api/save_question/${currentQuestionIndex}`, { method: "POST" });

    const response = await fetch("/api/saved_questions");
    savedQuestions = await response.json();
    updateSavedCount();

    alert("Domanda salvata.");
}

async function startSavedQuiz() {
    if (mode === "exam" && isExamMode) {
        alert("Non puoi usare le domande salvate durante la simulazione.");
        return;
    }

    const response = await fetch("/api/saved_questions");
    savedQuestions = await response.json();
    updateSavedCount();

    if (!savedQuestions || savedQuestions.length === 0) {
        alert("Nessuna domanda salvata.");
        return;
    }

    isSavedQuiz = true;
    currentQuestionIndex = 0;
    hideExamSummary();
    renderExamSidebar();
    updateProgress();
    loadSavedQuestion();
    showNavButtons();
}

function loadSavedQuestion() {
    const question = savedQuestions[currentQuestionIndex];
    if (!question) return;

    hasAnsweredCurrent = false;
    renderQuestionPayload(question, false);

    const resultEl = document.getElementById("result");
    if (resultEl) resultEl.innerText = "";
}

async function clearSavedQuestions() {
    await fetch("/api/clear_saved_questions", { method: "DELETE" });
    savedQuestions = [];
    updateSavedCount();
    alert("Tutte le domande salvate sono state cancellate.");
}

async function removeSavedQuestion() {
    if (isSavedQuiz && savedQuestions.length > 0) {
        const questionId = savedQuestions[currentQuestionIndex].id;
        await fetch(`/api/remove_saved_question/${questionId}`, {
            method: "DELETE",
        });

        const response = await fetch("/api/saved_questions");
        savedQuestions = await response.json();
        updateSavedCount();

        if (savedQuestions.length === 0) {
            alert("Non ci sono più domande salvate.");
            isSavedQuiz = false;
            currentQuestionIndex = 1;
        } else {
            if (currentQuestionIndex >= savedQuestions.length) {
                currentQuestionIndex = savedQuestions.length - 1;
            }
            loadSavedQuestion();
        }
    } else {
        alert("Nessuna domanda salvata da rimuovere.");
    }
}

// --------- AVVIO E UI ---------

function startQuiz() {
    const dbSelect = document.getElementById("dbSelect");
    if (dbSelect && !dbSelect.value) {
        alert("Seleziona una materia prima di iniziare.");
        return;
    }

    if (mode === "exam") {
        startExamMode();
    } else {
        startTrainingMode();
    }
}

function setMode(newMode) {
    mode = newMode;

    // attiva tab corretta
    document.querySelectorAll(".mode-tab").forEach((btn) => {
        btn.classList.toggle("active", btn.dataset.mode === newMode);
    });

    // mostra/nasconde blocchi impostazioni
    document.getElementById("trainingSettings").style.display =
        newMode === "training" ? "block" : "none";
    document.getElementById("examSettings").style.display =
        newMode === "exam" ? "block" : "none";

    // se esco da exam, stop sidebar, progress e timer
    if (newMode !== "exam") {
        isExamMode = false;
        examQuestions = [];
        examAnswers = [];
        renderExamSidebar();
        updateProgress();
        stopExamTimer();
    }

    hideExamSummary();
}

function toggleTheme() {
    const body = document.body;
    const btn = document.getElementById("themeToggle");
    body.classList.toggle("light-theme");
    if (btn) {
        btn.innerText = body.classList.contains("light-theme")
            ? "Tema chiaro"
            : "Tema scuro";
    }
}

/* INIT */
window.addEventListener("DOMContentLoaded", async () => {
    
    // ---- DATABASE SELECT ----
    await loadDbOptions();

    const dbSelect = document.getElementById("dbSelect");
    if (dbSelect) {
        dbSelect.addEventListener("change", async () => {
            if (!dbSelect.value) return;
            await setDatabase(dbSelect.value);
        });
    }
    
    const startBtn = document.getElementById("startButton");
    if (startBtn) startBtn.onclick = startQuiz;

    const resetBtn = document.getElementById("resetSessionBtn");
    if (resetBtn) resetBtn.onclick = resetSession;

    const themeBtn = document.getElementById("themeToggle");
    if (themeBtn) themeBtn.onclick = toggleTheme;

    // tab modalità
    document.querySelectorAll(".mode-tab").forEach((btn) => {
        btn.addEventListener("click", () => {
            setMode(btn.dataset.mode);
        });
    });

    // nascondo nav all'inizio
    const nextBtn = document.getElementById("nextBtn");
    const prevBtn = document.getElementById("prevBtn");
    if (nextBtn) nextBtn.style.display = "none";
    if (prevBtn) prevBtn.style.display = "none";

    updateSavedCount();
    updateSessionStats();
    renderExamSidebar();
    updateProgress();
});
