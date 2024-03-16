import logging
import logging.config
from typing import Any

logger = logging.getLogger(__name__)


def load_dict_config(dic: dict[str, Any]) -> None:
    logging.config.dictConfig(dic)
    logger.debug("Logging configured")
