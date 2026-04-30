from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.user_schema import UserCreate, UserRead
from services import user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # 서비스를 호출해서 유저를 생성합니다.
    new_user = user_service.create_user(db=db, user=user)
    if new_user is None:
        raise HTTPException(status_code=409, detail="이미 가입된 이메일입니다.")

    return {"message": "회원가입 성공", "user": UserRead.model_validate(new_user, from_attributes=True)}
