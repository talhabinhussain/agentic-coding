from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


# print(get_password_hash("talha123\n"))
# print(get_password_hash("123"))


hash_password = "$2b$12$8RYmsbf94YAUOo0Q3iQroemR69pmYoSW1KrmuBdIWd8VSjrUWSb3a"


print(verify_password("talha123", hash_password))
