"""
Logging utility for the video generation pipeline.
Provides consistent logging across all modules.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    project_name: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
        project_name: Optional project name for log file naming
        
    Returns:
        Logger instance
    """
    # Create logger
    logger = logging.getLogger("faceless_viral_bot")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
    elif project_name:
        # Create logs directory in project folder
        log_dir = Path("projects") / project_name / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = log_dir / f"{timestamp}.log"
    else:
        log_path = None
    
    if log_path:
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)  # Log everything to file
        logger.addHandler(file_handler)
        logger.info(f"Log file created: {log_path}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class ProgressLogger:
    """Helper class for logging progress of long-running tasks."""
    
    def __init__(self, logger: logging.Logger, total: int, description: str = "Processing"):
        """
        Initialize progress logger.
        
        Args:
            logger: Logger instance
            total: Total number of items
            description: Description of the task
        """
        self.logger = logger
        self.total = total
        self.description = description
        self.current = 0
    
    def update(self, n: int = 1, message: Optional[str] = None) -> None:
        """
        Update progress.
        
        Args:
            n: Number of items completed
            message: Optional additional message
        """
        self.current += n
        percent = (self.current / self.total) * 100 if self.total > 0 else 0
        
        if message:
            self.logger.info(f"{self.description}: {self.current}/{self.total} ({percent:.1f}%) - {message}")
        else:
            self.logger.info(f"{self.description}: {self.current}/{self.total} ({percent:.1f}%)")
    
    def finish(self, message: Optional[str] = None) -> None:
        """
        Mark task as complete.
        
        Args:
            message: Optional completion message
        """
        if message:
            self.logger.info(f"{self.description} completed: {message}")
        else:
            self.logger.info(f"{self.description} completed successfully")
