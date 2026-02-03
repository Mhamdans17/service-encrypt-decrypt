import logging
import sys
from datetime import datetime, timezone, timedelta


# Define WIB timezone (UTC+7)
WIB = timezone(timedelta(hours=7))


# Custom formatter dengan warna dan format profesional
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',     # Blue
        'INFO': '\033[92m',      # Green
        'WARNING': '\033[93m',   # Yellow
        'ERROR': '\033[91m',     # Red
        'CRITICAL': '\033[95m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Format timestamp dengan WIB timezone
        timestamp = datetime.now(WIB).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        # Build formatted message
        formatted_msg = (
            f"{color}[{timestamp}]{reset} "
            f"{color}[{record.levelname:^8}]{reset} "
            f"{record.getMessage()}"
        )
        return formatted_msg


def setup_logger(name: str = "api") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(ColoredFormatter())
    
    logger.addHandler(console_handler)
    
    return logger


# Global logger instance
logger = setup_logger()
