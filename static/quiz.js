// --- STATI GLOBALI ---
let correctCount = 0;
let incorrectCount = 0;
let answeredCount = 0;
let sessionXp = 0;
let comboCount = 0;
let bestCombo = 0;

let currentQuestionIndex = 1;
let activeQuestion = null;
let savedQuestions = [];
let isSavedQuiz = false;
let hasAnsweredCurrent = false;
let lastFeedbackIndex = -1;
let saveTimer = null;
let lastSavedState = "";
let isRestoringSession = false;
let planRefreshTimer = null;
let activeSubjectProfile = null;
let subjectProfileKey = null;
let todayDashboardData = null;
let focusTimerId = null;
let focusSecondsRemaining = 0;
let activePlaylist = null;
let playlistRun = null;
let activeReviewTopic = null;

let studyQuestions = [];
let studyIndex = 0;

let mode = "training";
let isExamMode = false;
let tutorialLessons = [];
let tutorialProgress = null;
let activeTutorialLesson = null;
let tutorialSaveTimer = null;
let architecturePractice = null;
let activeArchitectureExercise = null;
let selectedArchitectureOption = "";

let examQuestions = [];
let examIndex = 0;
let examAnswers = [];
let examFinished = false;
let examTimerId = null;
let examTimeRemaining = 0;
let examStartTimestamp = null;

const STATUS_LABELS = {
    new: "Nuova",
    weak: "Debole",
    shaky: "Incerta",
    learning: "In apprendimento",
    solid: "Solida",
    mastered: "Padroneggiata"
};

const REVIEW_LABELS = {
    mixed: "miste intelligenti",
    plan: "piano di oggi",
    weak: "deboli",
    due: "scadute",
    easy: "facili",
    mastered: "padroneggiate",
    new: "nuove",
    random: "casuali"
};

const PLAYLIST_SEGMENTS = {
    weak: {
        key: "weak",
        label: "Errori caldi",
        detail: "Partiamo dalle domande che ti hanno fatto inciampare.",
        tone: "danger"
    },
    due: {
        key: "due",
        label: "Ripasso scaduto",
        detail: "Rinforzo rapido prima che scivolino via.",
        tone: "warning"
    },
    new: {
        key: "new",
        label: "Scoperta",
        detail: "Domande nuove a blocchi, senza maratona infinita.",
        tone: "info"
    },
    learn_preview: {
        key: "learn_preview",
        label: "Studio guidato",
        detail: "Leggi risposta e spiegazione, poi te la chiedo senza aiuti.",
        tone: "info"
    },
    easy: {
        key: "easy",
        label: "Warm-up",
        detail: "Domande piu leggere per prendere ritmo.",
        tone: "success"
    },
    random: {
        key: "random",
        label: "Misto finale",
        detail: "Controllo senza schema, come all'esame.",
        tone: "neutral"
    },
    retry: {
        key: "retry",
        label: "Ritenta",
        detail: "Questa torna subito per chiudere l'errore.",
        tone: "recover"
    }
};

const SUBJECT_SCOPED_MODES = {
    tutorial: "programmazione_2",
    architecture: "architettura_calcolatori"
};

const LEGACY_MODE_TO_REVIEW_FLOW = {
    daily: "new",
    tutor: "tutor",
    sprint: "sprint_quick"
};

const REVIEW_FLOW_CONFIG = {
    smart: {
        label: "Ripasso intelligente",
        hint: "Scegli il focus: l'app pesca le domande piu utili per fissarle meglio."
    },
    learn_new: {
        label: "Impara nuove",
        preset: "new",
        hint: "Il numero indica le domande nuove reali: ogni domanda fa Studio rapido + Quiz, quindi 12 nuove = 24 passaggi."
    },
    new: {
        label: "Nuove domande",
        preset: "new",
        hint: "Copri domande mai viste e aumenta la percentuale di programma toccato."
    },
    tutor: {
        label: "Casuali con spiegazione",
        preset: "random",
        hint: "Domande casuali con scheda studio dopo la risposta: utile quando vuoi imparare mentre fai quiz."
    },
    sprint_quick: {
        label: "Sprint rapido",
        preset: "mixed",
        hint: "Sessione breve: poche domande, ritmo alto, zero dispersione."
    },
    sprint_recover: {
        label: "Recupera errori",
        preset: "weak",
        hint: "Riprende soprattutto domande sbagliate o incerte."
    },
    sprint_boss: {
        label: "Boss finale",
        preset: "random",
        hint: "Dieci domande dagli argomenti deboli e dal misto: controllo serio da fine sessione."
    },
    sprint_combo: {
        label: "Combo challenge",
        preset: "easy",
        hint: "Warm-up sulle facili per fare serie corrette e rinforzare sicurezza."
    }
};

function normalizedSubjectText() {
    const dbSelect = document.getElementById("dbSelect");
    const value = dbSelect?.value || "";
    const label = dbSelect?.selectedOptions?.[0]?.textContent || "";
    return `${value} ${label}`
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/[_-]+/g, " ");
}

function currentSubjectContext() {
    const dbSelect = document.getElementById("dbSelect");
    const subjectText = normalizedSubjectText();
    return {
        hasSubject: Boolean(dbSelect?.value),
        isProgrammazione2: /\bprogrammazione\s*2\b/.test(subjectText),
        isArchitetturaCalcolatori: subjectText.includes("architettura") && subjectText.includes("calcolatori")
    };
}

function isModeAllowedForCurrentSubject(targetMode) {
    const scope = SUBJECT_SCOPED_MODES[targetMode];
    if (!scope) return true;

    const subject = currentSubjectContext();
    if (scope === "programmazione_2") return subject.isProgrammazione2;
    if (scope === "architettura_calcolatori") return subject.isArchitetturaCalcolatori;
    return false;
}

function resolveModeForCurrentSubject(targetMode) {
    targetMode = LEGACY_MODE_TO_REVIEW_FLOW[targetMode] ? "review" : targetMode;
    return isModeAllowedForCurrentSubject(targetMode) ? targetMode : "training";
}

function updateModeAvailability() {
    document.querySelectorAll(".mode-tab").forEach((btn) => {
        const allowed = isModeAllowedForCurrentSubject(btn.dataset.mode);
        btn.hidden = !allowed;
        btn.disabled = !allowed;
        btn.setAttribute("aria-hidden", allowed ? "false" : "true");
    });

    const toolsSection = document.getElementById("subjectToolsSection");
    if (toolsSection) {
        const hasVisibleTool = Array.from(toolsSection.querySelectorAll(".mode-tab"))
            .some((btn) => !btn.hidden);
        toolsSection.hidden = !hasVisibleTool;
    }
}

function setReviewFlow(flow) {
    const select = document.getElementById("reviewFlow");
    if (!select) return;
    const nextFlow = REVIEW_FLOW_CONFIG[flow] ? flow : "smart";
    select.value = nextFlow;
    updateReviewControls();
}

function updateStartButtonCopy() {
    const startBtn = document.getElementById("startButton");
    if (!startBtn) return;
    if (mode === "tutorial") {
        startBtn.textContent = "Apri Scrittura Python";
        return;
    }
    if (mode === "architecture") {
        startBtn.textContent = "Genera esercizio";
        return;
    }
    if (mode === "exam") {
        startBtn.textContent = "Inizia simulazione";
        return;
    }
    if (mode === "plan") {
        startBtn.textContent = "Avvia piano di oggi";
        return;
    }
    if (mode === "review") {
        const flow = document.getElementById("reviewFlow")?.value || "smart";
        const config = REVIEW_FLOW_CONFIG[flow] || REVIEW_FLOW_CONFIG.smart;
        startBtn.textContent = `Avvia: ${config.label}`;
        return;
    }
    startBtn.textContent = "Inizia allenamento";
}

function updateReviewControls() {
    const flow = document.getElementById("reviewFlow")?.value || "smart";
    const config = REVIEW_FLOW_CONFIG[flow] || REVIEW_FLOW_CONFIG.smart;
    const presetGroup = document.getElementById("reviewPresetGroup");
    const hint = document.getElementById("reviewModeHint");
    const countLabel = document.querySelector('label[for="reviewQuestionCount"]');
    if (presetGroup) presetGroup.hidden = Boolean(config.preset);
    if (hint) hint.textContent = config.hint;
    if (countLabel) {
        countLabel.textContent = flow === "learn_new" ? "Nuove" : "Domande";
    }
    updateStartButtonCopy();
}

function updateMobileNav() {
    document.querySelectorAll(".mobile-bottom-nav button").forEach((btn) => {
        const mobileMode = btn.dataset.mobileMode;
        btn.classList.toggle("active", Boolean(mobileMode && mobileMode === mode));
    });
}

function currentReviewFlow() {
    return document.getElementById("reviewFlow")?.value || "smart";
}

function attemptModeFromReviewFlow() {
    const flow = currentReviewFlow();
    if (flow === "new" || flow === "learn_new") return "daily";
    if (flow === "tutor") return "tutor";
    if (flow.startsWith("sprint_")) return "sprint";
    return "review";
}

const CORRECT_FEEDBACK = [
    "Risposta corretta. Continua cosi.",
    "Centro. Tieni il ritmo.",
    "Giusta. Questa sta diventando stabile.",
    "Bene. Un altro mattoncino fissato."
];

const WRONG_FEEDBACK = [
    "Risposta errata. Perfetto materiale da ripasso.",
    "Non era questa. La riportiamo nel giro.",
    "Errore utile: questa ora vale doppio nello studio.",
    "Segnata come debole. La riprendiamo piu avanti."
];

function isStudyMode() {
    return mode === "plan" || mode === "daily" || mode === "review" || mode === "tutor" || mode === "sprint";
}

async function fetchJson(url, options = {}) {
    const res = await fetch(url, options);
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
        if (res.status === 401) {
            window.location.href = "/login";
            return null;
        }
        throw new Error(data.error || "Errore di rete");
    }
    return data;
}

async function loadDbOptions() {
    const sel = document.getElementById("dbSelect");
    if (!sel) return;

    const data = await fetchJson("/api/databases");
    if (!data) return;

    sel.innerHTML = "";

    const ph = document.createElement("option");
    ph.value = "";
    ph.textContent = "Seleziona una materia";
    ph.disabled = true;
    ph.selected = true;
    sel.appendChild(ph);

    (data.options || []).forEach((opt) => {
        const o = document.createElement("option");
        o.value = opt.key;
        o.textContent = opt.label;
        sel.appendChild(o);
    });

    if (data.active) {
        sel.value = data.active;
        await loadProgressSummary();
    }

    updateModeAvailability();
}

async function setDatabase(dbKey) {
    const previousMode = mode;
    const data = await fetchJson("/api/set_database", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ db_key: dbKey })
    });

    if (!data) return false;

    resetSession();
    savedQuestions = [];
    studyQuestions = [];
    studyIndex = 0;
    clearActivePlaylist();
    updateSavedCount();
    await loadProgressSummary();
    await loadSubjectProfile({ showSetup: true });

    updateModeAvailability();

    const nextMode = resolveModeForCurrentSubject(previousMode);
    mode = nextMode;
    setMode(nextMode);
    if (nextMode === "plan") {
        resetQuestionShell("Materia selezionata. Imposta la data esame e premi Inizia.");
        await refreshStudyPlan();
    } else {
        resetQuestionShell("Materia selezionata. Premi Inizia per continuare.");
    }
    saveCurrentStudySession(true);
    return true;
}

function resetQuestionShell(message) {
    const domandaIdEl = document.getElementById("domanda-id");
    const domandaText = document.getElementById("domanda");
    const answersList = document.getElementById("risposte");
    const resultEl = document.getElementById("result");
    const nextBtn = document.getElementById("nextBtn");
    const prevBtn = document.getElementById("prevBtn");

    activeQuestion = null;
    if (domandaIdEl) domandaIdEl.innerText = "ID Domanda: -";
    if (domandaText) domandaText.innerText = message;
    if (answersList) answersList.innerHTML = "";
    if (resultEl) resultEl.innerText = "";
    if (nextBtn) nextBtn.style.display = "none";
    if (prevBtn) prevBtn.style.display = "none";
    hideRecallGate();
    hideStudyPanel();
    updateQuestionProgressBadge(null);
    renderPlaylistPanel();
}

function updateSavedCount() {
    const savedCountEl = document.getElementById("savedCount");
    if (savedCountEl) savedCountEl.innerText = `Salvate: ${savedQuestions.length}`;
}

function updateSessionStats() {
    const answeredEl = document.getElementById("answeredCount");
    const accEl = document.getElementById("accuracy");
    const perfEl = document.getElementById("performanceLabel");
    const perfContainer = document.querySelector(".session-item.session-performance");

    if (answeredEl) answeredEl.innerText = answeredCount;

    const total = correctCount + incorrectCount;
    const accuracy = total > 0 ? Math.round((correctCount / total) * 100) : 0;
    if (accEl) accEl.innerText = `${accuracy}%`;

    const score30 = total > 0 ? Math.floor((correctCount / total) * 30) : 0;
    if (perfEl) perfEl.innerText = total === 0 ? "-/30" : `${score30}/30`;

    if (perfContainer) {
        perfContainer.classList.remove("perf-bad", "perf-medium", "perf-good");
        if (total > 0) {
            if (score30 < 18) perfContainer.classList.add("perf-bad");
            else if (score30 <= 24) perfContainer.classList.add("perf-medium");
            else perfContainer.classList.add("perf-good");
        }
    }
}

async function loadProgressSummary() {
    const totalEl = document.getElementById("progressTotal");
    if (!totalEl) return;

    const dbSelect = document.getElementById("dbSelect");
    if (dbSelect && !dbSelect.value) return;

    try {
        const summary = await fetchJson("/api/progress_summary");
        if (!summary) return;

        const seenPct = summary.total_questions
            ? Math.round((summary.seen / summary.total_questions) * 100)
            : 0;
        totalEl.innerText = `${summary.seen}/${summary.total_questions}`;
        setText("progressSeenPct", `${seenPct}%`);
        setText("progressNew", summary.new);
        setText("progressDue", summary.due);
        setText("progressWeak", summary.weak + summary.shaky);
        setText("progressMastered", summary.mastered);
        setText("progressAccuracy", `${summary.accuracy}%`);
        setText("progressToday", summary.answered_today);
        loadTodayDashboard().catch((dashboardErr) => console.warn(dashboardErr));
    } catch (err) {
        console.warn(err);
    }
}

function setTodayMetric(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
}

function renderSubjectMap(topics = []) {
    const section = document.getElementById("subjectMap");
    const list = document.getElementById("subjectMapList");
    if (!section || !list) return;
    list.innerHTML = "";
    if (!topics.length) {
        section.hidden = true;
        return;
    }
    topics.forEach((topic) => {
        const item = document.createElement("article");
        item.className = "subject-map-item";
        if ((topic.weak_count || 0) + (topic.due_count || 0) > 0) {
            item.classList.add("needs-practice");
        }
        item.dataset.topicId = topic.id || "";
        item.dataset.topicAction = topic.action || "";

        const title = document.createElement("strong");
        title.textContent = topic.label || "Argomento";

        const detail = document.createElement("small");
        detail.textContent = topic.detail || "";

        const bars = document.createElement("div");
        bars.className = "subject-map-bars";

        [
            ["Viste", topic.seen_pct || 0, ""],
            ["Solide", topic.solid_pct || 0, "solid-fill"]
        ].forEach(([label, value, className]) => {
            const row = document.createElement("div");
            row.className = "subject-map-bar";
            const name = document.createElement("span");
            name.textContent = label;
            const track = document.createElement("span");
            track.className = "subject-map-track";
            const fill = document.createElement("span");
            if (className) fill.className = className;
            fill.style.width = `${Math.max(0, Math.min(100, value))}%`;
            track.appendChild(fill);
            const pct = document.createElement("span");
            pct.textContent = `${value}%`;
            row.appendChild(name);
            row.appendChild(track);
            row.appendChild(pct);
            bars.appendChild(row);
        });

        item.appendChild(title);
        if (detail.textContent) item.appendChild(detail);
        item.appendChild(bars);
        const action = document.createElement("button");
        action.type = "button";
        action.className = "topic-action-btn";
        action.textContent = topic.action === "architecture"
            ? "Esercizi"
            : topic.action === "review_topic"
                ? "Quiz mirato"
                : "Allena";
        action.addEventListener("click", () => startTopicPractice(topic));
        item.appendChild(action);
        list.appendChild(item);
    });
    section.hidden = false;
}

