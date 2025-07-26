from fastapi import APIRouter, Depends
from src.utils.session import get_session_id
from src.utils.session_store import ensure_session, get_session_data

router = APIRouter()


@router.get("/results", tags=["result"])
def get_result(session_id: str = Depends(get_session_id)):
    ensure_session(session_id)
    session = get_session_data(session_id)

    good_jobs = session["swipe"]["result"]["good"]
    bad_jobs = session["swipe"]["result"]["bad"]

    # 今回はおすすめを good から上位3件として仮定（実際は独自ロジックが入る）
    recommended_jobs = good_jobs[:3]

    return {
        "session_id": session_id,
        "recommend": recommended_jobs,
        "good": good_jobs,
        "bad": bad_jobs,
    }
