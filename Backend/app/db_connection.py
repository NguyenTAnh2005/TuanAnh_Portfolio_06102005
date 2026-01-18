from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# Find  Database URL (Load biến Database đang chạy ở đâu)
DATABASE_URL = settings.DATABASE_URL

# Create Engine that connect to Database  (Cỗ máy kết nối đến CSDL để thao tác với nó)
engine = create_engine(DATABASE_URL)

# Create Sesionmaker - create sesion to Database ( Tạo phiên làm việc với DB để thao tác với nó)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for ORM models ( Tạo lớp cơ sở cho các mô hình ORM để dựa vào đó tạo các bảng trong DB)
class Base(DeclarativeBase):
    pass

# Function to get database session ( Hàm để lấy phiên làm việc với DB bởi vì FastAPI cần hàm này để thao tác với DB)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

