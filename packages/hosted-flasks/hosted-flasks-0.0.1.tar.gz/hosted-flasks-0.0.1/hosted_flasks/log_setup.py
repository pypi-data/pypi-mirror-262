import logging

import os

# setup logging to stdout

logger = logging.getLogger(__name__)

LOG_LEVEL = os.environ.get("LOG_LEVEL") or "INFO"
FORMAT    = "[%(name)s] [%(levelname)s] %(message)s"
DATEFMT   = "%Y-%m-%d %H:%M:%S %z"

logging.basicConfig(level=LOG_LEVEL, format=FORMAT, datefmt=DATEFMT)
formatter = logging.Formatter(FORMAT, DATEFMT)
logging.getLogger().handlers[0].setFormatter(formatter)
