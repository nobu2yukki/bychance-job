import random

from fastapi import APIRouter, Depends
from src.schemas.job import Job
from src.schemas.swipe import SwipeResult
from src.utils.session import get_session_id
from src.utils.session_store import ensure_session, get_session_data

router = APIRouter()

# ダミーの求人データ
DUMMY_JOBS = [
    {"id": 1, "job": "カフェスタッフ", "place": "東京", "salary": "1200円"},
    {"id": 2, "job": "コンビニ夜勤", "place": "大阪", "salary": "1400円"},
    {"id": 3, "job": "引っ越しアシスタント", "place": "名古屋", "salary": "1500円"},
    {"id": 4, "job": "イベントスタッフ", "place": "福岡", "salary": "1300円"},
    {"id": 5, "job": "軽作業", "place": "札幌", "salary": "1100円"},
    {"id": 6, "job": "ピッキング作業", "place": "横浜", "salary": "1250円"},
    {"id": 7, "job": "居酒屋ホール", "place": "神戸", "salary": "1350円"},
    {"id": 8, "job": "警備スタッフ", "place": "新宿", "salary": "1450円"},
    {"id": 9, "job": "清掃スタッフ", "place": "千葉", "salary": "1150円"},
    {"id": 10, "job": "チラシ配り", "place": "京都", "salary": "1000円"},
    {"id": 11, "job": "レジ打ち", "place": "静岡", "salary": "1100円"},
    {"id": 12, "job": "コールセンター", "place": "仙台", "salary": "1200円"},
    {"id": 13, "job": "パン工場", "place": "埼玉", "salary": "1300円"},
    {"id": 14, "job": "引越し手伝い", "place": "広島", "salary": "1250円"},
    {"id": 15, "job": "交通量調査", "place": "金沢", "salary": "1050円"},
    {"id": 16, "job": "試食販売", "place": "岡山", "salary": "1150円"},
    {"id": 17, "job": "データ入力", "place": "鹿児島", "salary": "1100円"},
    {"id": 18, "job": "ポスティング", "place": "那覇", "salary": "1000円"},
    {"id": 19, "job": "ホテル清掃", "place": "小樽", "salary": "1200円"},
    {"id": 20, "job": "工場内軽作業", "place": "富山", "salary": "1250円"},
]


@router.get("/swipe-list", tags=["swipe"])
def get_swipe_jobs(session_id: str = Depends(get_session_id)):
    ensure_session(session_id)
    session = get_session_data(session_id)

    if session["swipe"]["target"]:
        return session["swipe"]["target"]  # すでに保存済みなら返す

    sampled_dicts = random.sample(DUMMY_JOBS, 20)
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
