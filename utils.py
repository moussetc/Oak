import logging
from logging.handlers import TimedRotatingFileHandler

# Log to file, rotate everyday, delete old ones
handler = TimedRotatingFileHandler('bot_oak.log', when='midnight', backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
