import os

from pathlib import Path

from dotenv import load_dotenv


class CapConfig:
    load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")

    BASE_URL: str = os.getenv("BASE_URL", "")
    NEWS_PATH: str = os.getenv("NEWS_PATH", "")

    PORTALS: list[str] = os.getenv("PORTALS", "").split(",")
