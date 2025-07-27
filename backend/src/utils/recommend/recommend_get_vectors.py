# recommend_get_vectors.py
#スワイプ結果からユーザの好み、好みでない職種ベクトルを獲得

import numpy as np
from elasticsearch import Elasticsearch

# Elasticsearchクライアントはここで初期化するか、呼び出し元から渡す
# ここでは呼び出し元から渡されることを想定し、関数内でesを使用
# es = Elasticsearch("http://elasticsearch:9200")
INDEX_NAME = "job_info"

def fetch_vectors(es_client: Elasticsearch, ids: list) -> list:
    """
    指定されたIDリストからElasticsearchのembeddingベクトルを取得します。

    Args:
        es_client (Elasticsearch): Elasticsearchクライアントインスタンス。
        ids (list): ドキュメントIDのリスト。

    Returns:
        list: 取得されたnumpy.array形式のベクトルリスト。
    """
    vectors = []
    for doc_id in ids:
        try:
            res = es_client.get(index=INDEX_NAME, id=doc_id)
            vec = res["_source"].get("embedding")
            if vec:
                vectors.append(np.array(vec))
        except Exception as e:
            print(f"Error fetching embedding for {doc_id}: {e}")
    return vectors

def calculate_mean_vectors(good_vecs: list, bad_vecs: list) -> tuple:
    """
    Good/Badベクトルのリストからそれぞれの平均ベクトルを計算します。

    Args:
        good_vecs (list): Goodな求人のベクトルリスト。
        bad_vecs (list): Badな求人のベクトルリスト。

    Returns:
        tuple: (mean_good_vector, mean_bad_vector)。
               ベクトルが計算できない場合はNone。
    """
    mean_good = np.mean(good_vecs, axis=0) if good_vecs else None
    mean_bad = np.mean(bad_vecs, axis=0) if bad_vecs else None
    return mean_good, mean_bad

# テスト用
if __name__ == "__main__":
    # このファイルを単独でテストする場合のみESクライアントを初期化
    es_test = Elasticsearch("http://elasticsearch:9200")
    dummy_good_ids = ["365", "628"] # 実際のIDに置き換えてください
    dummy_bad_ids = ["8", "9"]     # 実際のIDに置き換えてください

    good_vecs_test = fetch_vectors(es_test, dummy_good_ids)
    bad_vecs_test = fetch_vectors(es_test, dummy_bad_ids)
    mean_good_test, mean_bad_test = calculate_mean_vectors(good_vecs_test, bad_vecs_test)

    print(f"Mean Good Vector shape: {mean_good_test.shape if mean_good_test is not None else None}")
    print(f"Mean Bad Vector shape: {mean_bad_test.shape if mean_bad_test is not None else None}")