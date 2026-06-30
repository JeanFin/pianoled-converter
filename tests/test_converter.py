from pathlib import Path

import mido

from pianoled_converter.converter import convert


def test_converts_minimal_file(tmp_path: Path) -> None:
    source = tmp_path / "one-note.xml"
    destination = tmp_path / "one-note.mid"
    source.write_text(
        """<score-partwise><part-list/><part id="P1"><measure number="1">
        <attributes><divisions>1</divisions></attributes>
        <note><pitch><step>A</step><octave>4</octave></pitch><duration>1</duration><staff>1</staff></note>
        </measure></part></score-partwise>""",
        encoding="utf-8",
    )

    convert(source, destination)

    midi = mido.MidiFile(destination)
    note = next(message for message in midi.tracks[1] if message.type == "note_on")
    assert (note.note, note.time) == (69, 0)