async function startTopicPractice(topic = {}) {
    if (topic.action === "architecture") {
        setMode("architecture");
        const select = document.getElementById("architectureTopic");
        if (select && topic.id) select.value = topic.id;
        await startArchitectureMode();
        setAnalysisVisible(false);
        scrollToStudySurface();
        return;
    }

    setMode("review");
    setReviewFlow("sprint_recover");
    setReviewCount(12);
    activeReviewTopic = {
        id: topic.id || "",
        label: topic.label || "Argomento"
    };
    await startReviewMode(activeReviewTopic);
    activeReviewTopic = null;
    setAnalysisVisible(false);
}

function renderStudyDiary(diary = {}) {
    const section = document.getElementById("studyDiary");
    const list = document.getElementById("studyDiaryList");
    if (!section || !list) return;
    const items = diary.items || [];
    list.innerHTML = "";
    if (!items.length) {
        section.hidden = true;
        return;
    }

    const summary = document.createElement("p");
    summary.className = "study-diary-summary";
    summary.textContent = diary.summary || "Errori principali da recuperare oggi.";
    list.appendChild(summary);

    items.slice(0, 5).forEach((item) => {
        const row = document.createElement("button");
        row.type = "button";
        row.className = "study-diary-item";
        row.addEventListener("click", async () => {
            setMode("review");
            setReviewFlow("sprint_recover");
            setReviewCount(10);
            await startReviewMode();
        });

        const text = document.createElement("span");
        text.textContent = item.text || `Domanda ${item.question_id}`;
        const meta = document.createElement("small");
        meta.textContent = `${item.reason || "errore"} - ${item.wrong_count || 1} errori - ${item.action || "Rivedi"}`;
        row.appendChild(text);
        row.appendChild(meta);
        list.appendChild(row);
    });
    section.hidden = false;
}

function renderTodayDashboard(data) {
    todayDashboardData = data;
    const section = document.getElementById("todayDashboard");
    if (!section || !data) return;
    const today = data.today || {};
    const rec = data.recommendation || {};
    const streak = data.streak || {};
    const grade = today.projected_grade?.label || "-/30";

    setTodayMetric("todayTitle", data.subject_label || "Piano di studio");
    setTodayMetric("todaySubtitle", rec.reason || today.feasibility_label || "Premi Sessione consigliata per iniziare.");
    setTodayMetric("todayNew", today.new || 0);
    setTodayMetric("todayReview", today.review || 0);
    setTodayMetric("todayErrors", today.errors || 0);
    setTodayMetric("todayTime", `${today.estimated_minutes || 0} min`);
    setTodayMetric("todayDays", today.days_left ? `${today.days_left}` : "-");
    setTodayMetric("todayDailyLoad", today.daily_questions_required ? `${today.daily_questions_required} dom.` : "-");
    setTodayMetric("todayGrade", grade);
    setTodayMetric("todayStreak", streak.streak_days || 0);
    setTodayMetric("todayEnergyText", `Energia studio: ${streak.energy || 0}%`);
    setTodayMetric("todayRecovered", `${streak.recovered_today || 0} errori recuperati oggi`);
    const fill = document.getElementById("todayEnergyFill");
    if (fill) fill.style.width = `${Math.max(0, Math.min(100, streak.energy || 0))}%`;
    const recBtn = document.getElementById("recommendedSessionBtn");
    if (recBtn) recBtn.textContent = rec.label ? `Studia adesso: ${rec.label}` : "Studia adesso";
    renderStudyDiary(data.diary || {});
    renderSubjectMap(data.topics || []);
    const analysisEntry = document.getElementById("analysisEntry");
    if (analysisEntry) analysisEntry.hidden = false;
    section.hidden = false;
}

async function loadTodayDashboard() {
    const dbKey = document.getElementById("dbSelect")?.value || "";
    const section = document.getElementById("todayDashboard");
    const map = document.getElementById("subjectMap");
    const analysisEntry = document.getElementById("analysisEntry");
    const analysisPanel = document.getElementById("analysisPanel");
    if (!dbKey) {
        todayDashboardData = null;
        if (section) section.hidden = true;
        if (map) map.hidden = true;
        if (analysisEntry) analysisEntry.hidden = true;
        if (analysisPanel) analysisPanel.hidden = true;
        return null;
    }
    try {
        const data = await fetchJson("/api/today_dashboard");
        renderTodayDashboard(data);
        return data;
    } catch (err) {
        console.warn(err);
        return null;
    }
}

function setReviewCount(count) {
    const input = document.getElementById("reviewQuestionCount");
    if (input && count) input.value = String(Math.max(1, Math.min(300, count)));
}

async function startRecommendedSession() {
    if (!await ensureSubjectProfile()) return;
    const data = todayDashboardData || await loadTodayDashboard();
    if (!data?.recommendation) return;
    const rec = data.recommendation;
    setMode("review");
    setReviewFlow(rec.flow || "smart");
    if (rec.preset) {
        const preset = document.getElementById("reviewPreset");
        if (preset) preset.value = rec.preset;
    }
    setReviewCount(rec.count || 20);
    await startReviewMode();
}

async function startLearnNewSession(count = 12) {
    if (!await ensureSubjectProfile()) return;
    setMode("review");
    setReviewFlow("learn_new");
    setReviewCount(count);
    await startReviewMode();
}

async function startQuickTenSession() {
    if (!await ensureSubjectProfile()) return;
    setMode("review");
    setReviewFlow("sprint_quick");
    setReviewCount(10);
    await startReviewMode();
}

function renderFocusTimer() {
    const el = document.getElementById("focusTimer");
    if (!el) return;
    const minutes = Math.floor(focusSecondsRemaining / 60);
    const seconds = focusSecondsRemaining % 60;
    el.textContent = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
    el.hidden = false;
}

function startFocusCountdown() {
    clearInterval(focusTimerId);
    focusSecondsRemaining = 15 * 60;
    renderFocusTimer();
    focusTimerId = setInterval(() => {
        focusSecondsRemaining = Math.max(0, focusSecondsRemaining - 1);
        renderFocusTimer();
        if (focusSecondsRemaining <= 0) {
            clearInterval(focusTimerId);
            const result = document.getElementById("result");
            if (result) result.innerText = "Focus finito. Ottimo: fai una pausa breve o continua con il ripasso.";
        }
    }, 1000);
}

async function startFocusSession() {
    if (!await ensureSubjectProfile()) return;
    const data = todayDashboardData || await loadTodayDashboard();
    const focus = data?.focus || { flow: "sprint_recover", count: 8 };
    setMode("review");
    setReviewFlow(focus.flow || "sprint_recover");
    setReviewCount(focus.count || 8);
    startFocusCountdown();
    await startReviewMode();
}

function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.innerText = value;
}

function setAnalysisVisible(visible) {
    const panel = document.getElementById("analysisPanel");
    const button = document.getElementById("analysisToggleBtn");
    if (!panel) return;
    panel.hidden = !visible;
    if (button) button.textContent = visible ? "Nascondi Analisi" : "Apri Analisi";
    if (visible) {
        panel.scrollIntoView({ behavior: "smooth", block: "start" });
    }
}

function scrollToStudySurface() {
    const target = document.getElementById("quizContent")
        || document.getElementById("tutorialShell")
        || document.getElementById("architectureShell");
    if (!target) return;
    setTimeout(() => {
        target.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 120);
}

function safeNumber(value, fallback = 0) {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : fallback;
}

function setSaveStatus(text, state = "") {
    const el = document.getElementById("sessionSaveStatus");
    if (!el) return;
    el.innerText = text;
    el.classList.remove("saving", "saved", "error");
    if (state) el.classList.add(state);
}

function selectedSubjectLabel() {
    const dbSelect = document.getElementById("dbSelect");
    return dbSelect?.selectedOptions?.[0]?.textContent?.trim() || "questa materia";
}

function subjectProfilePayloadFromFields() {
    const onboardingPanel = document.getElementById("subjectOnboarding");
    const useOnboarding = onboardingPanel && !onboardingPanel.hidden;
    return {
        exam_date: (useOnboarding ? document.getElementById("onboardingExamDate")?.value : "") || document.getElementById("examDate")?.value || "",
        study_minutes: (useOnboarding ? document.getElementById("onboardingStudyMinutes")?.value : "") || document.getElementById("studyMinutes")?.value || "45",
        target_grade: (useOnboarding ? document.getElementById("onboardingTargetGrade")?.value : "") || document.getElementById("targetGrade")?.value || "24"
    };
}

function applySubjectProfile(profile) {
    if (!profile) return;
    const examDateInput = document.getElementById("examDate");
    const studyMinutesInput = document.getElementById("studyMinutes");
    const targetGradeInput = document.getElementById("targetGrade");
    const onboardingExamDate = document.getElementById("onboardingExamDate");
    const onboardingStudyMinutes = document.getElementById("onboardingStudyMinutes");
    const onboardingTargetGrade = document.getElementById("onboardingTargetGrade");
    if (examDateInput && profile.exam_date) examDateInput.value = profile.exam_date;
    if (studyMinutesInput && profile.study_minutes) studyMinutesInput.value = profile.study_minutes;
    if (targetGradeInput && profile.target_grade) targetGradeInput.value = profile.target_grade;
    if (onboardingExamDate && profile.exam_date) onboardingExamDate.value = profile.exam_date;
    if (onboardingStudyMinutes && profile.study_minutes) onboardingStudyMinutes.value = profile.study_minutes;
    if (onboardingTargetGrade && profile.target_grade) onboardingTargetGrade.value = profile.target_grade;
}

function showSubjectOnboarding(subjectLabel = selectedSubjectLabel()) {
    const panel = document.getElementById("subjectOnboarding");
    if (!panel) return;
    setText("onboardingSubjectName", subjectLabel);
    const currentValues = subjectProfilePayloadFromFields();
    const onboardingExamDate = document.getElementById("onboardingExamDate");
    const onboardingStudyMinutes = document.getElementById("onboardingStudyMinutes");
    const onboardingTargetGrade = document.getElementById("onboardingTargetGrade");
    if (onboardingExamDate) onboardingExamDate.value = currentValues.exam_date || "";
    if (onboardingStudyMinutes) onboardingStudyMinutes.value = currentValues.study_minutes || "45";
    if (onboardingTargetGrade) onboardingTargetGrade.value = currentValues.target_grade || "24";
    panel.hidden = false;
    resetQuestionShell("Configura prima la materia: data esame, tempo al giorno e voto obiettivo.");
}

function hideSubjectOnboarding() {
    const panel = document.getElementById("subjectOnboarding");
    if (panel) panel.hidden = true;
}

async function loadSubjectProfile({ showSetup = false } = {}) {
    const dbKey = document.getElementById("dbSelect")?.value || "";
    if (!dbKey) {
        activeSubjectProfile = null;
        subjectProfileKey = null;
        hideSubjectOnboarding();
        return null;
    }

    const data = await fetchJson("/api/subject_profile");
    if (!data) return null;

    subjectProfileKey = data.subject_key;
    activeSubjectProfile = data.profile || null;
    if (activeSubjectProfile) {
        applySubjectProfile(activeSubjectProfile);
        hideSubjectOnboarding();
    } else if (showSetup) {
        showSubjectOnboarding(data.subject_label);
    }
    return activeSubjectProfile;
}

async function saveSubjectProfile({ silent = false } = {}) {
    const dbKey = document.getElementById("dbSelect")?.value || "";
    if (!dbKey) return null;

    const payload = subjectProfilePayloadFromFields();
    if (!payload.exam_date) {
        if (!silent) {
            showSubjectOnboarding();
            alert("Inserisci la data dell'esame per configurare la materia.");
        }
        return null;
    }
    if (isPastDate(payload.exam_date)) {
        if (!silent) alert("La data esame e gia passata. Inserisci una data futura.");
        return null;
    }

    const data = await fetchJson("/api/subject_profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
    if (!data) return null;

    activeSubjectProfile = data.profile;
    subjectProfileKey = data.subject_key;
    applySubjectProfile(activeSubjectProfile);
    hideSubjectOnboarding();
    if (!silent) {
        setSaveStatus("Profilo materia salvato", "saved");
        setMode("plan");
        await refreshStudyPlan();
        await loadTodayDashboard();
        resetQuestionShell("Materia configurata. Premi Inizia per seguire il piano di oggi.");
    }
    saveCurrentStudySession(true);
    return activeSubjectProfile;
}

async function ensureSubjectProfile() {
    const dbKey = document.getElementById("dbSelect")?.value || "";
    if (!dbKey) return true;
    if (activeSubjectProfile && subjectProfileKey === dbKey) return true;
    const profile = await loadSubjectProfile({ showSetup: true });
    return Boolean(profile);
}

function formatSaveTime(value) {
    if (!value) return "";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "";
    return date.toLocaleTimeString("it-IT", {
        hour: "2-digit",
        minute: "2-digit"
    });
}

function sessionPayload() {
    const dbKey = document.getElementById("dbSelect")?.value || null;
    const examDate = document.getElementById("examDate")?.value || "";
    const studyMinutes = document.getElementById("studyMinutes")?.value || "45";
    const targetGrade = document.getElementById("targetGrade")?.value || "24";
    const reviewFlow = document.getElementById("reviewFlow")?.value || "smart";
    const reviewPreset = document.getElementById("reviewPreset")?.value || "mixed";
    const reviewCount = document.getElementById("reviewQuestionCount")?.value || "40";
    const architectureTopic = document.getElementById("architectureTopic")?.value || "mixed";
    return {
        db_key: dbKey,
        mode,
        current_question_index: currentQuestionIndex,
        study_index: studyIndex,
        study_question_ids: studyQuestions.map((question) => question.id),
        plan_settings: {
            exam_date: examDate,
            study_minutes: studyMinutes,
            target_grade: targetGrade
        },
        review_settings: {
            flow: reviewFlow,
            preset: reviewPreset,
            count: reviewCount,
            topic: activeReviewTopic?.id || activePlaylist?.topicId || ""
        },
        architecture_settings: {
            topic: architectureTopic
        },
        playlist_state: playlistStatePayload(),
        session_stats: {
            correctCount,
            incorrectCount,
            answeredCount,
            sessionXp,
            comboCount,
            bestCombo,
            playlistRun
        }
    };
}

function restoreSessionStats(stats = {}) {
    correctCount = safeNumber(stats.correctCount);
    incorrectCount = safeNumber(stats.incorrectCount);
    answeredCount = safeNumber(stats.answeredCount);
    sessionXp = safeNumber(stats.sessionXp);
    comboCount = safeNumber(stats.comboCount);
    bestCombo = safeNumber(stats.bestCombo);
    playlistRun = stats.playlistRun || playlistRun;

    setText("correctCount", correctCount);
    setText("incorrectCount", incorrectCount);
    updateSessionStats();
    updatePlayStats();
}

async function saveCurrentStudySession(immediate = false, useBeacon = false) {
    if (isRestoringSession) return;
    const payload = sessionPayload();
    if (!payload.db_key && !["tutorial", "architecture"].includes(payload.mode)) return;

    const serialized = JSON.stringify(payload);
    if (serialized === lastSavedState && !immediate) return;

    if (!immediate) {
        clearTimeout(saveTimer);
        saveTimer = setTimeout(() => saveCurrentStudySession(true), 650);
        setSaveStatus("Salvataggio...", "saving");
        return;
    }

    lastSavedState = serialized;

    if (useBeacon && navigator.sendBeacon) {
        const blob = new Blob([serialized], { type: "application/json" });
        navigator.sendBeacon("/api/study_session", blob);
        return;
    }

    try {
        setSaveStatus("Salvataggio...", "saving");
        const data = await fetchJson("/api/study_session", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: serialized
        });
        const time = formatSaveTime(data?.updated_at);
        setSaveStatus(time ? `Salvata alle ${time}` : "Sessione salvata", "saved");
        return true;
    } catch (err) {
        console.warn(err);
        setSaveStatus("Salvataggio non riuscito", "error");
        return false;
    }
}

async function restoreSavedStudySession() {
    isRestoringSession = true;
    try {
        const data = await fetchJson("/api/study_session");
        const saved = data?.session;
        if (!saved || (!saved.db_key && !["tutorial", "architecture"].includes(saved.mode))) {
            setSaveStatus("Salvataggio automatico");
            return false;
        }

        const dbSelect = document.getElementById("dbSelect");
        if (dbSelect && saved.db_key) {
            dbSelect.value = saved.db_key;
            await loadProgressSummary();
        }
        updateModeAvailability();

        restoreSessionStats(saved.session_stats || {});
        currentQuestionIndex = safeNumber(saved.current_question_index, 1);
        studyIndex = safeNumber(saved.study_index, 0);

        const planSettings = saved.plan_settings || {};
        const examDateInput = document.getElementById("examDate");
        const studyMinutesInput = document.getElementById("studyMinutes");
        const targetGradeInput = document.getElementById("targetGrade");
        if (examDateInput && planSettings.exam_date) {
            examDateInput.value = planSettings.exam_date;
        }
        if (studyMinutesInput && planSettings.study_minutes) {
            studyMinutesInput.value = planSettings.study_minutes;
        }
        if (targetGradeInput && planSettings.target_grade) {
            targetGradeInput.value = planSettings.target_grade;
        }
        const loadedSubjectProfile = await loadSubjectProfile({ showSetup: false });
        if (!loadedSubjectProfile && planSettings.exam_date) {
            await saveSubjectProfile({ silent: true });
        }

        const reviewSettings = saved.review_settings || {};
        const reviewFlow = document.getElementById("reviewFlow");
        const reviewPreset = document.getElementById("reviewPreset");
        const reviewQuestionCount = document.getElementById("reviewQuestionCount");
        if (reviewFlow && reviewSettings.flow && REVIEW_FLOW_CONFIG[reviewSettings.flow]) {
            reviewFlow.value = reviewSettings.flow;
        }
        if (reviewPreset && reviewSettings.preset) {
            reviewPreset.value = reviewSettings.preset;
        }
        if (reviewQuestionCount && reviewSettings.count) {
            reviewQuestionCount.value = reviewSettings.count;
        }
        if (LEGACY_MODE_TO_REVIEW_FLOW[saved.mode]) {
            setReviewFlow(LEGACY_MODE_TO_REVIEW_FLOW[saved.mode]);
        } else {
            updateReviewControls();
        }

        const architectureSettings = saved.architecture_settings || {};
        const architectureTopic = document.getElementById("architectureTopic");
        if (architectureTopic && architectureSettings.topic) {
            architectureTopic.value = architectureSettings.topic;
        }

        const savedMode = resolveModeForCurrentSubject(saved.mode || "training");
        setMode(savedMode);

        if (["plan", "daily", "review", "tutor", "sprint"].includes(savedMode) && saved.study_question_ids?.length) {
            const queue = await fetchJson("/api/questions_by_ids", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ids: saved.study_question_ids })
            });
            studyQuestions = queue?.questions || [];
            if (studyQuestions.length) {
                restorePlaylistState(saved.playlist_state, studyQuestions);
                studyIndex = Math.min(studyIndex, studyQuestions.length - 1);
                mode = savedMode;
                renderStudyQuestion();
                showNavButtons();
            }
        } else if (savedMode === "training") {
            await getTrainingQuestion();
        } else if (savedMode === "architecture") {
            await loadArchitecturePractice();
        } else {
            resetQuestionShell("Sessione precedente ripristinata. Premi Inizia per continuare.");
        }

        setSaveStatus("Sessione ripristinata", "saved");
        lastSavedState = JSON.stringify(sessionPayload());
        return true;
    } catch (err) {
        console.warn(err);
        setSaveStatus("Ripristino non riuscito", "error");
        return false;
    } finally {
        isRestoringSession = false;
    }
}

