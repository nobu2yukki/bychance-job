from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.utils.session import get_session_id
from src.utils.session_store import ensure_session, get_session_data

router = APIRouter()

# モックの質問データ
DUMMY_QUESTIONS = [
    {
        "id": "q1",
        "text": "アルバイトを探すうえで一番大事にしたいことは？",
        "options": ["未経験歓迎", "高時給", "シフト自由"],
    },
    {
        "id": "q2",
        "text": "職場の雰囲気で重視したいのは？",
        "options": ["静か", "わいわい", "柔軟"],
    },
    {
        "id": "q3",
        "text": "働き方として希望するスタイルは？",
        "options": ["短期", "長期", "単発"],
    },
]


@router.get("/questions", tags=["question"])
def get_questions():
    return DUMMY_QUESTIONS


# 回答送信用モデル
class QuestionAnswer(BaseModel):
    answers: dict[str, str]


@router.post("/questions/answer", tags=["question"])
def post_answers(
    answer_data: QuestionAnswer, session_id: str = Depends(get_session_id)
):
    ensure_session(session_id)
    session = get_session_data(session_id)

    session["question"] = answer_data.answers

    return {"message": "回答を受け取りました", "answers": answer_data.answers}
