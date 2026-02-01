import logging
from pathlib import Path
import yaml
from .schemas import PoliciesConfig

logger = logging.getLogger(__name__)


def load_policies_config(path: Path) -> PoliciesConfig:
    """
    Load and validate the policies configuration from a YAML file.
    """
    if not path.exists():
        raise FileNotFoundError(f"Policies config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if raw is None:
        raise ValueError(f"Policies config file is empty: {path}")

    logger.debug(f"Successfully built PoliciesConfig object from {path.name}")

    return PoliciesConfig(**raw)