function updatePlayStats() {
    setText("sessionXp", sessionXp);
    setText("comboCount", comboCount);

    const comboEl = document.querySelector(".session-item.session-combo");
    if (comboEl) {
        comboEl.classList.toggle("combo-hot", comboCount >= 3);
    }
}

function randomFeedback(isCorrect) {
    const list = isCorrect ? CORRECT_FEEDBACK : WRONG_FEEDBACK;
    let index = Math.floor(Math.random() * list.length);
    if (list.length > 1 && index === lastFeedbackIndex) {
        index = (index + 1) % list.length;
    }
    lastFeedbackIndex = index;
    return list[index];
}

function awardAnswerXp(isCorrect, question) {
    const progress = question?.progress || {};
    let points = isCorrect ? 10 : 4;

    if (progress.status === "new") points += 3;
    if (progress.status === "weak" || progress.status === "shaky") points += isCorrect ? 8 : 2;
    const attemptMode = mode === "review" ? attemptModeFromReviewFlow() : mode;
    if (attemptMode === "daily") points += 2;
    if (attemptMode === "review") points += 3;
    if (attemptMode === "tutor") points += 2;

    sessionXp += points;
    return points;
}

function applyAnswerRhythm(isCorrect) {
    if (isCorrect) {
        comboCount += 1;
        bestCombo = Math.max(bestCombo, comboCount);
    } else {
        comboCount = 0;
    }
    updatePlayStats();
}

function resetSession() {
    correctCount = 0;
    incorrectCount = 0;
    answeredCount = 0;
    sessionXp = 0;
    comboCount = 0;
    bestCombo = 0;
    hasAnsweredCurrent = false;

    setText("correctCount", "0");
    setText("incorrectCount", "0");
    updateSessionStats();
    updatePlayStats();
    setText("result", "");
    saveCurrentStudySession();
}

function shuffleArray(array) {
    return array.sort(() => Math.random() - 0.5);
}

function clampInt(value, min, max, fallback) {
    const parsed = parseInt(value, 10);
    if (Number.isNaN(parsed)) return fallback;
    return Math.max(min, Math.min(max, parsed));
}

function playlistSegment(key, overrides = {}) {
    return { ...(PLAYLIST_SEGMENTS[key] || PLAYLIST_SEGMENTS.random), ...overrides };
}

function tagQuestionForPlaylist(question, segment, extra = {}) {
    const learnStage = Object.prototype.hasOwnProperty.call(extra, "learnStage")
        ? extra.learnStage
        : question?._learnStage || "";
    return {
        ...question,
        _playlistSegment: segment,
        _isRecovery: Boolean(extra.isRecovery),
        _retryCount: safeNumber(extra.retryCount, 0),
        _learnStage: learnStage,
        _learnQuestionNumber: safeNumber(extra.learnQuestionNumber, question?._learnQuestionNumber || 0)
    };
}

async function fetchReviewQuestionsForPlaylist(preset, limit, topicId = "") {
    const safeLimit = clampInt(limit, 0, 300, 0);
    if (safeLimit <= 0) return [];
    const params = new URLSearchParams({
        mode: preset,
        limit: String(safeLimit)
    });
    if (topicId) params.set("topic", topicId);
    const data = await fetchJson(`/api/review_questions?${params.toString()}`);
    return data?.questions || [];
}

function appendUniquePlaylistQuestions(queue, seenIds, questions, segment, maxCount) {
    let added = 0;
    for (const question of questions || []) {
        if (added >= maxCount) break;
        if (seenIds.has(question.id)) continue;
        seenIds.add(question.id);
        queue.push(tagQuestionForPlaylist(question, segment));
        added++;
    }
    return added;
}

function playlistPartsFor(flow, preset, limit) {
    const third = Math.max(1, Math.round(limit * 0.33));
    const quarter = Math.max(1, Math.round(limit * 0.25));

    if (flow === "tutor") {
        return [{ preset: "random", count: limit, segment: playlistSegment("random", {
            label: "Quiz-studio",
            detail: "Ogni domanda sblocca una spiegazione compatta."
        }) }];
    }

    if (flow === "sprint_recover") {
        return [
            { preset: "weak", count: Math.max(3, Math.round(limit * 0.7)), segment: playlistSegment("weak") },
            { preset: "due", count: Math.max(1, Math.round(limit * 0.2)), segment: playlistSegment("due") },
            { preset: "random", count: limit, segment: playlistSegment("random") }
        ];
    }

    if (flow === "sprint_boss") {
        return [
            { preset: "weak", count: Math.max(3, Math.round(limit * 0.45)), segment: playlistSegment("weak", {
                label: "Boss: deboli",
                detail: "Prima gli argomenti che possono toglierti punti."
            }) },
            { preset: "due", count: Math.max(2, Math.round(limit * 0.25)), segment: playlistSegment("due", {
                label: "Boss: scadute",
                detail: "Poi controllo le domande che vanno richiamate oggi."
            }) },
            { preset: "random", count: limit, segment: playlistSegment("random", {
                label: "Boss finale",
                detail: "Chiusura mista senza schema, come all'esame."
            }) }
        ];
    }

    if (flow === "sprint_combo") {
        return [
            { preset: "easy", count: Math.max(3, Math.round(limit * 0.75)), segment: playlistSegment("easy", {
                label: "Combo",
                detail: "Serie rapide per consolidare sicurezza."
            }) },
            { preset: "random", count: limit, segment: playlistSegment("random") }
        ];
    }

    if (flow === "sprint_quick") {
        return [
            { preset: "weak", count: quarter, segment: playlistSegment("weak") },
            { preset: "new", count: third, segment: playlistSegment("new") },
            { preset: "random", count: limit, segment: playlistSegment("random") }
        ];
    }

    if (preset && preset !== "mixed") {
        return [
            { preset, count: Math.max(1, Math.round(limit * 0.75)), segment: playlistSegment(preset === "mastered" ? "easy" : preset) },
            { preset: "new", count: Math.max(1, Math.round(limit * 0.15)), segment: playlistSegment("new") },
            { preset: "random", count: limit, segment: playlistSegment("random") }
        ];
    }

    return [
        { preset: "weak", count: quarter, segment: playlistSegment("weak") },
        { preset: "due", count: quarter, segment: playlistSegment("due") },
        { preset: "new", count: third, segment: playlistSegment("new") },
        { preset: "random", count: limit, segment: playlistSegment("random") }
    ];
}

async function createDiscoveryPlaylist(limit, topicContext = {}) {
    const queue = [];
    const seenIds = new Set();
    const topicId = topicContext?.id || "";
    const fresh = await fetchReviewQuestionsForPlaylist("new", limit, topicId);
    fresh.forEach((question, index) => {
        if (seenIds.has(question.id)) return;
        seenIds.add(question.id);
        const block = Math.floor(index / 10) + 1;
        queue.push(tagQuestionForPlaylist(question, playlistSegment("new", {
            key: `new-${block}`,
            label: `Scoperta ${block}`,
            detail: "Blocchi da 10 domande nuove, poi si cambia ritmo.",
            baseKey: "new"
        })));
    });

    if (queue.length < limit) {
        const filler = await fetchReviewQuestionsForPlaylist("random", limit - queue.length, topicId);
        appendUniquePlaylistQuestions(queue, seenIds, filler, playlistSegment("random", {
            label: "Misto di rinforzo",
            detail: "Ho finito le nuove disponibili: chiudiamo con controllo misto."
        }), limit - queue.length);
    }

    return {
        title: topicContext?.label ? `Scoperta: ${topicContext.label}` : "Scoperta nuove domande",
        flow: "new",
        preset: "new",
        topicId,
        topicLabel: topicContext?.label || "",
        questions: queue,
        segments: summarizePlaylistSegments(queue),
        targetCount: limit
    };
}

async function createLearnNewPlaylist(limit, topicContext = {}) {
    const requestedNewCount = Math.max(1, limit);
    const topicId = topicContext?.id || "";
    const fresh = await fetchReviewQuestionsForPlaylist("new", requestedNewCount, topicId);
    const queue = [];
    const seenIds = new Set();

    fresh.forEach((question) => {
        if (seenIds.has(question.id)) return;
        seenIds.add(question.id);
        const learnQuestionNumber = seenIds.size;
        queue.push(tagQuestionForPlaylist(question, playlistSegment("learn_preview", {
            key: "learn-preview",
            label: "Studio",
            detail: "Leggi risposta corretta, perche ed esempio.",
            baseKey: "learn_preview"
        }), { learnStage: "preview", learnQuestionNumber }));
        queue.push(tagQuestionForPlaylist(question, playlistSegment("new", {
            key: "learn-quiz",
            label: "Quiz",
            detail: "Ora rispondi subito alla stessa domanda.",
            baseKey: "new"
        }), { learnStage: "quiz", learnQuestionNumber }));
    });

    if (!queue.length) {
        return createDiscoveryPlaylist(limit, topicContext);
    }

    const newQuestionCount = seenIds.size;
    return {
        title: topicContext?.label
            ? `Impara ${newQuestionCount}: ${topicContext.label}`
            : `Impara nuove: ${newQuestionCount}`,
        flow: "learn_new",
        preset: "new",
        topicId,
        topicLabel: topicContext?.label || "",
        newQuestionCount,
        totalSteps: queue.length,
        requestedNewCount,
        questions: queue,
        segments: summarizePlaylistSegments(queue),
        targetCount: newQuestionCount
    };
}

async function createStudyPlaylist(flow, preset, limit, topicContext = {}) {
    const safeLimit = clampInt(limit, 1, 300, 30);
    const topicId = topicContext?.id || "";
    if (flow === "learn_new") {
        return createLearnNewPlaylist(safeLimit, topicContext);
    }
    if (flow === "new" || preset === "new") {
        return createDiscoveryPlaylist(safeLimit, topicContext);
    }

    const queue = [];
    const seenIds = new Set();
    const parts = playlistPartsFor(flow, preset, safeLimit);

    for (const part of parts) {
        if (queue.length >= safeLimit) break;
        const needed = Math.min(part.count, safeLimit - queue.length);
        const questions = await fetchReviewQuestionsForPlaylist(part.preset, Math.max(needed + 8, needed), topicId);
        appendUniquePlaylistQuestions(queue, seenIds, questions, part.segment, needed);
    }

    if (queue.length < safeLimit) {
        const filler = await fetchReviewQuestionsForPlaylist("random", safeLimit - queue.length, topicId);
        appendUniquePlaylistQuestions(queue, seenIds, filler, playlistSegment("random"), safeLimit - queue.length);
    }

    return {
        title: topicContext?.label
            ? `Quiz mirato: ${topicContext.label}`
            : flow?.startsWith("sprint_")
                ? "Sfida breve"
                : "Playlist intelligente",
        flow,
        preset,
        topicId,
        topicLabel: topicContext?.label || "",
        questions: queue,
        segments: summarizePlaylistSegments(queue),
        targetCount: safeLimit
    };
}

function summarizePlaylistSegments(questions) {
    const map = new Map();
    (questions || []).forEach((question) => {
        const segment = question._playlistSegment || playlistSegment("random");
        const key = segment.key || "random";
        if (!map.has(key)) {
            map.set(key, { ...segment, count: 0 });
        }
        map.get(key).count += 1;
    });
    return Array.from(map.values());
}

function createPlaylistRun(playlist, savedRun = null) {
    return {
        startedAt: savedRun?.startedAt || Date.now(),
        answered: safeNumber(savedRun?.answered, 0),
        correct: safeNumber(savedRun?.correct, 0),
        wrong: safeNumber(savedRun?.wrong, 0),
        recovered: safeNumber(savedRun?.recovered, 0),
        retriesScheduled: safeNumber(savedRun?.retriesScheduled, 0),
        newSeen: safeNumber(savedRun?.newSeen, 0),
        title: playlist?.title || "Sessione"
    };
}

function playlistStatePayload() {
    if (!activePlaylist || !studyQuestions.length) return null;
    return {
        title: activePlaylist.title,
        flow: activePlaylist.flow,
        preset: activePlaylist.preset,
        topic_id: activePlaylist.topicId || "",
        topic_label: activePlaylist.topicLabel || "",
        new_question_count: activePlaylist.newQuestionCount || 0,
        total_steps: activePlaylist.totalSteps || studyQuestions.length,
        requested_new_count: activePlaylist.requestedNewCount || 0,
        targetCount: activePlaylist.targetCount,
        segments: activePlaylist.segments || summarizePlaylistSegments(studyQuestions),
        run: playlistRun,
        items: studyQuestions.map((question) => ({
            id: question.id,
            segment: question._playlistSegment || null,
            is_recovery: Boolean(question._isRecovery),
            retry_count: safeNumber(question._retryCount, 0),
            learn_stage: question._learnStage || "",
            learn_question_number: safeNumber(question._learnQuestionNumber, 0)
        }))
    };
}

