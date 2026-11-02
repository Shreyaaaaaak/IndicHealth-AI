from typing import List, Dict, Any

# Rule definitions for prototype symptom checker
RULES: List[Dict[str, Any]] = [
    {
        "keywords": ["chest pain", "shortness of breath", "difficulty breathing", "heart pain", "left arm pain"],
        "condition": "Acute Cardiac / Respiratory Warning",
        "specialist": "Cardiologist / Emergency Medical Officer",
        "advice": "URGENT: Seek immediate emergency medical care or call local emergency services immediately.",
        "is_emergency": True
    },
    {
        "keywords": ["fever", "cough"],
        "condition": "Common Viral Infection / Respiratory Tract Infection",
        "specialist": "General Physician",
        "advice": "Drink warm fluids, rest adequately, monitor temperature, and seek medical attention if fever exceeds 102°F or persists for more than 3 days.",
        "is_emergency": False
    },
    {
        "keywords": ["fever", "chills", "body ache"],
        "condition": "Possible Seasonal Flu / Dengue / Malaria",
        "specialist": "General Physician",
        "advice": "Maintain hydration with ORS and water. Get a complete blood count (CBC) test done if fever continues.",
        "is_emergency": False
    },
    {
        "keywords": ["stomach pain", "vomiting", "diarrhea", "loose motion"],
        "condition": "Acute Gastroenteritis / Food Poisoning",
        "specialist": "Gastroenterologist / General Physician",
        "advice": "Sip ORS solution frequently to prevent dehydration. Eat light foods like rice gruel and bananas. Avoid spicy food.",
        "is_emergency": False
    },
    {
        "keywords": ["skin rash", "itching", "redness"],
        "condition": "Allergic Reaction / Contact Dermatitis",
        "specialist": "Dermatologist",
        "advice": "Avoid scratching affected area. Keep skin clean and dry. Consult a doctor for antihistamine prescriptions.",
        "is_emergency": False
    },
    {
        "keywords": ["headache", "dizziness", "nausea"],
        "condition": "Migraine / Tension Headache / Blood Pressure Fluctuations",
        "specialist": "Neurologist / General Physician",
        "advice": "Rest in a quiet, dark room. Stay hydrated. Check your blood pressure at a nearby clinic.",
        "is_emergency": False
    },
    {
        "keywords": ["joint pain", "swelling", "knee pain"],
        "condition": "Arthritis / Musculoskeletal Strain",
        "specialist": "Orthopedic Specialist",
        "advice": "Apply warm/cold compresses, avoid heavy physical strain, and get an orthopedic consultation.",
        "is_emergency": False
    },
    {
        "keywords": ["burning urination", "frequent urination"],
        "condition": "Urinary Tract Infection (UTI)",
        "specialist": "Urologist / General Physician",
        "advice": "Increase daily water intake significantly. Avoid caffeine and acidic drinks. Consult doctor for antibiotic course.",
        "is_emergency": False
    }
]


def check_symptoms(symptoms: List[str]) -> Dict[str, Any]:
    """
    Rule-based symptom assessment engine.
    Matches input symptoms against predefined clinical rules.
    """
    symptoms_lower = [s.strip().lower() for s in symptoms if s.strip()]

    # 1. Check for emergency rules first
    for rule in RULES:
        if rule.get("is_emergency"):
            matched = any(kw in " ".join(symptoms_lower) for kw in rule["keywords"])
            if matched:
                return {
                    "matched_symptoms": symptoms,
                    "possible_condition": rule["condition"],
                    "recommended_specialist": rule["specialist"],
                    "advice": rule["advice"],
                    "is_emergency": True
                }

    # 2. Check rule combinations
    best_rule = None
    max_matches = 0

    for rule in RULES:
        matches = sum(1 for kw in rule["keywords"] if any(kw in s for s in symptoms_lower))
        if matches > max_matches:
            max_matches = matches
            best_rule = rule

    if best_rule and max_matches > 0:
        return {
            "matched_symptoms": symptoms,
            "possible_condition": best_rule["condition"],
            "recommended_specialist": best_rule["specialist"],
            "advice": best_rule["advice"],
            "is_emergency": False
        }

    # 3. Default fallback
    return {
        "matched_symptoms": symptoms,
        "possible_condition": "Unspecified Mild Ailment",
        "recommended_specialist": "General Physician",
        "advice": "Your symptoms require general evaluation. Please consult a qualified General Physician for a complete physical assessment.",
        "is_emergency": False
    }
