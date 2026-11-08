---
name: malayalam-music-visualizer
description: Recreate polished, synchronized music-notation and sargam visualizer videos from a user-provided reference video and song audio. Use when the user asks to make Instagram Reels like their Malayalam musical-note videos, analyze a reference animation, map notes to Malayalam swaras, or render a song visualizer.
---

# Malayalam Music Visualizer

Create a complete, verified vertical music-notation Reel by learning the visual language and animation behavior from the user's reference video, then applying it to a different song or notation sequence.

## Core behavior

- Treat the **reference video** as the authority for visual layout, animation language, pacing, transitions, typography, and interaction patterns.
- Treat the **target song/audio and its verified notation** as the authority for musical timing and content.
- Never assume that the reference song's notes, lyrics, title, or timing belong to the target song.
- Never invent a note, Malayalam character, lyric, heading, singer, composer, or credit.
- If note recognition is uncertain, create a review list and ask for confirmation rather than silently guessing.
- Preserve the supplied original audio unless the user explicitly requests a different audio source.
- Aim for a professional 9:16 Instagram Reel, normally 1080×1920 at 30 fps.

## When to use

Trigger this skill when the user:
- provides a reference Reel/video and asks to make another video like it;
- asks for a Malayalam sargam, swara, musical-note, or notation visualizer;
- asks to recreate the animation, note movement, pitch graph, active-note tiles, counter, or watermark from their examples.

## Workflow

### 1. Identify inputs and ask only for missing essentials

Look for:
1. Reference video (one or more examples).
2. Target song audio or target video containing the audio.
3. Correct song heading/title and movie/album.
4. Musical notation source, if available (PDF, image, text, MIDI, MusicXML, CSV, or user-confirmed swara sequence).
5. Required watermark/username.

If the target audio is embedded in a video, extract it. If no target song/audio is supplied, ask for it. If a title is not visible or provided, ask rather than guessing.

### 2. Inspect the reference video

Run:

```bash
python scripts/inspect_video.py "/path/to/reference.mp4" --out-dir work/reference
```

Inspect the generated:
- `metadata.json`
- `contact_sheet.jpg`
- `frame_samples/`

Also inspect the reference manually at the beginning, middle, end, and every major transition. Record:
- frame size, fps, duration, aspect ratio, audio codec;
- background, palette, typography and hierarchy;
- title placement and style;
- pitch graph/lines and note markers;
- Malayalam swara labels and note tiles;
- active-note glow, cursor, trail, pulse, and transitions;
- counters, phrase labels, rhythm indicators, watermark;
- margins and safe areas.

For multiple references, identify shared elements and per-video variations. Do not assume all examples use the same layout.

### 3. Build an exact event timeline

Create `MUSIC_EVENT_TIMELINE.csv` before rendering. Use one row per note activation or other timed visual event.

Required columns:

```csv
event_id,frame,time_seconds,phrase_id,event_type,original_symbol,malayalam_text,pitch_row,duration_frames,confidence,source,needs_review
```

Rules:
- Use zero-based frame numbers.
- `time_seconds = frame / fps`.
- Keep events sorted by frame.
- Preserve repeated notes as separate events.
- Record rests, phrase changes, sustained notes, rhythm syllables and transitions when they affect the animation.
- Do not infer pitch rows from visual position alone if the notation is unclear.
- If a source notation file exists, cross-check every event against it.
- Mark uncertain events `needs_review=true`; explain the uncertainty in a separate `REVIEW_NOTES.md`.
- If the user supplied a verified CSV, preserve its content and use it as the source of truth.

### 4. Malayalam text and notation accuracy

- Use correct Unicode Malayalam characters; do not transliterate into Latin letters.
- Keep the distinction between similar Malayalam letters and chillus/diacritics.
- Preserve octave markers, komal/tivra marks, underlines, dots, rhythm syllables and other notation marks exactly as supplied.
- Choose a font with full Malayalam glyph coverage, such as Noto Sans Malayalam. Verify rendered glyphs visually; do not accept tofu boxes or broken conjuncts.
- Never convert a musical symbol into a Malayalam syllable based only on a guess.
- If the source uses Devanagari or another script, document the mapping and get confirmation for ambiguous mappings.