function restorePlaylistState(state, questions) {
    if (!state || !questions?.length) {
        activePlaylist = null;
        playlistRun = null;
        renderPlaylistPanel();
        return;
    }

    const items = Array.isArray(state.items) ? state.items : [];
    questions.forEach((question, index) => {
        const item = items[index];
        if (item && Number(item.id) === Number(question.id)) {
            question._playlistSegment = item.segment || playlistSegment("random");
            question._isRecovery = Boolean(item.is_recovery);
            question._retryCount = safeNumber(item.retry_count, 0);
            question._learnStage = item.learn_stage || "";
            question._learnQuestionNumber = safeNumber(item.learn_question_number, 0);
        } else {
            question._playlistSegment = playlistSegment("random");
            question._learnStage = "";
            question._learnQuestionNumber = 0;
        }
    });

    activePlaylist = {
        title: state.title || "Sessione salvata",
        flow: state.flow || "saved",
        preset: state.preset || "mixed",
        topicId: state.topicId || state.topic_id || "",
        topicLabel: state.topicLabel || state.topic_label || "",
        newQuestionCount: safeNumber(state.newQuestionCount || state.new_question_count, 0),
        totalSteps: safeNumber(state.totalSteps || state.total_steps, questions.length),
        requestedNewCount: safeNumber(state.requestedNewCount || state.requested_new_count, 0),
        targetCount: safeNumber(state.targetCount, questions.length),
        segments: Array.isArray(state.segments) && state.segments.length
            ? state.segments
            : summarizePlaylistSegments(questions)
    };
    playlistRun = createPlaylistRun(activePlaylist, state.run);
    renderPlaylistPanel();
}

function clearActivePlaylist() {
    activePlaylist = null;
    playlistRun = null;
    renderPlaylistPanel();
}

function updatePlaylistRun(isCorrect, question) {
    if (!activePlaylist) return;
    if (!playlistRun) playlistRun = createPlaylistRun(activePlaylist);
    playlistRun.answered += 1;
    if (isCorrect) playlistRun.correct += 1;
    else playlistRun.wrong += 1;
    const segmentKey = question?._playlistSegment?.baseKey || question?._playlistSegment?.key;
    if (segmentKey === "new") playlistRun.newSeen += 1;
    if (question?._isRecovery && isCorrect) playlistRun.recovered += 1;
}

function scheduleRecoveryQuestion(question) {
    if (!isStudyMode() || !studyQuestions.length || !question) return false;
    const retryCount = safeNumber(question._retryCount, 0);
    if (retryCount >= 2) return false;

    const alreadyQueued = studyQuestions
        .slice(studyIndex + 1)
        .some((item) => Number(item.id) === Number(question.id) && item._isRecovery);
    if (alreadyQueued) return false;

    const retryQuestion = tagQuestionForPlaylist(
        question,
        playlistSegment("retry"),
        { isRecovery: true, retryCount: retryCount + 1, learnStage: "" }
    );
    const insertAt = Math.min(studyQuestions.length, studyIndex + 4);
    studyQuestions.splice(insertAt, 0, retryQuestion);

    if (playlistRun) playlistRun.retriesScheduled += 1;
    if (activePlaylist) activePlaylist.segments = summarizePlaylistSegments(studyQuestions);
    updateProgress();
    renderPlaylistPanel();
    return true;
}

function playlistAnswerMessage(isCorrect, question) {
    if (!activePlaylist || !question) return "";
    if (question._isRecovery && isCorrect) {
        return " Errore recuperato.";
    }
    if (question._isRecovery && !isCorrect) {
        return " Non e ancora chiusa: la rivediamo con calma.";
    }
    const key = question._playlistSegment?.baseKey || question._playlistSegment?.key;
    if (!isCorrect && isStudyMode()) {
        return " Te la ripropongo tra poco.";
    }
    if (isCorrect && key === "new") {
        return " Nuova domanda agganciata.";
    }
    return "";
}

function renderPlaylistPanel() {
    const panel = document.getElementById("playlistPanel");
    if (!panel) return;
    const phase = document.getElementById("playlistPhase");
    const detail = document.getElementById("playlistDetail");
    const pills = document.getElementById("playlistPills");

    if (!activePlaylist || !isStudyMode() || !studyQuestions.length) {
        panel.style.display = "none";
        if (pills) pills.innerHTML = "";
        return;
    }

    const question = studyQuestions[studyIndex] || {};
    const segment = question._playlistSegment || activePlaylist.segments?.[0] || playlistSegment("random");
    const remaining = Math.max(0, studyQuestions.length - studyIndex - 1);

    panel.style.display = "grid";
    if (phase) phase.textContent = activePlaylist.title || "Sessione";
    if (detail) {
        if (activePlaylist.flow === "learn_new") {
            const totalNew = safeNumber(activePlaylist.newQuestionCount, Math.ceil(studyQuestions.length / 2));
            const questionNumber = safeNumber(question._learnQuestionNumber, Math.ceil((studyIndex + 1) / 2));
            const stage = question._learnStage === "preview" ? "Studio" : "Quiz";
            detail.textContent = `${stage} ${questionNumber}/${totalNew}: ${segment.detail || ""} · passaggio ${studyIndex + 1}/${studyQuestions.length}`;
        } else {
            detail.textContent = `${segment.label || "Blocco"}: ${segment.detail || ""} ${remaining ? `(${remaining} dopo questa)` : "(ultima)"}`;
        }
    }

    if (!pills) return;
    pills.innerHTML = "";
    (activePlaylist.segments || summarizePlaylistSegments(studyQuestions)).forEach((item) => {
        const pill = document.createElement("span");
        pill.className = `playlist-pill tone-${item.tone || "neutral"}`;
        if (item.key === segment.key) pill.classList.add("active");
        pill.textContent = `${item.label || "Blocco"} ${item.count || 0}`;
        pills.appendChild(pill);
    });
}

function appendSummaryStat(parent, label, value) {
    const item = document.createElement("div");
    const small = document.createElement("small");
    const strong = document.createElement("strong");
    small.textContent = label;
    strong.textContent = value;
    item.appendChild(small);
    item.appendChild(strong);
    parent.appendChild(item);
}

