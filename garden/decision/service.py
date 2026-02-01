import logging
from .exc import DecisionServiceException
from .repository import DecisionRepository
from ..state.schemas import DerivedStateSnapshot

logger = logging.getLogger(__name__)


class DecisionService:

    def __init__(self, repo: DecisionRepository | None = None):
        self.repo = repo or DecisionRepository()
    
    def decide(self, state: DerivedStateSnapshot):
        ...

    def _save_decision(self):
        # self.repo.