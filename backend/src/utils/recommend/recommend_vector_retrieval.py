# recommend_vector_retrieval.py
#ベクトル検索をelastic search内で行い好みに意味的に似た求人を収集

from elasticsearch import Elasticsearch
import numpy as np

# Elasticsearchクライアントは呼び出し元から渡す
# es = Elasticsearch("http://elasticsearch:9200")
INDEX_NAME = "job_info"

def knn_search(es_client: Elasticsearch, query_vec: np.ndarray, k: int = 70, num_candidates: int = 600) -> list:
    """
    指定されたクエリベクトルに基づいてKNN検索を実行します。

    Args:
        es_client (Elasticsearch): Elasticsearchクライアントインスタンス。
        query_vec (np.ndarray): 検索クエリベクトル。
        k (int): 返すヒット数。
        num_candidates (int): KNN探索の候補数。

    Returns:
        list: Elasticsearchの検索結果（ヒットリスト）。
    """
    if query_vec is None: # ベクトルがNoneの場合は検索をスキップ
        print("Warning: Query vector is None. Skipping KNN search.")
        return []

    query = {
        "knn": {
            "field": "embedding",
            "query_vector": query_vec.tolist(),
            "k": k,
            "num_candidates": num_candidates
        },
        "size": k
    }
    try:
        return es_client.search(index=INDEX_NAME, body=query)["hits"]["hits"]
    except Exception as e:
        print(f"Error during KNN search: {e}")
        return []

# テスト用
if __name__ == "__main__":
    es_test = Elasticsearch("http://elasticsearch:9200")
    # ダミーベクトル（実際にはrecommend_get_vectorsから取得）
    dummy_query_vec = np.random.rand(384)
    hits_test = knn_search(es_test, dummy_query_vec, k=5)
    print(f"KNN search test results count: {len(hits_test)}")
    if hits_test:
        print(f"First hit ID: {hits_test[0]['_id']}, Score: {hits_test[0]['_score']}")