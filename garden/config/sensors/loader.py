import logging
from pathlib import Path
import yaml
from .schemas import SensorsConfig

logger = logging.getLogger(__name__)

def load_sensors_config(path: Path) -> SensorsConfig:
    """
    Load and validate the sensors configuration from a YAML file.

    This function is responsible for:
    - reading sensors.yaml
    - parsing YAML into a Python dict
    - validating and coercing it into a SensorsConfig object

    It should be called once at startup. Downstream code should
    only interact with the returned SensorsConfig instance.
    """
    if not path.exists():
        raise FileNotFoundError(f"Sensors config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if raw is None:
        raise ValueError(f"Sensors config file is empty: {path}")

    logger.debug(f"Successfully built SensorsConfig object from {path.name}")

    return SensorsConfig(**raw)
