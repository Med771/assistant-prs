import os

from pathlib import Path

from logging import getLogger, Logger, FileHandler, Formatter, Filter, LogRecord
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

from tools.logger.config import LoggerConfig

handlers = LoggerConfig.HANDLERS


class LevelFilter(Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record: LogRecord) -> bool:
        return record.levelno == self.level


def ensure_log_dirs(name: str = __name__):
    current_file_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    base_dir = Path(os.path.dirname(os.path.dirname(current_file_dir)))

    base_logs_dir = Path(os.path.join(base_dir, LoggerConfig.LOGS_DIR))
    os.makedirs(base_logs_dir, exist_ok=True)

    module_log_dir = Path(os.path.join(base_logs_dir, name))
    os.makedirs(module_log_dir, exist_ok=True)

    return module_log_dir


def create_handler(level: int, module_log_dir: Path) -> FileHandler:
    path = Path(os.path.join(module_log_dir, LoggerConfig.LOG_LEVELS[level]["dir"]))

    handler: FileHandler = FileHandler(
        filename=path,
        mode=LoggerConfig.LOG_LEVELS[level]["record_mode"],
        encoding=LoggerConfig.ENCODING)

    formatter: Formatter = Formatter(
        fmt=LoggerConfig.LOG_LEVELS[level]["format"])

    handler.setFormatter(formatter)
    handler.addFilter(LevelFilter(level))

    return handler


def create_level(logger: Logger, level: int, module: str):
    module_log_dir = ensure_log_dirs(module)

    if module not in handlers:
        handlers[module] = {}

    if handlers[module].get(level, {}) == {}:
        handler = create_handler(level, module_log_dir)

        handlers[module][level] = handler
        logger.addHandler(handler)
    else:
        existing_handler = handlers[module][level]

        if existing_handler not in logger.handlers:
            logger.addHandler(existing_handler)


class LoggerHelper:
    @staticmethod
    def get_logger(name: str,
                   module: str,
                   debug: bool = False,
                   info: bool = False,
                   warn: bool = False,
                   error: bool = False,
                   critical: bool = False,
                   ) -> Logger:
        logger: Logger = getLogger(name)
        logger.setLevel(DEBUG)

        if debug: create_level(logger, DEBUG, module)

        if info: create_level(logger, INFO, module)

        if warn: create_level(logger, WARNING, module)

        if error: create_level(logger, ERROR, module)

        if critical: create_level(logger, CRITICAL, module)

        return logger