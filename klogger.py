# -*- encoding:utf-8 -*-
import logging
import defines
from logging import getLogger
from logging import FileHandler
from logging import DEBUG
from logging import WARNING
from logging import INFO
from logging import ERROR
from defines import TEST_LOG_PATH


logger = getLogger("Kurowiz")

# stream用のハンドラ
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(DEBUG)
STREAM_HANDLER.setFormatter(logging.Formatter(
    "%(message)s : %(pathname)s(%(lineno)d)"
    ))

# testフィアル用のハンドラ
TEST_FILE_HANDLER = FileHandler(TEST_LOG_PATH, 'a+')
TEST_FILE_HANDLER.setLevel(INFO)
#TEST_FILE_HANDLER.setLevel(DEBUG)
TEST_FILE_HANDLER.setFormatter(logging.Formatter(
    "%(message)s : %(asctime)s %(pathname)s(%(lineno)d)"
    ))

logger.addHandler(STREAM_HANDLER)
logger.addHandler(TEST_FILE_HANDLER)
logger.setLevel(DEBUG)
#logger.setLevel(INFO)

