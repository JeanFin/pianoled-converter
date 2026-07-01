# PianoLED Converter

Convert MusicXML files into Standard MIDI files optimized for interactive piano learning software.

## Overview

PianoLED Converter reads MusicXML scores and generates Standard MIDI files with separate tracks and MIDI channels for the right and left hand.

The project was originally developed to create MIDI files compatible with the learning mode of Piano LED Plus from MusicXML files exported by Dorico.

## Features

- Read MusicXML files
- Split right and left hand by staff
- Generate Standard MIDI File Type 1
- Create separate tracks for both hands
- Assign separate MIDI channels for both hands
- Preserve tempo information
- Tested with Piano LED Plus learning mode.

## Installation

```bash
pip install -e .
```

## Usage

```bash
pianoled-converter input.musicxml output.mid
```

## Compatibility

The converter has been tested successfully with MusicXML files exported from:

- StaffPad
- Dorico

Both export formats produce MIDI files that work correctly with Piano LED Plus interactive mode, including:

- Hand separation
- Stop-and-go playback
- LED guidance

Contributions and compatibility reports for other MusicXML editors (such as MuseScore, Finale and Sibelius) are welcome.

## Known limitation

The generated MIDI files fully support Piano LED Plus interactive playback (LED guidance, hand separation and stop-and-go mode).

However, the optional score view inside Piano LED Plus may not be available for imported MIDI files. Based on current testing, this feature appears to rely on additional metadata that is present in the application's built-in library but not in standard MIDI files.

## Roadmap

### v0.1
- ✅ MusicXML reader
- ✅ MIDI writer
- ✅ Command line interface

### Planned

- MIDI validator
- Unit test improvements
- Drag & Drop GUI
- Better MusicXML support
- Sustain pedal support
- Repeat handling

## License

MIT License
