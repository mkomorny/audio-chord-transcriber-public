#!/usr/bin/env python3
"""
Polyphonic Audio Chord Transcriber & Lead Sheet Generator
Powered by Spotify Basic Pitch and pretty_midi.

Features:
- Polyphonic chord and harmony extraction (guitar, piano, rhodes, synths).
- Strum alignment: quantizes loose acoustic guitar/piano strums into clean chord blocks.
- Real-time chord symbol detection (Cmaj7, Am, G7, F#m7, etc.).
- Exports both a clean polyphonic .mid file and a readable .txt / .md chord lead sheet.
"""

import os
import sys
import warnings
import logging
import json
import argparse
import importlib.util
import subprocess
from pathlib import Path

warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
logging.basicConfig(level=logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)

BASIC_PITCH_PYTHON = r"C:\Users\<you>\AppData\Roaming\uv\tools\basic-pitch\Scripts\python.exe"

# Auto re-exec in dedicated uv environment if needed
if not importlib.util.find_spec("basic_pitch"):
    if os.path.exists(BASIC_PITCH_PYTHON) and sys.executable.lower() != BASIC_PITCH_PYTHON.lower():
        result = subprocess.run([BASIC_PITCH_PYTHON] + sys.argv)
        sys.exit(result.returncode)

import numpy as np
import pretty_midi
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH

PITCH_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

CHORD_TEMPLATES = {
    # Triads
    (0, 4, 7): "",
    (0, 3, 7): "m",
    (0, 3, 6): "dim",
    (0, 4, 8): "aug",
    (0, 2, 7): "sus2",
    (0, 5, 7): "sus4",
    # 7ths
    (0, 4, 7, 11): "maj7",
    (0, 3, 7, 10): "m7",
    (0, 4, 7, 10): "7",
    (0, 3, 6, 10): "m7b5",
    (0, 3, 6, 9): "dim7",
    (0, 3, 7, 11): "m(maj7)",
    # Extensions
    (0, 2, 4, 7): "add9",
    (0, 4, 7, 9): "6",
    (0, 3, 7, 9): "m6"
}


def identify_chord(pitch_classes: set, bass_pitch: int = None) -> str:
    """Identify root and chord name from a set of active pitch classes."""
    if len(pitch_classes) < 2:
        if pitch_classes:
            root_pc = list(pitch_classes)[0]
            return PITCH_NAMES[root_pc]
        return ""

    best_match = None
    best_score = -1

    # Try every pitch in the chord as potential root
    for root in range(12):
        rel_intervals = tuple(sorted((p - root) % 12 for p in pitch_classes))
        for template, quality in CHORD_TEMPLATES.items():
            intersection = set(rel_intervals).intersection(set(template))
            score = len(intersection) / max(len(template), len(rel_intervals))
            if score > best_score and score >= 0.6:
                best_score = score
                root_name = PITCH_NAMES[root]
                bass_suffix = ""
                if bass_pitch is not None and (bass_pitch % 12) != root:
                    bass_suffix = f"/{PITCH_NAMES[bass_pitch % 12]}"
                best_match = f"{root_name}{quality}{bass_suffix}"

    return best_match or "-".join([PITCH_NAMES[p] for p in sorted(pitch_classes)])


def align_strummed_chords(instrument: pretty_midi.Instrument, strum_window_s: float = 0.045) -> None:
    """Align onsets within a strumming window into clean synchronous block chords."""
    if not instrument.notes:
        return

    notes = sorted(instrument.notes, key=lambda n: n.start)
    i = 0
    while i < len(notes):
        curr_start = notes[i].start
        j = i + 1
        while j < len(notes) and (notes[j].start - curr_start) <= strum_window_s:
            notes[j].start = curr_start
            j += 1
        i = j


