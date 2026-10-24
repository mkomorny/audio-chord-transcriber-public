---
name: audio-chord-transcriber
description: Polyphonic chord and harmony transcriber for guitars, acoustic/electric pianos, and synths using Spotify Basic Pitch. Detects chord symbols (e.g. Cmaj7, Am9, F#m), aligns strummed onsets, and outputs both a clean MIDI chord track and a Markdown lead sheet.
---

# Polyphonic Audio Chord Transcriber & Lead Sheet Generator

Transcribes harmonic recordings (acoustic guitar strumming, piano chords, Rhodes keys, synth pads) into clean polyphonic MIDI chords while automatically analyzing and charting the musical chord progression.

## Key Capabilities

1. **Polyphonic Transcription**: Captures dense multi-note voicings, chord extensions (7ths, 9ths, sus2/sus4), and sustained harmonies.
2. **Strum Alignment**: Guitarists and pianists rarely strike all strings or keys at the exact same millisecond. The built-in strum aligner groups onsets within a customizable window (default: 45ms) into clean, synchronous block chords without destroying the timing of the progression.
3. **Automatic Chord Identification**: Analyzes active pitch classes and bass root notes across the timeline, generating a complete, human-readable Chord Lead Sheet markdown table (`_lead_sheet.md`).
4. **Dual Output**: Delivers both a `.mid` file for virtual instruments/DAWs and a formatted text/markdown lead sheet.

---

## Usage

```bash
# Transcribe acoustic guitar chords with lead sheet:
python "C:\Users\<you>\.agents\skills\audio-chord-transcriber\scripts\chord_transcribe.py" "C:\Music\guitar_chords.wav"

# Transcribe piano chords without strum alignment (preserves arpeggios):
python "C:\Users\<you>\.agents\skills\audio-chord-transcriber\scripts\chord_transcribe.py" "C:\Music\rhodes_keys.mp3" --no-align
```
