# elasticsearch_queries.py


INDEX_NAME = "job_info"


def build_job_search_query(dami_input):
    """
    ユーザー入力に基づいてElasticsearchの検索クエリを構築します。

    Args:
        dami_input (dict): ユーザーの希望やフィルタリング条件を含む辞書。

    Returns:
        dict: 構築されたElasticsearchの検索クエリ。
    """
    # 基本となるクエリ（希望職種によるフィルタリング）
    must_clauses = [
        {
            "term": {
                # 変更: 'job_tag.industry.parent.keyword' -> 'category.parent.keyword'
                "category.parent": dami_input["desired_job_category"]
            }
        }
    ]

    # must_not（除外）条件を初期化
    must_not_clauses = []

    # 過去にバイトをやっていてかつ、バイト情報をもとにフィルタリングする人用のクエリ
    if dami_input.get("previous_employment_label"):
        # user_filter_labelがTrueの場合、過去の勤務経験による除外フィルタを追加
        if dami_input.get("user_filter_label"):
            field_to_exclude = f"category.{dami_input['category_to_exclude']}.keyword"

            if dami_input["category_to_exclude"] == "parent":
                # parentの場合、previous_employment_historyの最初の要素のみを除外
                if (
                    dami_input["previous_employment_history"]
                    and len(dami_input["previous_employment_history"]) > 0
                ):
                    must_not_clauses.append(
                        {
                            "term": {
                                field_to_exclude: dami_input[
                                    "previous_employment_history"
                                ][0]
                            }
                        }
                    )
            else:  # "child"の場合、またはその他の場合
                # previous_employment_history リストのすべての要素を除外条件として追加
                if dami_input["previous_employment_history"]:
                    must_not_clauses.append(
                        {
                            "terms": {
                                field_to_exclude: dami_input[
                                    "previous_employment_history"
                                ]
                            }
                        }
                    )

    # 最終的なElasticsearchクエリの構築
    # 十分な件数を取得するため、sizeを大きく設定（例: 500件）
    search_query = {
        "query": {
            "bool": {
                "must": must_clauses,
                "must_not": must_not_clauses if must_not_clauses else [],
            }
        },
        "size": 500,  # 後で多様性とランダム性を考慮して選ぶため、多めに取得
    }
    return search_query


# # テスト用のダミーデータ（このファイルを直接実行する場合やテスト用に使用）
# if __name__ == "__main__":
#     dami_input_test = {
#         "desired_job_category": "販売・接客",
#         "previous_employment_history": ["イベント", "音楽フェス"],
#         "user_filter_label": True,
#         "category_to_exclude": "parent" # "parent" または "child"
#     }
#     query = build_job_search_query(dami_input_test)
#     print("--- 構築されたElasticsearchクエリ ---")
#     print(json.dumps(query, indent=2, ensure_ascii=False))
