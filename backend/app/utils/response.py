"""
API Response Utilities
"""

from typing import Any, Dict, Optional
from fastapi import status
from fastapi.responses import JSONResponse


def success_response(data: Any = None, message: str = "Success", status_code: int = status.HTTP_200_OK) -> JSONResponse:
    """Create a success response"""
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    return JSONResponse(content=response, status_code=status_code)


def error_response(message: str = "Error", status_code: int = status.HTTP_400_BAD_REQUEST, details: Optional[Dict] = None) -> JSONResponse:
    """Create an error response"""
    response = {
        "success": False,
        "message": message,
        "details": details or {}
    }
    return JSONResponse(content=response, status_code=status_code)
