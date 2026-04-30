from fastapi import APIRouter

router = APIRouter()

stocks = [
    {"id": 1, "name": "삼성전자", "price": 72000},
    {"id": 2, "name": "카카오", "price": 50000}
]

@router.get("/stocks")
def get_stocks():
    return stocks