import logging

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.database import get_session
from app.auth.schemas import LoginRequest, LoginResponse, ErrorResponse
from app.auth.service import authenticate
from app.auth.jwt import create_access_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post(
    "/login",
    responses={
        200: {"model": LoginResponse},
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def login(body: LoginRequest, db: Session = Depends(get_session)):
    try:
        user = authenticate(body.email, body.password, db)

        if user is None:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid email or password."},
            )

        token = create_access_token(sub=str(user.id), email=user.email)
        # print(f" ===>` {token}")
        return LoginResponse(token=token, expires_in=3600)

    except Exception:
        logger.exception("Unexpected error during login")
        return JSONResponse(
            status_code=500,
            content={"error": "An unexpected error occurred."},
        )
