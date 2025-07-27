import random

from elasticsearch import Elasticsearch
from src.schemas.job import Job, JobCategory

# クエリ構築ロジックをインポート
from .swipe_make_query import (  # ここはswipe_make_query.pyを想定
    INDEX_NAME,
    build_job_search_query,
)

# Elasticsearchクライアント
es = Elasticsearch("http://elasticsearch:9200")


def search_and_recommend_jobs(dami_input, target_results=20):
    """
    Elasticsearchから求人を検索し、多様性を考慮して推薦します。

    Args:
        dami_input (dict): ユーザーの希望やフィルタリング条件を含む辞書。
        target_results (int): 最終的に返す求人の目標件数。

    Returns:
        list: フロントエンド向けに整形された推薦求人のリスト。
    """
    # === Elasticsearchクエリの構築 ===
    search_query = build_job_search_query(dami_input)

    # === Elasticsearch検索の実行 ===
    try:
        res = es.search(index=INDEX_NAME, body=search_query)
        all_hits = res["hits"]["hits"]
        print(f"\n🔎 Elasticsearchで取得した候補件数: {len(all_hits)}")
    except Exception as e:
        print(f"Elasticsearch検索エラー: {e}")
        all_hits = []
        return []

    # === 結果の加工と選定 ===
    def select_diverse_and_random_jobs(hits, target_count):
        diverse_candidates = {}  # {child_category: [hit1, hit2, ...]}
        for hit in hits:
            # childカテゴリのパスも新しいマッピングに合わせる
            # categoryフィールドがトップレベルのオブジェクトになったため
            child = hit["_source"].get("category", {}).get("child", "不明な子カテゴリ")
            if child not in diverse_candidates:
                diverse_candidates[child] = []
            diverse_candidates[child].append(hit)

        final_selected_hits = []
        unique_child_categories = list(diverse_candidates.keys())
        random.shuffle(unique_child_categories)  # 子カテゴリの順序をシャッフル

        # 各ユニークな子カテゴリから1つずつランダムに選択し、多様性を確保
        for child in unique_child_categories:
            if diverse_candidates[child]:
                selected_hit = random.choice(diverse_candidates[child])
                final_selected_hits.append(selected_hit)
                diverse_candidates[child].remove(selected_hit)

        # 目標件数に達していない場合、残りのプールからランダムに追加
        remaining_hits_pool = []
        for child_list in diverse_candidates.values():
            remaining_hits_pool.extend(child_list)

        random.shuffle(remaining_hits_pool)

        for hit in remaining_hits_pool:
            if len(final_selected_hits) >= target_count:
                break
            final_selected_hits.append(hit)

        random.shuffle(
            final_selected_hits
        )  # 最終的なリストをシャッフルしてランダム性を確保
        return final_selected_hits[:target_count]

    recommended_hits = select_diverse_and_random_jobs(all_hits, target_results)
    print(
        f"✨ 最終選定された求人件数（子カテゴリ重複なし・ランダム{target_results}件）: {len(recommended_hits)}"
    )

    # === フロントエンド向け整形 ===
    def format_job_for_frontend(hit):
        source = hit["_source"]
        # 新しいマッピングに合わせてキー名を変更
        category_info = source.get(
            "category", {}
        )  # job_tag.industry -> category に変更
        work_style_tags = source.get(
            "work_style", []
        )  # job_tag.work_style -> work_style に変更
        audience_tags = source.get(
            "audience", []
        )  # job_tag.audience -> audience に変更
        job_id = int(source.get("id", hit["_id"]))
        return Job(
            id=job_id,
            page_url=source.get("page_url", ""),
            company_name=source.get("company_name", ""),
            image_url=source.get("image_url", ""),
            place=source.get("place", ""),
            salary=source.get("salary", ""),
            description=source.get("description", ""),
            category=JobCategory(
                parent=category_info.get("parent", ""),
                child=category_info.get("child", ""),
            ),
            work_style=work_style_tags,
            audience=audience_tags,
        )

    final_recommended_jobs = []
    for hit in recommended_hits:
        final_recommended_jobs.append(format_job_for_frontend(hit))
    return final_recommended_jobs


# # === このファイルを直接実行した場合の例 ===
# if __name__ == "__main__":
#     # ダミーデータ（テスト用）
#     test_dami_input = {
#         "desired_job_category": "飲食",
#         "previous_employment_label": False,
#         "previous_employment_history": ["イベント", "音楽フェス"],
#         "user_filter_label": True,
#         "category_to_exclude": "parent",
#     }

#     recommended_jobs = search_and_recommend_jobs(test_dami_input, target_results=20)

#     # === 結果の表示 ===
#     print("\n--- フロントエンド向け最終出力 ---")
#     if not recommended_jobs:
#         print("条件に合致する求人は見つかりませんでした。")
#     else:
#         for i, job in enumerate(recommended_jobs):
#             print(f"--- 求人 {i + 1} / ID: {job.get('id')} ---")
#             print(f"会社名: {job.get('company_name')}")
#             print(
#                 f"カテゴリ: 親={job.get('category', {}).get('parent')}, 子={job.get('category', {}).get('child')}"
#             )
#             print(f"場所: {job.get('place')}")
#             print(f"給与: {job.get('salary')}")
#             # print(f"説明: {job.get('description')[:70]}...") # 長いので一部表示
#             print(f"勤務スタイル: {', '.join(job.get('work_style'))}")
#             print(f"ターゲット層: {', '.join(job.get('audience'))}")
#             print(f"画像URL: {job.get('image_url')}")  # image_urlの表示を有効に
#         print("\n--- 出力ここまで ---")

#     print(f"\n最終的な推薦件数: {len(recommended_jobs)} 件")
