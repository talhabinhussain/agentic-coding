import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models.user_models import User, UserCreate, UserRead, UserUpdate
from app.security import get_password_hash

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"model": UserRead, "description": "User created successfully."},
        400: {"model": dict, "description": "Validation or duplicate email error."},
        500: {"model": dict, "description": "Internal server error."},
    },
)
async def create_user(body: UserCreate, db: Session = Depends(get_session)):
    try:
        existing = db.exec(select(User).where(User.email == body.email)).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail={"error": "A user with this email already exists."},
            )

        new_user = User.model_validate(body)
        new_user.password = get_password_hash(body.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info("Created new user with email: %s", body.email)
        return new_user

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error while creating user")
        raise HTTPException(
            status_code=500,
            detail={"error": "An unexpected error occurred while creating the user."},
        )


@router.get(
    "/",
    response_model=list[UserRead],
    responses={
        200: {"model": list[UserRead], "description": "List of all users."},
        500: {"model": dict, "description": "Internal server error."},
    },
)
async def list_users(db: Session = Depends(get_session)):
    try:
        users = db.exec(select(User)).all()
        return users
    except Exception:
        logger.exception("Unexpected error while fetching users")
        raise HTTPException(
            status_code=500,
            detail={"error": "An unexpected error occurred while fetching users."},
        )


@router.get(
    "/{user_id}",
    response_model=UserRead,
    responses={
        200: {"model": UserRead, "description": "User found."},
        404: {"model": dict, "description": "User not found."},
        500: {"model": dict, "description": "Internal server error."},
    },
)
async def get_user(user_id: int, db: Session = Depends(get_session)):
    try:
        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail={"error": f"User with id {user_id} not found."},
            )
        return user
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error while fetching user %d", user_id)
        raise HTTPException(
            status_code=500,
            detail={"error": "An unexpected error occurred while fetching the user."},
        )


@router.put(
    "/{user_id}",
    response_model=UserRead,
    responses={
        200: {"model": UserRead, "description": "User updated successfully."},
        404: {"model": dict, "description": "User not found."},
        400: {"model": dict, "description": "Duplicate email or validation error."},
        500: {"model": dict, "description": "Internal server error."},
    },
)
async def update_user(
    user_id: int, body: UserUpdate, db: Session = Depends(get_session)
):
    try:
        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail={"error": f"User with id {user_id} not found."},
            )

        if body.email is not None and body.email != user.email:
            existing = db.exec(select(User).where(User.email == body.email)).first()
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail={"error": "Another user already has this email."},
                )

        update_data = body.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"] is not None:
            update_data["password"] = get_password_hash(update_data["password"])
        for key, value in update_data.items():
            setattr(user, key, value)

        db.add(user)
        db.commit()
        db.refresh(user)

        logger.info("Updated user with id: %d", user_id)
        return user

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error while updating user %d", user_id)
        raise HTTPException(
            status_code=500,
            detail={"error": "An unexpected error occurred while updating the user."},
        )


@router.delete(
    "/{user_id}",
    response_model=dict,
    responses={
        200: {"model": dict, "description": "User deleted successfully."},
        404: {"model": dict, "description": "User not found."},
        500: {"model": dict, "description": "Internal server error."},
    },
)
async def delete_user(user_id: int, db: Session = Depends(get_session)):
    try:
        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail={"error": f"User with id {user_id} not found."},
            )

        db.delete(user)
        db.commit()

        logger.info("Deleted user with id: %d", user_id)
        return {"message": f"User with id {user_id} has been deleted successfully."}

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error while deleting user %d", user_id)
        raise HTTPException(
            status_code=500,
            detail={"error": "An unexpected error occurred while deleting the user."},
        )
