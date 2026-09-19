import pytest

from sentinal.core.lifecycle import Lifecycle, LifecycleState


def test_startup_and_repeated_shutdown() -> None:
    events: list[str] = []
    lifecycle = Lifecycle(
        on_startup=lambda: events.append("start"), on_shutdown=lambda: events.append("stop")
    )
    lifecycle.startup()
    lifecycle.shutdown()
    lifecycle.shutdown()
    assert lifecycle.state is LifecycleState.STOPPED
    assert events == ["start", "stop"]


def test_failed_startup_can_still_shutdown() -> None:
    lifecycle = Lifecycle(on_startup=lambda: (_ for _ in ()).throw(RuntimeError("failure")))
    with pytest.raises(RuntimeError, match="failure"):
        lifecycle.startup()
    assert lifecycle.state is LifecycleState.FAILED
    lifecycle.shutdown()
    assert lifecycle.state is LifecycleState.STOPPED