function showStudyCompletionSummary() {
    const summary = document.getElementById("examSummary");
    if (!summary) return;

    const total = correctCount + incorrectCount;
    const accuracy = total > 0 ? Math.round((correctCount / total) * 100) : 0;
    const recovered = safeNumber(playlistRun?.recovered, 0);
    const newSeen = safeNumber(playlistRun?.newSeen, 0);
    const retries = safeNumber(playlistRun?.retriesScheduled, 0);

    summary.className = "exam-summary study-complete-summary";
    summary.innerHTML = "";

    const title = document.createElement("h2");
    title.textContent = "Sessione chiusa";
    summary.appendChild(title);

    const subtitle = document.createElement("p");
    subtitle.textContent = incorrectCount > 0
        ? "Hai materiale fresco da recuperare: conviene fare un giro breve sugli errori."
        : "Pulita. Puoi scoprire nuove domande o chiudere qui con una pausa.";
    summary.appendChild(subtitle);

    const stats = document.createElement("div");
    stats.className = "study-summary-grid";
    appendSummaryStat(stats, "Risposte", String(total));
    appendSummaryStat(stats, "Accuratezza", `${accuracy}%`);
    appendSummaryStat(stats, "Nuove viste", String(newSeen));
    appendSummaryStat(stats, "Errori recuperati", String(recovered));
    appendSummaryStat(stats, "Ritentativi creati", String(retries));
    summary.appendChild(stats);

    const actions = document.createElement("div");
    actions.className = "study-summary-actions";

    const recoverBtn = document.createElement("button");
    recoverBtn.type = "button";
    recoverBtn.className = "btn primary";
    recoverBtn.textContent = incorrectCount > 0 ? "Recupera errori ora" : "Ripasso intelligente";
    recoverBtn.addEventListener("click", async () => {
        setMode("review");
        setReviewFlow(incorrectCount > 0 ? "sprint_recover" : "smart");
        setReviewCount(incorrectCount > 0 ? Math.min(20, Math.max(6, incorrectCount * 2)) : 15);
        await startReviewMode();
    });
    actions.appendChild(recoverBtn);

    const newBtn = document.createElement("button");
    newBtn.type = "button";
    newBtn.className = "btn ghost";
    newBtn.textContent = "Scopri 10 nuove";
    newBtn.addEventListener("click", async () => {
        setMode("review");
        setReviewFlow("new");
        setReviewCount(10);
        await startReviewMode();
    });
    actions.appendChild(newBtn);

    summary.appendChild(actions);
    summary.style.display = "block";
    summary.scrollIntoView({ behavior: "smooth", block: "nearest" });
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

function updateProgress() {
    const wrapper = document.getElementById("progressBarWrapper");
    const label = document.getElementById("progressLabel");
    const fill = document.getElementById("progressFill");
    if (!wrapper || !label || !fill) return;

    if (isExamMode && examQuestions.length) {
        wrapper.style.display = "block";
        label.innerText = `Domanda ${examIndex + 1}/${examQuestions.length}`;
        fill.style.width = `${Math.round(((examIndex + 1) / examQuestions.length) * 100)}%`;
        return;
    }

    if (isStudyMode() && studyQuestions.length) {
        wrapper.style.display = "block";
        if (activePlaylist?.flow === "learn_new") {
            const question = studyQuestions[studyIndex] || {};
            const totalNew = safeNumber(activePlaylist.newQuestionCount, Math.ceil(studyQuestions.length / 2));
            const questionNumber = safeNumber(question._learnQuestionNumber, Math.ceil((studyIndex + 1) / 2));
            const stage = question._learnStage === "preview" ? "Studio" : "Quiz";
            label.innerText = `${stage} nuova ${questionNumber}/${totalNew} - passaggio ${studyIndex + 1}/${studyQuestions.length}`;
        } else {
            label.innerText = `Domanda ${studyIndex + 1}/${studyQuestions.length}`;
        }
        fill.style.width = `${Math.round(((studyIndex + 1) / studyQuestions.length) * 100)}%`;
        return;
    }

    wrapper.style.display = "none";
}

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
        if (idx === examIndex) btn.classList.add("current");
        if (examAnswers[idx] != null) btn.classList.add("answered");
        btn.onclick = () => {
            examIndex = idx;
            renderExamQuestion();
        };
        list.appendChild(btn);
    });
}

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
        timerDisplay.innerText = `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;

        if (examTimeRemaining <= 0) {
            stopExamTimer();
            if (!examFinished && isExamMode) finishExam();
        } else {
            examTimeRemaining--;
        }
    }

    update();
    examTimerId = setInterval(update, 1000);
}

function applyCardAnimation() {
    const card = document.querySelector(".question-card");
    if (!card) return;
    card.classList.remove("fade-in");
    void card.offsetWidth;
    card.classList.add("fade-in");
}

function updateQuestionProgressBadge(progress) {
    const badge = document.getElementById("questionProgress");
    if (!badge) return;

    badge.className = "progress-badge";
    if (!progress) {
        badge.innerText = "Stato: -";
        return;
    }

    const status = progress.status || "new";
    badge.classList.add(`status-${status}`);
    badge.innerText = STATUS_LABELS[status] || status;
}

function decodeQuestionText(value) {
    return String(value || "")
        .replace(/&nbsp;/gi, " ")
        .replace(/\u00a0/g, " ")
        .replace(/&lt;br\s*\/?&gt;/gi, "\n")
        .replace(/<br\s*\/?\s*>/gi, "\n")
        .replace(/\r\n/g, "\n")
        .replace(/\r/g, "\n")
        .split("\n")
        .map((line) => line.replace(/[ \t]+$/g, ""))
        .join("\n")
        .trim();
}

function looksLikeCodeLine(line) {
    const trimmed = line.trim();
    if (!trimmed) return false;
    return /^(if|elif|else|for|while|def|class|try|except|finally|with|print|return|import|from|[A-Za-z_]\w*\s*=)/.test(trimmed)
        || /^[A-Za-z_]\w*\([^)]*\)\s*(->|:|=)/.test(trimmed)
        || (/[:=(){}\[\];]/.test(trimmed) && /\b(print|range|len|input|self|True|False|None)\b/.test(trimmed));
}

function splitInlineCodeLine(line) {
    const trimmed = line.trim();
    const lower = trimmed.toLowerCase();
    const italianPrefix = /^(in python|il codice|se dal codice|nel codice|nell'istruzione|nella funzione|nell'ambito)/;
    if (looksLikeCodeLine(trimmed) && !italianPrefix.test(lower)) {
        return { intro: "", code: trimmed };
    }

    const markers = ["istruzione", "istruzioni", "funzione", "blocco di istruzioni", "codice"];
    for (const marker of markers) {
        const index = lower.indexOf(marker);
        if (index === -1) continue;
        const afterMarker = index + marker.length;
        const tail = trimmed.slice(afterMarker).replace(/^[:\s]+/, "");
        if (looksLikeCodeLine(tail)) {
            return {
                intro: trimmed.slice(0, afterMarker).replace(/[:\s]+$/, ""),
                code: tail
            };
        }
    }

    const match = trimmed.match(/\b(if|elif|else|for|while|def|class|print|return|[A-Za-z_]\w*\s*=)/);
    if (match) {
        const tail = trimmed.slice(match.index).trim();
        if (looksLikeCodeLine(tail)) {
            return {
                intro: trimmed.slice(0, match.index).replace(/[:\s]+$/, ""),
                code: tail
            };
        }
    }

    return { intro: trimmed, code: "" };
}

function appendFormattedText(parent, value, paragraphTag = "p") {
    const text = decodeQuestionText(value);
    if (!text) return;

    const lines = text.split("\n");
    const introLines = [];
    const codeLines = [];
    let inCode = false;
    let expectCodeAfterIntro = false;

    lines.forEach((line) => {
        const rawLine = line.replace(/\t/g, "    ");
        const cleaned = rawLine.trim();
        if (!cleaned) return;
        const isEndingText = /^(visualizza|produce|risulta|serve|quale|e:|e'|è)/i.test(cleaned);
        const splitLine = splitInlineCodeLine(cleaned);
        if (splitLine.code) {
            if (splitLine.intro) introLines.push(splitLine.intro);
            inCode = true;
            expectCodeAfterIntro = false;
            codeLines.push(rawLine.startsWith(cleaned) ? splitLine.code : rawLine.replace(cleaned, splitLine.code));
        } else if ((inCode || expectCodeAfterIntro) && !isEndingText && (/[:=(){}\[\];]/.test(cleaned) || looksLikeCodeLine(cleaned))) {
            inCode = true;
            expectCodeAfterIntro = false;
            codeLines.push(rawLine);
        } else {
            inCode = false;
            expectCodeAfterIntro = /^(il codice|codice|dato il codice|considera il codice|nel codice|programma|frammento)/i.test(cleaned);
            introLines.push(splitLine.intro || cleaned);
        }
    });

    if (!codeLines.length) {
        const p = document.createElement(paragraphTag);
        p.textContent = text;
        parent.appendChild(p);
        return;
    }

    if (introLines.length) {
        const p = document.createElement(paragraphTag);
        p.textContent = introLines.join(" ");
        parent.appendChild(p);
    }

    const pre = document.createElement("pre");
    pre.className = "code-question";
    const code = document.createElement("code");
    code.textContent = normalizeCodeIndent(codeLines).join("\n");
    pre.appendChild(code);
    parent.appendChild(pre);
}

function normalizeCodeIndent(lines) {
    const useful = lines.filter((line) => line.trim());
    if (!useful.length) return [];
    const minIndent = Math.min(
        ...useful.map((line) => {
            const match = line.match(/^\s*/);
            return match ? match[0].length : 0;
        })
    );
    return lines.map((line) => line.slice(minIndent));
}

function shouldUseRecallGate(question, forExam) {
    return false;
}

function hideRecallGate() {
    const gate = document.getElementById("recallGate");
    const answersList = document.getElementById("risposte");
    if (gate) gate.style.display = "none";
    if (answersList) answersList.style.display = "";
}

function showAnswerOptions() {
    const gate = document.getElementById("recallGate");
    const answersList = document.getElementById("risposte");
    if (gate) gate.style.display = "none";
    if (answersList) {
        answersList.style.display = "";
        answersList.classList.add("answers-revealed");
    }
}

function renderRecallGate(question, forExam) {
    const gate = document.getElementById("recallGate");
    const answersList = document.getElementById("risposte");
    const button = document.getElementById("showOptionsBtn");
    const title = document.getElementById("recallGateTitle");
    const text = document.getElementById("recallGateText");
    if (!gate || !answersList) return;

    answersList.classList.remove("answers-revealed");
    if (!shouldUseRecallGate(question, forExam)) {
        hideRecallGate();
        return;
    }

    if (title) title.textContent = question?._isRecovery ? "Ripasso errore" : "Quiz rapido";
    if (text) {
        text.textContent = question?._isRecovery
            ? "Rispondi subito: se sbagli, te la rimetto nel giro."
            : "Risposte visibili subito: scegli e vai avanti.";
    }
    if (button) {
        button.textContent = "Mostra opzioni";
        button.onclick = showAnswerOptions;
    }
    answersList.style.display = "none";
    gate.style.display = "block";
}

function renderQuestionPayload(question, forExam) {
    activeQuestion = question;
    const domandaIdEl = document.getElementById("domanda-id");
    const domandaText = document.getElementById("domanda");
    const answersList = document.getElementById("risposte");
    const resultEl = document.getElementById("result");

    if (domandaIdEl) domandaIdEl.innerText = `ID Domanda: ${question.id}`;
    updateQuestionProgressBadge(question.progress);
    hideStudyPanel();

    if (domandaText) {
        domandaText.innerHTML = "";
        if (question.immagine) {
            const img = document.createElement("img");
            img.src = `data:image/jpeg;base64,${question.immagine}`;
            img.alt = "Immagine della domanda";
            domandaText.appendChild(img);
        }
        if (question.testo) {
            appendFormattedText(domandaText, question.testo);
        }
    }

    if (answersList) answersList.innerHTML = "";
    if (resultEl) resultEl.innerText = "";
    if (!answersList) return;

    shuffleArray(question.risposte.slice()).forEach((risposta) => {
        const li = document.createElement("li");
        const container = document.createElement("div");

        if (risposta.immagine) {
            const img = document.createElement("img");
            img.src = `data:image/jpeg;base64,${risposta.immagine}`;
            img.alt = "Immagine risposta";
            container.appendChild(img);
        }

        if (risposta.testo) {
            appendFormattedText(container, risposta.testo, "span");
        }

        li.appendChild(container);
        li.dataset.answerId = risposta.id;
        li.onclick = forExam
            ? () => selectExamAnswer(li, risposta.id)
            : () => checkAnswerTraining(li, risposta.id, question.corretta);
        answersList.appendChild(li);
    });

    renderRecallGate(question, forExam);
    applyCardAnimation();
}

async function getTrainingQuestion() {
    const question = await fetchJson(`/api/question/${currentQuestionIndex}`);
    hasAnsweredCurrent = false;
    hideExamSummary();
    renderExamSidebar();
    updateProgress();
    stopExamTimer();

    if (!question || question.error) {
        resetQuestionShell("Domanda non trovata.");
        return;
    }

    renderQuestionPayload(question, false);
    showNavButtons();
}

function currentAttemptMode() {
    if (isSavedQuiz) return "saved";
    if (mode === "plan") return "plan";
    if (mode === "review") return attemptModeFromReviewFlow();
    if (mode === "daily") return "daily";
    if (mode === "tutor") return "tutor";
    if (mode === "sprint") return "sprint";
    return "training";
}

async function recordAttempt(questionId, selectedId, correctId, attemptMode, silent = false, errorReason = null) {
    const rating = selectedId === correctId ? "know" : "dont_know";
    const data = await fetchJson("/api/attempt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            question_id: questionId,
            selected_answer_id: selectedId,
            mode: attemptMode,
            self_rating: rating,
            error_reason: errorReason
        })
    });

    if (!data) return null;

    if (!silent && activeQuestion && activeQuestion.id === questionId) {
        activeQuestion.progress = data.progress;
        updateQuestionProgressBadge(data.progress);
        if (attemptMode === "tutor" || !data.is_correct) {
            await loadStudyNote(questionId, selectedId);
        }
    }

    await loadProgressSummary();
    return data;
}

function askErrorReason() {
    const result = document.getElementById("result");
    if (!result) return Promise.resolve(null);
    const reasons = [
        ["confused_concept", "Concetto confuso"],
        ["distraction", "Distrazione"],
        ["forgot_definition", "Definizione"],
        ["calculation", "Calcolo"]
    ];
    const wrap = document.createElement("div");
    wrap.className = "error-reason-panel";
    const label = document.createElement("span");
    label.textContent = "Perche l'hai sbagliata?";
    wrap.appendChild(label);

    return new Promise((resolve) => {
        let done = false;
        const finish = (value) => {
            if (done) return;
            done = true;
            wrap.remove();
            resolve(value);
        };
        reasons.forEach(([value, text]) => {
            const btn = document.createElement("button");
            btn.type = "button";
            btn.textContent = text;
            btn.addEventListener("click", () => finish(value));
            wrap.appendChild(btn);
        });
        result.appendChild(wrap);
        setTimeout(() => finish(null), 6500);
    });
}

async function checkAnswerTraining(selectedLi, selectedId, correctId) {
    const result = document.getElementById("result");

    if (hasAnsweredCurrent || !activeQuestion) return;
    const questionAtAnswer = activeQuestion;
    hasAnsweredCurrent = true;

    const allLis = document.querySelectorAll(".answer-list li");
    allLis.forEach((li) => li.classList.remove("selected", "correct", "wrong"));

    answeredCount++;
    const isCorrect = selectedId === correctId;
    const earnedXp = awardAnswerXp(isCorrect, questionAtAnswer);
    updatePlaylistRun(isCorrect, questionAtAnswer);
    if (selectedId === correctId) {
        selectedLi.classList.add("selected", "correct");
        correctCount++;
    } else {
        selectedLi.classList.add("selected", "wrong");
        incorrectCount++;
    }
    applyAnswerRhythm(isCorrect);

    if (result) {
        const comboSuffix = comboCount >= 3 ? ` Combo ${comboCount}.` : "";
        result.innerText = `${randomFeedback(isCorrect)}${playlistAnswerMessage(isCorrect, questionAtAnswer)} +${earnedXp} XP.${comboSuffix}`;
    }

    const correctLi = Array.from(allLis).find(
        (li) => Number(li.dataset.answerId) === Number(correctId)
    );
    if (correctLi) correctLi.classList.add("correct");

    setText("correctCount", correctCount);
    setText("incorrectCount", incorrectCount);
    updateSessionStats();
    showNavButtons();

    try {
        const attemptMode = currentAttemptMode();
        const errorReason = !isCorrect && attemptMode === "training" ? await askErrorReason() : null;
        await recordAttempt(questionAtAnswer.id, selectedId, correctId, attemptMode, false, errorReason);
        if (!isCorrect) {
            scheduleRecoveryQuestion(questionAtAnswer);
        }
        renderPlaylistPanel();
        saveCurrentStudySession(true);
    } catch (err) {
        console.warn(err);
    }
}

function showConfidencePanel() {
    const panel = document.getElementById("confidencePanel");
    if (panel) panel.style.display = "block";
}

function hideStudyPanel() {
    const panel = document.getElementById("studyPanel");
    const confidence = document.getElementById("confidencePanel");
    if (panel) {
        panel.style.display = "none";
        panel.innerHTML = "";
        panel.classList.remove("learn-study-panel");
    }
    if (confidence) confidence.style.display = "none";
}

async function submitConfidence(rating) {
    if (!activeQuestion) return;
    try {
        const data = await fetchJson("/api/confidence", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                question_id: activeQuestion.id,
                self_rating: rating
            })
        });
        if (data && data.progress) {
            activeQuestion.progress = data.progress;
            updateQuestionProgressBadge(data.progress);
            await loadProgressSummary();
            saveCurrentStudySession();
        }
    } catch (err) {
        alert(err.message);
    }
}

function appendPythonLab(parent, lab) {
    if (!lab) return;

    const wrap = document.createElement("section");
    wrap.className = `python-lab python-lab-${lab.status || "ok"}`;

    const header = document.createElement("div");
    header.className = "python-lab-header";

    const title = document.createElement("h4");
    title.textContent = "Laboratorio Python";

    const status = document.createElement("span");
    status.className = "lab-status";
    status.textContent =
        lab.status === "ok"
            ? "Esegue"
            : lab.status === "error"
                ? "Errore"
                : lab.status === "timeout"
                    ? "Timeout"
                    : "Bloccato";

    header.appendChild(title);
    header.appendChild(status);
    wrap.appendChild(header);

    if (lab.label) {
        const label = document.createElement("p");
        label.className = "lab-label";
        label.textContent = lab.label;
        wrap.appendChild(label);
    }

    const codePre = document.createElement("pre");
    codePre.className = "code-question lab-code";
    const codeEl = document.createElement("code");
    codeEl.textContent = lab.code || "";
    codePre.appendChild(codeEl);
    wrap.appendChild(codePre);

    if (lab.setup) {
        const setup = document.createElement("p");
        setup.className = "lab-setup";
        setup.textContent = `Per provarlo uso valori di esempio: ${lab.setup.replace(/\n/g, "; ")}`;
        wrap.appendChild(setup);
    }

    if (lab.stdout) {
        const output = document.createElement("div");
        output.className = "lab-run";
        const outputTitle = document.createElement("strong");
        outputTitle.textContent = "Output";
        const outputPre = document.createElement("pre");
        outputPre.textContent = lab.stdout;
        output.appendChild(outputTitle);
        output.appendChild(outputPre);
        wrap.appendChild(output);
    }

    if (lab.stderr) {
        const error = document.createElement("div");
        error.className = "lab-run lab-error";
        const errorTitle = document.createElement("strong");
        errorTitle.textContent = "Errore Python";
        const errorPre = document.createElement("pre");
        errorPre.textContent = lab.stderr;
        error.appendChild(errorTitle);
        error.appendChild(errorPre);
        wrap.appendChild(error);
    }

    const explanation = document.createElement("p");
    explanation.className = "lab-explanation";
    explanation.textContent = lab.explanation || "Questo e il comportamento reale del frammento quando Python prova a eseguirlo.";
    wrap.appendChild(explanation);

    parent.appendChild(wrap);
}

function appendActiveExplanationPrompt(parent) {
    const wrap = document.createElement("section");
    wrap.className = "active-explanation";

    const title = document.createElement("strong");
    title.textContent = "Richiamo attivo";
    const text = document.createElement("p");
    text.textContent = "Spiegala in una frase con parole tue. Non viene valutata: serve a fissarla.";
    const textarea = document.createElement("textarea");
    textarea.rows = 2;
    textarea.placeholder = "Es. perche la parola chiave della domanda indica...";
    const button = document.createElement("button");
    button.type = "button";
    button.className = "btn small-btn ghost";
    button.textContent = "Ho fissato il concetto";
    const feedback = document.createElement("small");
    button.addEventListener("click", () => {
        feedback.textContent = textarea.value.trim()
            ? "Bene: spiegata con parole tue."
            : "Ok, ma la prossima volta prova a scriverla: resta molto di piu.";
    });

    wrap.appendChild(title);
    wrap.appendChild(text);
    wrap.appendChild(textarea);
    wrap.appendChild(button);
    wrap.appendChild(feedback);
    parent.appendChild(wrap);
}

function sourcePageLabel(source) {
    if (!source) return "";
    if (source.page_start && source.page_end && source.page_start !== source.page_end) {
        return `pp. ${source.page_start}-${source.page_end}`;
    }
    if (source.page_start) return `p. ${source.page_start}`;
    return "";
}

function appendExpandableSourceNote(parent, source) {
    if (!source) return;

    const item = document.createElement("article");
    item.className = "source-note";

    const meta = document.createElement("strong");
    const page = sourcePageLabel(source);
    meta.textContent = `${source.topic || "Fonte collegata"}${page ? ` - ${page}` : ""}`;
    item.appendChild(meta);

    if (source.source_title) {
        const origin = document.createElement("small");
        origin.textContent = source.source_title;
        item.appendChild(origin);
    }

    const excerptText = source.excerpt || "";
    const fullText = (source.full_text || "").trim();
    const hasFullText = fullText && fullText.length > excerptText.length + 20;

    const excerpt = document.createElement("p");
    excerpt.textContent = excerptText || fullText || "";
    item.appendChild(excerpt);

    if (hasFullText) {
        const full = document.createElement("p");
        full.className = "source-note-full";
        full.textContent = fullText;
        full.hidden = true;

        const toggle = document.createElement("button");
        toggle.type = "button";
        toggle.className = "source-note-toggle";
        toggle.textContent = "Mostra tutto";
        toggle.addEventListener("click", () => {
            const expanded = full.hidden;
            full.hidden = !expanded;
            excerpt.hidden = expanded;
            toggle.textContent = expanded ? "Mostra meno" : "Mostra tutto";
        });

        item.appendChild(full);
        item.appendChild(toggle);
    }

    parent.appendChild(item);
}

async function loadStudyNote(questionId, selectedAnswerId = null) {
    const panel = document.getElementById("studyPanel");
    if (!panel) return;

    const params = new URLSearchParams();
    if (selectedAnswerId) params.set("selected_answer_id", selectedAnswerId);
    const suffix = params.toString() ? `?${params.toString()}` : "";
    const note = await fetchJson(`/api/study_note/${questionId}${suffix}`);
    if (!note) return;

    panel.innerHTML = "";
    panel.classList.remove("learn-study-panel");
    const title = document.createElement("h3");
    title.textContent = "Spiegazione rapida";
    panel.appendChild(title);

    const sections = [];
    if (note.mistake) {
        sections.push(["Dove hai sbagliato", note.mistake]);
    }
    sections.push(
        ["Perche", note.why || note.focus || ""],
        ["Trucchetto", note.memory_tip || note.hint || ""]
    );
    sections.forEach(([label, value]) => {
        const block = document.createElement("div");
        block.className = "study-answer compact-explanation";
        const blockLabel = document.createElement("strong");
        blockLabel.textContent = label;
        const body = document.createElement("div");
        appendFormattedText(body, value || "-");
        block.appendChild(blockLabel);
        block.appendChild(body);
        panel.appendChild(block);
    });

    appendPythonLab(panel, note.python_lab);
    appendActiveExplanationPrompt(panel);

    if (note.source_notes && note.source_notes.length) {
        const source = note.source_notes[0];
        const sourceWrap = document.createElement("div");
        sourceWrap.className = "source-notes";
        const sourceTitle = document.createElement("h4");
        sourceTitle.textContent = note.python_lab ? "Dalla dispensa" : "Fonte collegata";
        sourceWrap.appendChild(sourceTitle);
        appendExpandableSourceNote(sourceWrap, source);

        panel.appendChild(sourceWrap);
    }

    panel.style.display = "block";
}

function appendStudyText(parent, value) {
    const body = document.createElement("div");
    body.className = "learn-study-text";
    appendFormattedText(body, value || "-");
    parent.appendChild(body);
}

async function loadLearnPreviewNote(questionId) {
    const panel = document.getElementById("studyPanel");
    if (!panel) return;

    const note = await fetchJson(`/api/study_note/${questionId}`);
    if (!note) return;

    panel.innerHTML = "";
    panel.classList.add("learn-study-panel");

    const head = document.createElement("div");
    head.className = "learn-study-head";
    const title = document.createElement("h3");
    title.textContent = "Prima aggancia la risposta";
    const badge = document.createElement("span");
    badge.textContent = "Nuova";
    head.appendChild(title);
    head.appendChild(badge);
    panel.appendChild(head);

    const answer = document.createElement("section");
    answer.className = "learn-correct-answer";
    const answerLabel = document.createElement("strong");
    answerLabel.textContent = "Risposta corretta";
    answer.appendChild(answerLabel);
    appendStudyText(answer, note.correct_text || "");
    panel.appendChild(answer);

    const grid = document.createElement("div");
    grid.className = "learn-study-grid";
    [
        ["Perche", note.why || note.focus || ""],
        ["Esempio", note.example || ""],
        ["Trucchetto", note.memory_tip || note.hint || ""]
    ].forEach(([label, value]) => {
        const block = document.createElement("section");
        block.className = "learn-study-block";
        const blockLabel = document.createElement("strong");
        blockLabel.textContent = label;
        block.appendChild(blockLabel);
        appendStudyText(block, value || "-");
        grid.appendChild(block);
    });
    panel.appendChild(grid);

    appendPythonLab(panel, note.python_lab);
    panel.style.display = "block";
}

async function prepareLearnPreview(question) {
    const answersList = document.getElementById("risposte");
    const result = document.getElementById("result");
    const gate = document.getElementById("recallGate");
    if (answersList) answersList.style.display = "none";
    if (gate) {
        const title = document.getElementById("recallGateTitle");
        const text = document.getElementById("recallGateText");
        const button = document.getElementById("showOptionsBtn");
        if (title) title.textContent = "Leggi, aggancia, rispondi";
        if (text) {
            text.textContent = "Guarda la corretta e il trucchetto. Poi premi il bottone: subito dopo fai il quiz sulla stessa domanda.";
        }
        if (button) {
            button.textContent = "Fai il quiz";
            button.onclick = nextQuestion;
        }
        gate.style.display = "block";
    }
    if (result) result.textContent = "";
    await loadLearnPreviewNote(question.id);
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function startTrainingMode() {
    mode = "training";
    isExamMode = false;
    isSavedQuiz = false;
    clearActivePlaylist();

    hideExamSummary();
    stopExamTimer();
    studyQuestions = [];
    studyIndex = 0;

    const startingQuestion = document.getElementById("startingQuestion").value || "1";
    currentQuestionIndex = parseInt(startingQuestion, 10);

    getTrainingQuestion();
    showNavButtons();
    saveCurrentStudySession(true);
    scrollToStudySurface();
}

async function startDailyMode() {
    setReviewFlow("new");
    await startReviewMode();
}

async function fetchStudyPlan() {
    const examDate = document.getElementById("examDate")?.value || "";
    const minutes = document.getElementById("studyMinutes")?.value || "45";
    const targetGrade = document.getElementById("targetGrade")?.value || "24";
    const params = new URLSearchParams();
    if (examDate) params.set("exam_date", examDate);
    params.set("minutes", minutes);
    params.set("target_grade", targetGrade);
    return fetchJson(`/api/study_plan?${params.toString()}`);
}

function isPastDate(value) {
    if (!value) return false;
    const selected = new Date(`${value}T00:00:00`);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return selected < today;
}

function formatItalianDate(value) {
    if (!value) return "-";
    const date = new Date(`${value}T00:00:00`);
    if (Number.isNaN(date.getTime())) return value;
    return date.toLocaleDateString("it-IT", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric"
    });
}

function renderPlanPreview(plan) {
    const preview = document.getElementById("planPreview");
    if (!preview || !plan) return;
    const forecast = plan.forecast || {};
    const projectedGrade = forecast.grade_projected?.label || "-";
    const currentGrade = forecast.grade_now?.label || "-";
    const feasibilityClass = plan.feasible ? "plan-ok" : "plan-risk";
    const targetClass = forecast.target_reached ? "plan-ok" : "plan-risk";
    const missingLine = plan.feasible
        ? ""
        : `<span>Mancano circa ${plan.missing_minutes} min totali (${plan.missing_daily_minutes} min/giorno in piu).</span>`;
    preview.innerHTML = `
        <strong>Da oggi (${formatItalianDate(plan.today)}) all'esame: ${plan.days_left} giorni</strong>
        <span>Ritmo impostato: ${plan.minutes} min/giorno = circa ${plan.capacity} domande/giorno.</span>
        <span>Carico stimato: ${plan.total_work} passaggi. Capacita fino all'esame: ${plan.total_capacity} passaggi.</span>
        <span class="${feasibilityClass}">${plan.feasibility_label}</span>
        <span class="${targetClass}">${forecast.target_label || ""}</span>
        ${missingLine}
        <div class="plan-metrics">
            <div><small>Voto obiettivo</small><strong>${forecast.target_grade ?? 24}/30</strong></div>
            <div><small>Voto stimato ora</small><strong>${currentGrade}</strong></div>
            <div><small>Seguendo il piano</small><strong>${projectedGrade}</strong></div>
            <div><small>Copertura prevista</small><strong>${forecast.coverage_projected ?? 0}%</strong></div>
        </div>
        <strong>Oggi: ${plan.new_today} nuove + ${plan.review_today} ripasso</strong>
        <span>${plan.total_today} domande - circa ${plan.estimated_minutes} min.</span>
    `;
}

async function refreshStudyPlan() {
    const dbSelect = document.getElementById("dbSelect");
    const preview = document.getElementById("planPreview");
    const examDate = document.getElementById("examDate")?.value || "";
    if (dbSelect && !dbSelect.value) {
        if (preview) preview.textContent = "Scegli una materia per calcolare il piano.";
        return null;
    }
    if (isPastDate(examDate)) {
        if (preview) preview.textContent = "La data esame e gia passata. Inserisci una data futura.";
        return null;
    }
    try {
        const plan = await fetchStudyPlan();
        renderPlanPreview(plan);
        saveCurrentStudySession();
        return plan;
    } catch (err) {
        console.warn(err);
        if (preview) preview.textContent = "Non riesco a calcolare il piano adesso.";
        return null;
    }
}

function queuePlanRefresh() {
    clearTimeout(planRefreshTimer);
    planRefreshTimer = setTimeout(async () => {
        await refreshStudyPlan();
        saveCurrentStudySession();
    }, 350);
}

async function startPlanMode() {
    mode = "plan";
    isExamMode = false;
    isSavedQuiz = false;
    hideExamSummary();
    renderExamSidebar();
    stopExamTimer();
    resetSession();

    const plan = await refreshStudyPlan();
    if (!plan || plan.total_today <= 0) {
        alert("Non ci sono domande da mettere nel piano di oggi.");
        return;
    }

    const dueData = plan.review_today > 0
        ? await fetchJson(`/api/review_questions?mode=due&limit=${plan.review_today}`)
        : { questions: [] };
    const weakNeeded = Math.max(plan.review_today - (dueData?.questions?.length || 0), 0);
    const weakData = weakNeeded > 0
        ? await fetchJson(`/api/review_questions?mode=weak&limit=${weakNeeded}`)
        : { questions: [] };
    const newData = plan.new_today > 0
        ? await fetchJson(`/api/review_questions?mode=new&limit=${plan.new_today}`)
        : { questions: [] };

    const seenIds = new Set();
    studyQuestions = [];
    [
        [dueData.questions || [], playlistSegment("due")],
        [weakData.questions || [], playlistSegment("weak")],
        [newData.questions || [], playlistSegment("new")]
    ].forEach(([questions, segment]) => {
        questions.forEach((q) => {
            if (!seenIds.has(q.id)) {
                seenIds.add(q.id);
                studyQuestions.push(tagQuestionForPlaylist(q, segment));
            }
        });
    });

    if (!studyQuestions.length) {
        alert("Il piano non ha trovato domande disponibili.");
        return;
    }

    activePlaylist = {
        title: "Piano di oggi",
        flow: "plan",
        preset: "plan",
        targetCount: studyQuestions.length,
        segments: summarizePlaylistSegments(studyQuestions)
    };
    playlistRun = createPlaylistRun(activePlaylist);
    studyIndex = 0;
    renderStudyQuestion();
    showNavButtons();
    saveCurrentStudySession(true);
    setAnalysisVisible(false);
    scrollToStudySurface();
}

async function startReviewMode(topicContext = activeReviewTopic || {}) {
    const flow = document.getElementById("reviewFlow")?.value || "smart";
    const config = REVIEW_FLOW_CONFIG[flow] || REVIEW_FLOW_CONFIG.smart;
    const preset = config.preset || document.getElementById("reviewPreset")?.value || "mixed";
    const started = await startStudyQueue("review", preset, "reviewQuestionCount", flow, topicContext);
    if (!started) return;
    const result = document.getElementById("result");
    if (result) {
        result.innerText = topicContext?.label
            ? `${config.label} avviato su ${topicContext.label}.`
            : `${config.label} avviato.`;
    }
}

async function startTutorMode() {
    setReviewFlow("tutor");
    await startReviewMode();
}

async function startSprintMode() {
    const type = document.getElementById("sprintType")?.value || "quick";
    const flow = {
        quick: "sprint_quick",
        recover: "sprint_recover",
        boss: "sprint_boss",
        combo: "sprint_combo"
    }[type] || "sprint_quick";
    setReviewFlow(flow);
    await startReviewMode();
}

async function startStudyQueue(nextMode, preset, countInputId, flow = "smart", topicContext = {}) {
    mode = nextMode;
    isExamMode = false;
    isSavedQuiz = false;
    hideExamSummary();
    renderExamSidebar();
    stopExamTimer();
    resetSession();

    let limit = parseInt(document.getElementById(countInputId)?.value || "30", 10);
    if (Number.isNaN(limit) || limit <= 0) limit = 30;

    activePlaylist = await createStudyPlaylist(flow, preset, limit, topicContext);
    studyQuestions = activePlaylist?.questions || [];
    activePlaylist.segments = summarizePlaylistSegments(studyQuestions);
    playlistRun = createPlaylistRun(activePlaylist);
    studyIndex = 0;

    if (!studyQuestions.length) {
        const label = REVIEW_LABELS[preset] || "domande";
        alert(`Nessuna domanda disponibile per: ${label}.`);
        resetQuestionShell("Non ci sono domande in questa coda.");
        clearActivePlaylist();
        updateProgress();
        return false;
    }

    renderStudyQuestion();
    showNavButtons();
    saveCurrentStudySession(true);
    setAnalysisVisible(false);
    scrollToStudySurface();
    return true;
}

function renderStudyQuestion() {
    const question = studyQuestions[studyIndex];
    if (!question) return;

    hasAnsweredCurrent = false;
    renderQuestionPayload(question, false);
    updateProgress();
    renderPlaylistPanel();
    if (question._learnStage === "preview") {
        prepareLearnPreview(question).catch((err) => console.warn(err));
    }
}

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
        if (!Number.isNaN(parsed) && parsed > 0) limit = parsed;
    }

    examQuestions = await fetchJson(`/api/random_questions?limit=${limit}`);
    if (!Array.isArray(examQuestions) || examQuestions.length === 0) {
        alert("Non e stato possibile caricare le domande casuali.");
        isExamMode = false;
        return;
    }

    examIndex = 0;
    examAnswers = new Array(examQuestions.length).fill(null);

    const timerEnabled = document.getElementById("examTimerEnabled").checked;
    if (timerEnabled) {
        let minutes = parseInt(document.getElementById("examTimerMinutes").value, 10);
        if (Number.isNaN(minutes) || minutes <= 0) minutes = 30;
        startExamTimer(minutes * 60);
    } else {
        stopExamTimer();
    }

    renderExamQuestion();
    showNavButtons();
    saveCurrentStudySession(true);
}

function renderExamQuestion() {
    const question = examQuestions[examIndex];
    if (!question) return;

    renderQuestionPayload(question, true);
    renderExamSidebar();
    updateProgress();
    setText("result", "");
}

function selectExamAnswer(selectedLi, answerId) {
    const allLis = document.querySelectorAll(".answer-list li");
    allLis.forEach((li) => li.classList.remove("selected", "correct", "wrong"));

    selectedLi.classList.add("selected");
    examAnswers[examIndex] = answerId;
    renderExamSidebar();
}

async function finishExam() {
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

    const attemptPromises = [];

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

        if (isCorrect) localCorrect++;
        else localWrong++;

        if (chosenId != null) {
            attemptPromises.push(recordAttempt(q.id, chosenId, correctId, "exam", true));
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

    const total = localCorrect + localWrong;
    const score30 = total > 0 ? Math.floor((localCorrect / total) * 30) : 0;
    const elapsedSec = examStartTimestamp
        ? Math.round((Date.now() - examStartTimestamp) / 1000)
        : 0;
    const mm = String(Math.floor(elapsedSec / 60)).padStart(2, "0");
    const ss = String(elapsedSec % 60).padStart(2, "0");

    const overview = document.createElement("div");
    overview.className = "exam-overview";
    if (total > 0) {
        if (score30 < 18) overview.classList.add("perf-bad");
        else if (score30 <= 24) overview.classList.add("perf-medium");
        else overview.classList.add("perf-good");
    }

    overview.innerHTML = `
        <div class="exam-overview-main">
            Punteggio: <strong>${total === 0 ? "-/30" : `${score30}/30`}</strong>
        </div>
        <div class="exam-overview-sub">
            Corrette: <strong>${localCorrect}</strong> -
            Errate: <strong>${localWrong}</strong> -
            Tempo: <strong>${mm}:${ss}</strong>
        </div>
    `;

    summary.insertBefore(overview, title.nextSibling);
    summary.style.display = "block";

    correctCount = localCorrect;
    incorrectCount = localWrong;
    answeredCount = localCorrect + localWrong;
    setText("correctCount", correctCount);
    setText("incorrectCount", incorrectCount);
    updateSessionStats();
    summary.scrollIntoView({ behavior: "smooth" });

    const list = document.getElementById("examQuestionList");
    if (list) {
        const items = list.querySelectorAll(".sidebar-item");
        items.forEach((el, idx) => {
            const chosenId = examAnswers[idx];
            const correctId = examQuestions[idx].corretta;
            if (chosenId === correctId) el.classList.add("answered");
            else el.classList.add("wrong");
        });
    }

    await Promise.allSettled(attemptPromises);
    await loadProgressSummary();
    saveCurrentStudySession(true);
}

function nextQuestion() {
    if (mode === "exam" && isExamMode) {
        if (examIndex < examQuestions.length - 1) {
            examIndex++;
            renderExamQuestion();
            saveCurrentStudySession();
        } else if (!examFinished) {
            finishExam();
        }
        return;
    }

    if (isStudyMode()) {
        if (studyIndex < studyQuestions.length - 1) {
            studyIndex++;
            renderStudyQuestion();
            saveCurrentStudySession();
        } else {
            showStudyCompletionSummary();
            loadProgressSummary();
            saveCurrentStudySession(true);
        }
        return;
    }

    if (isSavedQuiz) {
        if (currentQuestionIndex < savedQuestions.length - 1) {
            currentQuestionIndex++;
            loadSavedQuestion();
            saveCurrentStudySession();
        } else {
            alert("Hai completato il quiz delle domande salvate.");
            isSavedQuiz = false;
        }
    } else {
        currentQuestionIndex++;
        getTrainingQuestion();
        saveCurrentStudySession();
    }
    showNavButtons();
}

function prevQuestion() {
    if (mode === "exam" && isExamMode) {
        if (examIndex > 0) {
            examIndex--;
            renderExamQuestion();
            saveCurrentStudySession();
        }
        return;
    }

    if (isStudyMode()) {
        if (studyIndex > 0) {
            studyIndex--;
            renderStudyQuestion();
            saveCurrentStudySession();
        }
        return;
    }

    if (isSavedQuiz) {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            loadSavedQuestion();
            saveCurrentStudySession();
        }
    } else if (currentQuestionIndex > 1) {
        currentQuestionIndex--;
        getTrainingQuestion();
        saveCurrentStudySession();
    }
    showNavButtons();
}

async function saveQuestion() {
    if (mode === "exam" && isExamMode) {
        alert("Salvataggio non disponibile in modalita simulazione.");
        return;
    }

    if (!activeQuestion) {
        alert("Nessuna domanda da salvare.");
        return;
    }

    await fetchJson(`/api/save_question/${activeQuestion.id}`, { method: "POST" });
    savedQuestions = await fetchJson("/api/saved_questions");
    updateSavedCount();
    alert("Domanda salvata.");
}

async function startSavedQuiz() {
    if (mode === "exam" && isExamMode) {
        alert("Non puoi usare le domande salvate durante la simulazione.");
        return;
    }

    savedQuestions = await fetchJson("/api/saved_questions");
    updateSavedCount();

    if (!savedQuestions || savedQuestions.length === 0) {
        alert("Nessuna domanda salvata.");
        return;
    }

    isSavedQuiz = true;
    studyQuestions = [];
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
    setText("result", "");
}

async function clearSavedQuestions() {
    await fetchJson("/api/clear_saved_questions", { method: "DELETE" });
    savedQuestions = [];
    updateSavedCount();
    alert("Tutte le domande salvate sono state cancellate.");
}

async function removeSavedQuestion() {
    if (!activeQuestion) {
        alert("Nessuna domanda salvata da rimuovere.");
        return;
    }

    await fetchJson(`/api/remove_saved_question/${activeQuestion.id}`, { method: "DELETE" });
    savedQuestions = await fetchJson("/api/saved_questions");
    updateSavedCount();

    if (isSavedQuiz && savedQuestions.length === 0) {
        alert("Non ci sono piu domande salvate.");
        isSavedQuiz = false;
        currentQuestionIndex = 1;
    } else if (isSavedQuiz) {
        if (currentQuestionIndex >= savedQuestions.length) {
            currentQuestionIndex = savedQuestions.length - 1;
        }
        loadSavedQuestion();
    } else {
        alert("Domanda rimossa dalle salvate.");
    }
}

function setTutorialStatus(text, state = "") {
    const status = document.getElementById("tutorialRunStatus");
    if (!status) return;
    status.textContent = text;
    status.classList.remove("ok", "error");
    if (state) status.classList.add(state);
}

function updateTutorialProgress(progress) {
    if (!progress) return;
    tutorialProgress = progress;
    tutorialLessons = progress.lessons || tutorialLessons;
    setText("tutorialProgressText", `${progress.completed_count || 0}/${progress.total_count || 0}`);
    const fill = document.getElementById("tutorialProgressFill");
    if (fill) fill.style.width = `${progress.percent || 0}%`;
}

function renderTutorialLessonList() {
    const list = document.getElementById("tutorialLessonList");
    if (!list) return;
    list.innerHTML = "";

    tutorialLessons.forEach((lesson) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "tutorial-lesson-btn";
        btn.classList.toggle("active", activeTutorialLesson?.id === lesson.id);
        btn.classList.toggle("locked", Boolean(lesson.locked));
        btn.classList.toggle("completed", Boolean(lesson.completed));
        btn.disabled = Boolean(lesson.locked);
        btn.dataset.lessonId = lesson.id;

        const title = document.createElement("span");
        title.textContent = lesson.title;
        const meta = document.createElement("small");
        const state = lesson.completed ? "Completata" : lesson.locked ? "Bloccata" : "Disponibile";
        meta.textContent = `Python - ${lesson.module} - ${state}`;

        btn.appendChild(title);
        btn.appendChild(meta);
        btn.addEventListener("click", () => selectTutorialLesson(lesson.id));
        list.appendChild(btn);
    });
}

function renderTutorialLesson(lesson) {
    activeTutorialLesson = lesson;
    setText("tutorialModule", `Python - ${lesson.module || "Fondamenta"} - ${lesson.level || "base"}`);
    setText("tutorialTitle", lesson.title || "Tutorial Python");
    setText("tutorialGoal", lesson.goal || "");
    setText("tutorialConcept", lesson.concept || "");
    setText("tutorialTask", lesson.task || "");
    const hint = document.getElementById("tutorialHint");
    if (hint) {
        hint.textContent = lesson.hint || "";
        hint.style.display = "none";
    }

    const editor = document.getElementById("tutorialEditor");
    if (editor) editor.value = lesson.code || lesson.starter_code || "";

    const outputPanel = document.getElementById("tutorialOutputPanel");
    if (outputPanel) outputPanel.style.display = "none";
    const checks = document.getElementById("tutorialChecks");
    if (checks) checks.innerHTML = "";
    setText("tutorialOutput", "");
    setTutorialStatus(lesson.completed ? "Completata" : "Pronto", lesson.completed ? "ok" : "");

    const nextBtn = document.getElementById("nextTutorialLessonBtn");
    if (nextBtn) nextBtn.disabled = !lesson.completed;

    renderTutorialLessonList();
}

function isTutorialHelpCommand(value) {
    return String(value || "").trim().toLowerCase() === "aiuto";
}

function showTutorialHelp() {
    const hint = document.getElementById("tutorialHint");
    if (!hint || !activeTutorialLesson) return;
    hint.textContent = activeTutorialLesson.hint || "Rileggi consegna e concetto: manca solo un passaggio piccolo.";
    hint.style.display = "block";
    setTutorialStatus("Aiuto mostrato", "");
}

async function loadPythonTutorial() {
    const data = await fetchJson("/api/python_tutorial");
    if (!data) return;
    updateTutorialProgress(data);
    renderTutorialLessonList();
    const activeId = data.active_lesson_id || tutorialLessons.find((lesson) => !lesson.locked)?.id;
    if (activeId) {
        await selectTutorialLesson(activeId);
    }
}

async function selectTutorialLesson(lessonId) {
    const data = await fetchJson(`/api/python_tutorial/${lessonId}`);
    if (!data) return;
    if (data.progress) updateTutorialProgress(data.progress);
    renderTutorialLesson(data.lesson);
}

function renderTutorialResult(payload) {
    const outputPanel = document.getElementById("tutorialOutputPanel");
    const output = document.getElementById("tutorialOutput");
    const checksWrap = document.getElementById("tutorialChecks");
    const result = payload?.result || {};

    if (outputPanel) outputPanel.style.display = "block";
    if (output) {
        const parts = [];
        if (result.error_info) {
            const line = result.error_info.line ? ` alla riga ${result.error_info.line}` : "";
            parts.push(`Errore Python${line}: ${result.error_info.type} - ${result.error_info.message}`);
        }
        if (result.stdout) parts.push(result.stdout.trimEnd());
        if (result.error) parts.push(result.error.trimEnd());
        output.textContent = parts.join("\n\n") || "Nessun output stampato.";
    }

    if (checksWrap) {
        checksWrap.innerHTML = "";
        (result.checks || []).forEach((check) => {
            const row = document.createElement("div");
            row.className = `tutorial-check ${check.passed ? "passed" : "failed"}`;

            const label = document.createElement("strong");
            label.textContent = check.label || "Controllo";
            const mark = document.createElement("span");
            mark.textContent = check.passed ? "OK" : "Da correggere";

            row.appendChild(label);
            row.appendChild(mark);
            if (!check.passed) {
                const detail = document.createElement("small");
                const details = [];
                if (check.feedback) details.push(check.feedback);
                if (check.expected !== undefined) details.push(`Atteso: ${formatCheckValue(check.expected)}`);
                if (check.actual !== undefined) details.push(`Ottenuto: ${formatCheckValue(check.actual)}`);
                if (check.detail) details.push(check.detail);
                detail.textContent = details.join(" | ");
                row.appendChild(detail);
            }
            checksWrap.appendChild(row);
        });

        if (result.retry_message) {
            const retry = document.createElement("div");
            retry.className = `tutorial-retry ${result.success ? "passed" : "failed"}`;
            retry.textContent = result.retry_message;
            checksWrap.appendChild(retry);
        }
    }

    if (result.success) {
        setTutorialStatus("Completata", "ok");
        if (payload.progress) updateTutorialProgress(payload.progress);
        if (payload.lesson) activeTutorialLesson = payload.lesson;
        renderTutorialLessonList();
        const nextBtn = document.getElementById("nextTutorialLessonBtn");
        if (nextBtn) nextBtn.disabled = !payload.next_lesson;
    } else {
        setTutorialStatus(result.blocked ? "Bloccato" : "Da correggere", "error");
    }
}

function formatCheckValue(value) {
    if (value === null) return "null";
    if (value === undefined) return "non definito";
    if (typeof value === "string") return value.replace(/\n/g, "\\n");
    return JSON.stringify(value);
}

async function saveActiveTutorialCode() {
    if (!activeTutorialLesson) return;
    const editor = document.getElementById("tutorialEditor");
    if (!editor) return;
    try {
        await fetchJson(`/api/python_tutorial/${activeTutorialLesson.id}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code: editor.value })
        });
    } catch (err) {
        console.warn(err);
    }
}

