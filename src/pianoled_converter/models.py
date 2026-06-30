"""Small, format-independent score model used by the converter."""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Note:
    """A MIDI note positioned in absolute ticks."""

    pitch: int
    start: int
    duration: int
    velocity: int = 64

    def __post_init__(self) -> None:
        if not 0 <= self.pitch <= 127:
            raise ValueError("pitch must be between 0 and 127")
        if self.start < 0:
            raise ValueError("start must not be negative")
        if self.duration <= 0:
            raise ValueError("duration must be positive")
        if not 1 <= self.velocity <= 127:
            raise ValueError("velocity must be between 1 and 127")


@dataclass(slots=True)
class Score:
    """The subset of a piano score needed for MIDI output."""

    title: str | None = None
    tempo_bpm: float = 120.0
    ticks_per_beat: int = 480
    right_hand: list[Note] = field(default_factory=list)
    left_hand: list[Note] = field(default_factory=list)
