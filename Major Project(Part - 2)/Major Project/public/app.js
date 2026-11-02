// IndicHealth AI Frontend JavaScript Client

// Global DOM State & Elements
const authModal = document.getElementById("auth-modal");
const authModalBtn = document.getElementById("auth-modal-btn");
const closeAuthModalBtn = document.getElementById("close-auth-modal");
const authForm = document.getElementById("auth-form");
const authModalTitle = document.getElementById("auth-modal-title");
const registerNameField = document.getElementById("register-name-field");
const authNameInput = document.getElementById("auth-name");
const authEmailInput = document.getElementById("auth-email");
const authPasswordInput = document.getElementById("auth-password");
const authSubmitBtn = document.getElementById("auth-submit-btn");
const authToggleBtn = document.getElementById("auth-toggle-btn");
const authErrorMsg = document.getElementById("auth-error-msg");
const userChip = document.getElementById("user-chip");
const userInitial = document.getElementById("user-initial");
const userName = document.getElementById("user-name");

// Navigation & Views
const navButtons = document.querySelectorAll(".nav-button");
const pageViews = document.querySelectorAll(".page-view");

// Chat Assistant
const messageList = document.getElementById("message-list");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const micBtn = document.getElementById("mic-btn");

// Symptom Checker
const symptomForm = document.getElementById("symptom-form");
const symptomName = document.getElementById("symptom-name");
const symptomChips = document.getElementById("symptom-chips");
const symptomResult = document.getElementById("symptom-result");

// Medicine Search
const medicineSearchForm = document.getElementById("medicine-search-form");
const medicineSearchInput = document.getElementById("medicine-search-input");
const medicineDetailCard = document.getElementById("medicine-detail-card");
const medDetailTitle = document.getElementById("med-detail-title");
const medicineDirectoryList = document.getElementById("medicine-directory-list");

// Health Profile
const profileForm = document.getElementById("profile-form");
const profileName = document.getElementById("profile-name");
const profileAge = document.getElementById("profile-age");
const profileGender = document.getElementById("profile-gender");
const profileBlood = document.getElementById("profile-blood");
const profileAllergies = document.getElementById("profile-allergies");
const profileHistory = document.getElementById("profile-history");

// App State Variables
let authToken = localStorage.getItem("aarogya_token") || "";
let currentUser = null;
let isRegisterMode = false;

// -------------------------------------------------------------
// Helper: HTML Escaper for Security
// -------------------------------------------------------------
function escapeHtml(text) {
    if (!text) return "";
    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// -------------------------------------------------------------
// Helper: Centralized API Fetcher
// -------------------------------------------------------------
async function apiFetch(endpoint, method = "GET", body = null) {
    const headers = { "Content-Type": "application/json" };
    if (authToken) {
        headers["Authorization"] = `Bearer ${authToken}`;
    }

    const options = { method, headers };
    if (body) {
        options.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(endpoint, options);
        const data = await response.json();
        return { status: response.status, data };
    } catch (err) {
        console.error("API Request Error:", err);
        return { status: 500, data: { success: false, message: "Network connection failure. Please check backend server." } };
    }
}

// -------------------------------------------------------------
// 1. Navigation & Page View Switcher
// -------------------------------------------------------------
navButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        const targetPage = btn.dataset.page;

        navButtons.forEach(b => b.classList.remove("is-active"));
        pageViews.forEach(p => p.classList.remove("is-active"));

        btn.classList.add("is-active");
        const activeView = document.getElementById(`page-${targetPage}`);
        if (activeView) activeView.classList.add("is-active");

        if (targetPage === "profile") loadProfileData();
    });
});

// Quick Prompt Buttons handler
document.querySelectorAll(".suggestion-panel button").forEach(btn => {
    btn.addEventListener("click", () => {
        const promptText = btn.dataset.prompt;
        if (promptText) {
            chatInput.value = promptText;
            chatForm.dispatchEvent(new Event("submit"));
        }
    });
});

// -------------------------------------------------------------
// 2. Authentication & Navigation Handler
// -------------------------------------------------------------
authModalBtn.addEventListener("click", () => {
    if (authToken) {
        // Logout action
        if (confirm("Are you sure you want to log out?")) {
            authToken = "";
            localStorage.removeItem("aarogya_token");
            currentUser = null;
            window.location.href = "/login.html";
        }
    } else {
        window.location.href = "/login.html";
    }
});

