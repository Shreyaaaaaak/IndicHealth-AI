from fastapi import APIRouter, UploadFile, File
from app.services.vision_service import analyze_prescription_image
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/prescription", tags=["Prescription OCR & Vision AI"])

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/jpg"
}

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


@router.post("/scan", summary="Scan and extract medicine details from a prescription photo")
async def scan_prescription(file: UploadFile = File(...)):
    """
    Accepts an uploaded image file (prescription or medicine strip)
    and utilizes Gemini Vision AI to extract medicine names, dosages,
    frequencies, duration, and doctor instructions.
    """
    # 1. Validate MIME type
    content_type = file.content_type or "image/jpeg"
    if content_type.lower() not in ALLOWED_MIME_TYPES:
        return error_response(
            message=f"Unsupported file format '{content_type}'. Please upload an image file (JPEG, PNG, or WEBP).",
            status_code=400
        )

    # 2. Read image bytes and validate size
    image_bytes = await file.read()
    if len(image_bytes) == 0:
        return error_response(message="Uploaded file is empty. Please select a valid image.", status_code=400)

    if len(image_bytes) > MAX_FILE_SIZE_BYTES:
        return error_response(
            message=f"File exceeds maximum allowed size of 10MB. Current size: {len(image_bytes) / (1024*1024):.1f}MB",
            status_code=400
        )

    # 3. Process image with Vision AI
    result = await analyze_prescription_image(image_bytes, mime_type=content_type)
    return success_response(data=result)
