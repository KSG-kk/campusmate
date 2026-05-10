from functools import lru_cache
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    deepseek_base_url: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    # 项目只允许这一个 DeepSeek 模型。不要在前端暴露多个模型选项。
    deepseek_model: str = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")

@lru_cache
def get_settings() -> Settings:
    return Settings()
