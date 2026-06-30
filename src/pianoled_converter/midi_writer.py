"""Write the internal score model as a three-track Standard MIDI file."""

from collections.abc import Iterable
from pathlib import Path

import mido

from .models import Note, Score


def _note_track(name: str, notes: Iterable[Note], channel: int) -> mido.MidiTrack:
    track = mido.MidiTrack()
    track.append(mido.MetaMessage("track_name", name=name, time=0))
    track.append(mido.Message("program_change", program=0, channel=channel, time=0))

    events: list[tuple[int, int, mido.Message]] = []
    for note in notes:
        events.append(
            (
                note.start,
                1,
                mido.Message(
                    "note_on", note=note.pitch, velocity=note.velocity, channel=channel
                ),
            )
        )
        events.append(
            (
                note.start + note.duration,
                0,
                mido.Message(
                    "note_off", note=note.pitch, velocity=0, channel=channel
                ),
            )
        )

    previous_tick = 0
    events.sort(key=lambda event: (event[0], event[1], event[2].note))
    for tick, _priority, message in events:
        message.time = tick - previous_tick
        track.append(message)
        previous_tick = tick
    track.append(mido.MetaMessage("end_of_track", time=0))
    return track


def write_pianoled_midi(score: Score, path: str | Path) -> None:
    """Write metadata, right-hand, and left-hand tracks to ``path``."""

    midi = mido.MidiFile(type=1, ticks_per_beat=score.ticks_per_beat)
    metadata = mido.MidiTrack()
    metadata.append(mido.MetaMessage("track_name", name="Metadata", time=0))
    metadata.append(
        mido.MetaMessage(
            "set_tempo", tempo=mido.bpm2tempo(score.tempo_bpm), time=0
        )
    )
    metadata.append(mido.MetaMessage("end_of_track", time=0))
    midi.tracks.extend(
        [
            metadata,
            _note_track("Right Hand", score.right_hand, channel=0),
            _note_track("Left Hand", score.left_hand, channel=1),
        ]
    )
    midi.save(path)
