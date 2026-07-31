import re

from pydantic import BaseModel, field_validator

EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
MAX_INPUT_LENGTH = 1024


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Email is required.")
        if len(stripped) > MAX_INPUT_LENGTH:
            raise ValueError("Email must not exceed 1024 characters.")
        if not EMAIL_REGEX.match(stripped):
            raise ValueError("Invalid email format.")
        return stripped.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v:
            raise ValueError("Password is required.")
        if len(v) > MAX_INPUT_LENGTH:
            raise ValueError("Password must not exceed 1024 characters.")
        return v


class LoginResponse(BaseModel):
    token: str
    expires_in: int = 3600


class ErrorDetail(BaseModel):
    field: str
    message: str


class ErrorResponse(BaseModel):
    error: str
    details: list[ErrorDetail] | None = None