function queueTutorialCodeSave() {
    const editor = document.getElementById("tutorialEditor");
    if (editor && isTutorialHelpCommand(editor.value)) {
        showTutorialHelp();
        return;
    }
    clearTimeout(tutorialSaveTimer);
    tutorialSaveTimer = setTimeout(saveActiveTutorialCode, 700);
}

async function runTutorialCode() {
    if (!activeTutorialLesson) return;
    const editor = document.getElementById("tutorialEditor");
    if (!editor) return;

    if (isTutorialHelpCommand(editor.value)) {
        showTutorialHelp();
        const outputPanel = document.getElementById("tutorialOutputPanel");
        if (outputPanel) outputPanel.style.display = "none";
        return;
    }

    setTutorialStatus("Esecuzione...", "");
    try {
        const data = await fetchJson("/api/python_tutorial/run", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                lesson_id: activeTutorialLesson.id,
                code: editor.value
            })
        });
        renderTutorialResult(data);
    } catch (err) {
        setTutorialStatus("Errore", "error");
        const outputPanel = document.getElementById("tutorialOutputPanel");
        if (outputPanel) outputPanel.style.display = "block";
        setText("tutorialOutput", err.message);
    }
}

function resetTutorialCode() {
    if (!activeTutorialLesson) return;
    const editor = document.getElementById("tutorialEditor");
    if (editor) editor.value = activeTutorialLesson.starter_code || "";
    setTutorialStatus("Ripristinato", "");
    queueTutorialCodeSave();
}

