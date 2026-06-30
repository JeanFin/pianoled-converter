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