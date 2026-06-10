import logging
import os

# Default log level
_log_level = "INFO"
_configured = False

def configure_logging(level="INFO"):
    """Configure logging for the entire application"""
    global _log_level, _configured
    _log_level = level.upper()

    logging.basicConfig(
        level=_log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S',
        force=True  # Reconfigure if already configured
    )

    # Quiet down noisy third-party loggers
    logging.getLogger('pychromecast.socket_client').setLevel(logging.WARNING)
    logging.getLogger('pychromecast.discovery').setLevel(logging.WARNING)
    logging.getLogger('pychromecast.dial').setLevel(logging.WARNING)
    logging.getLogger('pychromecast.controllers').setLevel(logging.WARNING)
    logging.getLogger('pychromecast').setLevel(logging.INFO)
    logging.getLogger('asyncio').setLevel(logging.WARNING)

    _configured = True

def get_logger(name):
    """Get a logger for a specific module"""
    # Auto-configure with default if not already configured
    if not _configured:
        configure_logging(os.getenv("FURBY_LOG_LEVEL", "INFO"))
    return logging.getLogger(name)