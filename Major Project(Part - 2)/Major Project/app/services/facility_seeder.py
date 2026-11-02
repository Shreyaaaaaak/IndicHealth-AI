from sqlalchemy.orm import Session
from app.models.facility import HealthcareFacility

SEED_FACILITIES = [
    {
        "name": "Barasat Government Primary Health Center (PHC)",
        "facility_type": "PHC",
        "address": "KNC Road, Barasat",
        "district": "North 24 Parganas",
        "state": "West Bengal",
        "contact_number": "+91 33 2584 1001",
        "latitude": 22.7214,
        "longitude": 88.4812,
        "emergency_24x7": True,
        "operating_hours": "Open 24 Hours"
    },
    {
        "name": "Habra Community Health Center (CHC)",
        "facility_type": "CHC",
        "address": "Jessore Road, Habra",
        "district": "North 24 Parganas",
        "state": "West Bengal",
        "contact_number": "+91 33 2584 2002",
        "latitude": 22.8364,
        "longitude": 88.6548,
        "emergency_24x7": True,
        "operating_hours": "Open 24 Hours"
    },
    {
        "name": "Madhyamgram Rural Primary Health Unit",
        "facility_type": "PHC",
        "address": "Sodepur Road, Madhyamgram",
        "district": "North 24 Parganas",
        "state": "West Bengal",
        "contact_number": "+91 33 2584 3003",
        "latitude": 22.7001,
        "longitude": 88.4552,
        "emergency_24x7": False,
        "operating_hours": "08:00 AM - 08:00 PM"
    },
    {
        "name": "Barasat District Hospital & Trauma Center",
        "facility_type": "Hospital",
        "address": "Hospital Road, Barasat",
        "district": "North 24 Parganas",
        "state": "West Bengal",
        "contact_number": "+91 33 2584 4004",
        "latitude": 22.7265,
        "longitude": 88.4795,
        "emergency_24x7": True,
        "operating_hours": "Open 24 Hours"
    },
    {
        "name": "Jan-Aushadhi 24x7 Medical & Generic Pharmacy",
        "facility_type": "Pharmacy",
        "address": "Station Road Market, Barasat",
        "district": "North 24 Parganas",
        "state": "West Bengal",
        "contact_number": "+91 98311 22334",
        "latitude": 22.7230,
        "longitude": 88.4820,
        "emergency_24x7": True,
        "operating_hours": "Open 24 Hours"
    },
    {
        "name": "Rajarhat Primary Health Center",
        "facility_type": "PHC",
        "address": "Chinar Park, Rajarhat Main Road",
        "district": "North 24 Parganas",
        "state": "West Bengal",
        "contact_number": "+91 33 2573 5005",
        "latitude": 22.6245,
        "longitude": 88.4410,
        "emergency_24x7": True,
        "operating_hours": "Open 24 Hours"
    },
    {
        "name": "Salt Lake Sub-District Hospital",
        "facility_type": "Hospital",
        "address": "DD Block, Sector 1, Salt Lake",
        "district": "Kolkata",
        "state": "West Bengal",
        "contact_number": "+91 33 2337 6006",
        "latitude": 22.5855,
        "longitude": 88.4111,
        "emergency_24x7": True,
        "operating_hours": "Open 24 Hours"
    },
    {
        "name": "Howrah District General Hospital & PHC Cell",
        "facility_type": "Hospital",
        "address": "Biplabi Haren Ghosh Sarani, Howrah",
        "district": "Howrah",
        "state": "West Bengal",
        "contact_number": "+91 33 2638 7007",
        "latitude": 22.5892,
        "longitude": 88.3245,
        "emergency_24x7": True,
        "operating_hours": "Open 24 Hours"
    },
    {
        "name": "Sonarpur Rural Community Health Center",
        "facility_type": "CHC",
        "address": "Station Road, Sonarpur",
        "district": "South 24 Parganas",
        "state": "West Bengal",
        "contact_number": "+91 33 2434 8008",
        "latitude": 22.4412,
        "longitude": 88.4310,
        "emergency_24x7": True,
        "operating_hours": "Open 24 Hours"
    },
    {
        "name": "Serampore Walsh Sub-Divisional Hospital",
        "facility_type": "Hospital",
        "address": "GT Road, Serampore",
        "district": "Hooghly",
        "state": "West Bengal",
        "contact_number": "+91 33 2662 9009",
        "latitude": 22.7511,
        "longitude": 88.3412,
        "emergency_24x7": True,
        "operating_hours": "Open 24 Hours"
    }
]


def seed_facilities(db: Session):
    """Populates database with initial verified healthcare facilities if table is empty."""
    existing_count = db.query(HealthcareFacility).count()
    if existing_count == 0:
        for fac_data in SEED_FACILITIES:
            facility = HealthcareFacility(**fac_data)
            db.add(facility)
        db.commit()
        print(f"Successfully seeded {len(SEED_FACILITIES)} healthcare facilities.")
