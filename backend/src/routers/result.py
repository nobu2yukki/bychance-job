from fastapi import APIRouter

router = APIRouter()


# 結果を取得
@router.get("/get_results", tags=["result"])
def get_results():
    pass
