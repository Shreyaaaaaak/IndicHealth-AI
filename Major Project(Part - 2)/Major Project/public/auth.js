// auth.js — Multilingual Patient Auth & Demo Quick-Login for IndicHealth AI

const API_BASE_URL =
  window.location.origin.includes("5000") ||
  window.location.origin.includes("5173") ||
  window.location.origin.includes("3000") ||
  window.location.origin.includes("5500")
    ? "http://127.0.0.1:8000"
    : window.location.origin;

const TOKEN_KEY = "aarogya_token";
const LANG_KEY = "aarogya_lang";

const AUTH_I18N = {
  en: {
    badge_text: "Multilingual Rural Healthcare Portal",
    hero_heading: "Compassionate primary care in your own language.",
    hero_sub: "Instant clinical symptom triage, handwritten prescription OCR, free PHC doctor booking, and 500+ essential medicines with voice read-aloud.",
    stat_1: "Verified Rural Medicines",
    stat_2: "8 Specialist PHC Doctors",
    stat_3_title: "Voice & Text AI Triage",
    stat_3_sub: "English · ଓଡ଼ିଆ · हिन्दी · বাংলা",
    helpline_label: "24×7 Emergency Ambulance: 108",
    phc_label: "Rural Health Helpline: 104",
    login_eyebrow: "Patient Portal Access",
    login_title: "Welcome back",
    login_sub: "Enter your 10-digit mobile number to open your health card, active reminders, and OPD appointments.",
    lbl_phone: "Registered Mobile Number",
    btn_login: "Sign In to Dashboard",
    demo_hint: "Evaluating the project?",
    btn_demo_fill: "Fill Demo Patient",
    new_patient_q: "New to IndicHealth AI?",
    link_create_account: "Create patient account",
    signup_eyebrow: "Quick 10-Second Registration",
    signup_title: "Create your account",
    signup_sub: "Register with your name and mobile number—no complicated passwords or email addresses required.",
    lbl_name: "Patient Full Name",
    btn_signup: "Create Account & Continue",
    already_patient_q: "Already registered?",
    link_sign_in: "Sign in here"
  },
  or: {
    badge_text: "ବହୁଭାଷୀ ଗ୍ରାମୀଣ ସ୍ୱାସ୍ଥ୍ୟ ପୋର୍ଟାଲ୍",
    hero_heading: "ଆପଣଙ୍କ ନିଜ ଭାଷାରେ ସହଜ ଓ ଭରସାଯୋଗ୍ୟ ପ୍ରାଥମିକ ଚିକିତ୍ସା |",
    hero_sub: "ତୁରନ୍ତ ଲକ୍ଷଣ ପରୀକ୍ଷା, ହাতে ଲେଖା ପ୍ରେସକ୍ରିପସନ୍ ସ୍କାନ୍, ମାଗଣା PHC ଡାକ୍ତର ବୁକିଂ ଏବଂ ୫୦୦+ ଜରୁରୀ ଔଷଧର ସମ୍ପୂର୍ଣ୍ଣ ସୂଚନା |",
    stat_1: "୫୦୦+ ଜରୁରୀ ଗ୍ରାମୀଣ ଔଷଧ",
    stat_2: "୮ ବିଶେଷଜ୍ଞ PHC ଡାକ୍ତର",
    stat_3_title: "ଭଏସ୍ ଓ ଟେକ୍ସ୍ଟ AI ପରାମର୍ଶ",
    stat_3_sub: "ଓଡ଼ିଆ · English · हिन्दी · বাংলা",
    helpline_label: "୨୪×୭ ଜରୁରୀ ଆମ୍ବୁଲାନ୍ସ: ୧୦୮",
    phc_label: "ସ୍ୱାସ୍ଥ୍ୟ ହେଲ୍ପଲାଇନ୍: ୧୦୪",
    login_eyebrow: "ରୋଗୀ ଲଗଇନ୍ ପୋର୍ଟାଲ୍",
    login_title: "ପୁଣି ସ୍ୱାଗତ",
    login_sub: "ଆପଣଙ୍କର ସ୍ୱାସ୍ଥ୍ୟ କାର୍ଡ, ଔଷଧ ରିମାଇଣ୍ଡର୍ ଓ ଡାକ୍ତର ଆପଏଣ୍ଟମେଣ୍ଟ ଦେଖିବାକୁ ୧୦-ଅଙ୍କର ମୋବାଇଲ୍ ନମ୍ବର ଦିଅନ୍ତୁ |",
    lbl_phone: "ମୋବାଇଲ୍ ନମ୍ବର (୧୦ ଅଙ୍କ)",
    btn_login: "ଡ୍ୟାସବୋର୍ଡରେ ପ୍ରବେଶ କରନ୍ତୁ",
    demo_hint: "ପ୍ରୋଜେକ୍ଟ ଡେମୋ ଦେখୁଛନ୍ତି କି?",
    btn_demo_fill: "ଡେମୋ ନମ୍ବର ଭରନ୍ତୁ",
    new_patient_q: "IndicHealth AI ରେ ନୂଆ କି?",
    link_create_account: "ନୂଆ ଆକାଉଣ୍ଟ ଖୋଲନ୍ତୁ",
    signup_eyebrow: "୧୦ ସେକେଣ୍ଡରେ ସହଜ ପଞ୍ଜୀକରଣ",
    signup_title: "ନୂଆ ଆକାଉଣ୍ଟ ଖୋଲନ୍ତୁ",
    signup_sub: "କେବଳ ଆପଣଙ୍କର ନାମ ଓ ମୋବାଇଲ୍ ନମ୍ବର ଦେଇ ପଞ୍ଜୀକରଣ କରନ୍ତୁ |",
    lbl_name: "ରୋଗୀଙ୍କର ସମ୍ପୂର୍ଣ୍ଣ ନାମ",
    btn_signup: "ଆକାଉଣ୍ଟ ଖୋଲନ୍ତୁ ଓ ଆଗକୁ ବଢନ୍ତୁ",
    already_patient_q: "ପୂର୍ବରୁ ଆକାଉଣ୍ଟ ଅଛି କି?",
    link_sign_in: "ଏଠାରେ ଲଗଇନ୍ କରନ୍ତୁ"
  },
  hi: {
    badge_text: "बहुभाषी ग्रामीण स्वास्थ्य पोर्टल",
    hero_heading: "आपकी अपनी भाषा में सरल और भरोसेमंद प्राथमिक स्वास्थ्य सेवा।",
    hero_sub: "त्वरित लक्षण जांच, हस्तलिखित पर्ची स्कैनर, निःशुल्क PHC डॉक्टर बुकिंग और ऑडियो सुविधा के साथ 500+ आवश्यक दवाएं।",
    stat_1: "सत्यापित ग्रामीण दवाएं",
    stat_2: "8 विशेषज्ञ PHC डॉक्टर",
    stat_3_title: "वॉइस और टेक्स्ट AI परामर्श",
    stat_3_sub: "हिन्दी · ଓଡ଼ିଆ · বাংলা · English",
    helpline_label: "24×7 आपातकालीन एम्बुलेंस: 108",
    phc_label: "ग्रामीण स्वास्थ्य हेल्पलाइन: 104",
    login_eyebrow: "मरीज पोर्टल लॉगिन",
    login_title: "पुनः स्वागत है",
    login_sub: "अपना स्वास्थ्य कार्ड, दवा रिमाइंडर और ओपीडी अपॉइंटमेंट देखने के लिए 10-अंकीय मोबाइल नंबर दर्ज करें।",
    lbl_phone: "पंजीकृत मोबाइल नंबर",
    btn_login: "डैशबोर्ड में लॉग इन करें",
    demo_hint: "प्रोजेक्ट डेमो जांच रहे हैं?",
    btn_demo_fill: "डेमो मरीज भरें",
    new_patient_q: "IndicHealth AI पर नए हैं?",
    link_create_account: "नया खाता बनाएं",
    signup_eyebrow: "त्वरित 10-सेकंड पंजीकरण",
    signup_title: "अपना खाता बनाएं",
    signup_sub: "केवल अपने नाम और मोबाइल नंबर के साथ पंजीकरण करें—किसी जटिल पासवर्ड की आवश्यकता नहीं है।",
    lbl_name: "मरीज का पूरा नाम",
    btn_signup: "खाता बनाएं और आगे बढ़ें",
    already_patient_q: "पहले से पंजीकृत हैं?",
    link_sign_in: "यहां लॉग इन करें"
  },
  bn: {
    badge_text: "বহুভাষিক গ্রামীণ স্বাস্থ্য পোর্টাল",
    hero_heading: "আপনার নিজের ভাষায় সহজ ও নির্ভরযোগ্য প্রাথমিক স্বাস্থ্যসেবা।",
    hero_sub: "তাৎক্ষণিক উপসর্গ যাচাই, হাতে লেখা প্রেসক্রিপশন স্ক্যানার, বিনামূল্যে PHC ডাক্তার বুকিং এবং ৫০০+ জরুরি ওষুধ।",
    stat_1: "যাচাইকৃত গ্রামীণ ওষুধ",
    stat_2: "৮ জন বিশেষজ্ঞ PHC ডাক্তার",
    stat_3_title: "ভয়েস ও টেক্সট AI পরামর্শ",
    stat_3_sub: "বাংলা · ଓଡ଼ିଆ · हिन्दी · English",
    helpline_label: "২৪×৭ জরুরি অ্যাম্বুলেন্স: ১০৮",
    phc_label: "স্বাস্থ্য হেল্পলাইন: ১০৪",
    login_eyebrow: "রোগী পোর্টাল লগইন",
    login_title: "স্বাগতম",
    login_sub: "আপনার স্বাস্থ্য কার্ড, ওষুধের রিমাইন্ডার এবং ওপিডি অ্যাপয়েন্টমেন্ট দেখতে ১০-সংখ্যার মোবাইল নম্বর দিন।",
    lbl_phone: "নিবন্ধিত মোবাইল নম্বর",
    btn_login: "ড্যাশবোর্ডে প্রবেশ করুন",
    demo_hint: "প্রজেক্ট ডেমো দেখছেন?",
    btn_demo_fill: "ডেমো রোগী ভরুন",
    new_patient_q: "IndicHealth AI-তে নতুন?",
    link_create_account: "নতুন অ্যাকাউন্ট খুলুন",
    signup_eyebrow: "১০ সেকেন্ডে দ্রুত নিবন্ধন",
    signup_title: "আপনার অ্যাকাউন্ট তৈরি করুন",
    signup_sub: "শুধুমাত্র আপনার নাম এবং মোবাইল নম্বর দিয়ে নিবন্ধন করুন।",
    lbl_name: "রোগীর পুরো নাম",
    btn_signup: "অ্যাকাউন্ট তৈরি করুন ও এগিয়ে যান",
    already_patient_q: "ইতিমধ্যে অ্যাকাউন্ট আছে?",
    link_sign_in: "এখানে লগ ইন করুন"
  }
};

