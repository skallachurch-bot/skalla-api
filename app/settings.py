from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_ENV: str = "production"
    APP_NAME: str = "SKALLA API"
    BASE_URL: str = "https://api.skalla.pt"

    DATABASE_URL: str

    VERIFY_TOKEN: str = "CHANGE_ME_VERIFY"
    WEBHOOK_SECRET: str = "CHANGE_ME_SECRET"

    WHATSAPP_TOKEN: str = ""
    WHATSAPP_PHONE_NUMBER_ID: str = ""

    OPENAI_API_KEY: str = ""

settings = Settings()
