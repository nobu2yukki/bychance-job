# src/utils/session_store.py

from typing import Any

from src.routers.session import sessions

# セッションごとのデータ格納
# sessions: dict[str, dict[str, Any]] = {}


def init_session(session_id: str):
    """指定されたセッションIDで空のセッションを初期化"""
    sessions[session_id] = {
        "question": {},
        "swipe": {"target": [], "result": {"good": [], "bad": []}},
        "result": {"recommendations": []},  # 空のrecommendationsを追加
    }


def ensure_session(session_id: str):
    """セッションが存在しなければ初期化"""
    print(sessions.keys())
    if session_id not in sessions.keys():
        init_session(session_id)


def get_session_data(session_id: str) -> dict[str, Any]:
    """セッションデータを取得（存在しない場合は初期化して返す）"""
    ensure_session(session_id)
    return sessions[session_id]
