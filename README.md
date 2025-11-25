# yt-notes ✦

YouTube videos/playlists → extract chapters/timestamps → auto-generate Markdown "notes" with TOC (table of contents), title, description, and links.  
Bonus: Audio-only mode for podcasts, watch mode for channel RSS feeds.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python >=3.10](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

```bash
pip install git+https://github.com/iminierai-aig/yt-notes.git

```
# Features

- 📹 Smart Downloads: Single videos, playlists, or channels via yt-dlp (1,000+ sites supported)
- 📝 Chapter Magic: Auto-parses timestamps → clickable Markdown TOC (- [Intro](video.mp4#t=0s))
- 🎧 Audio Mode: Extract MP3s for podcasts (no video bloat)
- 👀 Watch Mode: Poll RSS feeds → auto-download new uploads
- 🎨 Pro UX: Rich progress + Loguru logs
- ⚡ Lightweight: Minimal deps — runs fast, outputs clean notes.md

# Installation
Requires Python 3.10+ and ffmpeg (for audio/merges — install via brew/apt/choco).
```
pip install git+https://github.com/iminierai-aig/yt-notes.git

```
# Quick Start & Usage

# Download video + generate notes
```
yt-notes https://youtube.com/watch?v=abc123

# Playlist batch (saves to ./downloads/)
yt-notes https://youtube.com/playlist?list=PLxyz -o ./downloads

# Audio-only (MP3 + notes)
yt-notes https://youtube.com/watch?v=abc123 --audio

# Notes only (no download, from metadata)
yt-notes https://youtube.com/watch?v=abc123 --notes-only

# Watch channel (auto-download new vids every 5 min)
yt-notes --watch "https://youtube.com/feeds/videos.xml?channel_id=UC123" -o ./auto --interval 300

# Quiet mode
yt-notes big-playlist --quiet
```

See yt-notes --help for more.

# Demo
```
(Loom video incoming — watch --watch mode snag new uploads live!)
<iframe src="https://www.loom.com/embed/YOUR_LOOM_ID" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: relative; top: 0; left: 0; width: 100%; max-width: 700px; height: 450px;"></iframe>

```

# Development

1. Clone: git clone https://github.com/iminierai-aig/yt-notes.git
2. Install: pip install -e .
3. Run: python -m ytnotes --help
4. Build: python -m build && twine upload dist/*

Built with yt-dlp in ~24 hours. PRs for subtitle integration or AI summaries welcome!
License
MIT — see LICENSE.