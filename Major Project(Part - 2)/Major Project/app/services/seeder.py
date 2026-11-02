import os
import json
from sqlalchemy.orm import Session
from app.models.medicine import Medicine

SEED_MEDICINES = [
    {
        "medicine_name": "Paracetamol",
        "uses": "Relief of fever, mild to moderate pain (headache, body ache, toothache).",
        "dosage": "Adults: 500mg - 650mg every 4-6 hours as needed. Maximum 4000mg per day.",
        "side_effects": "Rarely causes side effects at normal doses. High doses can cause severe liver damage.",
        "precautions": "Do not combine with other paracetamol-containing products. Avoid alcohol consumption."
    },
    {
        "medicine_name": "Dolo 650",
        "uses": "Effective for high fever, severe headache, body pain, and viral infections.",
        "dosage": "1 tablet (650mg) after food, 3 to 4 times a day as prescribed by a physician.",
        "side_effects": "Nausea, allergic skin rash, liver toxicity in case of overdose.",
        "precautions": "Consult doctor if fever persists for more than 3 days. Caution in kidney/liver patients."
    },
    {
        "medicine_name": "Crocin",
        "uses": "Fever reducer and analgesic for headache, feverishness, and muscle aches.",
        "dosage": "500mg tablet every 4 to 6 hours after meals.",
        "side_effects": "Skin rash, stomach upset in rare cases.",
        "precautions": "Keep out of reach of children. Do not exceed recommended dosage."
    },
    {
        "medicine_name": "Cetirizine",
        "uses": "Relieves allergic symptoms like runny nose, sneezing, watery eyes, and itching.",
        "dosage": "Adults: 10mg once daily, preferably in the evening.",
        "side_effects": "Drowsiness, dry mouth, tiredness, dizziness.",
        "precautions": "May cause sedation. Avoid driving or operating machinery after taking."
    },
    {
        "medicine_name": "Amoxicillin",
        "uses": "Antibiotic used to treat bacterial infections of ear, nose, throat, chest, and skin.",
        "dosage": "500mg twice or thrice daily for 5-7 days as prescribed.",
        "side_effects": "Diarrhea, nausea, vomiting, skin rashes.",
        "precautions": "Must complete full course. Not effective against viral infections like common cold."
    },
    {
        "medicine_name": "Azithromycin",
        "uses": "Broad-spectrum antibiotic for respiratory tract infections, typhoid fever, and skin infections.",
        "dosage": "500mg once daily for 3 to 5 days, taken 1 hour before or 2 hours after meals.",
        "side_effects": "Abdominal cramps, diarrhea, nausea, temporary taste changes.",
        "precautions": "Do not skip doses. Inform doctor if you have heart rhythm disorders."
    },
    {
        "medicine_name": "ORS",
        "uses": "Oral Rehydration Salts to prevent and treat dehydration caused by diarrhea and vomiting.",
        "dosage": "Dissolve 1 packet in 1 liter of clean drinking water. Drink small sips frequently.",
        "side_effects": "Vomiting if consumed too rapidly.",
        "precautions": "Do not boil prepared ORS solution. Use within 24 hours of preparation."
    },
    {
        "medicine_name": "Ibuprofen",
        "uses": "Non-steroidal anti-inflammatory drug (NSAID) for severe pain, joint inflammation, and fever.",
        "dosage": "400mg after food every 6-8 hours as required.",
        "side_effects": "Stomach irritation, heart burn, nausea, risk of stomach ulcers.",
        "precautions": "Always take with or after food. Avoid if you have active stomach ulcers or asthma."
    },
    {
        "medicine_name": "Pantoprazole",
        "uses": "Proton pump inhibitor (PPI) for hyperacidity, acid reflux (GERD), and stomach ulcers.",
        "dosage": "400mg once daily in the morning, 30 minutes before breakfast.",
        "side_effects": "Headache, flatulence, mild diarrhea, abdominal pain.",
        "precautions": "Swallow tablet whole; do not crush or chew."
    },
    {
        "medicine_name": "Ranitidine",
        "uses": "Reduces stomach acid generation to relieve indigestion and heartburn.",
        "dosage": "150mg twice daily or 300mg at bedtime.",
        "side_effects": "Headache, constipation, dizziness.",
        "precautions": "Inform physician if taking antacids simultaneously."
    },
    {
        "medicine_name": "Metformin",
        "uses": "First-line oral medication to control blood sugar levels in Type 2 Diabetes.",
        "dosage": "500mg or 850mg once or twice daily with meals as prescribed.",
        "side_effects": "Metallic taste, stomach upset, loss of appetite, diarrhea.",
        "precautions": "Regular monitoring of kidney function and blood glucose required."
    },
    {
        "medicine_name": "Amlodipine",
        "uses": "Calcium channel blocker used to treat high blood pressure (hypertension) and angina.",
        "dosage": "5mg once daily, increased to 10mg if needed under medical supervision.",
        "side_effects": "Swelling in ankles/feet (edema), flushing, dizziness, fatigue.",
        "precautions": "Do not stop abruptly without consulting your physician."
    },
    {
        "medicine_name": "Ciprofloxacin",
        "uses": "Fluoroquinolone antibiotic for urinary tract infections (UTIs) and severe abdominal infections.",
        "dosage": "500mg twice daily for 5-7 days.",
        "side_effects": "Nausea, tendonitis risk, joint pain, headache.",
        "precautions": "Avoid dairy products or calcium-fortified drinks within 2 hours of taking."
    },
    {
        "medicine_name": "Metronidazole",
        "uses": "Antibacterial and antiprotozoal drug for stomach amoebiasis, loose motions, and dental infections.",
        "dosage": "400mg thrice daily after meals for 5 days.",
        "side_effects": "Metallic taste, dark urine, nausea, dry mouth.",
        "precautions": "Strictly avoid alcohol during treatment and for 48 hours after stopping."
    },
    {
        "medicine_name": "Disprin",
        "uses": "Soluble aspirin for acute headache, toothache, and early emergency management of chest pain.",
        "dosage": "1 tablet dissolved in half glass of water. Maximum 3 tablets daily.",
        "side_effects": "Gastric discomfort, bleeding risk, allergic reaction.",
        "precautions": "Contraindicated in children under 12 years and individuals with bleeding disorders."
    },
    {
        "medicine_name": "Montelukast",
        "uses": "Leukotriene receptor antagonist for allergic rhinitis, seasonal allergies, and asthma prevention.",
        "dosage": "10mg tablet once daily at bedtime.",
        "side_effects": "Headache, abdominal pain, fever, mood changes.",
        "precautions": "Not meant for acute asthma attacks; use rescue inhaler instead."
    },
    {
        "medicine_name": "Domperidone",
        "uses": "Antiemetic drug used to prevent nausea, vomiting, and feeling excessively full.",
        "dosage": "10mg 15-30 minutes before meals, up to 3 times a day.",
        "side_effects": "Dry mouth, headache, muscle cramps.",
        "precautions": "Caution in patients with cardiac arrhythmias or severe liver impairment."
    },
    {
        "medicine_name": "Levosalbutamol",
        "uses": "Bronchodilator for rapid relief of wheezing, shortness of breath, and asthma tightness.",
        "dosage": "As per inhaler puff instructions or 1-2mg syrup thrice daily as prescribed.",
        "side_effects": "Tremors, increased heart rate (palpitations), headache.",
        "precautions": "Use strictly according to doctor's dosage guidelines."
    },
    {
        "medicine_name": "Cough Syrup",
        "uses": "Symptomatic relief of dry cough or wet chesty cough depending on formulation.",
        "dosage": "5-10ml 3 times a day after food.",
        "side_effects": "Drowsiness, mild stomach upset.",
        "precautions": "Ensure correct formulation (Expectorant for wet cough, Suppressant for dry cough)."
    },
    {
        "medicine_name": "Antacid Gel",
        "uses": "Fast relief from heart burn, hyperacidity, gas, and stomach heaviness.",
        "dosage": "10-20ml 30 minutes after meals and before bedtime.",
        "side_effects": "Mild constipation or diarrhea.",
        "precautions": "Take at least 2 hours apart from other oral prescription medicines."
    },
    {
        "medicine_name": "Atorvastatin",
        "uses": "Statin drug to lower elevated LDL cholesterol and reduce cardiovascular event risks.",
        "dosage": "10mg to 40mg once daily at bedtime as prescribed.",
        "side_effects": "Muscle ache, elevated liver enzymes, indigestion.",
        "precautions": "Inform doctor immediately if experiencing unexplained muscle weakness."
    },
    {
        "medicine_name": "Telmisartan",
        "uses": "Angiotensin II receptor blocker (ARB) for controlling high blood pressure and protecting kidneys.",
        "dosage": "40mg once daily with or without food.",
        "side_effects": "Dizziness, sinus infection symptoms, back pain.",
        "precautions": "Do not take during pregnancy. Monitor blood potassium levels."
    },
    {
        "medicine_name": "Oral Rehydration Salt",
        "uses": "Restores electrolyte balance lost during heat stroke, heavy sweating, or stomach flu.",
        "dosage": "Dissolve contents in 1 liter clean water and sip throughout the day.",
        "side_effects": "None when diluted correctly.",
        "precautions": "Always use correct proportion of clean water."
    },
    {
        "medicine_name": "Paracetamol 500mg",
        "uses": "Standard strength fever reducer and mild analgesic.",
        "dosage": "1 tablet every 4-6 hours post food.",
        "side_effects": "Minimal at normal doses.",
        "precautions": "Maximum 8 tablets (4g) in 24 hours."
    },
    {
        "medicine_name": "Diclofenac",
        "uses": "Strong anti-inflammatory analgesic for joint pain, arthritis, sprains, and post-injury swelling.",
        "dosage": "50mg 2 to 3 times daily after food.",
        "side_effects": "Gastric irritation, elevated blood pressure, kidney stress.",
        "precautions": "Shortest duration of treatment recommended. Take with food."
    }
]


def seed_medicines(db: Session):
    """Populates database with 500 essential medicines from app/data/medicines.json or fallback list."""
    json_path = os.path.join(os.path.dirname(__file__), "..", "data", "medicines.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                med_list = json.load(f)
        except Exception as e:
            print(f"[Seeder Warning] Error reading medicines.json: {e}, falling back to default list.")
            med_list = SEED_MEDICINES
    else:
        med_list = SEED_MEDICINES

    existing_names = {name for (name,) in db.query(Medicine.medicine_name).all()}
    added_count = 0
    for med_data in med_list:
        if med_data["medicine_name"] not in existing_names:
            med = Medicine(
                medicine_name=med_data["medicine_name"],
                uses=med_data.get("uses", ""),
                dosage=med_data.get("dosage", ""),
                side_effects=med_data.get("side_effects", ""),
                precautions=med_data.get("precautions", "")
            )
            db.add(med)
            existing_names.add(med_data["medicine_name"])
            added_count += 1

    if added_count > 0:
        db.commit()
        print(f"Successfully seeded {added_count} new medicines (Total in DB: {db.query(Medicine).count()}).")
    else:
        print(f"Medicines table already fully up to date ({len(existing_names)} medicines).")
