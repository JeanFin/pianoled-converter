"""Read a deliberately small, useful subset of partwise MusicXML."""

from pathlib import Path
import xml.etree.ElementTree as ET

from .models import Note, Score

_STEPS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def _tag(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def _child(element: ET.Element, name: str) -> ET.Element | None:
    return next((item for item in element if _tag(item) == name), None)


def _text(element: ET.Element, name: str, default: str | None = None) -> str | None:
    child = _child(element, name)
    return child.text.strip() if child is not None and child.text else default


def _descendant(root: ET.Element, name: str) -> ET.Element | None:
    return next((item for item in root.iter() if _tag(item) == name), None)


def _midi_pitch(note: ET.Element) -> int:
    pitch = _child(note, "pitch")
    if pitch is None:
        raise ValueError("pitched MusicXML note is missing <pitch>")
    step = _text(pitch, "step")
    octave = _text(pitch, "octave")
    if step not in _STEPS or octave is None:
        raise ValueError("MusicXML pitch requires a valid step and octave")
    alter = int(_text(pitch, "alter", "0") or 0)
    return 12 * (int(octave) + 1) + _STEPS[step] + alter


def _ticks(duration: int, divisions: int, ticks_per_beat: int) -> int:
    if divisions <= 0:
        raise ValueError("MusicXML <divisions> must be positive")
    return round(duration * ticks_per_beat / divisions)


def _work_title(root: ET.Element) -> str | None:
    work = _child(root, "work")
    if work is None:
        return None
    title = _child(work, "work-title")
    return title.text.strip() if title is not None and title.text else None


def _tempo(direction: ET.Element) -> float | None:
    sound = _descendant(direction, "sound")
    if sound is not None and sound.get("tempo"):
        return float(sound.get("tempo", "120"))

    per_minute = _descendant(direction, "per-minute")
    if per_minute is not None and per_minute.text:
        return float(per_minute.text.strip())
    return None


def read_musicxml(path: str | Path) -> Score:
    """Parse a partwise MusicXML file into a two-hand score.

    Staff 1 is assigned to the right hand and staff 2 to the left. Only the
    first ``<part>`` is read; the initial implementation targets piano scores
    represented as one part with two staves.
    """

    root = ET.parse(path).getroot()
    if _tag(root) != "score-partwise":
        raise ValueError("only partwise MusicXML scores are supported")

    score = Score(title=_work_title(root))
    part = _child(root, "part")
    if part is None:
        raise ValueError("MusicXML score does not contain a part")

    tempo_found = False
    measure_start = 0
    divisions = 1

    for measure in (item for item in part if _tag(item) == "measure"):
        position = measure_start
        furthest = measure_start
        previous_note_start = position

        for item in measure:
            kind = _tag(item)
            if kind == "attributes":
                value = _text(item, "divisions")
                if value is not None:
                    divisions = int(value)
            elif kind == "direction" and not tempo_found:
                tempo = _tempo(item)
                if tempo is not None:
                    score.tempo_bpm = tempo
                    tempo_found = True
            elif kind in {"backup", "forward"}:
                duration = int(_text(item, "duration", "0") or 0)
                delta = _ticks(duration, divisions, score.ticks_per_beat)
                if kind == "backup":
                    position = max(measure_start, position - delta)
                else:
                    position += delta
                furthest = max(furthest, position)
            elif kind == "note":
                duration_value = int(_text(item, "duration", "0") or 0)
                duration = _ticks(duration_value, divisions, score.ticks_per_beat)
                is_chord = _child(item, "chord") is not None
                start = previous_note_start if is_chord else position
                if not is_chord:
                    previous_note_start = start

                if _child(item, "rest") is None and duration > 0:
                    staff = int(_text(item, "staff", "1") or 1)
                    target = {1: score.right_hand, 2: score.left_hand}.get(staff)
                    if target is not None:
                        target.append(Note(_midi_pitch(item), start, duration))

                if not is_chord:
                    position += duration
                    furthest = max(furthest, position)
                else:
                    furthest = max(furthest, start + duration)

        measure_start = furthest

    score.right_hand.sort(key=lambda note: (note.start, note.pitch))
    score.left_hand.sort(key=lambda note: (note.start, note.pitch))
    return score
