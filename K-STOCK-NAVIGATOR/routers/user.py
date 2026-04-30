from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.user_schema import UserCreate
from services import user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # 서비스를 호출해서 유저를 생성합니다.
    new_user = user_service.create_user(db=db, user=user)
    return {"message": "회원가입 성공", "user": new_user}