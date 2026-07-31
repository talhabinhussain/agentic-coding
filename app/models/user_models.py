from typing import Optional

from sqlmodel import Field, SQLModel, VARCHAR, Column, Integer, Identity, FLOAT


class User(SQLModel, table=True):
    """A registered user of the app."""

    id: Optional[int] = Field(
        default=None, sa_column=Column(Integer, Identity(), primary_key=True)
    )
    name: str = Field(default=None, sa_column=Column(VARCHAR(225), nullable=False))
    email: str = Field(sa_column=Column(VARCHAR(225), unique=True, nullable=False))

    password: str = Field(sa_column=Column(VARCHAR(225), nullable=False))
    is_employed: bool = Field(default=False)


class UserCreate(SQLModel):
    """Schema for creating a new user."""

    name: str
    email: str
    password: str
    is_employed: bool = False


class UserUpdate(SQLModel):
    """Schema for updating an existing user. All fields are optional."""

    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_employed: Optional[bool] = None


class UserRead(SQLModel):
    """Schema for reading user data. Excludes sensitive fields."""

    id: int
    name: str
    email: str
    is_employed: bool


class Expense(SQLModel, table=True):
    """An expense record with category breakdown."""

    id: Optional[int] = Field(
        default=None, sa_column=Column(Integer, Identity(), primary_key=True)
    )
    user_id: int = Field(sa_column=Column(Integer, nullable=False))
    amount: float = Field(sa_column=Column(FLOAT, nullable=False))
    month: str = Field(sa_column=Column(VARCHAR(50), nullable=False))
    category: str = Field(sa_column=Column(VARCHAR(225), nullable=False))
    sub_category: str = Field(sa_column=Column(VARCHAR(225), nullable=False))
