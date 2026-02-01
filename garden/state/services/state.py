from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import logging

from ..exc import StateServiceException
from ..schemas import (
    ClimateStateSchema,
    LightStateSchema,
    SoilMoistureStateSchema,
    DerivedStateSnapshot,
)
from .climate import ClimateStateService
from .light import LightStateService
from .soil_moisture import SoilMoistureStateService

from ...config.sensors import SensorsConfig, EvidenceConfig
from ...config.policies import PoliciesConfig
from ...hardware.sensors.repository import SensorReadingRepository
from ...hardware.sensors.enums import SensorType
from ...hardware.sensors.dto import ClimateReading, LightReading, SoilMoistureReading
from ...hardware.sensors.schemas import ClimatePayload, LightPayload, SoilMoisturePayload

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PreviousStates:
    """Carries forward state needed for hysteresis calculations."""
    light: LightStateSchema | None = None


class StateService:
    """
    Orchestrates state derivation across all sensor domains.

    Responsible for:
    - Fetching readings within configured evidence windows
    - Delegating to domain-specific services
    - Bundling results into a unified snapshot

    This service aggregates recent readings, smooths noise, infers trends,
    and produces a point-in-time snapshot representing the system's current
    belief about environmental conditions (e.g. soil moisture, climate, light).

    It contains no decision-making logic and performs no actions. Its sole role
    is to describe reality as best as possible given incomplete and noisy data,
    providing a stable and explainable input for downstream rules and agent
    reasoning.
    """

    def __init__(
        self,
        repository: SensorReadingRepository,
        sensors_config: SensorsConfig,
        policies_config: PoliciesConfig,
    ):
        self.repository = repository
        self.sensors = sensors_config
        self.policies = policies_config

        self._climate = ClimateStateService(policies_config)
        self._soil_moisture = SoilMoistureStateService(policies_config)
        self._light = LightStateService(policies_config)

    def derive_snapshot(
        self,
        as_of: datetime | None = None,
        previous: PreviousStates | None = None,
    ) -> DerivedStateSnapshot:
        """
        Derive a complete state snapshot as of a given time.

        Args:
            as_of: The reference time for the snapshot. Defaults to now (UTC).
            previous: Previous states needed for hysteresis (e.g., light on/off).

        Returns:
            DerivedStateSnapshot with all domain states (None for domains
            with insufficient data).
        """
        now = as_of or datetime.now(timezone.utc)
        previous = previous or PreviousStates()

        climate = self._derive_climate(now)
        soil_moisture = self._derive_soil_moisture(now)
        light = self._derive_light(now, previous.light)

        return DerivedStateSnapshot(
            created=now,
            climate=climate,
            soil_moisture=soil_moisture,
            light=light,
        )

    def _derive_climate(self, as_of: datetime) -> ClimateStateSchema | None:
        """Derive climate state from configured climate sensors."""
        cfg = self.sensors.climate
        window_start = self._window_start(as_of, cfg.evidence)

        # For now: use first sensor. Future: aggregate multiple sensors.
        sensor = cfg.sensors[0]

        readings = self.repository.fetch_readings(
            sensor_type=SensorType.CLIMATE,
            sensor_id=sensor.id,
            window_start=window_start,
            window_end=as_of,
        )

        if not readings:
            logger.warning(f"No climate readings in window [{window_start}, {as_of}]")
            return None

        parsed = [
            ClimateReading(
                created=r.created,
                sensor_type=SensorType.CLIMATE,
                sensor_id=r.sensor_id,
                payload=ClimatePayload(**r.payload),
            )
            for r in readings
        ]

        return self._climate.derive_state(parsed)

    def _derive_soil_moisture(self, as_of: datetime) -> SoilMoistureStateSchema | None:
        """Derive soil moisture state from configured sensors."""
        cfg = self.sensors.soil_moisture
        window_start = self._window_start(as_of, cfg.evidence)

        sensor = cfg.sensors[0]

        readings = self.repository.fetch_readings(
            sensor_type=SensorType.SOIL_MOISTURE,
            sensor_id=sensor.id,
            window_start=window_start,
            window_end=as_of,
        )

        if not readings:
            logger.warning(f"No soil moisture readings in window [{window_start}, {as_of}]")
            return None

        parsed = [
            SoilMoistureReading(
                created=r.created,
                sensor_type=SensorType.SOIL_MOISTURE,
                sensor_id=r.sensor_id,
                payload=SoilMoisturePayload(**r.payload),
            )
            for r in readings
        ]

        return self._soil_moisture.derive_state(parsed)

    def _derive_light(
        self,
        as_of: datetime,
        previous: LightStateSchema | None,
    ) -> LightStateSchema | None:
        """Derive light state, using previous state for hysteresis."""
        cfg = self.sensors.light
        window_start = self._window_start(as_of, cfg.evidence)

        sensor = cfg.sensors[0]

        readings = self.repository.fetch_readings(
            sensor_type=SensorType.LIGHT,
            sensor_id=sensor.id,
            window_start=window_start,
            window_end=as_of,
        )

        if not readings:
            logger.warning(f"No light readings in window [{window_start}, {as_of}]")
            return None

        parsed = [
            LightReading(
                created=r.created,
                sensor_type=SensorType.LIGHT,
                sensor_id=r.sensor_id,
                payload=LightPayload(**r.payload),
            )
            for r in readings
        ]

        return self._light.derive_state(parsed, previous_state=previous)

    def _window_start(self, as_of: datetime, evidence: EvidenceConfig) -> datetime:
        """
        Calculate window start based on evidence config.

        For time-based lookback, subtracts the configured seconds.
        For sample-based lookback, uses a generous 1-hour window and relies
        on domain services to limit samples as needed.
        """
        if evidence.lookback_seconds is not None:
            return as_of - timedelta(seconds=evidence.lookback_seconds)

        # Sample-based: use generous window, let domain service handle limiting
        return as_of - timedelta(hours=1)
