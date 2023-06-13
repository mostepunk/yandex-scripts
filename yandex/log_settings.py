"""Настройки логгера для проекта."""

import logging

root_logger = "main_logger"
LOGGERS = (root_logger,)

log_format = "%(levelname)s  - %(filename)s.(%(funcName)s:%(lineno)d): %(message)s "
formatter = logging.Formatter(log_format)

st = logging.StreamHandler()
st.setFormatter(formatter)

for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [st]
    logging_logger.setLevel("INFO")
