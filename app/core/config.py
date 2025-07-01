from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneralSettings(BaseSettings):
    PGDB_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class SecuritySettings(BaseSettings):
    SALT_ROUNDS: int
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRY: int
    REFRESH_TOKEN_EXPIRY: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


GeneralConfig = GeneralSettings()
SecurityConfig = SecuritySettings()
