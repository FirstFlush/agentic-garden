import logging
from .models import DecisionLog
from .schemas import DecisionSchema
from ..state.schemas import DerivedStateSnapshot
from ..common.exc import RepositoryError

logger = logging.getLogger(__name__)


class DecisionRepository:

    def save(
        self,
        result: DecisionSchema,
        snapshot: DerivedStateSnapshot,
    ) -> DecisionLog:
        """
        Persist a decision result along with the state snapshot that produced it.
        """
        try:
            return DecisionLog.create(
                decision_outcome=result.outcome.value,
                confidence=result.confidence,
                derived_state=snapshot.model_dump(mode="json"),
                policy_version=result.policy_version,
            )
        except Exception as e:
            msg = f"Failed to save DecisionLog: {e}"
            logger.error(msg, exc_info=True)
            raise RepositoryError(msg) from e
