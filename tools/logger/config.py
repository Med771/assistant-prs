import os

from pathlib import Path

from dotenv import load_dotenv

from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL, FileHandler


class LoggerConfig:
    load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")

    LOGS_DIR = Path(os.path.join(Path(__file__).parent.parent.parent, "logs"))
    ENCODING: str = os.getenv("ENCODING", "utf-8")

    DEBUG_FILENAME: str = os.getenv('DEBUG_FILENAME', 'debug.log')
    INFO_FILENAME: str = os.getenv('INFO_FILENAME', 'info.log')
    WARN_FILENAME: str = os.getenv('WARN_FILENAME', 'warn.log')
    ERROR_FILENAME: str = os.getenv('ERROR_FILENAME', 'error.log')
    CRIT_FILENAME: str = os.getenv('CRIT_FILENAME', 'crit.log')

    RECORD_MODE_W: str = "w"
    RECORD_MODE_A: str = "a"

    DEBUG_FMT: str = '#%(levelname)-5s [%(asctime)s] - %(message)s'
    INFO_FMT: str = '#%(levelname)-5s [%(asctime)s] - %(message)s'
    WARN_FMT: str = '[%(asctime)s] #%(levelname)-8s %(filename)s:%(lineno)d - %(message)s'
    ERROR_FMT: str = '[%(asctime)s] #%(levelname)-8s %(filename)s:%(lineno)d %(funcName)s() - %(message)s'
    CRIT_FMT: str = '[%(asctime)s] #%(levelname)-8s  %(filename)s:%(lineno)d %(funcName)s() - %(message)s'

    LOG_LEVELS: dict[int, dict[str, str]] = {
        DEBUG: {
            "dir": DEBUG_FILENAME,
            "format": DEBUG_FMT,
            "record_mode": RECORD_MODE_A
        },
        INFO: {
            "dir": INFO_FILENAME,
            "format": INFO_FMT,
            "record_mode": RECORD_MODE_A
        },
        WARNING: {
            "dir": WARN_FILENAME,
            "format": WARN_FMT,
            "record_mode": RECORD_MODE_A
        },
        ERROR: {
            "dir": ERROR_FILENAME,
            "format": ERROR_FMT,
            "record_mode": RECORD_MODE_A
        },
        CRITICAL: {
            "dir": CRIT_FILENAME,
            "format": CRIT_FMT,
            "record_mode": RECORD_MODE_A
        }
    }

    HANDLERS: dict[str, dict[int, FileHandler]] = dict()
