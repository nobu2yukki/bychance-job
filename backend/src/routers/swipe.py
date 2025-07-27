import json
import random

from fastapi import APIRouter, Depends
from src.schemas.job import Job
from src.schemas.swipe import SwipeResult
from src.utils.session import get_session_id
from src.utils.session_store import ensure_session, get_session_data

router = APIRouter()


with open("src/mock_data/jobs.json", encoding="utf-8") as f:
    DUMMY_JOBS = json.load(f)


@router.get("/swipe-list", tags=["swipe"])
def get_swipe_jobs(session_id: str = Depends(get_session_id)):
    ensure_session(session_id)
    session = get_session_data(session_id)

    if session["swipe"]["target"]:
        return session["swipe"]["target"]  # すでに保存済みなら返す

    sampled_dicts = random.sample(DUMMY_JOBS, len(DUMMY_JOBS) * 2 // 3)
    sampled_jobs = [Job(**job) for job in sampled_dicts]  # Jobインスタンス化

    session["swipe"]["target"] = sampled_jobs
    return sampled_jobs


@router.post("/swipe-results", tags=["swipe"])
def post_swipe_results(result: SwipeResult):
    ensure_session(result.session_id)
    session = get_session_data(result.session_id)

    # 保存されたJob一覧からID検索用辞書を作成
    job_dict = {job.id: job for job in session["swipe"]["target"]}

    good_jobs = [job_dict[jid] for jid in result.good if jid in job_dict]
    bad_jobs = [job_dict[jid] for jid in result.bad if jid in job_dict]

    session["swipe"]["result"]["good"] = good_jobs
    session["swipe"]["result"]["bad"] = bad_jobs

    return {
        "message": "スワイプ結果を受け取りました（Jobモデル）",
        "session_id": result.session_id,
        "good_count": len(good_jobs),
        "bad_count": len(bad_jobs),
    }


@router.get("/swipe-results", tags=["swipe"])
def get_swipe_results(session_id: str = Depends(get_session_id)):
    ensure_session(session_id)
    session = get_session_data(session_id)

    return {
        "good": session["swipe"]["result"]["good"],
        "bad": session["swipe"]["result"]["bad"],
    }
