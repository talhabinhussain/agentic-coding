import logging

from sqlmodel import Session, select

from app.models.user_models import User
from app.security import verify_password

logger = logging.getLogger(__name__)


def authenticate(email: str, password: str, db: Session) -> User | None:
    normalized_email = email.strip().lower()
    statement = select(User).where(User.email == normalized_email)
    user = db.exec(statement).first()

    if user is None:
        logger.warning("Login attempt for unknown email: %s", normalized_email)
        return None

    if not verify_password(password, user.password):
        logger.warning("Wrong password attempt for email: %s", normalized_email)
        return None

    logger.info("Successful login for email: %s", normalized_email)
    return user
