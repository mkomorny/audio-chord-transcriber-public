# Audio Chord Transcriber

**Audio Chord Transcriber** (`audio-chord-transcriber`) is an AI skill and CLI tool that transcribes polyphonic harmonic recordings (acoustic guitar strumming, piano chords, Rhodes keys, synth pads) into clean Type 1 MIDI files (`.mid`) and automatically charts a human-readable chord progression lead sheet (`_lead_sheet.md`).

---

## ⚡ Key Highlights

- **Polyphonic Neural Inference**: Powered by Spotify Basic Pitch (`ICASSP_2022_MODEL_PATH`) to detect dense voicings, extensions (7ths, 9ths, sus2/sus4), and sustained notes.
- **Intelligent Strum Alignment**: Guitarists and keyboardists naturally strike strings or keys with slight timing offsets. The strum aligner groups onsets within a customizable window (default: 45ms) into clean, synchronous block chords without destroying the progression's groove.
- **Harmonic Chord Recognition**: Analyzes active pitch classes and bass root notes across the timeline, generating a complete, human-readable Chord Lead Sheet markdown table (`_lead_sheet.md`).
- **Dual Output Delivery**: Generates both a `.mid` file for virtual instruments/DAWs and a formatted text/markdown lead sheet.
- **Transparent Runtime Delegation**: Automatically calls into the dedicated `basic-pitch` uv Python environment (`C:\Users\<you>\AppData\Roaming\uv\tools\basic-pitch\Scripts\python.exe`) without polluting global Python packages.
- **Zero-Duplicate Tri-Platform Availability**: Installed canonically in `.agents/skills/audio-chord-transcriber` and linked via NTFS junctions to Claude, Grok, and Antigravity.

---

## 🚀 Usage

### In Chat (Prompts & Slash Commands)

- `/audio-chord-transcriber "C:\Music\acoustic_guitar.wav"`
- *"Transcribe the chords and generate a lead sheet for 'C:\Recordings\rhodes_jam.mp3'"*
- *"Extract the MIDI chords from this guitar audio: 'D:\Samples\fingerpicked_intro.wav' --no-align"*
- *"Transcribe this audio file into chords and show me the chord progression table."*

### Command Line Interface (`scripts/chord_transcribe.py`)

```powershell
# Standard transcription with strum alignment and lead sheet:
python scripts/chord_transcribe.py "C:\Music\guitar_chords.wav"

# Transcribe without strum alignment (preserves arpeggios and runs):
python scripts/chord_transcribe.py "C:\Music\rhodes_keys.mp3" --no-align

# Custom strum alignment window (30ms for tight keyboard chords):
python scripts/chord_transcribe.py "C:\Music\piano.wav" --strum-window 0.03

# Custom output directory:
python scripts/chord_transcribe.py "C:\Music\synth_pad.wav" --output-dir "C:\Music\Transcriptions"
```

---

## 📁 Repository Structure

```
audio-chord-transcriber/
├── SKILL.md                  # Skill trigger and platform integration instructions
├── HOW_TO_USE.txt            # Quick-reference cheat sheet & prompt guide
├── IMPLEMENTATION_PLAN.md    # Multi-version roadmap and completed tasks
├── App Changes Tracker.html  # Permanent interactive HTML version changelog
├── README.md                 # This overview
└── scripts/
    └── chord_transcribe.py   # Basic Pitch neural inference & chord detection engine
```

---

## 📜 Documentation & Lifecycle

- **Version History & Releases**: Tracked permanently in [App Changes Tracker.html](App%20Changes%20Tracker.html).
- **Roadmap & Completed Features**: Documented in [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md).
