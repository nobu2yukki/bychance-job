import uuid

from fastapi import APIRouter

router = APIRouter()

# セッション一覧
active_sessions = []
sessions: dict[str, dict] = {}


# @router.post("/session/init", tags=["session"])
# def init_session(session_id: str):
#     """指定されたセッションIDで空のセッションを初期化"""
#     sessions[session_id] = {
#         "question": {},
#         "swipe": {"target": [], "result": {"good": [], "bad": []}},
#         "result": {"recommendations": []},
#     }
#     return sessions


@router.post("/session/start", tags=["session"])
def start_session():
    session_id = str(uuid.uuid4())
    # active_sessions.append(session_id)
    sessions[session_id] = {
        "question": {},
        "swipe": {"target": [], "result": {"good": [], "bad": []}},
        "result": {"recommendations": []},
    }
    print(sessions)
    return {"session_id": session_id}


@router.get("/session/exists/{session_id}", tags=["session"])
def check_session(session_id: str):
    return {"session_id": session_id, "valid": session_id in sessions.keys()}
