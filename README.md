# Malayalam Music Visualizer — Claude Code Skill

A Claude Code skill for turning a reference music-notation Reel and a target song into a synchronized Malayalam sargam / musical-note visualizer.

## Install

Copy this folder into your project:

```bash
mkdir -p .claude/skills
cp -R malayalam-music-visualizer .claude/skills/
```

Or install it for all your Claude Code projects:

```bash
mkdir -p ~/.claude/skills
cp -R malayalam-music-visualizer ~/.claude/skills/
```

Then restart Claude Code (or start a new session). Invoke it with:

```text
/malayalam-music-visualizer
```

You can also ask naturally: "Use the Malayalam music visualizer skill to recreate this reference animation for my new song."

## Requirements

- Python 3.9+
- FFmpeg and FFprobe available on PATH
- Python packages: `opencv-python`, `Pillow`
- Claude Code should be able to read the reference video and target audio files.

Install Python packages:

```bash
python -m pip install opencv-python pillow
```

## Included tools

- `scripts/inspect_video.py`: extracts metadata, frame samples and a contact sheet from a reference video.
- `scripts/validate_render.py`: checks exported video dimensions, frame rate, duration, audio presence and optional timeline CSV structure.

The skill does not pretend to identify exact swaras from audio alone. Use verified notation, MIDI/MusicXML, a user-supplied event CSV, or ask the user to confirm uncertain notes.
