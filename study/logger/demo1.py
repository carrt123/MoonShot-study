import logging
import sys


def init_logger(file_name="running.log", logger_name="my_logger", log_level=logging.INFO, stdout=False):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)

    handler = logging.FileHandler(file_name)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if stdout:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger


# 使用参数 stdout=True 来开启输出到标准输出
logger = init_logger(stdout=True)

# 输出日志消息
logger.info('This is an informational message')
logger.warning('This is a warning message')
