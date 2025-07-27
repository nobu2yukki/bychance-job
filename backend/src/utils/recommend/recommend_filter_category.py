# recommend_filter_category.py
# ベクトル検索後にフィルタをかけ、最初のアンケートで除外したいカテゴリのものを削除


def filter_bad_hits(good_hits: list, bad_hits: list) -> list:
    """
    good_hitsからbad_hitsと同一のIDおよびjobを持つ求人を除外します。

    Args:
        good_hits (list): Goodな求人の検索結果リスト。
        bad_hits (list): Badな求人の検索結果リスト。

    Returns:
        list: 除外された求人のリスト。
    """
    bad_ids_set = set(hit["_id"] for hit in bad_hits)
    # Elasticsearchのjobフィールドはcompany_nameにマッピングされていることを想定
    bad_company_names_set = set(
        hit["_source"].get("company_name", "") for hit in bad_hits
    )

    filtered = []
    for hit in good_hits:
        if (hit["_id"] not in bad_ids_set) and (
            hit["_source"].get("company_name", "") not in bad_company_names_set
        ):
            filtered.append(hit)
    return filtered


def filter_by_category(
    hits: list, category_values: str | list[str], field_type: str
) -> list:  # ★ここを修正★
    """
    指定されたカテゴリ値（単一またはリスト）とフィールドタイプに基づいて求人をフィルタリングします。
    除外対象のカテゴリ値と一致しない場合に含めます。

    Args:
        hits (list): フィルタリング対象の求人リスト。
        category_values (Union[str, List[str]]): 除外したいカテゴリの値（単一の文字列または文字列のリスト）。
        field_type (str): 除外対象のカテゴリフィールド ('parent' または 'child')。

    Returns:
        list: フィルタリングされた求人リスト。
    """
    filtered = []
    # category_values を常にリストとして扱う
    if isinstance(category_values, str):
        exclude_list = [category_values]
    else:
        exclude_list = category_values

    for hit in hits:
        category_info = hit["_source"].get("category", {})
        target_category_field_value = category_info.get(field_type, "")

        # 除外リストに含まれていない場合にのみフィルタリング結果に含める
        if target_category_field_value not in exclude_list:  # ★ここを修正★
            filtered.append(hit)
    return filtered


# テスト用 (変更なし)
if __name__ == "__main__":
    # ダミーのヒットデータ
    dummy_hits = [
        {
            "_id": "1",
            "_source": {
                "company_name": "A社",
                "category": {"parent": "飲食", "child": "カフェ"},
            },
        },
        {
            "_id": "2",
            "_source": {
                "company_name": "B社",
                "category": {"parent": "販売・接客", "child": "コンビニ"},
            },
        },
        {
            "_id": "3",
            "_source": {
                "company_name": "A社",
                "category": {"parent": "飲食", "child": "レストラン"},
            },
        },
        {
            "_id": "4",
            "_source": {
                "company_name": "C社",
                "category": {"parent": "イベント", "child": "音楽フェス"},
            },
        },
    ]
    dummy_bad_hits = [
        {
            "_id": "3",
            "_source": {
                "company_name": "A社",
                "category": {"parent": "飲食", "child": "レストラン"},
            },
        },
    ]

    # bad除外テスト
    filtered_by_bad = filter_bad_hits(dummy_hits, dummy_bad_hits)
    print(f"Filtered by bad hits count: {len(filtered_by_bad)}")
    for h in filtered_by_bad:
        print(h["_id"], h["_source"]["company_name"])

    # カテゴリ除外テスト (parentが「飲食」ではないものを取得)
    filtered_by_category_test = filter_by_category(dummy_hits, "飲食", "parent")
    print(
        f"Filtered by category (parent='飲食'ではない) count: {len(filtered_by_category_test)}"
    )
    for h in filtered_by_category_test:
        print(h["_id"], h["_source"]["category"])

    # カテゴリ除外テスト (childが「カフェ」または「レストラン」ではないものを取得)
    filtered_by_category_list_test = filter_by_category(
        dummy_hits, ["カフェ", "レストラン"], "child"
    )
    print(
        f"Filtered by category (child='カフェ'または'レストラン'ではない) count: {len(filtered_by_category_list_test)}"
    )
    for h in filtered_by_category_list_test:
        print(h["_id"], h["_source"]["category"])
