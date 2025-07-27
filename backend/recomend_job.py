from elasticsearch import Elasticsearch
import numpy as np
import json

# Elasticsearchクライアント
es = Elasticsearch("http://elasticsearch:9200")
INDEX_NAME = "job_info"

# ダミーデータ
dami_input = {
    "labels": [
        { "id": "365", "label": "good" },
        { "id": "628", "label": "good" },
        { "id": "395", "label": "good" },
        { "id": "665", "label": "good" },
        { "id": "599", "label": "good" },
        { "id": "574", "label": "good" },
        { "id": "389", "label": "good" },
        { "id": "8", "label": "bad" },
        { "id": "9", "label": "bad" },
        { "id": "10", "label": "bad" }
    ],
    "user_filter_label": False,
    "category_value": ""
}

# === ラベル分類 ===
good_ids = [entry["id"] for entry in dami_input["labels"] if entry["label"] == "good"]
bad_ids = [entry["id"] for entry in dami_input["labels"] if entry["label"] == "bad"]

# === ベクトル取得 ===
def fetch_vectors(ids):
    vectors = []
    for doc_id in ids:
        try:
            res = es.get(index=INDEX_NAME, id=doc_id)
            vec = res["_source"].get("embedding")
            if vec:
                vectors.append(np.array(vec))
        except Exception as e:
            print(f"Error fetching {doc_id}: {e}")
    return vectors

good_vecs = fetch_vectors(good_ids)
bad_vecs = fetch_vectors(bad_ids)

mean_good = np.mean(good_vecs, axis=0) if good_vecs else None
mean_bad = np.mean(bad_vecs, axis=0) if bad_vecs else None

# === KNN検索 ===
def knn_search(query_vec, k=70, num_candidates=600):
    query = {
        "knn": {
            "field": "embedding",
            "query_vector": query_vec.tolist(),
            "k": k,
            "num_candidates": num_candidates
        },
        "size": k
    }
    return es.search(index=INDEX_NAME, body=query)["hits"]["hits"]

good_hits = knn_search(mean_good)
bad_hits = knn_search(mean_bad)
print(f"\n🔎 KNN検索結果件数（mean_good）: {len(good_hits)}")

# === Step 1: badと同一ID/jobを除外 ===
bad_ids_set = set(hit["_id"] for hit in bad_hits)
bad_jobs_set = set(hit["_source"].get("job", "") for hit in bad_hits)

filtered_hits = []
for hit in good_hits:
    if (hit["_id"] not in bad_ids_set) and (hit["_source"].get("job", "") not in bad_jobs_set):
        filtered_hits.append(hit)
print(f"✅ bad除外後: {len(filtered_hits)}")

# === Step 2: カテゴリ除外 ===
def filter_by_category(hits, category_value):
    filtered = []
    for hit in hits:
        industry = hit["_source"].get("job_tag", {}).get("industry", {})
        parent = industry.get("parent", "")
        child = industry.get("child", "")
        # category_valueが親カテゴリまたは子カテゴリと一致しない場合に含める
        if category_value != parent and category_value != child:
            filtered.append(hit)
    return filtered

# user_filter_labelがTrueの場合のみカテゴリフィルタリングを適用
if dami_input.get("user_filter_label"): # Trueの場合に実行
    filtered_hits = filter_by_category(filtered_hits, dami_input["category_value"])
    print(f"✅ カテゴリ除外後（{dami_input['category_value']}）: {len(filtered_hits)}")
else: # Falseの場合（またはキーがない場合）はフィルタリングをスキップ
    print("☑ カテゴリフィルタリングはスキップされました。")

# === Step 3: childカテゴリが重複しないように抽出 ===
def select_diverse_hits(hits, max_results=10):
    seen_childs = set()
    diverse_hits = []
    for hit in hits:
        child = hit["_source"].get("job_tag", {}).get("industry", {}).get("child", "")
        if child not in seen_childs:
            diverse_hits.append(hit)
            seen_childs.add(child)
        if len(diverse_hits) >= max_results:
            break
    return diverse_hits

diverse_top_hits = select_diverse_hits(filtered_hits, max_results=10)

# === 詳細取得（ベクトル以外） ===
def fetch_job_details(ids):
    jobs = []
    for doc_id in ids:
        try:
            res = es.get(index=INDEX_NAME, id=doc_id)
            source = res["_source"].copy()
            source["id"] = doc_id
            source.pop("embedding", None)
            jobs.append(source)
        except Exception as e:
            print(f"Error fetching job details for {doc_id}: {e}")
    return jobs

good_job_details = fetch_job_details(good_ids)
bad_job_details = fetch_job_details(bad_ids)

recommended_jobs = []
for hit in diverse_top_hits:
    job = hit["_source"].copy()
    job["id"] = hit["_id"]
    job.pop("embedding", None)
    job["score"] = hit["_score"]
    recommended_jobs.append(job)

# === 最終レスポンス ===
response = {
    "good_jobs": good_job_details,
    "bad_jobs": bad_job_details,
    "recommended_jobs": recommended_jobs
}

# === 表示用出力 ===
print("\n✅ GOOD ラベル付き求人:")
for job in good_job_details:
    print(f"ID: {job.get('id')} / Job: {job.get('job')} / Parent: {job.get('job_tag', {}).get('industry', {}).get('parent')} / Child: {job.get('job_tag', {}).get('industry', {}).get('child')}")

print("\n❌ BAD ラベル付き求人:")
for job in bad_job_details:
    print(f"ID: {job.get('id')} / Job: {job.get('job')} / Parent: {job.get('job_tag', {}).get('industry', {}).get('parent')} / Child: {job.get('job_tag', {}).get('industry', {}).get('child')}")

print("\n⭐ RECOMMENDED JOBS（ランキング上位・多様性あり）:")
for job in recommended_jobs:
    print(f"ID: {job.get('id')} / Job: {job.get('job')} / Child: {job.get('job_tag', {}).get('industry', {}).get('child')} / Score: {job.get('score'):.4f}")
