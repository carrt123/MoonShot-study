import sys
import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler


def init_logger(file_name="running.log", logger_name="my_logger", log_level=logging.INFO, stdout=False):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    # 定义格式
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)

    # 定义文件日志， 单个文件最大10M
    handler = RotatingFileHandler(file_name, maxBytes=1024 * 1024 * 100, backupCount=10)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if stdout:
        stream_handler = StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
