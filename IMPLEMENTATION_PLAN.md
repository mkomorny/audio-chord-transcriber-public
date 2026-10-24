# Implementation Plan: Audio Chord Transcriber

This document tracks planned, in-progress, and completed work for the **Audio Chord Transcriber** skill. It persists across all version passes.

---

## Completed Work

### v1.0.0 — Initial Release (2026-09-24)
- [x] **Neural Polyphonic Audio-to-MIDI (`scripts/chord_transcribe.py`)**: Built inference pipeline wrapping Spotify Basic Pitch (`ICASSP_2022_MODEL_PATH`) to transcribe polyphonic harmony from guitar, piano, keys, and synths. (✅ done in v1.0.0)
- [x] **Strum Alignment Engine**: Created onset quantization window (default 45ms) that aligns asynchronous strummed/struck notes into coherent block chords without destroying progression timing. (✅ done in v1.0.0)
- [x] **Harmonic Chord Symbol Recognition**: Built template-matching dictionary covering triads, 7ths, add9, 6ths, sus2/sus4, diminished, augmented, and slash chords from active pitch classes and bass pitch notes. (✅ done in v1.0.0)
- [x] **Dual Output Delivery**: Automatically writes both standard `.mid` MIDI tracks and Markdown chord progression lead sheet documents (`_lead_sheet.md`). (✅ done in v1.0.0)
- [x] **Automatic Runtime Delegation**: Built transparent process delegation to the dedicated `basic-pitch` uv Python environment (`C:\Users\<you>\AppData\Roaming\uv\tools\basic-pitch\Scripts\python.exe`). (✅ done in v1.0.0)
- [x] **Tri-Platform Deployment**: Established canonical skill in `.agents/skills/audio-chord-transcriber` with NTFS directory junctions to `.claude/skills`, `.grok/skills`, and `.gemini/config/skills`. (✅ done in v1.0.0)
- [x] **Documentation & Versioning**: Authored `SKILL.md`, standardized `HOW_TO_USE.txt`, `README.md`, and permanent `App Changes Tracker.html`. (✅ done in v1.0.0)

---

## Planned Future Work

- [ ] **Ableton User Library Auto-Export**: Add flag `--to-ableton` to automatically deposit the transcribed `.mid` into `A:\User Library\Clips\Chord Progressions`.
- [ ] **Camelot Key / Scale Detection**: Integrate key and scale detection to display Roman numeral analysis (e.g. `ii - V - I`) alongside chord symbols.
- [ ] **Stem Separation Pre-Pass**: Support passing full mix audio by automatically isolating guitar/keys stems prior to chord transcription.