function setAuthLanguage(langCode) {
  const cleanLang = langCode.split("-")[0];
  localStorage.setItem(LANG_KEY, cleanLang);
  document.documentElement.lang = cleanLang;

  document.querySelectorAll(".lang-pill-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.getAttribute("data-lang") === cleanLang);
  });

  const dict = AUTH_I18N[cleanLang] || AUTH_I18N.en;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (dict[key]) el.textContent = dict[key];
  });
}

window.fillDemoLogin = function () {
  const phoneInput = document.getElementById("login-phone");
  if (phoneInput) {
    phoneInput.value = "9876543210";
    phoneInput.focus();
  }
};

async function apiFetch(endpoint, method = "GET", body = null) {
  const headers = { "Content-Type": "application/json" };
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const options = { method, headers };
  if (body) options.body = JSON.stringify(body);

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    const data = await response.json();
    return { status: response.status, data };
  } catch (error) {
    console.error("API Fetch Error:", error);
    return {
      status: 500,
      data: {
        success: false,
        message: "Server connection failed. Is the FastAPI backend running on :8000?"
      }
    };
  }
}

function showError(el, message) {
  el.textContent = message;
  el.style.display = "block";
}
function hideError(el) {
  el.style.display = "none";
}
function setLoading(btn, loadingText, isLoading, originalText) {
  btn.disabled = isLoading;
  btn.textContent = isLoading ? loadingText : originalText;
}

