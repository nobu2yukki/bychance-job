from fastapi import APIRouter
from src.schemas.swipe import SwipeResult
from src.utils.session import ensure_valid_session

router = APIRouter()

# ダミーの求人データ
DUMMY_JOBS = [
    {"id": 1, "job": "カフェスタッフ", "place": "東京", "salary": "1200円"},
    {"id": 2, "job": "コンビニ夜勤", "place": "大阪", "salary": "1400円"},
    {"id": 3, "job": "引っ越しアシスタント", "place": "名古屋", "salary": "1500円"},
    {"id": 4, "job": "イベントスタッフ", "place": "福岡", "salary": "1300円"},
    {"id": 5, "job": "軽作業", "place": "札幌", "salary": "1100円"},
]


@router.get("/swipe-list", tags=["swipe"])
def get_swipe_jobs():
    pass


@router.post("/swipe-results", tags=["swipe"])
def post_swipe_results(result: SwipeResult):
    ensure_valid_session(result.session_id)

    return {
        "message": "スワイプ結果を受け取りました",
        "session_id": result.session_id,
        "good": result.good,
        "bad": result.bad,
    }
