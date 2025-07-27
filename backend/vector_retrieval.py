from elasticsearch import Elasticsearch

es = Elasticsearch("http://elasticsearch:9200")
INDEX_NAME = "job_info"

query_id = 149

# クエリベクトルと job 名(=会社名)の取得
res = es.get(index=INDEX_NAME, id=query_id)
query_vec = res["_source"]["embedding"]
query_job_name = res["_source"]["job"].strip()
print("🔍 クエリ求人:", query_job_name)

# KNN検索クエリ(少し多めにとっておく)
query = {
    "knn": {
        "field": "embedding",
        "query_vector": query_vec,
        "k": 30,  # 除外後に10件残るように多めに取得
        "num_candidates": 600
    }
}

res = es.search(index=INDEX_NAME, body=query)

# 類似求人トップ10(同一 job 名やクエリ自身を除外)
print("類似求人トップ10:")
rank = 1
for hit in res["hits"]["hits"]:
    hit_job_name = hit["_source"].get("job", "").strip()
    hit_id = hit["_source"].get("id", "")

    if hit_id == query_id:
        continue  # クエリ自身を除外
    if hit_job_name == query_job_name:
        continue  # job名(=会社名+店舗名など)が完全一致なら除外

    score = hit["_score"]
    print(f"{rank}. {hit_id}:hit{hit_job_name}(スコア: {score:.4f})")
    rank += 1
    if rank > 10:
        break
