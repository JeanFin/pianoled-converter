from pathlib import Path

import pytest

from pianoled_converter import __version__, convert
from pianoled_converter.cli import main


def test_cli_converts_file_and_reports_success(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "input.musicxml"
    output = tmp_path / "output.mid"
    source.write_text(
        """<score-partwise><part-list/><part id="P1"><measure number="1">
        <attributes><divisions>1</divisions></attributes>
        <note><pitch><step>C</step><octave>4</octave></pitch><duration>1</duration></note>
        </measure></part></score-partwise>""",
        encoding="utf-8",
    )

    result = main([str(source), str(output)])
    captured = capsys.readouterr()

    assert result == 0
    assert output.exists()
    assert str(output) in captured.out
    assert captured.err == ""
    assert callable(convert)
    assert __version__ == "0.1.0"


def test_cli_reports_conversion_failure(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "missing.musicxml"
    output = tmp_path / "output.mid"

    result = main([str(missing), str(output)])
    captured = capsys.readouterr()

    assert result != 0
    assert "pianoled-converter: error:" in captured.err
    assert str(missing) in captured.err