async function openNextTutorialLesson() {
    if (!activeTutorialLesson) return;
    const currentIndex = tutorialLessons.findIndex((lesson) => lesson.id === activeTutorialLesson.id);
    const next = tutorialLessons[currentIndex + 1];
    if (next && !next.locked) {
        await selectTutorialLesson(next.id);
    }
}

async function resetPythonTutorial() {
    const ok = window.confirm("Azzerare il progresso del tutorial Python?");
    if (!ok) return;
    const data = await fetchJson("/api/python_tutorial", { method: "DELETE" });
    if (!data) return;
    updateTutorialProgress(data);
    await loadPythonTutorial();
}

async function startTutorialMode() {
    await loadPythonTutorial();
}

function populateArchitectureTopics(topics = []) {
    const select = document.getElementById("architectureTopic");
    if (!select || !topics.length) return;
    const current = select.value || "mixed";
    select.innerHTML = "";
    topics.forEach((topic) => {
        const option = document.createElement("option");
        option.value = topic.id;
        option.textContent = topic.label;
        select.appendChild(option);
    });
    select.value = topics.some((topic) => topic.id === current) ? current : "mixed";
    renderArchitectureTopicChips();
}

function renderArchitectureTopicChips() {
    const wrap = document.getElementById("architectureTopicChips");
    const select = document.getElementById("architectureTopic");
    if (!wrap || !select) return;

    const topics = architecturePractice?.topics || Array.from(select.options).map((option) => ({
        id: option.value,
        label: option.textContent
    }));
    const active = select.value || "mixed";
    wrap.innerHTML = "";

    topics.forEach((topic) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "architecture-topic-chip";
        button.classList.toggle("active", topic.id === active);
        button.dataset.topic = topic.id;
        button.textContent = topic.label;
        button.setAttribute("aria-pressed", topic.id === active ? "true" : "false");
        button.addEventListener("click", () => setArchitectureTopic(topic.id, true));
        wrap.appendChild(button);
    });
}

async function setArchitectureTopic(topicId, generateNow = false) {
    const select = document.getElementById("architectureTopic");
    if (!select) return;
    select.value = topicId || "mixed";
    renderArchitectureTopicChips();
    saveCurrentStudySession();
    if (generateNow) {
        await fetchArchitectureExercise();
    }
}

function updateArchitectureStats(stats) {
    if (!stats) return;
    setText("architectureAccuracy", `${stats.accuracy || 0}%`);
    setText("architectureAttempts", `${stats.attempts || 0} esercizi svolti`);
    setText(
        "architectureStatsMini",
        `Architettura dei Calcolatori: ${stats.attempts || 0} esercizi - accuratezza ${stats.accuracy || 0}%`
    );

    const wrap = document.getElementById("architectureTopicStats");
    if (!wrap) return;
    wrap.innerHTML = "";
    const topics = architecturePractice?.topics || [];
    topics
        .filter((topic) => topic.id !== "mixed")
        .forEach((topic) => {
            const item = stats.by_topic?.[topic.id] || { attempts: 0, accuracy: 0 };
            const row = document.createElement("div");
            row.className = "architecture-topic-row";

            const label = document.createElement("span");
            label.textContent = topic.label;
            const score = document.createElement("strong");
            score.textContent = item.attempts ? `${item.accuracy}%` : "-";
            const count = document.createElement("small");
            count.textContent = `${item.attempts || 0}x`;

            row.appendChild(label);
            row.appendChild(score);
            row.appendChild(count);
            wrap.appendChild(row);
        });
}

function updateArchitectureSourceSummary(summary) {
    const wrap = document.getElementById("architectureSourcesMini");
    if (!wrap) return;
    if (!summary || !summary.note_count) {
        wrap.textContent = "Video non ancora collegati.";
        return;
    }
    const lessons = summary.lesson_count || 0;
    const notes = summary.note_count || 0;
    wrap.textContent = `${lessons} lezioni video collegate - ${notes} estratti pronti`;
}

async function loadArchitecturePractice() {
    const data = await fetchJson("/api/architecture_practice");
    if (!data) return null;
    architecturePractice = data;
    populateArchitectureTopics(data.topics || []);
    updateArchitectureStats(data.stats);
    updateArchitectureSourceSummary(data.source_summary);
    return data;
}

function renderArchitectureExercise(exercise) {
    activeArchitectureExercise = exercise;
    selectedArchitectureOption = "";

    const title = document.getElementById("architectureTitle");
    const topic = document.getElementById("architectureTopicLabel");
    const hint = document.getElementById("architectureHint");
    const prompt = document.getElementById("architecturePrompt");
    const guide = document.getElementById("architectureGuide");
    const example = document.getElementById("architectureExample");
    const options = document.getElementById("architectureOptions");
    const selectionStatus = document.getElementById("architectureSelectionStatus");
    const answer = document.getElementById("architectureAnswer");
    const result = document.getElementById("architectureResult");

    if (title) title.textContent = exercise.title || "Esercizio";
    if (topic) topic.textContent = exercise.topic_label || "Architettura";
    if (hint) hint.textContent = exercise.hint || "Risolvi e poi verifica.";

    if (prompt) {
        prompt.innerHTML = "";
        appendFormattedText(prompt, exercise.prompt || "Esercizio pronto.");
    }

    if (guide) {
        guide.innerHTML = "";
        const guideTitle = document.createElement("h3");
        guideTitle.textContent = "Come si fa da zero";
        guide.appendChild(guideTitle);

        const guideList = document.createElement("ol");
        (exercise.guide || []).forEach((step) => {
            const item = document.createElement("li");
            item.textContent = step;
            guideList.appendChild(item);
        });
        guide.appendChild(guideList);
    }

    if (example) {
        example.innerHTML = "";
        const exampleData = exercise.example || {};
        const exampleTitle = document.createElement("h3");
        exampleTitle.textContent = exampleData.title || "Esempio guidato";
        example.appendChild(exampleTitle);

        const exampleList = document.createElement("ol");
        (exampleData.lines || []).forEach((line) => {
            const item = document.createElement("li");
            item.textContent = line;
            exampleList.appendChild(item);
        });
        example.appendChild(exampleList);
        example.style.display = (exampleData.lines || []).length ? "block" : "none";
    }

    if (options) {
        options.innerHTML = "";
        (exercise.options || []).forEach((optionText) => {
            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = "architecture-option";
            btn.textContent = optionText;
            btn.dataset.value = optionText;
            btn.setAttribute("aria-pressed", "false");
            options.appendChild(btn);
        });
        options.style.display = exercise.answer_type === "choice" ? "grid" : "none";
    }

    if (selectionStatus) {
        selectionStatus.textContent = exercise.answer_type === "choice"
            ? "Tocca una risposta per selezionarla."
            : "";
        selectionStatus.style.display = exercise.answer_type === "choice" ? "block" : "none";
    }

    if (answer) {
        answer.value = "";
        answer.placeholder = exercise.placeholder || "Scrivi la risposta";
        answer.style.display = exercise.answer_type === "choice" ? "none" : "block";
    }

    if (result) {
        result.style.display = "none";
        result.innerHTML = "";
        result.className = "architecture-result";
    }
}

