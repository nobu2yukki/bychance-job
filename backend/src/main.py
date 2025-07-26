from fastapi import FastAPI
from routers import question

app = FastAPI()


@app.get("/")
def read_root():
    return {"greet": "Hello, World"}

app.include_router(questions.router)