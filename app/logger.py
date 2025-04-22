import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


# Create logs directory if it doesn't exist
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            'logs/bookstore.log', maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
        ),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger('bookstore')
