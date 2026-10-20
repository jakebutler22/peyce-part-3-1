"""Server-only configuration; importing this module never calls a provider."""
from dataclasses import dataclass, field
from pathlib import Path
import os
from dotenv import load_dotenv

# Explicit repository-local configuration. Existing process variables win.
load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)


@dataclass(frozen=True)
class Settings:
    db_path: str = field(default_factory=lambda: os.getenv("PEYCE_DB_PATH", str(Path(__file__).resolve().parents[1] / ".runtime/peyce.sqlite3")))
    model_mode: str = field(default_factory=lambda: os.getenv("PEYCE_MODEL_MODE", "mock"))
    model_id: str = field(default_factory=lambda: os.getenv("OPENROUTER_MODEL", ""))
    api_key: str = field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY", ""), repr=False)
    approved_budget_usd: float = field(default_factory=lambda: float(os.getenv("PEYCE_LIVE_APPROVED_BUDGET_USD", "0")))
    budget_approved: bool = field(default_factory=lambda: "PEYCE_LIVE_APPROVED_BUDGET_USD" in os.environ)
    live_max_attempts: int = field(default_factory=lambda: min(10, max(0, int(os.getenv("PEYCE_LIVE_MAX_ATTEMPTS", "10")))))
    input_price_per_million: float = field(default_factory=lambda: float(os.getenv("PEYCE_INPUT_PRICE_PER_MILLION", "0")))
    output_price_per_million: float = field(default_factory=lambda: float(os.getenv("PEYCE_OUTPUT_PRICE_PER_MILLION", "0")))
    pricing_verified: bool = field(default_factory=lambda: os.getenv("PEYCE_PRICING_VERIFIED", "0") == "1")
    model_timeout_seconds: float = field(default_factory=lambda: min(15.0, max(0.05, float(os.getenv("PEYCE_MODEL_TIMEOUT_SECONDS", "8")))))
    test_controls: bool = field(default_factory=lambda: os.getenv("PEYCE_TEST_CONTROLS", "0") == "1")
    test_late_seconds: float = 0.5

    def __post_init__(self):
        if self.model_mode not in ("mock", "openrouter"):
            raise ValueError("PEYCE_MODEL_MODE must be mock or the authorized openrouter provider")
        if not 0 <= self.live_max_attempts <= 10:
            raise ValueError("The user's revised Part 3.2 ceiling is ten outbound attempts")

    @property
    def live_configured(self):
        if self.model_mode == "openrouter":
            # Human authorization is this exact free model, zero dollars,
            # ten attempts. A paid model or fallback fails closed.
            return bool(self.model_id == "nvidia/nemotron-3.5-lightning:free" and self.api_key
                        and self.budget_approved and self.approved_budget_usd == 0
                        and self.live_max_attempts > 0 and self.pricing_verified
                        and self.input_price_per_million == self.output_price_per_million == 0)
        return False

    @property
    def attempt_reservation_usd(self):
        # Input is limited to 5,000 UTF-8 bytes; reserve 10,000 input tokens,
        # including framing, and 1,000 output tokens. This is conservative
        # budgeting, not a claim about exact provider billing.
        return (10000 * self.input_price_per_million + 1000 * self.output_price_per_million) / 1_000_000
