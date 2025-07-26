from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter()

# ダミーデータ読み込み
MOCK_PATH = Path(__file__).parent.parent / "mock_data" / "dummy.json"
with open(MOCK_PATH, encoding="utf-8") as f:
    QUESTIONS = json.load(f)

# 質問一覧取得API
@router.get("/questions")
def get_questions():
    return QUESTIONS

# 質問への回答受け取り（モック用）
@router.post("/answers")
def post_answers(answers: dict):
    # 本番ではDBに保存するが、今は確認のためログ出力のみ
    print("ユーザの回答:", answers)
    return {"message": "回答を受け取りました", "received": answers}