### 5. Recreate the visual style

Use the reference to match the *type* of animation, not to blindly copy every pixel. Reproduce the relevant visual grammar:
- vertical pitch lanes / horizontal pitch rows;
- moving playhead or glowing active-note marker;
- note markers positioned on pitch rows;
- active swara tiles or syllable blocks;
- synchronized note highlighting;
- counters and phrase progress, only when present or requested;
- transitions and background motion;
- song heading and username watermark.

Default design choices only when the reference does not establish them:
- 9:16 vertical composition;
- deep navy/charcoal background;
- restrained violet, cyan, teal or warm-gold accents;
- readable Malayalam typography;
- subtle glow and motion, with notation kept visually dominant.

Do not add decorative elements that obscure notation. Do not add a counter if it would be misleading or if the source has no meaningful count.

### 6. Timing and audio synchronization

- Derive animation timing from the target song, not from the reference video's duration.
- Prefer user-provided frame/timestamp events or verified MIDI/MusicXML timing.
- If extracting timing from audio, use waveform/onset analysis only as an aid; musical note identity and swara mapping require reliable notation or user confirmation.
- Maintain the original song start, duration, speed and pitch.
- Keep audio and video synchronized from frame 0.
- Preserve the original audio stream with stream copy when compatible; otherwise re-encode to AAC at a high bitrate and document that choice.
- Never stretch the song to fit an animation. Adjust animation timing to the audio.

### 7. Render

Use the project's existing framework if present. Otherwise choose a maintainable approach:
- HTML/CSS/Canvas or SVG animation rendered frame-by-frame;
- Remotion if the project already uses it;
- FFmpeg for compositing, scaling, encoding and audio muxing.

Keep source files editable. Separate:
- event/timeline data;
- design tokens and layout;
- animation/rendering logic;
- audio handling;
- validation.

Recommended output:
- `FINAL_REEL.mp4`
- `MUSIC_EVENT_TIMELINE.csv`
- `REVIEW_NOTES.md`
- `source/` or the complete project source
- `preview_contact_sheet.jpg`
- `render_report.json`

### 8. Export settings

Default:
- 1080×1920;
- 30 fps, unless user requests otherwise;
- H.264 video, `yuv420p`;
- AAC audio, 48 kHz where re-encoding is needed;
- `+faststart`;
- no black bars, stretching, or unintended cropping.

If the source is 512×910 or another low resolution, rebuild the composition at 1080×1920. Do not simply upscale a flattened reference video and call it a recreation.

### 9. Verify before delivery

Run:

```bash
python scripts/validate_render.py "/path/to/FINAL_REEL.mp4" --timeline "/path/to/MUSIC_EVENT_TIMELINE.csv" --expected-width 1080 --expected-height 1920 --expected-fps 30
```

Then:
- inspect contact sheets from the rendered video;
- watch the full render;
- compare note activation moments against the timeline;
- verify every Malayalam glyph and diacritic;
- verify title, watermark, counter and safe margins;
- verify audio duration and synchronization;
- check for dropped frames, black frames, clipping, glitches and encoding errors.

Do not claim perfect musical accuracy if notation was inferred from audio alone. State any remaining review items clearly.

## User-specific visual references

The user has provided two example videos. Use these as style references when they are available in the project:

- `MALANG_DHOOM3_MALAYALAM_FINAL(1).mp4` — 28.5 seconds, 512×910, 30 fps. Visual language: dark navy/blue-violet gradient, pitch rows and labels, cyan active-note cursor/glow, Malayalam note tiles, swara progress counter and small centered username watermark.
- `mere_dholna_malayalam_v2(1).mp4` — 55.433 seconds, 512×910, 30 fps. Visual language: dark purple/black background, horizontal pitch grid, gold and teal note families, active-note tiles, phrase/category labels and a compact notation/status indicator.

These are examples, not templates to flatten or reuse. Analyze the actual supplied files in each new project. The second example's title/notation treatment differs from the first; preserve that flexibility.

## Final response format

After completing the project, report:
1. output video path;
2. duration, resolution and fps;
3. audio preservation method;
4. event count and number of unresolved notation items;
5. validation status;
6. source and timeline file paths.

If any required source material is missing, ask one concise question and do not fabricate musical content.
