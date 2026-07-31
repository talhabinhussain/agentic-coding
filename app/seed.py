# import argparse
# import sys
# from pathlib import Path
# from typing import Any

# from sqlmodel import Session, select

# PROJECT_ROOT = Path(__file__).resolve().parent.parent
# if str(PROJECT_ROOT) not in sys.path:
#     sys.path.insert(0, str(PROJECT_ROOT))

# from app.database import create_db_and_tables, engine
# from app.models.models import User
# from app.security import get_password_hash

# # Define dummy users
# DUMMY_USERS = [
#     {
#         "name": "Alice Vance",
#         "email": "alice.vance@example.com",
#         "password": "securepassword123",
#         "is_employed": True,
#     },
#     {
#         "name": "Bob Miller",
#         "email": "bob.miller@example.com",
#         "password": "employeebob456",
#         "is_employed": False,
#     },
#     {
#         "name": "Charlie Smith",
#         "email": "charlie.smith@example.com",
#         "password": "charliepass789",
#         "is_employed": True,
#     },
#     {
#         "name": "Diana Prince",
#         "email": "diana.prince@example.com",
#         "password": "wonderwoman2026",
#         "is_employed": False,
#     },
# ]

# DEFAULT_USER = {
#     "name": "Seeded User",
#     "email": "seeded.user@example.com",
#     "password": "changeme123",
#     "is_employed": False,
# }


# def seed_user(user_data: dict[str, Any]) -> User | None:
#     """Insert a single user into the database if the email does not already exist."""
#     create_db_and_tables()

#     with Session(engine) as session:
#         statement = select(User).where(User.email == user_data["email"])
#         existing_user = session.exec(statement).first()

#         if existing_user:
#             print(f"[Skip] User with email {user_data['email']} already exists.")
#             return existing_user

#         hashed_pw = get_password_hash(user_data["password"])
#         new_user = User(
#             name=user_data["name"],
#             email=user_data["email"],
#             password=hashed_pw,
#             is_employed=user_data["is_employed"],
#         )
#         session.add(new_user)
#         session.commit()
#         session.refresh(new_user)
#         print(f"[Added] Created user: {new_user.name}")
#         return new_user


# def seed_data(users: list[dict[str, Any]] | None = None) -> list[User]:
#     """Seed the database with dummy users if they don't already exist."""
#     print("Initializing database tables...")
#     create_db_and_tables()

#     print("Seeding dummy users...")
#     created_users: list[User] = []
#     with Session(engine) as session:
#         for user_data in users or DUMMY_USERS:
#             statement = select(User).where(User.email == user_data["email"])
#             existing_user = session.exec(statement).first()

#             if existing_user:
#                 print(f"[Skip] User with email {user_data['email']} already exists.")
#             else:
#                 hashed_pw = get_password_hash(user_data["password"])
#                 new_user = User(
#                     name=user_data["name"],
#                     email=user_data["email"],
#                     password=hashed_pw,
#                     is_employed=user_data["is_employed"],
#                 )
#                 session.add(new_user)
#                 created_users.append(new_user)
#                 print(f"[Added] Created user: {user_data['name']}")

#         session.commit()
#     print("Database seeding completed successfully!")
#     return created_users


# def build_parser() -> argparse.ArgumentParser:
#     parser = argparse.ArgumentParser(description="Seed a user into the SQLite database")
#     parser.add_argument("--name", default=None, help="User name")
#     parser.add_argument("--email", default=None, help="User email")
#     parser.add_argument("--password", default=None, help="Plain-text password")
#     parser.add_argument(
#         "--is-employed",
#         action="store_true",
#         help="Set the user as employed",
#     )
#     return parser


# def main() -> None:
#     parser = build_parser()
#     args = parser.parse_args()

#     user_data = {
#         "name": args.name or DEFAULT_USER["name"],
#         "email": args.email or DEFAULT_USER["email"],
#         "password": args.password or DEFAULT_USER["password"],
#         "is_employed": args.is_employed,
#     }
#     seed_user(user_data)


# if __name__ == "__main__":
#     main()
