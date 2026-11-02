import httpx
from app.config import settings

SYSTEM_INSTRUCTION = (
    "You are IndicHealth AI, an empathetic rural healthcare assistant. "
    "Always reply in the exact language requested by the user. "
    "You MUST structure every medical response using these 3 clean markdown subheadings:\n"
    "### 🩺 Symptoms\n"
    "* (Bullet points)\n\n"
    "### 💊 Cure & Home Care\n"
    "* (Bullet points)\n\n"
    "### 🛡️ Precautions to be Taken\n"
    "* (Bullet points)\n\n"
    "Translate these subheading titles into the user's requested language (Odia, Hindi, Bengali, or English). "
    "Keep bullet points concise and formatted cleanly."
)

MODELS_PRIORITY = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash-latest"]


def generate_dynamic_fallback(clean_query: str, health_profile_summary: str, lang_code: str = "en") -> str:
    """Generates a structured 3-section medical response in English, Odia, Hindi, or Bengali."""
    
    if lang_code == "or":
        return (
            "### 🩺 ମୁଖ୍ୟ ଲକ୍ଷଣ (Symptoms)\n"
            f"* ଆପଣଙ୍କ ପ୍ରଶ୍ନ '{clean_query}' ଅନୁଯାୟୀ ହାଲୁକା କିମ୍ବା ପ୍ରବଳ ଜ୍ୱର, ଦେହ ହାତ ବିନ୍ଧା ଏବଂ ଦୁର୍ବଳତା ଦେଖାଯାଇପାରେ।\n"
            "* ପେଟ କାଟିବା, ପାତଳା ଝାଡ଼ା କିମ୍ବା ଜଳୀୟ ଅଂଶ ହ୍ରାସ (Dehydration) ରକ୍ଷା କରିବା।\n\n"
            "### 💊 ପ୍ରାଥମିକ ଚିକିତ୍ସା ଓ ଘରୋଇ ଯତ୍ନ (Cure & Home Care)\n"
            "* **WHO-ORS ଘୋଳ:** ୧ ଲିଟର ଫୁଟା ଥଣ୍ଡା ପାଣିରେ ୧ ପ୍ୟାକେଟ୍ ORS ମିଶାଇ ଅଳ୍ପ ଅଳ୍ପ ପିଅନ୍ତୁ।\n"
            "* **ହାଲୁକା ଖାଦ୍ୟ:** ନରମ ଖିଚୁଡ଼ି, ଦହି-ଭାତ, ପାଚିଲା କଦଳୀ କିମ୍ବା ଡାଲି ପାଣି ଦିଅନ୍ତୁ।\n"
            "* **ଜ୍ୱର ନିୟନ୍ତ୍ରଣ:** ଜ୍ୱର ୧୦୦°F ରୁ ଅଧିକ ହେଲେ ଖାଇବା ପରେ ପାରାସିଟାମଲ୍ (Paracetamol 500mg) ନିଅନ୍ତୁ।\n\n"
            "### 🛡️ ସତର୍କତା (Precautions to be Taken)\n"
            "* ଡାକ୍ତରଙ୍କ ବିନା ପରାମର୍ଶରେ ଆଣ୍ଟିବାୟୋଟିକ୍ କିମ୍ବା Ibuprofen ଖାଆନ୍ତୁ ନାହିଁ।\n"
            "* ୩ ଦିନରୁ ଅଧିକ ଜ୍ୱର ରହିଲେ ନିକଟସ୍ଥ ସରକାରୀ PHC କିମ୍ବା ଡାକ୍ତରଙ୍କ ପରାମର୍ଶ ନିଅନ୍ତୁ।"
        )
    elif lang_code == "hi":
        return (
            "### 🩺 मुख्य लक्षण (Symptoms)\n"
            f"* आपके प्रश्न '{clean_query}' के अनुसार हल्का या तेज बुखार, शरीर में दर्द, थकान और कमजोरी महसूस होना।\n"
            "* दस्त या उल्टी के कारण शरीर में पानी और नमक की कमी (डिहाइड्रेशन)।\n\n"
            "### 💊 प्राथमिक उपचार व देखभाल (Cure & Home Care)\n"
            "* **ओआरएस (ORS) और तरल पदार्थ:** 1 लीटर उबले ठंडे पानी में 1 पैकेट WHO-ORS घोलें और थोड़े-थोड़े अंतराल पर पिलाएं।\n"
            "* **सुपाच्य आहार:** खिचड़ी, दही-चावल, केला या दाल का पानी दें।\n"
            "* **बुखार प्रबंधन:** माथे पर सामान्य पानी की पट्टी रखें और डॉक्टर की सलाह से पैरासिटामोल लें।\n\n"
            "### 🛡️ सावधानियां (Precautions to be Taken)\n"
            "* बिना डॉक्टर की सलाह के एंटीबायोटिक या तेज दर्द निवारक दवा (Ibuprofen) न दें।\n"
            "* यदि बुखार 3 दिन से अधिक रहे, तो तुरंत नजदीकी सरकारी PHC या डॉक्टर से संपर्क करें।"
        )
    elif lang_code == "bn":
        return (
            "### 🩺 প্রধান লক্ষণ (Symptoms)\n"
            f"* আপনার প্রশ্ন '{clean_query}' অনুযায়ী হালকা বা তীব্র জ্বর, শরীরে ব্যথা এবং চরম দুর্বলতা।\n"
            "* পাতলা পায়খানার কারণে শরীরে জল ও লবণের ঘাটতি (ডিহাইড্রেশন)।\n\n"
            "### 💊 প্রাথমিক চিকিৎসা ও ঘরোয়া যত্ন (Cure & Home Care)\n"
            "* **WHO-ORS পানীয়:** ১ লিটার ফোটানো ঠান্ডা জলে ১ প্যাকেট ORS মিশিয়ে অল্প অল্প করে পান করান।\n"
            "* **হালকা খাবার:** নরম খিচুড়ি, দই-ভাত, পাকা কলা বা ডালের জল দিন।\n"
            "* **জ্বরের যত্ন:** কপালে জলপট্টি দিন এবং প্রয়োজনে প্যারাসিটামল নিন।\n\n"
            "### 🛡️ সতর্কতা (Precautions to be Taken)\n"
            "* ডাক্তারের পরামর্শ ছাড়া অ্যান্টিবায়োটিক বা ব্যথার ওষুধ খাবেন না।\n"
            "* ৩ দিনের বেশি জ্বর থাকলে অবিলম্বে নিকটবর্তী সরকারি PHC-তে যোগাযোগ করুন।"
        )
    else:
        return (
            "### 🩺 Key Symptoms\n"
            f"* Mild to high-grade fever, body ache, or fatigue related to '{clean_query}'.\n"
            "* Loose motions, abdominal cramps, or dehydration signs if fluid intake is low.\n\n"
            "### 💊 Cure & Home Care\n"
            "* **ORS Rehydration:** Dissolve 1 packet of WHO-ORS in 1 liter of boiled cooled water and sip 200ml after every loose stool.\n"
            "* **Fever & Pain Relief:** Use lukewarm cloth sponging and take Paracetamol (500mg–650mg) after food with a minimum 6-hour gap.\n"
            "* **Light Diet:** Take soft khichdi, curd-rice, ripe banana, or clear dal water.\n\n"
            "### 🛡️ Precautions to be Taken\n"
            "* Strictly avoid self-medicating with antibiotics or NSAIDs (like Ibuprofen/Aspirin) until Dengue is ruled out.\n"
            "* Visit your nearest Primary Health Centre (PHC) immediately if fever lasts beyond 3 days."
        )


