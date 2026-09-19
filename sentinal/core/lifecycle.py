"""Small, explicit ownership boundary for application startup and shutdown."""

from collections.abc import Callable
from enum import StrEnum


class LifecycleState(StrEnum):
    NEW = "new"
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"


class Lifecycle:
    def __init__(
        self,
        on_startup: Callable[[], None] | None = None,
        on_shutdown: Callable[[], None] | None = None,
    ) -> None:
        self._on_startup = on_startup
        self._on_shutdown = on_shutdown
        self.state = LifecycleState.NEW

    def startup(self) -> None:
        if self.state is LifecycleState.RUNNING:
            return
        try:
            if self._on_startup:
                self._on_startup()
            self.state = LifecycleState.RUNNING
        except Exception:
            self.state = LifecycleState.FAILED
            raise

    def shutdown(self) -> None:
        if self.state is LifecycleState.STOPPED:
            return
        try:
            if self._on_shutdown:
                self._on_shutdown()
        finally:
            self.state = LifecycleState.STOPPED
