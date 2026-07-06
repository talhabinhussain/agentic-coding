from typing import Optional

from sqlmodel import Field, SQLModel, VARCHAR, Column, Integer, Identity


class User(SQLModel, table=True):
    """A registered user of the app."""

    id: Optional[int] = Field(
        default=None, sa_column=Column(Integer, Identity(), primary_key=True)
    )
    name: str = Field(default=None, sa_column=Column(VARCHAR(225), nullable=False))
    email: str = Field(sa_column=Column(VARCHAR(225), unique=True, nullable=False))

    password: str = Field(sa_column=Column(VARCHAR(225), nullable=False))
    is_employed: bool = Field(default=False)
