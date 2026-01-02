from decouple import config, Csv

# Security settings
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES", default="30"))

# Database settings
DATABASE_URL = config(
    "DATABASE_URL", "postgresql://postgres:qpzm@localhost:5432/clozeencounters"
)

# API settings
CORS_ORIGINS = config(
    "CORS_ORIGINS", default="http://localhost:5173,http://localhost:8000", cast=Csv()
)
