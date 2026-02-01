import logging

from .enums import DecisionOutcome
from .repository import DecisionRepository
from .schemas import DecisionSchema
from ..config.policies import PoliciesConfig
from ..state.schemas import DerivedStateSnapshot
from ..state.enums import TemperatureLevel, HumidityLevel, SoilMoistureLevel

logger = logging.getLogger(__name__)

# Hard floor for confidence. Below this, data is unusable.
CONFIDENCE_FLOOR = 0.5


class DecisionService:
    """
    Evaluates a DerivedStateSnapshot and produces a decision.

    Responsibilities:
    - Validate snapshot integrity (missing states, low confidence, bad windows)
    - Check for policy violations (levels outside acceptable range)
    - Produce a DecisionSchema
    - Persist to DecisionLog

    Does NOT:
    - Read from the database
    - Call the LLM
    - Execute actions
    """

    def __init__(
        self,
        policies: PoliciesConfig,
        repo: DecisionRepository | None = None,
    ):
        self.policies = policies
        self.repo = repo or DecisionRepository()

    def decide(self, snapshot: DerivedStateSnapshot) -> DecisionSchema:
        """
        Evaluate the snapshot and produce a decision.
        """

        # Step 1: Validate snapshot integrity
        if not self._is_snapshot_valid(snapshot):
            result = DecisionSchema(
                outcome=DecisionOutcome.ALERT,
                confidence=0.0,
                policy_version=self.policies.policy_version,
            )
            self.repo.save(result, snapshot)
            return result

        # Step 2: Check for policy violations
        if self._has_policy_violations(snapshot):
            confidence = self._aggregate_confidence(snapshot)
            result = DecisionSchema(
                outcome=DecisionOutcome.ESCALATE,
                confidence=confidence,
                policy_version=self.policies.policy_version,
            )
            self.repo.save(result, snapshot)
            return result

        # Step 3: All good
        confidence = self._aggregate_confidence(snapshot)
        result = DecisionSchema(
            outcome=DecisionOutcome.NO_ACTION,
            confidence=confidence,
            policy_version=self.policies.policy_version,
        )
        self.repo.save(result, snapshot)
        return result

    def _is_snapshot_valid(self, snapshot: DerivedStateSnapshot) -> bool:
        """
        Check if snapshot is usable for decision-making.
        Returns False if any critical issues exist.
        """
        # Missing sub-states
        if snapshot.climate is None:
            return False
        if snapshot.soil_moisture is None:
            return False
        if snapshot.light is None:
            return False

        # Low confidence
        if snapshot.climate.confidence < CONFIDENCE_FLOOR:
            return False
        if snapshot.soil_moisture.confidence < CONFIDENCE_FLOOR:
            return False
        if snapshot.light.confidence < CONFIDENCE_FLOOR:
            return False

        # Empty windows
        if snapshot.climate.sample_count <= 0:
            return False
        if snapshot.soil_moisture.sample_count <= 0:
            return False
        if snapshot.light.sample_count <= 0:
            return False

        return True

    def _has_policy_violations(self, snapshot: DerivedStateSnapshot) -> bool:
        """
        Check if any levels violate acceptable ranges.
        Assumes snapshot has already passed validation.
        """
        # Climate checks
        if snapshot.climate and snapshot.climate.temperature_level != TemperatureLevel.OK:
            return True
        if snapshot.climate and snapshot.climate.humidity_level != HumidityLevel.OK:
            return True

        # Soil moisture check
        if snapshot.soil_moisture and snapshot.soil_moisture.level != SoilMoistureLevel.OK:
            return True

        return False

    def _aggregate_confidence(self, snapshot: DerivedStateSnapshot) -> float:
        """
        Compute aggregate confidence as the minimum across all sub-states.
        A chain is only as strong as its weakest link.
        """
        confidences = []
        if snapshot.climate:
            confidences.append(snapshot.climate.confidence)
        if snapshot.soil_moisture:
            confidences.append(snapshot.soil_moisture.confidence)
        if snapshot.light:
            confidences.append(snapshot.light.confidence)

        return min(confidences) if confidences else 0.0
