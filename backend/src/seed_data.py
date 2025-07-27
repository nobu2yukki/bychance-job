from elasticsearch import Elasticsearch
import json
from tqdm import tqdm

# Elasticsearchクライアント
es = Elasticsearch("http://elasticsearch:9200")
INDEX_NAME = "job_info"

# 新しいJSONの構造に対応するマッピング
# 各フィールドの型を適切に定義します
mapping = {
    "mappings": {
        "properties": {
            "embedding": {
                "type": "dense_vector",
                "dims": 384,
                "index": True,
                "similarity": "cosine"
            },
            "company_name": { "type": "text" }, # 'job'から変更
            "image_url": { "type": "keyword" }, # URLは通常keyword型が適しています
            "place": { "type": "text" }, # 'job_place'から変更
            "salary": { "type": "keyword" }, # 給与は厳密な値やファセット検索のためにkeyword型が良い場合があります
            "description": { "type": "text" }, # 'job_description'から変更
            "category": { # 'job_tag.industry'から変更、ネストされたオブジェクトとして定義
                "type": "object",
                "properties": {
                    "parent": { "type": "keyword" }, # 親カテゴリはkeyword型
                    "child": { "type": "keyword" }   # 子カテゴリはkeyword型
                }
            },
            "work_style": { "type": "keyword" }, # リスト要素はkeyword型として扱われます
            "audience": { "type": "keyword" }    # リスト要素はkeyword型として扱われます
        }
    }
}

# 既存のインデックスを削除して再作成する場合(任意)
# マッピング変更時はインデックスを削除・再作成するのが最も確実です
if es.indices.exists(index=INDEX_NAME):
    print(f"既存のインデックス '{INDEX_NAME}' を削除します。")
    es.indices.delete(index=INDEX_NAME)
print(f"インデックス '{INDEX_NAME}' を作成します。")
es.indices.create(index=INDEX_NAME, body=mapping)

# JSONファイル読み込み（idフィールドあり）
# ファイルパスはあなたの環境に合わせて調整してください
json_file_path = "/app/hamamatsu_jobs_info.json"
# もし整形後のJSONファイル名が異なる場合は、ここで正しいパスを指定してください
# 例: json_file_path = "/app/output.json"

try:
    with open(json_file_path, encoding="utf-8") as f:
        jobs = json.load(f)

    # データ投入(JSON内のidを使う)
    print(f"{len(jobs)} 件の求人情報をインデックス '{INDEX_NAME}' に登録します。")
    for job in tqdm(jobs):
        # job["id"]が存在することを確認
        if "id" in job:
            es.index(index=INDEX_NAME, id=job["id"], document=job)
        else:
            print(f"警告: IDがないドキュメントをスキップしました: {job}")

    print(f"{len(jobs)} 件の求人情報をインデックス {INDEX_NAME} に登録しました。")

except FileNotFoundError:
    print(f"エラー: JSONファイル '{json_file_path}' が見つかりません。パスを確認してください。")
except json.JSONDecodeError:
    print(f"エラー: JSONファイル '{json_file_path}' の形式が不正です。")
except Exception as e:
    print(f"データ投入中に予期せぬエラーが発生しました: {e}")