// Redirect to dashboard if a valid session already exists
(async function redirectIfLoggedIn() {
  const token = localStorage.getItem(TOKEN_KEY);
  if (!token) return;
  const res = await apiFetch("/me");
  if (res.data && res.data.success) {
    window.location.href = "/index.html";
  } else {
    localStorage.removeItem(TOKEN_KEY);
  }
})();

// Initialize saved language
setAuthLanguage(localStorage.getItem(LANG_KEY) || "en");

// ---------------- Sign Up page ----------------
const signupForm = document.getElementById("signup-form");
if (signupForm) {
  const errorBox = document.getElementById("signup-error");
  const submitBtn = document.getElementById("signup-submit");

  signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideError(errorBox);

    const name = document.getElementById("signup-name").value.trim();
    const phone = document.getElementById("signup-phone").value.trim();

    if (!name) return showError(errorBox, "Please enter your full name.");
    if (!/^[0-9]{10}$/.test(phone))
      return showError(errorBox, "Please enter a valid 10-digit mobile number.");

    const email = `${phone}@indichealth.ai`;
    const password = `ih${phone}`;

    setLoading(submitBtn, "Creating account…", true);
    const registerRes = await apiFetch("/register", "POST", { name, email, password });

    if (!registerRes.data.success) {
      setLoading(submitBtn, "", false, "Create Account & Continue →");
      return showError(
        errorBox,
        registerRes.data.message || "Registration failed. Please try again."
      );
    }

    setLoading(submitBtn, "Signing you in…", true);
    const loginRes = await apiFetch("/login", "POST", { email, password });

    if (loginRes.data.success) {
      localStorage.setItem(TOKEN_KEY, loginRes.data.data.access_token);
      localStorage.setItem("aarogya_user_name", name);
      localStorage.setItem("aarogya_user_phone", phone);
      window.location.href = "/index.html";
    } else {
      setLoading(submitBtn, "", false, "Create Account & Continue →");
      showError(errorBox, "Account created! Redirecting to login...");
      setTimeout(() => {
        window.location.href = "/login.html";
      }, 1200);
    }
  });
}

// ---------------- Login page ----------------
const loginForm = document.getElementById("login-form");
if (loginForm) {
  const errorBox = document.getElementById("login-error");
  const submitBtn = document.getElementById("login-submit");

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideError(errorBox);

    const phone = document.getElementById("login-phone").value.trim();

    if (!/^[0-9]{10}$/.test(phone))
      return showError(errorBox, "Please enter a valid 10-digit mobile number.");

    const email = `${phone}@indichealth.ai`;
    const password = `ih${phone}`;

    setLoading(submitBtn, "Signing in…", true);
    const res = await apiFetch("/login", "POST", { email, password });

    if (res.data.success) {
      localStorage.setItem(TOKEN_KEY, res.data.data.access_token);
      if (res.data.data.user && res.data.data.user.name) {
        localStorage.setItem("aarogya_user_name", res.data.data.user.name);
      }
      localStorage.setItem("aarogya_user_phone", phone);
      window.location.href = "/index.html";
    } else {
      setLoading(submitBtn, "", false, "Sign In to Dashboard →");
      showError(
        errorBox,
        res.data.message || "Mobile number not registered yet. Please create an account first."
      );
    }
  });
}