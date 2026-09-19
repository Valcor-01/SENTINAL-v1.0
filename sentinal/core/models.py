"""Shared foundation models; telemetry models are intentionally absent."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HealthStatus:
    status: str
    version: str
