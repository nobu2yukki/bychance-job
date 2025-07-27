from elasticsearch import Elasticsearch

# Elasticsearch に接続
es = Elasticsearch("http://elasticsearch:9200")

# 削除対象インデックス名
INDEX_NAME = "job_info"

# インデックス削除
if es.indices.exists(index=INDEX_NAME):
    es.indices.delete(index=INDEX_NAME)
    print(f"✅ インデックス '{INDEX_NAME}' を削除しました。")
else:
    print(f"⚠️ インデックス '{INDEX_NAME}' は存在しません。")
