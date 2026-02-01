"""
Prompt building for the LLM service.

Loads system prompt from YAML and formats state snapshots into user messages.
"""

import logging
from pathlib import Path
import yaml

from .exc import PromptBuildError
from ..state.schemas import DerivedStateSnapshot

logger = logging.getLogger(__name__)

# Default path to system prompt
DEFAULT_SYSTEM_PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts" / "system.yaml"


class PromptBuilder:
    """Builds messages for Claude from state snapshots."""

    def __init__(self, system_prompt_path: Path | None = None):
        self.system_prompt_path = system_prompt_path or DEFAULT_SYSTEM_PROMPT_PATH
        self._system_prompt: str | None = None

    @property
    def system_prompt(self) -> str:
        """Load and cache the system prompt."""
        if self._system_prompt is None:
            self._system_prompt = self._load_system_prompt()
        return self._system_prompt

    def _load_system_prompt(self) -> str:
        """Load system prompt from YAML file."""
        try:
            with open(self.system_prompt_path) as f:
                data = yaml.safe_load(f)

            parts = []
            if "role" in data:
                parts.append(data["role"].strip())
            if "constraints" in data:
                parts.append("\nConstraints:")
                for constraint in data["constraints"]:
                    parts.append(f"- {constraint}")
            if "context" in data:
                parts.append(f"\n{data['context'].strip()}")

            return "\n".join(parts)
        except Exception as e:
            msg = f"Failed to load system prompt from {self.system_prompt_path}: {e}"
            logger.error(msg, exc_info=True)
            raise PromptBuildError(msg) from e

    def build_user_message(self, snapshot: DerivedStateSnapshot) -> str:
        """Format the state snapshot as a user message for Claude."""
        lines = [
            f"Current time: {snapshot.created.isoformat()}",
            "",
            "=== STATE SNAPSHOT ===",
        ]

        # Climate
        if snapshot.climate:
            c = snapshot.climate
            lines.extend([
                "",
                "CLIMATE:",
                f"  Temperature: {c.temperature_c:.1f}°C",
                f"    Level: {c.temperature_level.value}",
                f"    Trend: {c.temperature_trend.value}",
                f"  Humidity: {c.humidity_rh:.1f}%",
                f"    Level: {c.humidity_level.value}",
                f"    Trend: {c.humidity_trend.value}",
                f"  Confidence: {c.confidence:.0%}",
            ])
        else:
            lines.append("\nCLIMATE: No data available")

        # Soil moisture
        if snapshot.soil_moisture:
            s = snapshot.soil_moisture
            lines.extend([
                "",
                "SOIL MOISTURE:",
                f"  Moisture: {s.avg_moisture:.2f}",
                f"  Level: {s.level.value}",
                f"  Trend: {s.trend.value}",
                f"  Confidence: {s.confidence:.0%}",
            ])
        else:
            lines.append("\nSOIL MOISTURE: No data available")

        # Light
        if snapshot.light:
            lt = snapshot.light
            lines.extend([
                "",
                "LIGHT:",
                f"  Intensity: {lt.intensity:.2f}",
                f"  Light on: {lt.is_light_on}",
                f"  Confidence: {lt.confidence:.0%}",
            ])
        else:
            lines.append("\nLIGHT: No data available")

        lines.extend([
            "",
            "=== DECISION REQUIRED ===",
            "Based on the state above, decide what action to take.",
            "Use no_action if conditions are acceptable.",
        ])

        return "\n".join(lines)