closeAuthModalBtn.addEventListener("click", () => authModal.style.display = "none");
authModal.addEventListener("click", (e) => {
    if (e.target === authModal) authModal.style.display = "none";
});

authToggleBtn.addEventListener("click", () => {
    isRegisterMode = !isRegisterMode;
    updateAuthModalState();
});

function openAuthModal(register = false) {
    isRegisterMode = register;
    updateAuthModalState();
    authErrorMsg.style.display = "none";
    authModal.style.display = "flex";
}

function updateAuthModalState() {
    if (isRegisterMode) {
        authModalTitle.textContent = "Create IndicHealth Account";
        registerNameField.style.display = "block";
        authSubmitBtn.textContent = "Register Account";
        authToggleBtn.textContent = "Already have an account? Log in";
    } else {
        authModalTitle.textContent = "Account Login";
        registerNameField.style.display = "none";
        authSubmitBtn.textContent = "Log In";
        authToggleBtn.textContent = "Need an account? Register";
    }
}

authForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    authErrorMsg.style.display = "none";

    const email = authEmailInput.value.trim();
    const password = authPasswordInput.value;

    if (isRegisterMode) {
        const name = authNameInput.value.trim();
        const res = await apiFetch("/register", "POST", { name, email, password });
        if (res.data.success) {
            // Auto login after register
            await loginUser(email, password);
        } else {
            showAuthError(res.data.message || "Registration failed.");
        }
    } else {
        await loginUser(email, password);
    }
});

async function loginUser(email, password) {
    const res = await apiFetch("/login", "POST", { email, password });
    if (res.data.success && res.data.data.access_token) {
        authToken = res.data.data.access_token;
        localStorage.setItem("aarogya_token", authToken);
        authModal.style.display = "none";
        await checkCurrentSession();
        loadChatHistory();
    } else {
        showAuthError(res.data.message || "Invalid credentials.");
    }
}

function showAuthError(msg) {
    authErrorMsg.textContent = msg;
    authErrorMsg.style.display = "block";
}

async function checkCurrentSession() {
    if (!authToken) {
        updateUserUI();
        return;
    }
    const res = await apiFetch("/me");
    if (res.data.success && res.data.data) {
        currentUser = res.data.data;
        updateUserUI();
    } else {
        authToken = "";
        localStorage.removeItem("aarogya_token");
        updateUserUI();
    }
}

function updateUserUI() {
    if (currentUser && authToken) {
        userInitial.textContent = (currentUser.name || currentUser.email || "U").charAt(0).toUpperCase();
        userName.textContent = currentUser.name || currentUser.email;
        authModalBtn.textContent = "Logout";
    } else {
        userInitial.textContent = "G";
        userName.textContent = "Guest";
        authModalBtn.textContent = "Login / Register";
    }
}

