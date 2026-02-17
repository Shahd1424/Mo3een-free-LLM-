from fastapi import HTTPException
from app.schemas.responses import ErrorResponse


def internal_error(request_id: str, code: str, message: str):
    """
    Standard internal server error handler used in Mo3een (Qwen Free Version).
    Returns a clean JSON error format identical to the project's structure.
    """
    error = ErrorResponse(
        code=code,
        message=message,
        request_id=request_id
    )

    raise HTTPException(
        status_code=500,
        detail=error.dict()
    )
