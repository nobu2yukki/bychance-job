from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.schemas.question import (
    AnswerPayload,
    InitialQuestion,
    InitialQuestionNoCondition,
)
from src.utils.session import get_session_id
from src.utils.session_store import ensure_session, get_session_data

router = APIRouter()

# モックの質問データ
DUMMY_QUESTIONS = [
    {
        "id": "q1",
        "text": "アルバイトを探すうえで一番大事にしたいことは？",
        "options": ["未経験歓迎", "高時給", "シフト自由"],
    },
    {
        "id": "q2",
        "text": "職場の雰囲気で重視したいのは？",
        "options": ["静か", "わいわい", "柔軟"],
    },
    {
        "id": "q3",
        "text": "働き方として希望するスタイルは？",
        "options": ["短期", "長期", "単発"],
    },
]


@router.get(
    "/questions/noCondition1",
    tags={"question"},
    response_model=InitialQuestionNoCondition,
)
def get_init_question_nocondition1():
    question1 = InitialQuestionNoCondition(
        id=1,
        type="choice",
        label="希望職種を選んでください",
        options=["イベント", "飲食", "接客", "医療・福祉"],
    )
    return question1


@router.get(
    "/questions/noCondition2",
    tags={"question"},
    response_model=InitialQuestionNoCondition,
)
def get_init_question_nocondition2():
    question1 = InitialQuestionNoCondition(
        id=2,
        type="choice",
        label="過去にアルバイト経験はありますか？",
        options=["はい", "いいえ"],
    )
    return question1


@router.get("/questions/Condition3", tags=["question"], response_model=InitialQuestion)
def get_init_question3():
    question3 = InitialQuestion(
        id=3,
        type="multi",
        label="過去に経験のある職種を選んでください",
        options=["イベント", "飲食", "接客"],
        showcondition={"questionId": 2, "selectedValue": "はい"},
    )
    return question3


@router.get("/questions/Condition4", tags=["question"], response_model=InitialQuestion)
def get_init_question4():
    question4 = InitialQuestion(
        id=4,
        type="multi",
        label="求人情報の推薦に、過去に経験のある職種を含めますか？",
        options=["はい", "いいえ"],
        showcondition={"questionId": 2, "selectedValue": "はい"},
    )
    return question4


@router.get("/questions/Condition5", tags=["question"], response_model=InitialQuestion)
def get_init_question5():
    question5 = InitialQuestion(
        id=5,
        type="multi",
        label="求人情報の推薦に、同じ業種の求人情報を含めますか？",
        options=["はい", "いいえ"],
        showcondition={"questionId": 2, "selectedValue": "はい"},
    )
    return question5


# 質問全部一気に返すAPI
@router.get("/questions/all", tags=["question"])
def get_all_questions():
    question_list = [
        {
            "id": 1,
            "type": "choice",
            "label": "希望職種を選んでください",
            "options": ["イベント", "飲食", "接客", "医療・福祉"],
        },
        {
            "id": 2,
            "type": "choice",
            "label": "過去にアルバイト経験はありますか？",
            "options": ["はい", "いいえ"],
        },
        {
            "id": 3,
            "type": "multi",
            "label": "過去に経験のある職種を選んでください",
            "options": ["イベント", "飲食", "接客"],
            "showCondition": {"questionId": 2, "selectedValue": "はい"},
        },
        {
            "id": 4,
            "type": "choice",
            "label": "求人情報の推薦に、過去に経験のある職種を含めますか？",
            "options": ["はい", "いいえ"],
            "showCondition": {"questionId": 2, "selectedValue": "はい"},
        },
        {
            "id": 5,
            "type": "coice",
            "label": "求人情報の推薦に、同じ業種の求人情報を含めますか？",
            "options": ["はい", "いいえ"],
            "showCondition": {"questionId": 2, "selectedValue": "はい"},
        },
    ]
    return question_list


@router.get("/questions", tags=["question"])
def get_questions():
    return DUMMY_QUESTIONS


# 回答送信用モデル
class QuestionAnswer(BaseModel):
    answers: dict[str, str]


@router.post("/questions/answer", tags=["question"])
def post_answers(
    answer_data: QuestionAnswer, session_id: str = Depends(get_session_id)
):
    ensure_session(session_id)
    session = get_session_data(session_id)

    session["question"] = answer_data.answers

    return {"message": "回答を受け取りました", "answers": answer_data.answers}


###ユーロ式に出力するPOST
@router.post("/questions/result", tags=["question"])
def post_question_result(payload: AnswerPayload):
    # ensure_session(session_id)

    # デフォルト値の定義
    result = {
        "desired_job_category": None,
        "previous_employment_history": [],
        "user_filter_label": True,
        "category_to_exclude": "parent",
    }

    answers = payload.answers

    # マッピング定義
    if 1 in answers:
        result["desired_job_category"] = answers[1]
    if 3 in answers:
        result["previous_employment_history"] = answers[3]
    if 4 in answers:
        result["user_filter_label"] = True if answers[4] == "はい" else False
    if 5 in answers:
        result["category_to_exclude"] = "parent" if answers[5] == "はい" else "child"

    # セッションに保存
    # session = get_session_data(session_id)
    # session["question"] = result

    return result