function selectArchitectureOption(button, value) {
    selectedArchitectureOption = value;
    document.querySelectorAll(".architecture-option").forEach((item) => {
        item.classList.toggle("selected", item === button);
        item.classList.remove("correct", "wrong");
        item.setAttribute("aria-pressed", item === button ? "true" : "false");
    });
    const status = document.getElementById("architectureSelectionStatus");
    if (status) status.textContent = `Risposta selezionata: ${value}`;
}

function selectArchitectureOptionFromElement(target) {
    const button = target?.closest?.(".architecture-option");
    if (!button) return false;
    selectArchitectureOption(button, button.dataset.value || button.textContent.trim());
    return true;
}

async function fetchArchitectureExercise() {
    const topic = document.getElementById("architectureTopic")?.value || "mixed";
    const params = new URLSearchParams({ topic });
    const data = await fetchJson(`/api/architecture_exercise?${params.toString()}`);
    if (!data) return;
    if (data.stats) updateArchitectureStats(data.stats);
    renderArchitectureExercise(data.exercise);
    renderArchitectureTopicChips();
    saveCurrentStudySession(true);
}

async function startArchitectureMode() {
    mode = "architecture";
    isExamMode = false;
    isSavedQuiz = false;
    hideExamSummary();
    renderExamSidebar();
    stopExamTimer();
    resetSession();
    await loadArchitecturePractice();
    await fetchArchitectureExercise();
}

function architectureSubmittedAnswer() {
    if (!activeArchitectureExercise) return "";
    if (activeArchitectureExercise.answer_type === "choice") {
        return selectedArchitectureOption;
    }
    return document.getElementById("architectureAnswer")?.value || "";
}

function applyArchitectureAttempt(isCorrect) {
    answeredCount++;
    if (isCorrect) correctCount++;
    else incorrectCount++;
    sessionXp += isCorrect ? 14 : 5;
    applyAnswerRhythm(isCorrect);
    setText("correctCount", correctCount);
    setText("incorrectCount", incorrectCount);
    updateSessionStats();
    return isCorrect ? 14 : 5;
}

function markArchitectureOptions(payload) {
    document.querySelectorAll(".architecture-option").forEach((button) => {
        const value = button.dataset.value || "";
        button.classList.remove("correct", "wrong");
        if (value.toLowerCase() === String(payload.expected || "").toLowerCase()) {
            button.classList.add("correct");
        }
        if (!payload.is_correct && value === selectedArchitectureOption) {
            button.classList.add("wrong");
        }
    });
}

function renderArchitectureResult(payload, earnedXp) {
    const result = document.getElementById("architectureResult");
    if (!result) return;

    result.innerHTML = "";
    result.className = `architecture-result ${payload.is_correct ? "correct" : "wrong"}`;

    const title = document.createElement("h3");
    title.textContent = payload.is_correct
        ? `Giusto. +${earnedXp} XP`
        : `Da correggere. +${earnedXp} XP`;

    const compare = document.createElement("p");
    compare.textContent = payload.is_correct
        ? `Risposta: ${payload.expected}`
        : `Hai scritto: ${payload.submitted || "(vuoto)"} - Risposta attesa: ${payload.expected}`;

    const explanationTitle = document.createElement("strong");
    explanationTitle.textContent = "Spiegazione guidata";

    const explanation = document.createElement("p");
    explanation.className = "architecture-explanation";
    explanation.textContent = payload.explanation || "Leggi i passaggi sotto e riprova a ricostruire il ragionamento senza guardare.";

    const stepsTitle = document.createElement("strong");
    stepsTitle.textContent = "Passaggi della soluzione";

    const list = document.createElement("ol");
    (payload.steps || []).forEach((step) => {
        const item = document.createElement("li");
        item.textContent = step;
        list.appendChild(item);
    });

    const retry = document.createElement("p");
    retry.className = "architecture-retry";
    retry.textContent = payload.retry_message || "";

    const sources = document.createElement("div");
    sources.className = "source-notes architecture-video-notes";
    if (payload.source_notes && payload.source_notes.length) {
        const sourceTitle = document.createElement("h4");
        sourceTitle.textContent = "Dai video";
        sources.appendChild(sourceTitle);

        payload.source_notes.slice(0, 2).forEach((source) => {
            appendExpandableSourceNote(sources, source);
        });
    }

    result.appendChild(title);
    result.appendChild(compare);
    result.appendChild(explanationTitle);
    result.appendChild(explanation);
    result.appendChild(stepsTitle);
    result.appendChild(list);
    if (payload.source_notes && payload.source_notes.length) {
        result.appendChild(sources);
    }
    result.appendChild(retry);
    result.style.display = "block";
}

async function checkArchitectureAnswer() {
    if (!activeArchitectureExercise) {
        await fetchArchitectureExercise();
        return;
    }

    const answer = architectureSubmittedAnswer();
    if (!String(answer || "").trim()) {
        alert("Scrivi una risposta prima di verificare.");
        return;
    }

    const payload = await fetchJson("/api/architecture_exercise/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            exercise_id: activeArchitectureExercise.id,
            answer
        })
    });
    if (!payload) return;

    const earnedXp = applyArchitectureAttempt(payload.is_correct);
    if (payload.stats) updateArchitectureStats(payload.stats);
    markArchitectureOptions(payload);
    renderArchitectureResult(payload, earnedXp);
    saveCurrentStudySession(true);
}

async function startQuiz() {
    const dbSelect = document.getElementById("dbSelect");
    if (dbSelect?.value) {
        const hasProfile = await ensureSubjectProfile();
        if (!hasProfile) return;
    }

    if (mode === "tutorial") {
        startTutorialMode();
        return;
    }

    if (mode === "architecture") {
        startArchitectureMode();
        return;
    }

    if (dbSelect && !dbSelect.value) {
        alert("Seleziona una materia prima di iniziare.");
        return;
    }

    if (mode === "exam") startExamMode();
    else if (mode === "plan") startPlanMode();
    else if (mode === "daily") startDailyMode();
    else if (mode === "review") startReviewMode();
    else if (mode === "sprint") startSprintMode();
    else if (mode === "tutor") startTutorMode();
    else startTrainingMode();
}

function setMode(newMode) {
    newMode = resolveModeForCurrentSubject(newMode);
    mode = newMode;
    updateModeAvailability();
    updateMobileNav();

    document.querySelectorAll(".mode-tab").forEach((btn) => {
        btn.classList.toggle("active", btn.dataset.mode === newMode);
    });

    ["training", "plan", "daily", "review", "sprint", "tutor", "tutorial", "architecture", "exam"].forEach((name) => {
        const el = document.getElementById(`${name}Settings`);
        if (el) el.style.display = newMode === name ? "block" : "none";
    });
    updateReviewControls();

    const tutorialShell = document.getElementById("tutorialShell");
    const architectureShell = document.getElementById("architectureShell");
    const quizContent = document.getElementById("quizContent");
    if (tutorialShell) tutorialShell.style.display = newMode === "tutorial" ? "grid" : "none";
    if (architectureShell) architectureShell.style.display = newMode === "architecture" ? "grid" : "none";
    if (quizContent) quizContent.style.display = ["tutorial", "architecture"].includes(newMode) ? "none" : "flex";

    updateStartButtonCopy();

    if (newMode !== "exam") {
        isExamMode = false;
        examQuestions = [];
        examAnswers = [];
        renderExamSidebar();
        updateProgress();
        stopExamTimer();
    }

    hideExamSummary();

    if (!["plan", "daily", "review", "tutor", "sprint"].includes(newMode)) {
        clearActivePlaylist();
    }

    if (newMode === "plan") {
        refreshStudyPlan();
    }
    else if (newMode === "tutorial") {
        loadPythonTutorial().catch((err) => console.warn(err));
    }
    else if (newMode === "architecture") {
        loadArchitecturePractice().catch((err) => console.warn(err));
    }

    saveCurrentStudySession();
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

window.addEventListener("DOMContentLoaded", async () => {
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

    const reviewFlow = document.getElementById("reviewFlow");
    if (reviewFlow) {
        reviewFlow.addEventListener("change", () => {
            updateReviewControls();
            saveCurrentStudySession();
        });
    }

    const reviewPreset = document.getElementById("reviewPreset");
    if (reviewPreset) {
        reviewPreset.addEventListener("change", () => saveCurrentStudySession());
    }

    const reviewQuestionCount = document.getElementById("reviewQuestionCount");
    if (reviewQuestionCount) {
        reviewQuestionCount.addEventListener("change", () => saveCurrentStudySession());
    }

    const saveSessionBtn = document.getElementById("saveSessionBtn");
    if (saveSessionBtn) saveSessionBtn.onclick = () => saveCurrentStudySession(true);

    const refreshPlanBtn = document.getElementById("refreshPlanBtn");
    if (refreshPlanBtn) {
        refreshPlanBtn.onclick = async () => {
            await saveSubjectProfile({ silent: true });
            await refreshStudyPlan();
        };
    }

    const saveSubjectProfileBtn = document.getElementById("saveSubjectProfileBtn");
    if (saveSubjectProfileBtn) saveSubjectProfileBtn.onclick = () => saveSubjectProfile();

    const analysisToggleBtn = document.getElementById("analysisToggleBtn");
    if (analysisToggleBtn) {
        analysisToggleBtn.onclick = () => {
            const panel = document.getElementById("analysisPanel");
            setAnalysisVisible(panel?.hidden !== false);
        };
    }

    const closeAnalysisBtn = document.getElementById("closeAnalysisBtn");
    if (closeAnalysisBtn) closeAnalysisBtn.onclick = () => setAnalysisVisible(false);

    const recommendedBtn = document.getElementById("recommendedSessionBtn");
    if (recommendedBtn) recommendedBtn.onclick = startRecommendedSession;

    const learnNewBtn = document.getElementById("learnNewBtn");
    if (learnNewBtn) learnNewBtn.onclick = () => startLearnNewSession(12);

    const quickTenBtn = document.getElementById("quickTenBtn");
    if (quickTenBtn) quickTenBtn.onclick = startQuickTenSession;

    const diaryRecoverBtn = document.getElementById("diaryRecoverBtn");
    if (diaryRecoverBtn) diaryRecoverBtn.onclick = async () => {
        setMode("review");
        setReviewFlow("sprint_recover");
        setReviewCount(12);
        await startReviewMode();
    };

    const focusBtn = document.getElementById("focusSessionBtn");
    if (focusBtn) focusBtn.onclick = startFocusSession;

    document.querySelectorAll(".mobile-bottom-nav button").forEach((btn) => {
        btn.addEventListener("click", () => {
            const targetId = btn.dataset.mobileTarget;
            const nextMode = btn.dataset.mobileMode;
            if (nextMode) setMode(nextMode);
            if (targetId === "analysisPanel") {
                setAnalysisVisible(true);
            }
            const target = targetId
                ? document.getElementById(targetId) || document.querySelector(`.${targetId}`)
                : document.querySelector(".mode-section");
            if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
        });
    });

    ["onboardingExamDate", "onboardingStudyMinutes", "onboardingTargetGrade"].forEach((id) => {
        const field = document.getElementById(id);
        if (field) {
            field.addEventListener("keydown", (event) => {
                if (event.key === "Enter") {
                    event.preventDefault();
                    saveSubjectProfile();
                }
            });
        }
    });

    const examDate = document.getElementById("examDate");
    if (examDate) {
        examDate.addEventListener("input", queuePlanRefresh);
        examDate.addEventListener("change", async () => {
            await refreshStudyPlan();
            await saveSubjectProfile({ silent: true });
            saveCurrentStudySession();
        });
    }

    const studyMinutes = document.getElementById("studyMinutes");
    if (studyMinutes) {
        studyMinutes.addEventListener("input", queuePlanRefresh);
        studyMinutes.addEventListener("change", async () => {
            await refreshStudyPlan();
            await saveSubjectProfile({ silent: true });
            saveCurrentStudySession();
        });
    }

    const targetGrade = document.getElementById("targetGrade");
    if (targetGrade) {
        targetGrade.addEventListener("input", queuePlanRefresh);
        targetGrade.addEventListener("change", async () => {
            await refreshStudyPlan();
            await saveSubjectProfile({ silent: true });
            saveCurrentStudySession();
        });
    }

    const runTutorialBtn = document.getElementById("runTutorialBtn");
    if (runTutorialBtn) runTutorialBtn.onclick = runTutorialCode;

    const resetTutorialCodeBtn = document.getElementById("resetTutorialCodeBtn");
    if (resetTutorialCodeBtn) resetTutorialCodeBtn.onclick = resetTutorialCode;

    const nextTutorialLessonBtn = document.getElementById("nextTutorialLessonBtn");
    if (nextTutorialLessonBtn) nextTutorialLessonBtn.onclick = openNextTutorialLesson;

    const resetTutorialBtn = document.getElementById("resetTutorialBtn");
    if (resetTutorialBtn) resetTutorialBtn.onclick = resetPythonTutorial;

    const tutorialEditor = document.getElementById("tutorialEditor");
    if (tutorialEditor) tutorialEditor.addEventListener("input", queueTutorialCodeSave);

    const architectureTopic = document.getElementById("architectureTopic");
    if (architectureTopic) {
        architectureTopic.addEventListener("change", async () => {
            renderArchitectureTopicChips();
            if (mode === "architecture") {
                await fetchArchitectureExercise();
            } else {
                saveCurrentStudySession();
            }
        });
    }

    const architectureOptions = document.getElementById("architectureOptions");
    if (architectureOptions) {
        architectureOptions.addEventListener("click", (event) => {
            selectArchitectureOptionFromElement(event.target);
        });
        architectureOptions.addEventListener("pointerup", (event) => {
            selectArchitectureOptionFromElement(event.target);
        });
        architectureOptions.addEventListener("keydown", (event) => {
            if (event.key === "Enter" || event.key === " ") {
                if (selectArchitectureOptionFromElement(event.target)) {
                    event.preventDefault();
                }
            }
        });
    }

    const checkArchitectureBtn = document.getElementById("checkArchitectureBtn");
    if (checkArchitectureBtn) checkArchitectureBtn.onclick = checkArchitectureAnswer;

    const newArchitectureExerciseBtn = document.getElementById("newArchitectureExerciseBtn");
    if (newArchitectureExerciseBtn) newArchitectureExerciseBtn.onclick = fetchArchitectureExercise;

    const architectureAnswer = document.getElementById("architectureAnswer");
    if (architectureAnswer) {
        architectureAnswer.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                checkArchitectureAnswer();
            }
        });
    }

    const themeBtn = document.getElementById("themeToggle");
    if (themeBtn) themeBtn.onclick = toggleTheme;

    document.querySelectorAll(".mode-tab").forEach((btn) => {
        btn.addEventListener("click", () => setMode(btn.dataset.mode));
    });

    document.querySelectorAll("[data-confidence]").forEach((btn) => {
        btn.addEventListener("click", () => submitConfidence(btn.dataset.confidence));
    });

    const nextBtn = document.getElementById("nextBtn");
    const prevBtn = document.getElementById("prevBtn");
    if (nextBtn) nextBtn.style.display = "none";
    if (prevBtn) prevBtn.style.display = "none";

    updateSavedCount();
    updateSessionStats();
    isRestoringSession = true;
    updatePlayStats();
    renderExamSidebar();
    updateProgress();
    isRestoringSession = false;

    await restoreSavedStudySession();
    if (document.getElementById("dbSelect")?.value) {
        await loadSubjectProfile({ showSetup: true });
    }

    window.addEventListener("beforeunload", () => {
        saveCurrentStudySession(true, true);
    });
});
