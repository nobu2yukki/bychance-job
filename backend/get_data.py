import json
from elasticsearch import Elasticsearch
from tqdm import tqdm

# Elasticsearch に接続
es = Elasticsearch("http://elasticsearch:9200")# 1件取得して確認

# インデックス名
INDEX_NAME = "job_info"
for i in range(10):
    res = es.get(index=INDEX_NAME, id=i+1)
    print(res["_source"])
