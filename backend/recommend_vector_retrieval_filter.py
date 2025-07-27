# recommend_search.py
# ベクトル検索と、好みに意味的に似た求人を、カテゴリフィルタを適用して収集

import json  # json.dumpsを使うためにインポート

import numpy as np
from elasticsearch import Elasticsearch

# Elasticsearchクライアントは呼び出し元から渡す
INDEX_NAME = "job_info"


def knn_search_with_filters(
    es_client: Elasticsearch,
    query_vec: np.ndarray,
    good_ids: list,
    bad_ids: list,
    dami_input: dict,  # フィルタリングに必要なdami_input全体を受け取る
    k: int = 70,
    num_candidates: int = 600,
) -> list:
    """
    指定されたクエリベクトルに基づいてKNN検索を実行し、同時に複数のフィルタリングを適用します。
    Elasticsearch 8.xの_search APIでのknnとqueryの併用に対応します。

    Args:
        es_client (Elasticsearch): Elasticsearchクライアントインスタンス。
        query_vec (np.ndarray): 検索クエリベクトル（mean_goodなど）。
        good_ids (list): goodと判定された求人のIDリスト (除外条件に使用)。
        bad_ids (list): badと判定された求人のIDリスト (除外条件に使用)。
        dami_input (dict): ユーザーの希望やフィルタリング条件を含む辞書。
        k (int): 返すヒット数。
        num_candidates (int): KNN探索の候補数。

    Returns:
        list: Elasticsearchの検索結果（ヒットリスト）。
    """
    if query_vec is None:
        print("Warning: Query vector is None. Skipping search.")
        return []

    # === boolクエリの構築 ===
    bool_query = {"must": [], "must_not": []}
    applied_filters_log = []  # 適用されたフィルタを記録するためのリスト

    # 1. 希望職種によるフィルタリング (desired_job_category)
    if dami_input.get("desired_job_category"):
        bool_query["must"].append(
            {"term": {"category.parent.keyword": dami_input["desired_job_category"]}}
        )
        applied_filters_log.append(f"希望職種: {dami_input['desired_job_category']}")

    # 2. previous_employment_history と user_filter_label による除外フィルタ
    if dami_input.get("previous_employment_label"):  # 過去のバイト経験がある
        if dami_input.get("user_filter_label"):  # かつ、その情報でフィルタリングする
            field_to_exclude = f"category.{dami_input['category_to_exclude']}.keyword"

            if dami_input["category_to_exclude"] == "parent":
                if (
                    dami_input["previous_employment_history"]
                    and len(dami_input["previous_employment_history"]) > 0
                ):
                    exclude_value = dami_input["previous_employment_history"][0]
                    bool_query["must_not"].append(
                        {"term": {field_to_exclude: exclude_value}}
                    )
                    applied_filters_log.append(
                        f"過去経験除外(親): {field_to_exclude}={exclude_value}"
                    )
            else:  # "child"の場合
                if dami_input["previous_employment_history"]:
                    exclude_values = dami_input["previous_employment_history"]
                    bool_query["must_not"].append(
                        {"terms": {field_to_exclude: exclude_values}}
                    )
                    applied_filters_log.append(
                        f"過去経験除外(子): {field_to_exclude}={exclude_values}"
                    )
        else:
            applied_filters_log.append(
                "過去経験に基づくフィルタリングは無効(user_filter_label=False)"
            )
    else:
        applied_filters_log.append(
            "過去経験に基づくフィルタリングは無効(previous_employment_label=False)"
        )

    # 3. badと同一IDの除外 (bad_ids_set を直接クエリに組み込む)
    if bad_ids:  # bad_idsがあれば除外
        bool_query["must_not"].append({"ids": {"values": bad_ids}})
        applied_filters_log.append(f"BAD ID除外: {bad_ids}")

    # === 最終的なElasticsearchクエリの構築 ===
    # knnとqueryを_search APIのトップレベルで組み合わせる (ES 8.x以降の記法)
    search_body = {
        "knn": {
            "field": "embedding",
            "query_vector": query_vec.tolist(),
            "k": k,
            "num_candidates": num_candidates,
        },
        "size": k,
    }

    # bool_queryに条件が設定されていれば、search_bodyにqueryセクションを追加
    if bool_query["must"] or bool_query["must_not"]:
        search_body["query"] = {"bool": bool_query}
    else:
        # フィルタが一つも適用されない場合、match_all をデフォルトのクエリとする
        search_body["query"] = {"match_all": {}}
        applied_filters_log.append("一般フィルタは適用されません (match_all)。")

    # === ここから修正：embeddingの表示を短縮 ===
    print("\n--- Elasticsearchクエリに適用されたフィルタリング条件 ---")
    if applied_filters_log:
        for log_entry in applied_filters_log:
            print(f" - {log_entry}")
    else:
        print(" - 特になし（すべてmatch_all）。")

    print("--- 生成されたElasticsearchクエリボディ ---")

    # ログ出力用に、一時的にquery_vectorを短縮表示用に加工
    display_search_body = search_body.copy()
    if "knn" in display_search_body and "query_vector" in display_search_body["knn"]:
        original_vector = display_search_body["knn"]["query_vector"]
        # ベクトルの最初の数要素と、そのサイズを表示
        display_search_body["knn"]["query_vector"] = (
            f"[ {original_vector[0]:.4f}, {original_vector[1]:.4f}, ... (truncated, size={len(original_vector)}) ]"
        )

    print(json.dumps(display_search_body, indent=2, ensure_ascii=False))
    # --- ここまで修正 ---


