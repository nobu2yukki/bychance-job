import json
import random

from fastapi import APIRouter, Depends, HTTPException
from src.schemas.job import Job
from src.schemas.swipe import SwipeResult
from src.utils.recommend.main_recommendation_flow import search_and_recommend_jobs
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
    print(session["swipe"]["result"]["good"])
    question_answers = session.get("question", {})
    print(question_answers)
    # ★dami_input形式への整形処理★
    dami_input = {
        "labels": [],
        "desired_job_category": question_answers.get("desired_job_category"),
        "previous_employment_label": question_answers.get("previous_employment_label"),
        "previous_employment_history": question_answers.get(
            "previous_employment_history"
        ),
        "user_filter_label": question_answers.get("user_filter_label"),
        "category_to_exclude": question_answers.get("category_to_exclude"),
    }

    # good_jobs_pydantic から ID を抽出し、"labels" リストに "good" として追加
    for job in good_jobs:
        # Pydantic Jobモデルのidはint型なので、stringに変換する必要があるか確認
        # search_and_recommend_jobs はidを文字列として受け取るので、str()で変換
        dami_input["labels"].append({"id": str(job.id), "label": "good"})

    # bad_jobs_pydantic から ID を抽出し、"labels" リストに "bad" として追加
    for job in bad_jobs:
        dami_input["labels"].append({"id": str(job.id), "label": "bad"})

    # dami_inputの必須フィールドがNoneでないことを確認 (Optionalにしている場合)
    if dami_input["desired_job_category"] is None:
        raise HTTPException(status_code=400, detail="desired_job_categoryは必須です。")
    if dami_input["previous_employment_label"] is None:
        # previous_employment_labelがない場合はデフォルト値Falseを設定 (APIの期待と合わせる)
        dami_input["previous_employment_label"] = False
    if dami_input["previous_employment_history"] is None:
        dami_input["previous_employment_history"] = []
    if dami_input["user_filter_label"] is None:
        dami_input["user_filter_label"] = False
    if dami_input["category_to_exclude"] is None:
        dami_input["category_to_exclude"] = "parent"  # デフォルト値

    print(f"Constructed dami_input for recommender: {dami_input}")  # デバッグ用ログ

    try:
        # search_and_recommend_jobs は整形済みの辞書リストを返す
        recommendation_raw_response = search_and_recommend_jobs(
            dami_input, target_results=20
        )

        # recommended_jobs の辞書リストを取得
        recommended_jobs_dicts = recommendation_raw_response.get("recommended_jobs", [])

        # ★Jobモデルのインスタンスに変換し、セッションに保存★
        # format_job_details_for_output が返す辞書はJobモデルのフィールドと一致するはず
        recommended_jobs_pydantic = [
            Job(**job_dict) for job_dict in recommended_jobs_dicts
        ]

        session["result"]["recommendations"] = recommended_jobs_pydantic
        print(
            f"Saved {len(recommended_jobs_pydantic)} recommended jobs to session['result']['recommendations']."
        )

        # APIの最終応答は、保存が成功したことを示すメッセージのみ
        return {
            "message": "スワイプ結果を受け取り、推薦結果をセッションに保存しました。",
            "session_id": result.session_id,
            "good_count": len(good_jobs),
            "bad_count": len(bad_jobs),
        }

    except Exception as e:
        raise e
        print(f"Error during recommendation process: {e}")
        raise HTTPException(
            status_code=500, detail=f"推薦処理中にエラーが発生しました: {e!s}"
        )


@router.get("/swipe-results", tags=["swipe"])
def get_swipe_results(session_id: str = Depends(get_session_id)):
    ensure_session(session_id)
    session = get_session_data(session_id)

    return {
        "good": session["swipe"]["result"]["good"],
        "bad": session["swipe"]["result"]["bad"],
    }
