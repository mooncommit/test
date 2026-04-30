from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Supabase 대신 내 컴퓨터에 파일로 저장되는 SQLite 사용
# 프로젝트 폴더 안에 'k_stock.db'라는 파일이 자동으로 생성됩니다.
SQLALCHEMY_DATABASE_URL = "sqlite:///./k_stock.db"

# 2. SQLite 엔진 설정
# check_same_thread: False는 FastAPI처럼 멀티 스레드 환경에서 SQLite를 쓸 때 필수입니다.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 최신 SQLAlchemy 2.0 권장 방식
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()