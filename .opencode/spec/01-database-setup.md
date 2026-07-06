# 01 - Database Setup

## Objective
Set up the SQLite database for this FastAPI app using SQLModel. Define the table(s), create the database file, and seed it with dummy data so the rest of the app can be built and tested against real data.

## Schema
This app uses a single `User` table with the following fields:

| Field         | Type     | Constraints                          |
|---------------|----------|---------------------------------------|
| `id`          | `int`    | primary key, auto-generated            |
| `name`        | `str`    | required                               |
| `email`       | `str`    | required, unique                       |
| `password`    | `str`    | required (store as a hashed string, not plain text — see Security Notes) |
| `is_employed` | `bool`   | required, default `False`              |


## Before You Start — Plan First
Before writing any code, write a short plan covering:
1. What table(s) are needed and why (based on the app's requirements).
2. The fields for each table, their types, and constraints (primary key, required/optional, defaults, foreign keys if multiple tables).
3. Relationships between tables, if any (one-to-many, many-to-many).
4. How many dummy rows you'll seed and what they'll represent.

Save this plan as a short section at the top of `spec/01-database-setup.md` (append below this instruction, or in a `## Plan` section) before moving to implementation.

## Plan

### 1. Exact Files to Create/Modify
- **`pyproject.toml`**: Add `passlib` (with `bcrypt` scheme) and `bcrypt` dependencies.
- **`app/models.py`**: Implement the `User` SQLModel.
- **`app/database.py`**: Configure the SQLite database engine, session retrieval, and tables creation.
- **`app/security.py`**: Define password hashing and verification utilities.
- **`app/seed.py`**: Script to safely seed dummy users.

### 2. User Model Schema Implementation
We will implement the `User` model using `SQLModel` with the following attributes:
- `id`: `Optional[int] = Field(default=None, primary_key=True)` (auto-generated primary key)
- `name`: `str` (required)
- `email`: `str = Field(unique=True, index=True)` (required, unique, indexed)
- `password`: `str` (required, stores bcrypt-hashed password)
- `is_employed`: `bool = Field(default=False)` (required, defaults to `False`)

### 3. Password Hashing Strategy
We will use `passlib.context.CryptContext` with the `bcrypt` hashing scheme in `app/security.py`:
- `get_password_hash(password: str) -> str` uses `pwd_context.hash(password)`.
- `verify_password(plain_password: str, hashed_password: str) -> bool` uses `pwd_context.verify(...)`.
- Seeded passwords will be hashed before being saved in the database.

### 4. Seed Data Details
We will seed exactly 4 unique, realistic dummy users:
1. **Alice Vance** (`alice.vance@example.com`, password: `securepassword123`, `is_employed=True`)
2. **Bob Miller** (`bob.miller@example.com`, password: `employeebob456`, `is_employed=False`)
3. **Charlie Smith** (`charlie.smith@example.com`, password: `charliepass789`, `is_employed=True`)
4. **Diana Prince** (`diana.prince@example.com`, password: `wonderwoman2026`, `is_employed=False`)

### 5. Idempotent / Re-runnable Seed Script
To ensure safety on repeated execution:
- Before inserting any user, the script executes `select(User).where(User.email == user_data.email)`.
- If the user exists, it skips addition and logs `[Skip] User with email {email} already exists`.
- If not, it hashes the password, instantiates the `User`, and calls `session.add()`.
- Finally, it commits the changes.

### 6. Assumptions and Decisions
- **Dependency Tooling**: We assume `uv` is the package manager because `uv.lock` is present, so we will use it to add `passlib` and `bcrypt`.
- **Database Location**: We will use `sqlite:///database.db` relative to the root directory.
- **Separation of Concerns**: We choose to create a separate `app/security.py` file to handle hashing logic cleanly and make it reusable for future login/signup flows.

## Tech Requirements
- **ORM**: SQLModel (not raw SQLAlchemy, not Pydantic-only models)
- **Database**: SQLite, stored as a local file, e.g. `database.db`
- **Framework**: FastAPI (this DB layer will be imported by FastAPI routes later)

## Implementation Steps

### 1. Project structure
Create the following files (adjust names if the project already has a different layout, but keep concerns separated):
```
app/
├── models.py       # SQLModel table definitions
├── database.py     # engine, session, init_db logic
└── seed.py         # script to populate dummy data
```

### 2. Define the model(s) — `app/models.py`
- Use `SQLModel` with `table=True` for a `User` model.
- Fields: `id` (`Optional[int]`, `primary_key=True`, `default=None`), `name` (`str`), `email` (`str`, `unique=True`, `index=True`), `password` (`str`), `is_employed` (`bool`, `default=False`).
- Example:
  ```python
  from typing import Optional
  from sqlmodel import SQLModel, Field

  class User(SQLModel, table=True):
      """A registered user of the app."""
      id: Optional[int] = Field(default=None, primary_key=True)
      name: str
      email: str = Field(unique=True, index=True)
      password: str
      is_employed: bool = Field(default=False)
  ```
- Add a docstring explaining what the table represents.

### 3. Set up the engine and session — `app/database.py`
- Create the SQLite engine:
  ```python
  from sqlmodel import SQLModel, create_engine, Session

  sqlite_url = "sqlite:///database.db"
  engine = create_engine(sqlite_url, echo=True)
  ```
- Add a `create_db_and_tables()` function that calls `SQLModel.metadata.create_all(engine)`.
- Add a `get_session()` generator function (for FastAPI's `Depends`) that yields a `Session(engine)`.

### 4. Seed dummy data — `app/seed.py`
- Import the `User` model and the engine/session from the two files above.
- On run, call `create_db_and_tables()` first.
- Insert **3–5 `User` rows** with realistic dummy data (real-looking names and emails, mix of `is_employed=True`/`False`), then `commit()`.
- Passwords must be hashed before insertion, not stored in plain text (see Security Notes below).
- Wrap the seeding logic in `if __name__ == "__main__":` so it only runs when executed directly (`python -m app.seed`).
- Make the script safe to re-run (e.g. check if a user with that email already exists before inserting) so it doesn't duplicate rows on repeated runs.

### 5. Verify
- Run the seed script.
- Confirm `database.db` is created in the project root.
- Query the table(s) (a quick throwaway script or `sqlite3 database.db "SELECT * FROM <table>;"`) and confirm the dummy rows are present with correct types.

## Deliverables
- [x] `app/models.py` with table definition(s)
- [x] `app/database.py` with engine, session dependency, and `create_db_and_tables()`
- [x] `app/seed.py` that creates tables and inserts dummy data, safely re-runnable
- [x] `database.db` file generated and populated
- [x] Plan section written at the top of this file describing the schema decisions made

## Security Notes
- Never store plain-text passwords, even for dummy/seed data. Use a hashing library such as `passlib[bcrypt]` or `bcrypt` directly.
- Example:
  ```python
  from passlib.context import CryptContext

  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  hashed = pwd_context.hash("plain_password")
  ```
- This hashing utility can live in `app/database.py` or a small `app/security.py` if you want it reusable later for login/signup routes.

## Notes
- Do not hardcode the database logic inside FastAPI route files — keep it in `database.py`/`models.py` so it can be imported cleanly later.
- Keep dummy data realistic (real-looking names, emails) rather than `"test1"`, `"test2"` placeholders — it makes manual testing easier later.
- `email` must be unique — the seed script should not attempt to insert duplicate emails on repeated runs.
