# job_recommender.py (旧 main_recommendation_flow.py)

import json

from elasticsearch import Elasticsearch

from .recommend_diversity import format_job_details_for_output, select_diverse_hits
from .recommend_filter_category import (  # <--- filter_bad_hits, filter_by_category
    filter_bad_hits,
    filter_by_category,
)

# 各モジュールから必要な関数と定数をインポート
from .recommend_get_vectors import calculate_mean_vectors, fetch_vectors
from .recommend_vector_retrieval import (
    knn_search,  # <--- knn_search (統合されていない方)
)

# Elasticsearchクライアントはモジュールレベルで初期化（FastAPIから利用される場合）
es = Elasticsearch("http://elasticsearch:9200")


def search_and_recommend_jobs(dami_input: dict, target_results: int = 20) -> dict:
    """
    Elasticsearchから求人を検索し、多様性を考慮して推薦します。

    Args:
        dami_input (dict): ユーザーの希望やフィルタリング条件を含む辞書。
        target_results (int): 最終的に返す求人の目標件数。

    Returns:
        dict: フロントエンド向けに整形された推薦求人のレスポンス辞書。
    """
    print("--- 推薦フロー開始 ---")

    # 1. ラベル分類
    good_ids = [
        entry["id"] for entry in dami_input["labels"] if entry["label"] == "good"
    ]
    bad_ids = [entry["id"] for entry in dami_input["labels"] if entry["label"] == "bad"]

    # 2. ベクトル取得と平均算出
    good_vecs = fetch_vectors(es, good_ids)
    bad_vecs = fetch_vectors(es, bad_ids)
    mean_good, mean_bad = calculate_mean_vectors(good_vecs, bad_vecs)

    # 3. KNN検索 (統合前の純粋なKNN検索)
    # good_hitsのkとnum_candidatesを十分に大きく設定し、後続のフィルタリングと多様性確保に備える
    good_hits = knn_search(es, mean_good, k=200, num_candidates=1000)
    bad_hits = knn_search(
        es, mean_bad, k=50, num_candidates=200
    )  # bad_hitsも同様に調整
    print(f"\n🔎 KNN検索結果件数（mean_good）: {len(good_hits)}")

    # 4. Step 1: badと同一ID/company_nameを除外
    filtered_hits_after_bad = filter_bad_hits(good_hits, bad_hits)
    print(f"✅ bad除外後: {len(filtered_hits_after_bad)}")

    # 5. Step 2: カテゴリ除外（user_filter_label設定に応じて）
    processed_hits_after_category_filter = filtered_hits_after_bad

    if dami_input.get(
        "previous_employment_label"
    ):  # 過去の経験がある場合のみ、このフィルタリングを考慮
        if dami_input.get(
            "user_filter_label"
        ):  # ユーザーがその経験でフィルタリングを希望する場合
            if dami_input[
                "previous_employment_history"
            ]:  # フィルタリング対象のカテゴリが指定されている場合のみ
                processed_hits_after_category_filter = filter_by_category(
                    processed_hits_after_category_filter,
                    dami_input[
                        "previous_employment_history"
                    ],  # ★改造後のfilter_by_categoryにリストを渡す★
                    dami_input["category_to_exclude"],
                )
                print(
                    f"✅ カテゴリ除外後（対象: {dami_input['previous_employment_history']}、タイプ: {dami_input['category_to_exclude']}）: {len(processed_hits_after_category_filter)}"
                )
            else:
                print(
                    "☑ カテゴリフィルタリングは有効ですが、除外対象の過去経験カテゴリが指定されていません。"
                )
        else:
            print(
                "☑ カテゴリフィルタリングはスキップされました。(user_filter_label=False)"
            )
    else:
        print(
            "☑ カテゴリフィルタリングはスキップされました。(previous_employment_label=False)"
        )

    # 6. Step 3: childカテゴリが重複しないように抽出し、ランダムに20件選択
    final_recommended_hits = select_diverse_hits(
        processed_hits_after_category_filter, max_results=target_results
    )  # target_resultsを渡す
    print(
        f"✨ 最終選定された求人件数（子カテゴリ重複なし・ランダム{target_results}件）: {len(final_recommended_hits)}"
    )

    # 7. 詳細取得と最終レスポンスの整形
    response = format_job_details_for_output(
        es, final_recommended_hits, good_ids, bad_ids
    )

    # === 表示用出力 ===
    print("\n✅ GOOD ラベル付き求人:")
    for job in response["good_jobs"]:
        print(
            f"ID: {job.get('id')} / Company: {job.get('company_name')} / Parent: {job.get('category', {}).get('parent')} / Child: {job.get('category', {}).get('child')}"
        )

    print("\n❌ BAD ラベル付き求人:")
    for job in response["bad_jobs"]:
        print(
            f"ID: {job.get('id')} / Company: {job.get('company_name')} / Parent: {job.get('category', {}).get('parent')} / Child: {job.get('category', {}).get('child')}"
        )

    print("\n⭐ RECOMMENDED JOBS（ランキング上位・多様性あり）:")
    if not response["recommended_jobs"]:
        print("推薦された求人はありませんでした。")
    else:
        for job in response["recommended_jobs"]:
            print(
                f"ID: {job.get('id')} / Company: {job.get('company_name')} / Child: {job.get('category', {}).get('child')}"
            )

    print("\n--- 推薦フロー終了 ---")
    return response  # 最終結果を返す


# === このファイルを直接実行した場合の例 ===
if __name__ == "__main__":
    # ダミーデータ（テスト用）
    test_dami_input = {
        "labels": [
            {"id": "365", "label": "good"},
            {"id": "628", "label": "good"},
            {"id": "395", "label": "good"},
            {"id": "665", "label": "good"},
            {"id": "599", "label": "good"},
            {"id": "574", "label": "good"},
            {"id": "389", "label": "good"},
            {"id": "8", "label": "bad"},
            {"id": "9", "label": "bad"},
            {"id": "10", "label": "bad"},
        ],
        "desired_job_category": "飲食",
        "previous_employment_label": True,
        "previous_employment_history": ["イベント", "音楽フェス"],
        "user_filter_label": True,
        "category_to_exclude": "parent",
    }

    # ユーザーがフィルタリングしないケースのテスト
    test_dami_input_no_filter = {
        "labels": [
            {"id": "365", "label": "good"},
            {"id": "628", "label": "good"},
            {"id": "395", "label": "good"},
            {"id": "665", "label": "good"},
            {"id": "599", "label": "good"},
            {"id": "574", "label": "good"},
            {"id": "389", "label": "good"},
            {"id": "8", "label": "bad"},
            {"id": "9", "label": "bad"},
            {"id": "10", "label": "bad"},
        ],
        "desired_job_category": "販売・接客",  # フィルタリングされないので何でも良い
        "previous_employment_label": False,  # フィルタしない
        "previous_employment_history": [],
        "user_filter_label": False,
        "category_to_exclude": "parent",
    }

    print("--- Test Case 1: Full Filtering ---")
    final_response1 = search_and_recommend_jobs(test_dami_input, target_results=20)
    print("\n--- Final API Response 1 ---")
    print(json.dumps(final_response1, indent=2, ensure_ascii=False))

    print("\n--- Test Case 2: No Filtering ---")
    final_response2 = search_and_recommend_jobs(
        test_dami_input_no_filter, target_results=10
    )
    print("\n--- Final API Response 2 ---")
    print(json.dumps(final_response2, indent=2, ensure_ascii=False))
