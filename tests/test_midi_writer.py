from pathlib import Path

import mido

from pianoled_converter.models import Note, Score
from pianoled_converter.midi_writer import write_pianoled_midi


def test_writes_expected_tracks_and_channels(tmp_path: Path) -> None:
    destination = tmp_path / "score.mid"
    score = Score(
        title="Example",
        tempo_bpm=100,
        right_hand=[Note(60, 0, 480, velocity=80), Note(62, 480, 240, velocity=70)],
        left_hand=[Note(48, 240, 480)],
    )

    write_pianoled_midi(score, destination)
    midi = mido.MidiFile(destination)

    assert midi.type == 1
    assert midi.ticks_per_beat == score.ticks_per_beat
    assert len(midi.tracks) == 3
    assert [track.name for track in midi.tracks] == ["Metadata", "Right Hand", "Left Hand"]

    tempo = next(message for message in midi.tracks[0] if message.type == "set_tempo")
    assert tempo.tempo == mido.bpm2tempo(100)

    right_program = next(message for message in midi.tracks[1] if message.type == "program_change")
    left_program = next(message for message in midi.tracks[2] if message.type == "program_change")
    assert (right_program.program, right_program.channel) == (0, 0)
    assert (left_program.program, left_program.channel) == (0, 1)

    right_notes = [message for message in midi.tracks[1] if message.type in {"note_on", "note_off"}]
    assert [(message.type, message.note, message.velocity, message.time) for message in right_notes] == [
        ("note_on", 60, 80, 0),
        ("note_off", 60, 0, 480),
        ("note_on", 62, 70, 0),
        ("note_off", 62, 0, 240),
    ]

    left_note = next(message for message in midi.tracks[2] if message.type == "note_on")
    assert (left_note.channel, left_note.time) == (1, 240)
