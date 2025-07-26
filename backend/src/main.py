from fastapi import FastAPI
from src.routers import question, result, session, swipe

app = FastAPI()

app.include_router(question.router)
app.include_router(swipe.router)
app.include_router(session.router)
app.include_router(result.router)

# @app.get("/")
# def read_root():
#     return {"greet": "Hello, World"}
