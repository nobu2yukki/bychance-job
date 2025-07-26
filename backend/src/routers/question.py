from fastapi import APIRouter

router = APIRouter()

@router.get("/questions", tags=["questions"])
def get_questions():
    return [{"id": 1, "question": "好きな時間帯は？", "options": ["朝", "昼", "夜"]}]
