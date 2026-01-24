from ..exc import StateServiceException
from .climate import ClimateStateService
from .light import LightStateService
from .soil_moisture import SoilMoistureService


class StateService:
    """
    Responsible for transforming raw sensor readings into coherent,
    plant-relevant derived state.

    This service aggregates recent readings, smooths noise, infers trends,
    and produces a point-in-time snapshot representing the system’s current
    belief about environmental conditions (e.g. soil moisture, climate, light).

    It contains no decision-making logic and performs no actions. Its sole role
    is to describe reality as best as possible given incomplete and noisy data,
    providing a stable and explainable input for downstream rules and agent
    reasoning.
    """
