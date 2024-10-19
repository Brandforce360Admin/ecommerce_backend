import logging
import os
from logging.handlers import TimedRotatingFileHandler

from app.core.config import settings

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Define log directory and file
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_file = os.path.join(LOG_DIR, "ecommerce_logs.log")
handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1)
handler.suffix = "%Y%m%d"

# Set the logging format
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
)

handler.setFormatter(formatter)
# Create logger and set level to INFO or DEBUG
logger = logging.getLogger("ecommerce_logs")
logger.setLevel(logging.INFO)  # Use DEBUG for more detailed logs
logger.addHandler(handler)

# Optional: Also log to console for debugging purposes
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
