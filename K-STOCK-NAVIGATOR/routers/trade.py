from fastapi import APIRouter

router = APIRouter()

@router.post("/buy")
def buy_stock():
    return {"message": "매수 완료"}

@router.post("/sell")
def sell_stock():
    return {"message": "매도 완료"}
