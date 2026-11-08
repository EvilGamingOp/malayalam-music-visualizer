# Malayalam Music Visualizer 🎵

A Claude Code skill for creating professional Malayalam musical notation and Sargam visualization Reels from reference videos and songs.

Recreate musical animations, synchronized swara highlights, pitch lines, Malayalam notation, transitions and more.

## ✨ Features

- Analyse reference music visualization videos.
- Recreate similar animation styles and layouts.
- Malayalam swara and musical notation support.
- Frame-by-frame musical event timeline.
- Synchronized note highlighting and animations.
- Custom song headings and Instagram watermarks.
- Original audio preservation.
- Instagram Reels export in 1080×1920.
- Automated video inspection and validation tools.

## 🚀 Installation

### Option 1: Install globally (all Claude Code projects)

```powershell
git clone https://github.com/EvilGamingOp/malayalam-music-visualizer.git "$HOME\.claude\skills\malayalam-music-visualizer"
```

### Option 2: Install in a single project

Run this inside your project directory:

```bash
git clone https://github.com/EvilGamingOp/malayalam-music-visualizer.git .claude/skills/malayalam-music-visualizer
```

Restart Claude Code or open a new session.

## 🎬 Usage

Invoke the skill:

```text
/malayalam-music-visualizer
```

Or simply ask:

```text
Use the Malayalam music visualizer skill.

Here is my reference video and new song.
Analyse the reference animation and recreate
a similar musical notation Reel for my song.

Preserve the original audio.
Use accurate Malayalam notation.
Add my requested heading and watermark.
Export in 1080×1920.
```

## 📁 Project Structure

```text
malayalam-music-visualizer/
├── SKILL.md
├── README.md
├── .gitignore
├── MUSIC_EVENT_TIMELINE_TEMPLATE.csv
└── scripts/
    ├── inspect_video.py
    └── validate_render.py
```

## ⚙️ Requirements

- Claude Code
- Python 3.9+
- FFmpeg and FFprobe
- OpenCV
- Pillow

Install Python packages:

```bash
python -m pip install opencv-python pillow
```

FFmpeg must also be installed and accessible through PATH.

## 🛠️ Included Tools

**Video Inspector**

```bash
python scripts/inspect_video.py "reference.mp4" --out-dir work/reference
```

Extracts video metadata, frame samples and a contact sheet.

**Render Validator**

```bash
python scripts/validate_render.py "FINAL_REEL.mp4" --timeline "MUSIC_EVENT_TIMELINE.csv" --expected-width 1080 --expected-height 1920 --expected-fps 30
```

Checks video resolution, FPS, audio presence, codec and timeline structure.

## 🎨 Default Export Settings

| Setting | Value |
|---|---|
| Resolution | 1080×1920 |
| Aspect ratio | 9:16 |
| Frame rate | 30 FPS |
| Video codec | H.264 |
| Pixel format | yuv420p |
| Audio | Original audio preserved where possible |

## ⚠️ Accuracy

The original reference video determines the visual style. The target song and verified notation determine the musical content and timing.

Audio analysis alone cannot guarantee exact swara identification. Use verified notation or confirm uncertain musical notes before rendering.

## 👤 Author

**EvilGamingOp**

GitHub: https://github.com/EvilGamingOp

## 📜 License

No license has been added yet. Usage and redistribution permissions are not currently specified.
