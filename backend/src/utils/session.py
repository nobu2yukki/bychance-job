from fastapi import HTTPException, Query

# routers/session.py の active_sessions を使いたい
from src.routers.session import active_sessions


def is_valid_session(session_id: str) -> bool:
    return session_id in active_sessions


def ensure_valid_session(session_id: str):
    if not is_valid_session(session_id):
        raise HTTPException(status_code=404, detail="Invalid session_id")


# Depends 用
def get_session_id(session_id: str = Query(...)):
    ensure_valid_session(session_id)
    return session_id
