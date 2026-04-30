from sqlalchemy.orm import Session
from models.user_model import User
from schemas.user_schema import UserCreate

def create_user(db: Session, user: UserCreate):
    # 암호화 과정 없이 입력받은 password를 그대로 저장합니다.
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=user.password  # 변수명은 hashed_password지만 실제론 평문 저장
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user