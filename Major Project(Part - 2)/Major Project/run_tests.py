from tests.test_backend import (
    test_root_endpoint,
    test_auth_and_profile_flow,
    test_guest_chat,
    test_symptom_checker,
    test_medicine_search,
    test_doctor_and_appointment_booking_flow,
    test_prescription_ocr_scanner,
    test_medication_reminder_crud,
    test_nearby_facilities_geo_search
)

if __name__ == "__main__":
    print("Running IndicHealth AI Backend Test Suite...")
    test_root_endpoint()
    print("[OK] Root Health Check Passed")
    test_auth_and_profile_flow()
    print("[OK] Registration, Login, JWT Auth, and Health Profile CRUD Passed")
    test_guest_chat()
    print("[OK] Guest Mode AI Chat (Unauthenticated) Passed")
    test_symptom_checker()
    print("[OK] Rule-based Symptom Assessment Engine Passed")
    test_medicine_search()
    print("[OK] Medicine Information Search & Fallback Passed")
    test_doctor_and_appointment_booking_flow()
    print("[OK] Doctor Directory & Appointment Booking Lifecycle Passed")
    test_prescription_ocr_scanner()
    print("[OK] Prescription OCR & Vision AI Scanner Passed")
    test_medication_reminder_crud()
    print("[OK] Medication & Pill Reminder CRUD Passed")
    test_nearby_facilities_geo_search()
    print("[OK] Nearby PHC, Clinic & Pharmacy Geo-Search Passed")
    print("\nALL BACKEND TESTS PASSED SUCCESSFULLY!")




