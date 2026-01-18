from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FRONTEND_URL: str = "http://localhost:5173"
    DATABASE_URL: str = "postgresql://postgres:ntaPGSQL2005@localhost/my_portfolio_db"
    SECRET_KEY: str
    MAIL_USERNAME:str = "23050118@student.bdu.edu.vn"
    MAIL_PASSWORD:str
    MAIL_FROM:str = "23050118@student.bdu.edu.vn"
    MAIL_PORT:str = "465"
    MAIL_SERVER:str = "smtp.gmail.com"

    # 60 minutes x 24 hours x 21 days = 30240 minutes == 3 weeks
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 30240

    # FIRST ACCOUNT FOR ADMIN
    FIRST_ADMIN_EMAIL:str = "23050118@student.bdu.edu.vn"
    FIRST_ADMIN_PASSWORD:str

    GITHUB_TOKEN : str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        case_sensitive = True

settings = Settings()