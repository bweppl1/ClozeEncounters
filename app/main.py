from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI(
    title="Cloze Encounters",
    description="CLI cloze style spanish learning application",
    version="3.0.0",
)

# !!!! MAKE .ENV !!!!!
# database_url = "postgresql://postgres:qpzm/localhost/clozeencounters"
# engine = create_engine(database_url)
#
# # session factory using the engine
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/")
def test_function():
    return {"Hello": "world!"}