def transcribe_chords(
    audio_path: str,
    output_midi_path: str = None,
    output_sheet_path: str = None,
    onset_threshold: float = 0.50,
    frame_threshold: float = 0.30,
    min_note_length: float = 120.0,
    align_strums: bool = True,
    strum_window: float = 0.045
) -> dict:
    audio_file = Path(audio_path).resolve()
    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    if output_midi_path is None:
        output_midi_path = audio_file.with_name(f"{audio_file.stem}_chords.mid")
    else:
        output_midi_path = Path(output_midi_path).resolve()

    if output_sheet_path is None:
        output_sheet_path = audio_file.with_name(f"{audio_file.stem}_lead_sheet.md")
    else:
        output_sheet_path = Path(output_sheet_path).resolve()

    print(f"\n[*] Transcribing Harmonic Chords: {audio_file.name}")
    print(f"    Thresholds: Onset={onset_threshold}, Frame={frame_threshold}, MinLen={min_note_length}ms")

    model_output, midi_data, note_events = predict(
        audio_path=str(audio_file),
        model_or_model_path=ICASSP_2022_MODEL_PATH,
        onset_threshold=onset_threshold,
        frame_threshold=frame_threshold,
        minimum_note_length=min_note_length,
        multiple_pitch_bends=True,
        melodia_trick=True
    )

    for inst in midi_data.instruments:
        if align_strums:
            align_strummed_chords(inst, strum_window_s=strum_window)

    midi_data.write(str(output_midi_path))
    total_notes = sum(len(i.notes) for i in midi_data.instruments)

    # Analyze time slices to extract chord progression lead sheet
    time_step = 0.25 # 250ms slice
    duration = midi_data.get_end_time()
    slices = int(np.ceil(duration / time_step))

    chord_events = []
    last_chord = None
    last_time = 0.0

    all_notes = []
    for inst in midi_data.instruments:
        all_notes.extend(inst.notes)

    for s in range(slices):
        t = s * time_step
        active_notes = [n for n in all_notes if n.start <= t < n.end]
        if active_notes:
            pitch_classes = set(n.pitch % 12 for n in active_notes)
            bass_pitch = min(n.pitch for n in active_notes)
            chord_name = identify_chord(pitch_classes, bass_pitch=bass_pitch)
            if chord_name and chord_name != last_chord:
                if last_chord is not None:
                    chord_events.append((last_time, t, last_chord))
                last_chord = chord_name
                last_time = t
        else:
            if last_chord is not None:
                chord_events.append((last_time, t, last_chord))
                last_chord = None

    if last_chord is not None:
        chord_events.append((last_time, duration, last_chord))

    # Write Lead Sheet Markdown
    with open(output_sheet_path, "w", encoding="utf-8") as f:
        f.write(f"# Chord Lead Sheet: {audio_file.stem}\n\n")
        f.write(f"- **Source Audio**: `{audio_file.name}`\n")
        f.write(f"- **Total Notes**: {total_notes}\n")
        f.write(f"- **Duration**: {duration:.2f}s\n\n")
        f.write("## Chord Progression Timeline\n\n")
        f.write("| Timestamp | Duration | Detected Chord |\n")
        f.write("| :--- | :--- | :--- |\n")
        for start, end, ch in chord_events:
            dur = end - start
            if dur >= 0.4: # Filter momentary passing blips
                mins = int(start // 60)
                secs = int(start % 60)
                ms = int((start - int(start)) * 1000)
                time_str = f"{mins:02d}:{secs:02d}.{ms:03d}"
                f.write(f"| `{time_str}` | {dur:.2f}s | **`{ch}`** |\n")

    print(f"[+] Chord MIDI saved: {output_midi_path}")
    print(f"[+] Chord Lead Sheet saved: {output_sheet_path}")

    return {
        "audio_path": str(audio_file),
        "midi_path": str(output_midi_path),
        "sheet_path": str(output_sheet_path),
        "total_notes": total_notes,
        "total_chords": len(chord_events)
    }


def main():
    parser = argparse.ArgumentParser(description="Polyphonic Audio Chord Transcriber & Lead Sheet Generator")
    parser.add_argument("audio_path", help="Path to chord/harmony audio file (guitar, piano, synth)")
    parser.add_argument("--output-mid", "-o", help="Path to output .mid file")
    parser.add_argument("--output-sheet", "-s", help="Path to output lead sheet markdown file")
    parser.add_argument("--onset", type=float, default=0.50, help="Onset threshold (default 0.50)")
    parser.add_argument("--frame", type=float, default=0.30, help="Frame sustain threshold (default 0.30)")
    parser.add_argument("--min-len", type=float, default=120.0, help="Minimum note length in ms")
    parser.add_argument("--no-align", action="store_true", help="Disable strum-alignment quantizer")
    parser.add_argument("--strum-window", type=float, default=0.045, help="Strum alignment window in seconds")

    args = parser.parse_args()

    res = transcribe_chords(
        audio_path=args.audio_path,
        output_midi_path=args.output_mid,
        output_sheet_path=args.output_sheet,
        onset_threshold=args.onset,
        frame_threshold=args.frame,
        min_note_length=args.min_len,
        align_strums=not args.no_align,
        strum_window=args.strum_window
    )

    print("\n[SUCCESS] Harmonic Transcription Complete:")
    print(f"  MIDI:       {res['midi_path']}")
    print(f"  Lead Sheet: {res['sheet_path']}")
    print(f"  Chords:     {res['total_chords']} detected")


if __name__ == "__main__":
    main()
