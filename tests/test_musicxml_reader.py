from pathlib import Path

from pianoled_converter.musicxml_reader import read_musicxml


def test_reads_two_staves_chord_and_tempo(tmp_path: Path) -> None:
    source = tmp_path / "score.musicxml"
    source.write_text(
        """<?xml version="1.0"?>
<score-partwise version="4.0">
  <work><work-title>Small Prelude</work-title></work>
  <part-list><score-part id="P1"><part-name>Piano</part-name></score-part></part-list>
  <part id="P1"><measure number="1">
    <attributes><divisions>2</divisions></attributes>
    <direction><sound tempo="90"/></direction>
    <note><pitch><step>C</step><octave>4</octave></pitch><duration>2</duration><staff>1</staff></note>
    <note><chord/><pitch><step>E</step><octave>4</octave></pitch><duration>2</duration><staff>1</staff></note>
    <backup><duration>2</duration></backup>
    <note><pitch><step>C</step><octave>3</octave></pitch><duration>4</duration><staff>2</staff></note>
  </measure></part>
</score-partwise>
""",
        encoding="utf-8",
    )

    score = read_musicxml(source)

    assert score.title == "Small Prelude"
    assert score.tempo_bpm == 90
    assert [(note.pitch, note.start, note.duration) for note in score.right_hand] == [
        (60, 0, 480),
        (64, 0, 480),
    ]
    assert [(note.pitch, note.start, note.duration) for note in score.left_hand] == [(48, 0, 960)]


def test_reads_namespaced_metronome_rest_and_forward(tmp_path: Path) -> None:
    source = tmp_path / "namespaced.musicxml"
    source.write_text(
        """<score-partwise xmlns="http://www.musicxml.org/ns/musicxml" version="4.0">
  <work><work-title>Timing</work-title></work>
  <part-list><score-part id="P1"><part-name>Piano</part-name></score-part></part-list>
  <part id="P1"><measure number="1">
    <attributes><divisions>4</divisions></attributes>
    <direction><direction-type><metronome><beat-unit>quarter</beat-unit><per-minute>72</per-minute></metronome></direction-type></direction>
    <note><pitch><step>C</step><alter>1</alter><octave>4</octave></pitch><duration>4</duration><staff>1</staff></note>
    <note><rest/><duration>2</duration><staff>1</staff></note>
    <forward><duration>2</duration></forward>
    <note><pitch><step>D</step><octave>4</octave></pitch><duration>4</duration><staff>1</staff></note>
  </measure>
  <measure number="2">
    <note><pitch><step>C</step><octave>3</octave></pitch><duration>4</duration><staff>2</staff></note>
  </measure></part>
</score-partwise>
""",
        encoding="utf-8",
    )

    score = read_musicxml(source)

    assert score.title == "Timing"
    assert score.tempo_bpm == 72
    assert score.ticks_per_beat == 480
    assert [(note.pitch, note.start, note.duration) for note in score.right_hand] == [
        (61, 0, 480),
        (62, 960, 480),
    ]
    assert [(note.pitch, note.start, note.duration) for note in score.left_hand] == [
        (48, 1440, 480)
    ]
