import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base, SessionLocal
from app.services.seeder import seed_medicines
from app.services.doctor_seeder import seed_doctors
from app.services.facility_seeder import seed_facilities

# Ensure tables and seed data are initialized
Base.metadata.create_all(bind=engine)
_db = SessionLocal()
try:
    seed_medicines(_db)
    seed_doctors(_db)
    seed_facilities(_db)
finally:
    _db.close()


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/health-status")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["data"]["status"] == "online"


def test_auth_and_profile_flow():
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    # 1. Register User
    register_payload = {
        "name": "Test User",
        "email": unique_email,
        "password": "password123"
    }
    response = client.post("/register", json=register_payload)
    assert response.status_code == 201, f"Register failed: {response.json()}"
    assert response.json()["success"] is True

    # 2. Login User
    login_payload = {
        "email": unique_email,
        "password": "password123"
    }
    response = client.post("/login", json=login_payload)
    assert response.status_code == 200, f"Login failed: {response.json()}"
    token_data = response.json()["data"]
    access_token = token_data["access_token"]
    assert access_token is not None

    headers = {"Authorization": f"Bearer {access_token}"}

    # 3. Get /me
    me_resp = client.get("/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["data"]["email"] == unique_email

    # 4. Create Health Profile
    profile_payload = {
        "age": 30,
        "gender": "Female",
        "blood_group": "B+",
        "allergies": "Pollen",
        "medical_history": "None"
    }
    prof_resp = client.post("/profile", json=profile_payload, headers=headers)
    assert prof_resp.status_code == 201
    assert prof_resp.json()["data"]["age"] == 30

    # 5. Get Health Profile
    get_prof_resp = client.get("/profile", headers=headers)
    assert get_prof_resp.status_code == 200
    assert get_prof_resp.json()["data"]["blood_group"] == "B+"

    # 6. Update Health Profile
    update_payload = {"age": 31, "medical_history": "Mild Asthma"}
    put_prof_resp = client.put("/profile", json=update_payload, headers=headers)
    assert put_prof_resp.status_code == 200
    assert put_prof_resp.json()["data"]["age"] == 31


def test_guest_chat():
    payload = {"message": "I have fever, cold, chest pain"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert "response" in json_data["data"]


def test_symptom_checker():
    payload = {"symptoms": ["Fever", "Cough"]}
    response = client.post("/symptom-check", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert "Common Viral Infection" in json_data["data"]["possible_condition"]


def test_medicine_search():
    # Exact search
    response = client.get("/medicine/Paracetamol")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["data"]["medicine_name"] == "Paracetamol"

    # Case insensitive search
    response_lower = client.get("/medicine/dolo 650")
    assert response_lower.status_code == 200
    assert response_lower.json()["data"]["medicine_name"] == "Dolo 650"

    # Invalid medicine search
    invalid_resp = client.get("/medicine/UnknownMedxyz")
    assert invalid_resp.status_code == 404
    assert invalid_resp.json()["success"] is False


def test_doctor_and_appointment_booking_flow():
    # 1. Fetch all seeded doctors
    doc_resp = client.get("/doctors")
    assert doc_resp.status_code == 200
    docs = doc_resp.json()["data"]
    assert len(docs) >= 8

    # 2. Filter by specialty
    cardio_resp = client.get("/doctors?specialty=Cardiologist")
    assert cardio_resp.status_code == 200
    cardio_docs = cardio_resp.json()["data"]
    assert len(cardio_docs) >= 1
    selected_doctor = cardio_docs[0]
    assert "Cardiologist" in selected_doctor["specialty"]

    # 3. Create a registered user for authenticated appointment booking
    user_email = f"patient_{uuid.uuid4().hex[:8]}@example.com"
    client.post("/register", json={"name": "Ramesh Patient", "email": user_email, "password": "password123"})
    login_resp = client.post("/login", json={"email": user_email, "password": "password123"})
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 4. Book an appointment
    appt_payload = {
        "doctor_id": selected_doctor["id"],
        "appointment_date": "2026-11-15",
        "time_slot": "10:30 AM",
        "patient_name": "Ramesh Patient",
        "patient_phone": "+91 98765 43210",
        "symptoms_summary": "Chest discomfort and high blood pressure follow-up"
    }
    book_resp = client.post("/appointments", json=appt_payload, headers=headers)
    assert book_resp.status_code == 201
    appt_data = book_resp.json()["data"]
    assert appt_data["doctor_id"] == selected_doctor["id"]
    assert appt_data["status"] == "confirmed"
    appt_id = appt_data["id"]

    # 5. List user appointments
    list_resp = client.get("/appointments", headers=headers)
    assert list_resp.status_code == 200
    user_appts = list_resp.json()["data"]
    assert len(user_appts) >= 1
    assert any(a["id"] == appt_id for a in user_appts)

    # 6. Retrieve single appointment
    single_resp = client.get(f"/appointments/{appt_id}", headers=headers)
    assert single_resp.status_code == 200
    assert single_resp.json()["data"]["id"] == appt_id

    # 7. Cancel the appointment
    cancel_resp = client.put(f"/appointments/{appt_id}/cancel", headers=headers)
    assert cancel_resp.status_code == 200
    assert cancel_resp.json()["data"]["status"] == "cancelled"


def test_prescription_ocr_scanner():
    import io
    # 1. Test with valid PNG image bytes (1x1 pixel)
    png_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc`\x00\x00\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82'
    files = {"file": ("test_prescription.png", io.BytesIO(png_bytes), "image/png")}
    response = client.post("/prescription/scan", files=files)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert "extracted_medicines" in json_data["data"]
    assert len(json_data["data"]["extracted_medicines"]) >= 1
    first_med = json_data["data"]["extracted_medicines"][0]
    assert "medicine_name" in first_med
    assert "dosage" in first_med

    # 2. Test invalid MIME rejection
    text_files = {"file": ("test.txt", io.BytesIO(b"Hello medical world"), "text/plain")}
    invalid_resp = client.post("/prescription/scan", files=text_files)
    assert invalid_resp.status_code == 400
    assert invalid_resp.json()["success"] is False


def test_medication_reminder_crud():
    # 1. Register and login test user
    user_email = f"reminder_user_{uuid.uuid4().hex[:8]}@example.com"
    client.post("/register", json={"name": "Reminder Patient", "email": user_email, "password": "password123"})
    login_resp = client.post("/login", json={"email": user_email, "password": "password123"})
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create reminder
    reminder_payload = {
        "medicine_name": "Dolo 650",
        "dosage": "1 tablet",
        "frequency": "Thrice daily",
        "reminder_time": "08:00 AM",
        "is_active": True,
        "notes": "Take after meals with water"
    }
    create_resp = client.post("/reminders", json=reminder_payload, headers=headers)
    assert create_resp.status_code == 201
    r_data = create_resp.json()["data"]
    assert r_data["medicine_name"] == "Dolo 650"
    assert r_data["reminder_time"] == "08:00 AM"
    reminder_id = r_data["id"]

    # 3. List reminders
    list_resp = client.get("/reminders", headers=headers)
    assert list_resp.status_code == 200
    reminders = list_resp.json()["data"]
    assert len(reminders) >= 1
    assert any(r["id"] == reminder_id for r in reminders)

    # 4. Get due reminders
    due_resp = client.get("/reminders/due", headers=headers)
    assert due_resp.status_code == 200
    due_list = due_resp.json()["data"]
    assert any(r["id"] == reminder_id for r in due_list)

    # 5. Update reminder
    update_payload = {"reminder_time": "09:00 AM", "dosage": "2 tablets"}
    update_resp = client.put(f"/reminders/{reminder_id}", json=update_payload, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["data"]["reminder_time"] == "09:00 AM"

    # 6. Delete reminder
    del_resp = client.delete(f"/reminders/{reminder_id}", headers=headers)
    assert del_resp.status_code == 200
    assert del_resp.json()["data"]["deleted_id"] == reminder_id


def test_nearby_facilities_geo_search():
    # 1. Nearby facilities search around Barasat GPS (22.7214, 88.4812) with 10km radius
    nearby_resp = client.get("/facilities/nearby?lat=22.7214&lng=88.4812&radius_km=10.0")
    assert nearby_resp.status_code == 200
    data = nearby_resp.json()["data"]
    assert len(data) >= 3
    # Check that results are sorted ascending by distance
    distances = [item["distance_km"] for item in data]
    assert distances == sorted(distances)
    # The closest one should have distance_km == 0.0 or near 0
    assert distances[0] <= 1.0

    # 2. Filter by facility_type (PHC)
    phc_resp = client.get("/facilities/nearby?lat=22.7214&lng=88.4812&radius_km=15.0&facility_type=PHC")
    assert phc_resp.status_code == 200
    phc_data = phc_resp.json()["data"]
    assert len(phc_data) >= 1
    for f in phc_data:
        assert "PHC" in f["facility_type"]

    # 3. Search facilities by district name
    district_resp = client.get("/facilities/search?district=North 24 Parganas")
    assert district_resp.status_code == 200
    dist_facilities = district_resp.json()["data"]
    assert len(dist_facilities) >= 4
    for f in dist_facilities:
        assert "North 24 Parganas" in f["district"]

    # 4. Search by facility ID
    first_id = dist_facilities[0]["id"]
    single_resp = client.get(f"/facilities/{first_id}")
    assert single_resp.status_code == 200
    assert single_resp.json()["data"]["id"] == first_id