// -------------------------------------------------------------
// Markdown Formatter & Text-to-Speech Helper
// -------------------------------------------------------------
function formatMarkdown(text) {
    if (!text) return "";
    let html = escapeHtml(text);

    // 1. Horizontal dividers: ---
    html = html.replace(/\s*---\s*/g, '<hr style="margin:14px 0; border:none; border-top:1px solid var(--line);">');

    // 2. Headings: ### Header or ## Header
    html = html.replace(/###\s*(.*?)(?=(###|<hr>|\n|$))/g, '<h4 style="margin:12px 0 6px; font-size:1.05rem; font-weight:800; color:var(--sage-deep);">$1</h4>');
    html = html.replace(/##\s*(.*?)(?=(##|<hr>|\n|$))/g, '<h3 style="margin:14px 0 8px; font-size:1.15rem; font-weight:800; color:var(--sage-deep);">$1</h3>');

    // 3. Bold text: **text**
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');

    // 4. Bullet items: * Item or - Item
    html = html.replace(/(?:^|\n|\s)\*\s+(.*?)(?=(\n|\s\*|$|<hr>|<h\d>))/g, '<li style="margin-bottom:6px;">$1</li>');
    html = html.replace(/(?:^|\n|\s)-\s+(.*?)(?=(\n|\s-|$|<hr>|<h\d>))/g, '<li style="margin-bottom:6px;">$1</li>');

    // Wrap consecutive <li> into clean <ul> list
    html = html.replace(/(<li[\s\S]*?<\/li>)/g, '<ul style="margin:8px 0 12px; padding-left:22px;">$1</ul>');
    html = html.replace(/<\/ul>\s*<ul style="margin:8px 0 12px; padding-left:22px;">/g, '');

    // 5. Convert line breaks
    html = html.replace(/\n/g, '<br>');

    return html;
}

function cleanTextForSpeech(text) {
    if (!text) return "";
    let clean = text;
    clean = clean.replace(/#{1,6}\s*/g, '');
    clean = clean.replace(/[\*_]{1,3}/g, '');
    clean = clean.replace(/\s*---\s*/g, ' ');
    clean = clean.replace(/(?:^|\n|\s)[-\*\+]\s+/g, ' ');
    clean = clean.replace(/`{1,3}/g, '');
    return clean.trim();
}

function speakText(text) {
    if (!window.speechSynthesis) {
        alert("Text-to-speech is not supported in this browser.");
        return;
    }
    window.speechSynthesis.cancel();
    const speechText = cleanTextForSpeech(text);
    const utterance = new SpeechSynthesisUtterance(speechText);
    utterance.lang = selectedLanguage;
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
}

// -------------------------------------------------------------
// 3. AI Chat Assistant & Voice Features
// -------------------------------------------------------------
function renderChatBubble(role, text) {
    const bubble = document.createElement("article");
    bubble.className = `chat-bubble ${role === "user" ? "is-user" : ""}`;
    
    const sender = role === "user" ? "You" : "IndicHealth AI";
    const speakerBtnHtml = role === "assistant" 
        ? `<button type="button" class="tts-btn" title="Listen to audio">🔊</button>` 
        : "";

    const contentHtml = role === "user" 
        ? `<p>${escapeHtml(text)}</p>` 
        : `<div class="chat-content" style="line-height:1.6;">${formatMarkdown(text)}</div>`;

    bubble.innerHTML = `
        <span>${sender} ${speakerBtnHtml}</span>
        ${contentHtml}
    `;

    if (role === "assistant") {
        const ttsBtn = bubble.querySelector(".tts-btn");
        ttsBtn.addEventListener("click", () => speakText(text));
    }

    messageList.appendChild(bubble);
    messageList.scrollTop = messageList.scrollHeight;
}

async function loadChatHistory() {
    if (!authToken) return;
    const res = await apiFetch("/chat/history");
    if (res.data.success && Array.isArray(res.data.data)) {
        messageList.innerHTML = "";
        renderChatBubble("assistant", "Namaste! I am IndicHealth AI, your healthcare assistant. How can I help you today?");
        res.data.data.forEach(item => {
            renderChatBubble("user", item.user_message);
            renderChatBubble("assistant", item.ai_response);
        });
        const elem = document.getElementById("today-symptoms");
        if (elem) elem.textContent = res.data.data.length;
    }
}

// Language Configuration
const languageSelect = document.getElementById("language-select");
let selectedLanguage = "en-IN";

const LANG_NAMES = {
    "en-IN": "English",
    "hi-IN": "Hindi",
    "bn-IN": "Bengali",
    "te-IN": "Telugu",
    "ta-IN": "Tamil",
    "mr-IN": "Marathi"
};

const UI_TRANSLATIONS = {
    "en-IN": {
        brand_sub: "AI Health Assistant",
        nav_chat: "AI Care Chat",
        nav_symptoms: "Symptom Checker",
        nav_medicine: "Medicine Search",
        nav_profile: "Health Profile",
        disclaimer: "💡 IndicHealth AI provides preliminary guidance. For medical emergencies, call local emergency services immediately.",
        page_kicker: "AI-Powered Rural Healthcare",
        page_title: "Voice & Text Healthcare Assistant in Regional Languages",
        hero_kicker: "Multilingual Voice & Text AI",
        hero_title: "Ask IndicHealth AI",
        hero_desc: "Get simple explanations for symptoms, medicines, and care routines in your local language.",
        chat_send: "Send",
        chat_placeholder: "Type your health question or click the mic to speak...",
        quick_q_title: "Quick Health Questions",
        prompt_1: "Fever & Cough Advice",
        prompt_2: "Dolo 650 Dosage & Uses",
        prompt_3: "Stomach Care Routine",
        symp_kicker: "Rule-Based Assessment",
        symp_title: "Check Your Symptoms",
        symp_label: "Select or Type Symptoms (comma separated):",
        symp_btn: "Assess Symptoms",
        triage_title: "Diagnostic Triage Result",
        med_kicker: "Database Lookup",
        med_title: "Search Medicine Information",
        med_btn: "Search Database",
        profile_kicker: "Digital Health Record",
        profile_btn: "Save Health Profile to Database",
        welcome_msg: "Namaste! I am IndicHealth AI, your healthcare assistant. How can I help you today?"
    },
    "hi-IN": {
        brand_sub: "एआई स्वास्थ्य सहायक",
        nav_chat: "एआई केयर चैट",
        nav_symptoms: "लक्षण जांच (Symptom Checker)",
        nav_medicine: "दवा खोज (Medicine Search)",
        nav_profile: "स्वास्थ्य प्रोफाइल (Health Profile)",
        disclaimer: "💡 IndicHealth AI प्राथमिक मार्गदर्शन प्रदान करता है। आपातकालीन स्थिति में तुरंत स्थानीय आपातकालीन सेवाओं को कॉल करें।",
        page_kicker: "एआई-संचालित ग्रामीण स्वास्थ्य सेवा",
        page_title: "क्षेत्रीय भाषाओं में वॉइस और टेक्स्ट स्वास्थ्य सहायक",
        hero_kicker: "बहुभाषी वॉइस और टेक्स्ट एआई",
        hero_title: "IndicHealth AI से पूछें",
        hero_desc: "अपनी स्थानीय भाषा में लक्षणों, दवाओं और देखभाल की जानकारी प्राप्त करें।",
        chat_send: "भेजें",
        chat_placeholder: "अपना स्वास्थ्य प्रश्न टाइप करें या बोलने के लिए माइक पर क्लिक करें...",
        quick_q_title: "त्वरित स्वास्थ्य प्रश्न",
        prompt_1: "बुखार और खांसी की सलाह",
        prompt_2: "डोलो 650 खुराक और उपयोग",
        prompt_3: "पेट दर्द देखभाल की दिनचर्या",
        symp_kicker: "नियम-आधारित मूल्यांकन",
        symp_title: "अपने लक्षणों की जांच करें",
        symp_label: "लक्षण चुनें या टाइप करें (कॉमा से अलग करें):",
        symp_btn: "लक्षणों का मूल्यांकन करें",
        triage_title: "नैदानिक मूल्यांकन परिणाम",
        med_kicker: "डेटाबेस खोज",
        med_title: "दवा की जानकारी खोजें",
        med_btn: "डेटाबेस खोजें",
        profile_kicker: "डिजिटल स्वास्थ्य रिकॉर्ड",
        profile_btn: "स्वास्थ्य प्रोफाइल सहेजें",
        welcome_msg: "नमस्ते! मैं IndicHealth AI हूँ, आपका स्वास्थ्य सहायक। आज मैं आपकी क्या सहायता कर सकता हूँ?"
    },
    "bn-IN": {
        brand_sub: "এআই স্বাস্থ্য সহকারী",
        nav_chat: "এআই কেয়ার চ্যাট",
        nav_symptoms: "লক্ষণ পরীক্ষা (Symptom Checker)",
        nav_medicine: "ওষুধ অনুসন্ধান (Medicine Search)",
        nav_profile: "স্বাস্থ্য প্রোফাইল (Health Profile)",
        disclaimer: "💡 IndicHealth AI প্রাথমিক নির্দেশিকা প্রদান করে। জরুরি চিকিৎসার জন্য স্থানীয় জরুরি পরিষেবাগুলিতে অবিলম্বে কল করুন।",
        page_kicker: "এআই-চালিত গ্রামীণ স্বাস্থ্যসেবা",
        page_title: "আঞ্চলিক ভাষায় ভয়েস ও টেক্সট স্বাস্থ্য সহকারী",
        hero_kicker: "বহুভাষিক ভয়েস ও টেক্সট এআই",
        hero_title: "IndicHealth AI-কে জিজ্ঞাসা করুন",
        hero_desc: "আপনার স্থানীয় ভাষায় লক্ষণ, ওষুধ এবং যত্ন রুটিন সম্পর্কিত সরল ব্যাখ্যা পান।",
        chat_send: "পাঠান",
        chat_placeholder: "আপনার স্বাস্থ্য প্রশ্ন লিখুন বা কথা বলতে মাইকে ক্লিক করুন...",
        quick_q_title: "দ্রুত স্বাস্থ্য প্রশ্ন",
        prompt_1: "জ্বর ও কাশির পরামর্শ",
        prompt_2: "ডলো ৬৫০ সেবন ও ব্যবহার",
        prompt_3: "পেটের সমস্যার যত্ন",
        symp_kicker: "নিয়ম-ভিত্তিক মূল্যায়ন",
        symp_title: "আপনার লক্ষণ পরীক্ষা করুন",
        symp_label: "লক্ষণ নির্বাচন করুন বা লিখুন (কমা দিয়ে আলাদা করুন):",
        symp_btn: "লক্ষণ মূল্যায়ন করুন",
        triage_title: "রোগ নির্ণয়ের ফলাফল",
        med_kicker: "ডাটাবেস অনুসন্ধান",
        med_title: "ওষুধের তথ্য সন্ধান করুন",
        med_btn: "ডাটাবেস সন্ধান করুন",
        profile_kicker: "ডিজিটাল স্বাস্থ্য রেকর্ড",
        profile_btn: "স্বাস্থ্য প্রোফাইল সংরক্ষণ করুন",
        welcome_msg: "নমস্কার! আমি IndicHealth AI, আপনার স্বাস্থ্য সহকারী। আজ আমি আপনাকে কীভাবে সাহায্য করতে পারি?"
    },
    "te-IN": {
        brand_sub: "AI ఆరోగ్య సహాయకుడు",
        nav_chat: "AI కేర్ చాట్",
        nav_symptoms: "లక్షణాల తనిఖీ (Symptom Checker)",
        nav_medicine: "మందుల శోధన (Medicine Search)",
        nav_profile: "ఆరోగ్య ప్రొఫైల్ (Health Profile)",
        disclaimer: "💡 IndicHealth AI ప్రాథమిక మార్గదర్శకత్వాన్ని అందిస్తుంది. అత్యవసర పరిస్థితికి వెంటనే అత్యవసర సేవలను సంప్రదించండి.",
        page_kicker: "AI-ఆధారిత గ్రామీణ ఆరోగ్య సంరక్షణ",
        page_title: "ప్రాంతీయ భాషలలో వాయిస్ మరియు టెక్స్ట్ ఆరోగ్య సహాయకుడు",
        hero_kicker: "బహుభాషా వాయిస్ & టెక్స్ట్ AI",
        hero_title: "IndicHealth AI ని అడగండి",
        hero_desc: "మీ ప్రాంతీయ భాషలో లక్షణాలు, మందులు మరియు సంరక్షణ వివరణలను పొందండి.",
        chat_send: "పంపండి",
        chat_placeholder: "మీ ఆరోగ్య ప్రశ్నను టైప్ చేయండి లేదా మాట్లాడటానికి మైక్ క్లిక్ చేయండి...",
        quick_q_title: "త్వరిత ఆరోగ్య ప్రశ్నలు",
        prompt_1: "జ్వరం మరియు దగ్గు సలహా",
        prompt_2: "డోలో 650 వాడకం మరియు మోతాదు",
        prompt_3: "కడుపు నొప్పి సంరక్షణ",
        symp_kicker: "నిబంధనల ఆధారిత అంచనా",
        symp_title: "మీ లక్షణాలను తనిఖీ చేయండి",
        symp_label: "లక్షణాలను ఎంచుకోండి లేదా టైప్ చేయండి:",
        symp_btn: "లక్షణాలను అంచనా వేయండి",
        triage_title: "రోగ నిర్ధారణ ఫలితం",
        med_kicker: "డేటాబేస్ శోధన",
        med_title: "మందుల సమాచారాన్ని శోధించండి",
        med_btn: "డేటాబేస్ శోధించండి",
        profile_kicker: "డిజిటల్ హెల్త్ రికార్డ్",
        profile_btn: "ఆరోగ్య ప్రొఫైల్ ని సేవ్ చేయండి",
        welcome_msg: "నమస్కారం! నేను IndicHealth AI, మీ ఆరోగ్య సహాయకుడిని. ఈ రోజు నేను మీకు ఎలా సహాయపడగలను?"
    },
    "ta-IN": {
        brand_sub: "AI சுகாதார உதவியாளர்",
        nav_chat: "AI பராமரிப்பு அரட்டை",
        nav_symptoms: "அறிகுறி பரிசோதனை",
        nav_medicine: "மருந்து தேடல்",
        nav_profile: "சுகாதார சுயவிவரம்",
        disclaimer: "💡 IndicHealth AI ஆரம்ப வழிகாட்டலை வழங்குகிறது. அவசரநிலைக்கு உடனடியாக அவசர சேவைகளை அழைக்கவும்.",
        page_kicker: "AI-இயக்கப்படும் கிராமப்புற சுகாதாரம்",
        page_title: "பிராந்திய மொழிகளில் குரல் மற்றும் உரை சுகாதார உதவியாளர்",
        hero_kicker: "பன்மொழி குரல் மற்றும் உரை AI",
        hero_title: "IndicHealth AI இடம் கேளுங்கள்",
        hero_desc: "உங்கள் உள்ளூர் மொழியில் அறிகுறிகள் மற்றும் மருந்துகள் பற்றிய எளிய விளக்கங்களைப் பெறுங்கள்.",
        chat_send: "அனுப்பு",
        chat_placeholder: "உங்கள் சுகாதார கேள்வியை தட்டச்சு செய்யவும் அல்லது பேச மைக்கை கிளிக் செய்யவும்...",
        quick_q_title: "விரைவான சுகாதார கேள்விகள்",
        prompt_1: "காய்ச்சல் மற்றும் இருமல் ஆலோசனை",
        prompt_2: "டோலோ 650 அளவு மற்றும் பயன்பாடுகள்",
        prompt_3: "வயிறு பராமரிப்பு முறை",
        symp_kicker: "விதி சார்ந்த மதிப்பீடு",
        symp_title: "உங்கள் அறிகுறிகளை சரிபார்க்கவும்",
        symp_label: "அறிகுறிகளைத் தேர்ந்தெடுக்கவும் அல்லது தட்டச்சு செய்யவும்:",
        symp_btn: "அறிகுறிகளை மதிப்பிடுங்கள்",
        triage_title: "பரிசோதனை முடிவு",
        med_kicker: "தரவுத்தள தேடல்",
        med_title: "மருந்து தகவலைத் தேடுங்கள்",
        med_btn: "தரவுத்தளத்தைத் தேடுங்கள்",
        profile_kicker: "டிஜிட்டல் சுகாதார பதிவு",
        profile_btn: "சுகாதார சுயவிவரத்தைச் சேமிக்கவும்",
        welcome_msg: "வணக்கம்! நான் IndicHealth AI, உங்கள் சுகாதார உதவியாளர். இன்று நான் உங்களுக்கு எவ்வாறு உதவ முடியும்?"
    },
    "mr-IN": {
        brand_sub: "एआय आरोग्य सहाय्यक",
        nav_chat: "एआय केअर चॅट",
        nav_symptoms: "लक्षणे तपासा (Symptom Checker)",
        nav_medicine: "औषध शोध (Medicine Search)",
        nav_profile: "आरोग्य प्रोफाईल (Health Profile)",
        disclaimer: "💡 IndicHealth AI प्राथमिक मार्गदर्शन प्रदान करते. वैद्यकीय आणीबाणीसाठी त्वरित स्थानिक आपत्कालीन सेवांना कॉल करा.",
        page_kicker: "एआय-आधारित ग्रामीण आरोग्य सेवा",
        page_title: "प्रादेशिक भाषांमध्ये व्हॉइस आणि टेक्स्ट आरोग्य सहाय्यक",
        hero_kicker: "बहुभाषिक व्हॉइस आणि टेक्स्ट एआय",
        hero_title: "IndicHealth AI ला विचारा",
        hero_desc: "तुमच्या स्थानिक भाषेत लक्षणे, औषधे आणि काळजी दिनचर्या बद्दल सोपे स्पष्टीकरण मिळवा.",
        chat_send: "पाठवा",
        chat_placeholder: "तुमचा आरोग्य प्रश्न टाइप करा किंवा बोलण्यासाठी मायक वर क्लिक करा...",
        quick_q_title: "त्वरित आरोग्य प्रश्न",
        prompt_1: "ताप आणि खोकल्याचा सल्ला",
        prompt_2: "डोलो 650 डोस आणि वापर",
        prompt_3: "पोटदुखी काळजी दिनचर्या",
        symp_kicker: "नियम-आधारित मूल्यमापन",
        symp_title: "तुमची लक्षणे तपासा",
        symp_label: "लक्षणे निवडा किंवा टाइप करा:",
        symp_btn: "लक्षणांचे मूल्यमापन करा",
        triage_title: "निदान मूल्यमापन निकाल",
        med_kicker: "डेटाबेस शोध",
        med_title: "औषध माहिती शोधा",
        med_btn: "डेटाबेस शोधा",
        profile_kicker: "डिजिटल आरोग्य नोंद",
        profile_btn: "आरोग्य प्रोफाइल जतन करा",
        welcome_msg: "नमस्ते! मी IndicHealth AI आहे, तुमचा आरोग्य सहाय्यक. आज मी तुम्हाला कशी मदत करू शकतो?"
    }
};

function updateLanguageUI() {
    const dict = UI_TRANSLATIONS[selectedLanguage] || UI_TRANSLATIONS["en-IN"];
    document.querySelectorAll("[data-i18n]").forEach(elem => {
        const key = elem.dataset.i18n;
        if (dict[key]) {
            elem.textContent = dict[key];
        }
    });

    if (dict.chat_placeholder) {
        chatInput.placeholder = dict.chat_placeholder;
    }
}

const savedLang = localStorage.getItem("aarogya_lang");
if (savedLang && LANG_NAMES[savedLang]) {
    selectedLanguage = savedLang;
    if (languageSelect) languageSelect.value = savedLang;
    updateLanguageUI();
}

if (languageSelect) {
    languageSelect.addEventListener("change", () => {
        selectedLanguage = languageSelect.value;
        localStorage.setItem("aarogya_lang", selectedLanguage);
        const langName = LANG_NAMES[selectedLanguage] || "English";
        updateLanguageUI();
    });
}

chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    chatInput.value = "";
    renderChatBubble("user", message);

    // Show temporary thinking indicator
    const thinkingBubble = document.createElement("article");
    thinkingBubble.className = "chat-bubble";
    thinkingBubble.innerHTML = `<span>IndicHealth AI</span><p>Thinking and processing health guidance...</p>`;
    messageList.appendChild(thinkingBubble);
    messageList.scrollTop = messageList.scrollHeight;

    const langName = LANG_NAMES[selectedLanguage] || "English";
    const formattedMessage = selectedLanguage !== "en-IN"
        ? `[Please respond in ${langName} language]: ${message}`
        : message;

    const res = await apiFetch("/chat", "POST", { message: formattedMessage });
    messageList.removeChild(thinkingBubble);

    if (res.data.success) {
        const aiResponse = res.data.data.response;
        renderChatBubble("assistant", aiResponse);
    } else {
        renderChatBubble("assistant", `Notice: ${res.data.message || "Please log in to chat with IndicHealth AI."}`);
    }
});

// Voice-to-Text (STT) Integration
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;

    micBtn.addEventListener("click", () => {
        recognition.lang = selectedLanguage;
        if (micBtn.classList.contains("is-listening")) {
            recognition.stop();
            micBtn.classList.remove("is-listening");
        } else {
            recognition.start();
            micBtn.classList.add("is-listening");
        }
    });

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        chatInput.value = transcript;
        micBtn.classList.remove("is-listening");
    };

    recognition.onerror = () => {
        micBtn.classList.remove("is-listening");
    };

    recognition.onend = () => {
        micBtn.classList.remove("is-listening");
    };
} else {
    micBtn.style.display = "none";
}

// -------------------------------------------------------------
// 4. Symptom Assessment Engine
// -------------------------------------------------------------
symptomChips.addEventListener("click", (e) => {
    const chip = e.target.closest(".chip-btn");
    if (!chip) return;
    const symptom = chip.dataset.symptom;
    const currentText = symptomName.value.trim();
    if (currentText) {
        if (!currentText.toLowerCase().includes(symptom.toLowerCase())) {
            symptomName.value = `${currentText}, ${symptom}`;
        }
    } else {
        symptomName.value = symptom;
    }
});

symptomForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const rawInput = symptomName.value.trim();
    if (!rawInput) return;

    const symptomsList = rawInput.split(",").map(s => s.trim()).filter(Boolean);

    symptomResult.innerHTML = `<h3>Evaluating symptoms...</h3><p>Running rule-based clinical triage...</p>`;

    const res = await apiFetch("/symptom-check", "POST", { symptoms: symptomsList });

    if (res.data.success) {
        const result = res.data.data;
        const emergencyClass = result.is_emergency ? "emergency" : "";

        symptomResult.className = `result-card ${emergencyClass}`;
        symptomResult.innerHTML = `
            ${result.is_emergency ? '<p class="eyebrow" style="color:var(--danger)">⚠️ EMERGENCY ALERT</p>' : ''}
            <h3>Possible Condition: ${escapeHtml(result.possible_condition)}</h3>
            <p><strong>Recommended Specialist:</strong> ${escapeHtml(result.recommended_specialist)}</p>
            <p><strong>Clinical Advice:</strong> ${escapeHtml(result.advice)}</p>
            <hr style="margin:10px 0; border:none; border-top:1px solid var(--line);">
            <small>Evaluated Symptoms: ${escapeHtml(result.matched_symptoms.join(", "))}</small>
        `;
    } else {
        symptomResult.innerHTML = `<h3>Assessment Error</h3><p>${escapeHtml(res.data.message)}</p>`;
    }
});

// -------------------------------------------------------------
// 5. Medicine Information Search & Directory
// -------------------------------------------------------------
medicineSearchForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = medicineSearchInput.value.trim();
    if (!query) return;

    medicineDetailCard.innerHTML = `<p>Searching database for '${escapeHtml(query)}'...</p>`;

    const res = await apiFetch(`/medicine/${encodeURIComponent(query)}`);

    if (res.data.success) {
        const med = res.data.data;
        medDetailTitle.textContent = med.medicine_name;
        medicineDetailCard.innerHTML = `
            <h3>${escapeHtml(med.medicine_name)}</h3>
            <p><strong>Uses:</strong> ${escapeHtml(med.uses)}</p>
            <p><strong>Dosage Guidelines:</strong> ${escapeHtml(med.dosage)}</p>
            <p><strong>Side Effects:</strong> ${escapeHtml(med.side_effects)}</p>
            <p><strong>Precautions:</strong> ${escapeHtml(med.precautions)}</p>
        `;
    } else {
        medDetailTitle.textContent = "Not Found";
        medicineDetailCard.innerHTML = `<p style="color:var(--danger)">${escapeHtml(res.data.message)}</p>`;
    }
});

async function loadMedicineDirectory() {
    const res = await apiFetch("/medicine");
    if (res.data.success && Array.isArray(res.data.data)) {
        medicineDirectoryList.innerHTML = res.data.data.map(med => `
            <article class="medicine-card" style="cursor:pointer;" onclick="quickSearchMedicine('${escapeHtml(med.medicine_name)}')">
                <time>MED</time>
                <div>
                    <strong>${escapeHtml(med.medicine_name)}</strong>
                    <p>${escapeHtml(med.uses)}</p>
                </div>
            </article>
        `).join("");
    }
}

window.quickSearchMedicine = (medName) => {
    medicineSearchInput.value = medName;
    medicineSearchForm.dispatchEvent(new Event("submit"));
};

// -------------------------------------------------------------
// 6. Patient Health Profile
// -------------------------------------------------------------
async function loadProfileData() {
    if (!authToken) return;
    const res = await apiFetch("/profile");
    if (res.data.success && res.data.data) {
        const p = res.data.data;
        if (currentUser) profileName.value = currentUser.name || "";
        profileAge.value = p.age || "";
        profileGender.value = p.gender || "";
        profileBlood.value = p.blood_group || "";
        profileAllergies.value = p.allergies || "";
        profileHistory.value = p.medical_history || "";
    }
}

profileForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!authToken) {
        alert("Please log in to save your digital health profile.");
        authModal.style.display = "flex";
        return;
    }

    const payload = {
        age: profileAge.value ? parseInt(profileAge.value) : null,
        gender: profileGender.value || null,
        blood_group: profileBlood.value || null,
        allergies: profileAllergies.value.trim() || null,
        medical_history: profileHistory.value.trim() || null
    };

    const res = await apiFetch("/profile", "PUT", payload);
    if (res.data.success) {
        alert("Health Profile saved successfully to the database!");
    } else {
        alert(`Error saving profile: ${res.data.message}`);
    }
});

// -------------------------------------------------------------
// 7. Initial App Initialization
// -------------------------------------------------------------
renderChatBubble("assistant", "Namaste! I am IndicHealth AI, your healthcare assistant. How can I help you today?");
checkCurrentSession();
loadProfileData();
loadMedicineDirectory();