async def generate_ai_response(user_message: str, health_profile_summary: str = "") -> str:
    raw_key = settings.GEMINI_API_KEY or ""
    api_key = raw_key.strip().strip('"').strip("'")

    # Detect language from frontend request
    lang_code = "en"
    if "[Please respond in Odia" in user_message or "ଓଡ଼ିଆ" in user_message:
        lang_code = "or"
    elif "[Please respond in Hindi" in user_message or "हिन्दी" in user_message:
        lang_code = "hi"
    elif "[Please respond in Bengali" in user_message or "বাংলা" in user_message:
        lang_code = "bn"

    clean_query = user_message.split("]: ")[-1] if "]: " in user_message else user_message

    if not api_key or api_key == "your_gemini_api_key_here":
        return generate_dynamic_fallback(clean_query, health_profile_summary, lang_code)

    prompt = f"{SYSTEM_INSTRUCTION}\n\n"
    if health_profile_summary:
        prompt += f"Patient Context: {health_profile_summary}\n\n"
    prompt += f"User Question: {user_message}"

    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            for model_name in MODELS_PRIORITY:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                try:
                    response = await client.post(url, json=payload, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        ai_text = data["candidates"][0]["content"]["parts"][0]["text"]
                        return ai_text
                except Exception:
                    continue
            return generate_dynamic_fallback(clean_query, health_profile_summary, lang_code)
    except Exception:
        return generate_dynamic_fallback(clean_query, health_profile_summary, lang_code)