# テスト用 (変更なし)
if __name__ == "__main__":
    es_test = Elasticsearch("http://elasticsearch:9200")
    dummy_query_vec = np.random.rand(384)
    dummy_good_ids = ["365", "628"]
    dummy_bad_ids = ["8"]

    test_dami_input = {
        "desired_job_category": "飲食",
        "previous_employment_label": True,
        "previous_employment_history": ["イベント"],
        "user_filter_label": True,
        "category_to_exclude": "parent",
    }

    test_dami_input_no_filter = {
        "desired_job_category": "飲食",
        "previous_employment_label": False,
    }

    test_dami_input_no_desired = {
        "desired_job_category": None,  # 希望職種なし
        "previous_employment_label": False,
    }

    print("\n--- Test 1: Combined search with filters (飲食, イベント除外) ---")
    hits_with_filters = knn_search_with_filters(
        es_test, dummy_query_vec, dummy_good_ids, dummy_bad_ids, test_dami_input, k=5
    )
    print(f"Combined search results count: {len(hits_with_filters)}")
    if hits_with_filters:
        for hit in hits_with_filters:
            print(
                f"   ID: {hit['_id']}, Score: {hit['_score']:.4f}, Parent: {hit['_source'].get('category', {}).get('parent')}, Child: {hit['_source'].get('category', {}).get('child')}"
            )

    print(
        "\n--- Test 2: Combined search without previous employment filters (desired_job_categoryのみ) ---"
    )
    hits_no_prev_filter = knn_search_with_filters(
        es_test,
        dummy_query_vec,
        dummy_good_ids,
        dummy_bad_ids,
        test_dami_input_no_filter,
        k=5,
    )
    print(
        f"Combined search (no prev filters) results count: {len(hits_no_prev_filter)}"
    )
    if hits_no_prev_filter:
        for hit in hits_no_prev_filter:
            print(
                f"   ID: {hit['_id']}, Score: {hit['_score']:.4f}, Parent: {hit['_source'].get('category', {}).get('parent')}, Child: {hit['_source'].get('category', {}).get('child')}"
            )

    print(
        "\n--- Test 3: No specific filters (desired_job_categoryなし、previous_employment_label=False) ---"
    )
    hits_no_specific_filters = knn_search_with_filters(
        es_test,
        dummy_query_vec,
        dummy_good_ids,
        dummy_bad_ids,
        test_dami_input_no_desired,  # desired_job_categoryがNone
        k=5,
    )
    print(f"No specific filters search results count: {len(hits_no_specific_filters)}")
    if hits_no_specific_filters:
        for hit in hits_no_specific_filters:
            print(
                f"   ID: {hit['_id']}, Score: {hit['_score']:.4f}, Parent: {hit['_source'].get('category', {}).get('parent')}, Child: {hit['_source'].get('category', {}).get('child')}"
            )
