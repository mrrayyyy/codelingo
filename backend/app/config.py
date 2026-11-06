"""Environment settings shared by the API and the cloud extractor."""
from pathlib import Path

from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "sqlite:///./.data/codelingo.db"
    # inline: dev, CI and Compose; github_actions: managed cloud (ADR 0004).
    job_mode: Literal["inline", "github_actions"] = "inline"
    api_key: str = "local-development-key"
    spool_dir: Path = Path(".data/uploads")
    dictionary_online: bool = False
    timezone: str = "Asia/Ho_Chi_Minh"
    max_upload_bytes: int = 20 * 1024 * 1024
    max_expanded_bytes: int = 50 * 1024 * 1024
    max_files: int = 5000
    piper_binary: str = ""
    piper_model: str = ""
    whisper_url: str = ""
    ollama_url: str = ""
    ollama_model: str = ""
    github_actions_token: str = ""
    github_actions_repo: str = ""
    github_actions_ref: str = "main"
    github_actions_workflow: str = "extract.yml"
    tts_provider: Literal["piper", "groq"] = "piper"
    stt_provider: Literal["whisper", "groq"] = "whisper"
    llm_provider: Literal["ollama", "groq"] = "ollama"
    groq_api_key: str = ""
    groq_tts_model: str = "canopylabs/orpheus-v1-english"
    groq_voice: str = "troy"
    groq_stt_model: str = "whisper-large-v3-turbo"
    groq_llm_model: str = "openai/gpt-oss-20b"


settings = Settings()
