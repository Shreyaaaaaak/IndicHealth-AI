from typing import Any, Optional
from fastapi.responses import JSONResponse


def success_response(data: Any = None, status_code: int = 200) -> JSONResponse:
    """Returns a standardized success JSON response."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "data": data
        }
    )


def error_response(message: str, status_code: int = 400) -> JSONResponse:
    """Returns a standardized error JSON response."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message
        }
    )
