#超長いけど全部動くコード
from elasticsearch import Elasticsearch
import numpy as np # NumPyは今回のクエリでは直接使用しませんが、既存コードから残しています
import json
import random

# Elasticsearchクライアント
es = Elasticsearch("http://elasticsearch:9200")
INDEX_NAME = "job_info"

# ダミーデータ
dami_input = {
    "desired_job_category": "販売・接客",  # 親カテゴリで回答 (希望職種)
    "previous_employment_history": ["イベント", "音楽フェス"],  # 親、子カテゴリをリストで (過去の勤務経験で除外したいカテゴリ)
    "user_filter_label": True,  # フィルタリングを有効にするか
    "category_to_exclude": "parent"  # previous_employment_historyのどのフィールドを除外するか（"parent" または "child"）
}

# === Elasticsearchクエリの構築 ===
# 基本となるクエリ（希望職種によるフィルタリング）
must_clauses = [
    {
        "term": {
            "job_tag.industry.parent.keyword": dami_input["desired_job_category"]
        }
    }
]

# must_not（除外）条件を初期化
must_not_clauses = []

# user_filter_labelがTrueの場合、過去の勤務経験による除外フィルタを追加
if dami_input.get("user_filter_label"):
    # 除外対象のフィールド名 (parentまたはchild)
    field_to_exclude = f"job_tag.industry.{dami_input['category_to_exclude']}.keyword"

    if dami_input["category_to_exclude"] == "parent":
        # parentの場合、previous_employment_historyの最初の要素のみを除外
        if dami_input["previous_employment_history"] and len(dami_input["previous_employment_history"]) > 0:
            must_not_clauses.append(
                {
                    "term": { # termsではなくtermを使用
                        field_to_exclude: dami_input["previous_employment_history"][0]
                    }
                }
            )
    else: # "child"の場合、またはその他の場合
        # previous_employment_history リストのすべての要素を除外条件として追加
        if dami_input["previous_employment_history"]:
            must_not_clauses.append(
                {
                    "terms": { # こちらはtermsを使用
                        field_to_exclude: dami_input["previous_employment_history"]
                    }
                }
            )

# 最終的なElasticsearchクエリの構築
# 十分な件数を取得するため、sizeを大きく設定（例: 500件）
search_query = {
    "query": {
        "bool": {
            "must": must_clauses,
            "must_not": must_not_clauses if must_not_clauses else []
        }
    },
    "size": 500 # 後で多様性とランダム性を考慮して選ぶため、多めに取得
}

# === Elasticsearch検索の実行 ===
try:
    res = es.search(index=INDEX_NAME, body=search_query)
    all_hits = res["hits"]["hits"]
    print(f"\n🔎 Elasticsearchで取得した候補件数: {len(all_hits)}")
except Exception as e:
    print(f"Elasticsearch検索エラー: {e}")
    all_hits = []


# === 結果の加工と選定 ===
def select_diverse_and_random_jobs(hits, target_results=20):
    diverse_candidates = {} # {child_category: [hit1, hit2, ...]}
    for hit in hits:
        child = hit["_source"].get("job_tag", {}).get("industry", {}).get("child", "不明な子カテゴリ")
        if child not in diverse_candidates:
            diverse_candidates[child] = []
        diverse_candidates[child].append(hit)

    final_selected_hits = []
    # 子カテゴリのユニークなリストを取得し、ランダムな順序で処理
    unique_child_categories = list(diverse_candidates.keys())
    random.shuffle(unique_child_categories) # 子カテゴリの順序をシャッフル

    # まず、各ユニークな子カテゴリから1つずつランダムに選択し、多様性を確保
    for child in unique_child_categories:
        if diverse_candidates[child]:
            selected_hit = random.choice(diverse_candidates[child])
            final_selected_hits.append(selected_hit)
            # 選択したヒットは候補リストから削除（重複選択を防ぐため、かつ残りのプール形成のため）
            diverse_candidates[child].remove(selected_hit)

    # 目標件数（20件）に達していない場合、残りのプールからランダムに追加
    remaining_hits_pool = []
    for child_list in diverse_candidates.values():
        remaining_hits_pool.extend(child_list) # 各子カテゴリに残っているヒットを全てプールに追加

    random.shuffle(remaining_hits_pool) # 残りのプールをシャッフル

    for hit in remaining_hits_pool:
        if len(final_selected_hits) >= target_results:
            break
        final_selected_hits.append(hit)

    # 最終的に目標件数に切り詰める（既にあるものは順序を保持）
    random.shuffle(final_selected_hits) # 最終的なリストをシャッフルしてランダム性を確保
    return final_selected_hits[:target_results]


recommended_hits = select_diverse_and_random_jobs(all_hits, target_results=20)
print(f"✨ 最終選定された求人件数（子カテゴリ重複なし・ランダム20件）: {len(recommended_hits)}")


# === フロントエンド向け整形 ===
def format_job_for_frontend(hit):
    source = hit["_source"]
    category_info = source.get("job_tag", {}).get("industry", {})
    work_style_tags = source.get("job_tag", {}).get("work_style", [])
    audience_tags = source.get("job_tag", {}).get("audience", [])

    return {
        "id": hit["_id"],
        "company_name": source.get("job", ""), # Elasticsearchの'job'フィールドを'company_name'にマッピング
        #"image_url": source.get("image_url", ""),
        "place": source.get("job_place", ""),
        "salary": source.get("salary", ""),
        "description": source.get("job_description", ""),
        "category": { # parentとchildを辞書で
            "parent": category_info.get("parent", ""),
            "child": category_info.get("child", "")
        },
        "work_style": work_style_tags, # リストのまま
        "audience": audience_tags,     # リストのまま
    }

final_recommended_jobs = []
for hit in recommended_hits:
    final_recommended_jobs.append(format_job_for_frontend(hit))


# === 最終レスポンス（表示用出力） ===
print("\n--- フロントエンド向け最終出力 ---")
if not final_recommended_jobs:
    print("条件に合致する求人は見つかりませんでした。")
else:
    for i, job in enumerate(final_recommended_jobs):
        print(f"--- 求人 {i+1} / ID: {job.get('id')} ---")
        print(f"会社名: {job.get('company_name')}")
        print(f"カテゴリ: 親={job.get('category', {}).get('parent')}, 子={job.get('category', {}).get('child')}")
        print(f"場所: {job.get('place')}")
        print(f"給与: {job.get('salary')}")
        # print(f"説明: {job.get('description')[:70]}...") # 長いので一部表示
        print(f"勤務スタイル: {', '.join(job.get('work_style'))}")
        print(f"ターゲット層: {', '.join(job.get('audience'))}")
        #print(f"画像URL: {job.get('image_url')}")
    print("\n--- 出力ここまで ---")

print(f"\n最終的な推薦件数: {len(final_recommended_jobs)} 件")