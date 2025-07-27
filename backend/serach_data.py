from elasticsearch import Elasticsearch

es = Elasticsearch("http://elasticsearch:9200")
INDEX_NAME = "job_info"

# クエリを定義(例:industry.parent が "飲食" 以外のものを取得)
#must_notで以外を取得
query = {
    "query": {
        "bool": {
            "must": [
                {
                    "term": {
                        "category.parent": "飲食"
                    }
                }
            ]
        }
    }
}


# 検索実行(上位10件)
res = es.search(index=INDEX_NAME, body=query, size=0)
hit_count = res["hits"]["total"]["value"]
print(hit_count,'件検索')
# # 結果を表示
# for hit in res["hits"]["hits"]:
#     print(hit["_source"])
