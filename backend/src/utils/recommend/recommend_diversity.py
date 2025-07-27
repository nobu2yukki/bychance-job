# recommend_diversity.py
# 最終的にユーザに見せるランキングの多様性を考慮したリランキングを行う
# recommend_diversity.py
import json
import random

from elasticsearch import (
    Elasticsearch,  # format_job_details_for_output関数内でesクライアントが必要なのでインポート
)


def select_diverse_hits(hits: list, max_results: int = 10) -> list:
    """
    ヒットリストからchildカテゴリが重複しないように、かつスコアを考慮して（ここではランダムに）
    最大指定件数の求人を選定します。

    Args:
        hits (list): フィルタリング済み求人リスト（Elasticsearchヒット形式）。
        max_results (int): 返す求人の最大件数。

    Returns:
        list: 選定された求人リスト。
    """
    diverse_candidates = {}  # {child_category: [hit1, hit2, ...]}
    for hit in hits:
        # childカテゴリのパスも新しいマッピングに合わせる
        child = hit["_source"].get("category", {}).get("child", "不明な子カテゴリ")
        if child not in diverse_candidates:
            diverse_candidates[child] = []
        diverse_candidates[child].append(hit)

    final_selected_hits = []
    unique_child_categories = list(diverse_candidates.keys())
    random.shuffle(unique_child_categories)  # 子カテゴリの順序をシャッフル

    # まず、各ユニークな子カテゴリから1つずつランダムに選択
    for child in unique_child_categories:
        if diverse_candidates[child]:
            selected_hit = random.choice(diverse_candidates[child])
            final_selected_hits.append(selected_hit)
            diverse_candidates[child].remove(
                selected_hit
            )  # 選択したヒットはプールから削除

    # 目標件数に達していない場合、残りのプールからランダムに追加
    remaining_hits_pool = []
    for child_list in diverse_candidates.values():
        remaining_hits_pool.extend(child_list)  # 残っているヒットを全てプールに追加

    random.shuffle(remaining_hits_pool)  # 残りのプールをシャッフル

    for hit in remaining_hits_pool:
        if len(final_selected_hits) >= max_results:
            break
        final_selected_hits.append(hit)

    random.shuffle(
        final_selected_hits
    )  # 最終的なリストをシャッフルしてランダム性を確保
    return final_selected_hits[:max_results]  # 目標件数に切り詰める


def format_job_details_for_output(
    es_client: Elasticsearch, hits: list, good_ids: list = None, bad_ids: list = None
) -> dict:
    """
    推薦された求人やGood/Badラベル付き求人をフロントエンド向けに整形します。

    Args:
        es_client (Elasticsearch): Elasticsearchクライアントインスタンス。
        hits (list): 推薦された求人のElasticsearchヒットリスト。
        good_ids (list, optional): Goodラベル付き求人のIDリスト。デフォルトはNone。
        bad_ids (list, optional): Badラベル付き求人のIDリスト。デフォルトはNone。

    Returns:
        dict: 最終的なレスポンス辞書。
    """

    def _fetch_and_format_job_details(ids_list: list) -> list:
        jobs = []
        if ids_list is None:
            return jobs
        for doc_id in ids_list:
            try:
                res = es_client.get(
                    index="job_info", id=doc_id
                )  # INDEX_NAMEはここで固定
                source = res["_source"].copy()  # _sourceは既に整形後のデータ
                job_id = int(source.get("id", doc_id))
                # ここを修正: sourceから直接新しいキー名で値を取得する
                # pop()ではなくget()を使用し、キーが存在しない場合もエラーにならないようにする
                job = {
                    "id": job_id,  # _idではなく、JSON内のidを使う場合
                    "page_url": source.get("page_url", ""),
                    "company_name": source.get("company_name", ""),
                    "image_url": source.get("image_url", ""),
                    "place": source.get("place", ""),
                    "salary": source.get("salary", ""),
                    "description": source.get("description", ""),
                    "category": {
                        "parent": source.get("category", {}).get("parent", ""),
                        "child": source.get("category", {}).get("child", ""),
                    },
                    "work_style": source.get("work_style", []),
                    "audience": source.get("audience", []),
                }
                jobs.append(job)
            except Exception as e:
                print(f"Error fetching job details for {doc_id}: {e}")
        return jobs

    # 推薦された求人の整形 (この部分はすでに正しく機能している)
    recommended_jobs_formatted = []
    for hit in hits:
        job = hit["_source"].copy()
        job_id = int(job.get("id", hit["_id"]))
        job["id"] = job_id  # ヒットの_idを使用
        job.pop("embedding", None)
        # job["score"] = hit["_score"]

        # これらのキーは既にformat_job_for_frontendの段階で整形済みであるはずなので、
        # ここでは単にget()で取得すればよい
        job["company_name"] = job.get("company_name", "")
        job["place"] = job.get("place", "")
        job["description"] = job.get("description", "")
        job["category"] = job.get("category", {"parent": "", "child": ""})
        job["work_style"] = job.get("work_style", [])
        job["audience"] = job.get("audience", [])
        job["image_url"] = job.get("image_url", "")
        job["page_url"] = job.get("page_url", "")

        recommended_jobs_formatted.append(job)

    # Good/Badの詳細取得（修正済みサブ関数を使用）
    good_job_details = _fetch_and_format_job_details(good_ids)
    bad_job_details = _fetch_and_format_job_details(bad_ids)

    return {
        "good_jobs": good_job_details,
        "bad_jobs": bad_job_details,
        "recommended_jobs": recommended_jobs_formatted,
    }


# テスト用
if __name__ == "__main__":
    es_test = Elasticsearch("http://elasticsearch:9200")
    # ダミーのヒットデータ（recommend_vector_retrievalから得られる想定）
    dummy_hits = [
        {
            "_id": "1",
            "_score": 0.9,
            "_source": {
                "company_name": "TestA",
                "category": {"parent": "飲食", "child": "カフェ"},
            },
        },
        {
            "_id": "2",
            "_score": 0.8,
            "_source": {
                "company_name": "TestB",
                "category": {"parent": "販売・接客", "child": "コンビニ"},
            },
        },
        {
            "_id": "3",
            "_score": 0.7,
            "_source": {
                "company_name": "TestC",
                "category": {"parent": "飲食", "child": "レストラン"},
            },
        },
        {
            "_id": "4",
            "_score": 0.6,
            "_source": {
                "company_name": "TestD",
                "category": {"parent": "イベント", "child": "音楽フェス"},
            },
        },
        {
            "_id": 5,
            "_score": 0.5,
            "_source": {
                "company_name": "TestE",
                "category": {"parent": "飲食", "child": "カフェ"},
            },
        },  # child重複
    ]

    selected_hits_test = select_diverse_hits(dummy_hits, max_results=3)
    print(f"Selected diverse hits count: {len(selected_hits_test)}")

    dummy_good_ids = ["1"]  # 実際のIDに置き換えてください
    dummy_bad_ids = ["3"]  # 実際のIDに置き換えてください

    final_response_test = format_job_details_for_output(
        es_test, selected_hits_test, dummy_good_ids, dummy_bad_ids
    )
    print("\n--- Final Response Test ---")
    print(json.dumps(final_response_test, indent=2, ensure_ascii=False))
