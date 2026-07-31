import os

JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 3600
