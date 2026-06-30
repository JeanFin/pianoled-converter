"""Public conversion orchestration."""

from pathlib import Path

from .midi_writer import write_pianoled_midi
from .musicxml_reader import read_musicxml


def convert(input_path: str | Path, output_path: str | Path) -> None:
    """Convert a MusicXML file to a three-track Standard MIDI file."""

    score = read_musicxml(input_path)
    write_pianoled_midi(score, output_path)
