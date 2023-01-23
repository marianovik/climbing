import os

CORS_ORIGINS = "*"
AUTH_TOKEN_DURATION = 10**7
SECRET_KEY = str(os.getenv("SECRET_KEY", "test"))
DATABASE_URL = os.getenv("DATABASE_URL")
