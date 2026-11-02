from sqlalchemy.orm import Session
from app.models.doctor import Doctor

SEED_DOCTORS = [
    {
        "name": "Dr. Ananya Sen",
        "specialty": "General Physician",
        "qualification": "MBBS, MD (Internal Medicine)",
        "experience_years": 12,
        "hospital_name": "District Civil Hospital & Rural Health Care Center",
        "location": "North 24 Parganas, West Bengal",
        "contact_phone": "+91 98301 11223",
        "consultation_fee": 0,
        "available_days": "Mon,Tue,Wed,Thu,Fri,Sat",
        "available_time": "09:00 AM - 01:00 PM, 05:00 PM - 08:00 PM"
    },
    {
        "name": "Dr. Rajesh Kumar Verma",
        "specialty": "Cardiologist",
        "qualification": "MBBS, MD, DM (Cardiology)",
        "experience_years": 16,
        "hospital_name": "Apex Heart & Emergency Care Institute",
        "location": "Kolkata, West Bengal",
        "contact_phone": "+91 98302 22334",
        "consultation_fee": 300,
        "available_days": "Mon,Wed,Fri",
        "available_time": "10:00 AM - 02:00 PM, 06:00 PM - 08:30 PM"
    },
    {
        "name": "Dr. Priya Deshmukh",
        "specialty": "Dermatologist",
        "qualification": "MBBS, DVD, MD (Dermatology)",
        "experience_years": 9,
        "hospital_name": "Skin & Allergy Care Community Clinic",
        "location": "Hooghly, West Bengal",
        "contact_phone": "+91 98303 33445",
        "consultation_fee": 150,
        "available_days": "Tue,Thu,Sat",
        "available_time": "11:00 AM - 03:00 PM"
    },
    {
        "name": "Dr. Amitav Banerjee",
        "specialty": "Gastroenterologist",
        "qualification": "MBBS, MD, DNB (Gastroenterology)",
        "experience_years": 14,
        "hospital_name": "Sub-Divisional Hospital & Gastro Care Unit",
        "location": "Barasat, West Bengal",
        "contact_phone": "+91 98304 44556",
        "consultation_fee": 200,
        "available_days": "Mon,Tue,Thu,Fri",
        "available_time": "09:30 AM - 01:30 PM"
    },
    {
        "name": "Dr. Sunita Roy",
        "specialty": "Pulmonologist",
        "qualification": "MBBS, DTCD, MD (Chest & Respiratory Diseases)",
        "experience_years": 11,
        "hospital_name": "National Chest & Respiratory Wellness Center",
        "location": "Howrah, West Bengal",
        "contact_phone": "+91 98305 55667",
        "consultation_fee": 200,
        "available_days": "Mon,Wed,Fri,Sat",
        "available_time": "10:00 AM - 02:00 PM, 05:30 PM - 07:30 PM"
    },
    {
        "name": "Dr. Ramesh Nair",
        "specialty": "Pediatrician",
        "qualification": "MBBS, DCH, MD (Pediatrics)",
        "experience_years": 15,
        "hospital_name": "Maternal & Child Health Care PHC Center",
        "location": "South 24 Parganas, West Bengal",
        "contact_phone": "+91 98306 66778",
        "consultation_fee": 0,
        "available_days": "Mon,Tue,Wed,Thu,Fri,Sat",
        "available_time": "08:30 AM - 12:30 PM, 04:30 PM - 07:30 PM"
    },
    {
        "name": "Dr. Vikramaditya Rathore",
        "specialty": "Orthopedic Specialist",
        "qualification": "MBBS, MS (Orthopedics)",
        "experience_years": 13,
        "hospital_name": "Joint & Trauma Community Hospital",
        "location": "Nadia, West Bengal",
        "contact_phone": "+91 98307 77889",
        "consultation_fee": 150,
        "available_days": "Mon,Wed,Sat",
        "available_time": "10:30 AM - 02:30 PM"
    },
    {
        "name": "Dr. Meenakshi Sundaram",
        "specialty": "ENT Specialist",
        "qualification": "MBBS, MS (ENT)",
        "experience_years": 10,
        "hospital_name": "Govt. Sub-District Hospital & ENT Clinic",
        "location": "Kolkata, West Bengal",
        "contact_phone": "+91 98308 88990",
        "consultation_fee": 100,
        "available_days": "Tue,Wed,Fri",
        "available_time": "11:00 AM - 03:30 PM"
    }
]


def seed_doctors(db: Session):
    """Populates database with initial verified doctors across specialties if table is empty."""
    existing_count = db.query(Doctor).count()
    if existing_count == 0:
        for doc_data in SEED_DOCTORS:
            doctor = Doctor(**doc_data)
            db.add(doctor)
        db.commit()
        print(f"Successfully seeded {len(SEED_DOCTORS)} verified doctors.")
