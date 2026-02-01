from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FRONTEND_URL: str 
    DATABASE_URL: str
    SECRET_KEY: str

    # 60 minutes x 24 hours x 7 days = 10080 minutes == 1 week
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 10080

    # FIRST ACCOUNT FOR ADMIN
    FIRST_ADMIN_EMAIL:str = "23050118@student.bdu.edu.vn"
    FIRST_ADMIN_PASSWORD:str
    GITHUB_TOKEN : str
    RECOVERY_KEY_ADMIN: str
    DISCORD_WEB_HOOK: str


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        case_sensitive = True

settings = Settings()

