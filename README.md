# yt-notes ✦

YouTube videos/playlists → extract chapters/timestamps → auto-generate Markdown "notes" with TOC (table of contents), title, description, and links.  
Bonus: Audio-only mode for podcasts, watch mode for channel RSS feeds.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python >=3.10](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://github.com/iminierai-aig/yt-notes)

## Features

- 📹 **Smart Downloads**: Single videos, playlists, or channels via yt-dlp (1,000+ sites supported)
- 📝 **Chapter Magic**: Auto-parses timestamps → clickable Markdown TOC (`- [Intro](video.mp4#t=0s)`)
- 🎧 **Audio Mode**: Extract MP3s for podcasts (no video bloat)
- 👀 **Watch Mode**: Poll RSS feeds → auto-download new uploads
- 🎨 **Pro UX**: Rich progress + Loguru logs
- ⚡ **Lightweight**: Minimal deps — runs fast, outputs clean notes.md

## Installation

Requires Python 3.10+ and ffmpeg (for audio/merges — install via brew/apt/choco).

```bash
pip install git+https://github.com/iminierai-aig/yt-notes.git
```

Or install from source:

```bash
git clone https://github.com/iminierai-aig/yt-notes.git
cd yt-notes
pip install -e .
```

## Quick Start & Usage

### Download video + generate notes
```bash
yt-notes https://youtube.com/watch?v=abc123
```

### Playlist batch (saves to ./downloads/)
```bash
yt-notes https://youtube.com/playlist?list=PLxyz -o ./downloads
```

### Audio-only (MP3 + notes)
```bash
yt-notes https://youtube.com/watch?v=abc123 --audio
```

### Notes only (no download, from metadata)
```bash
yt-notes https://youtube.com/watch?v=abc123 --notes-only
```

### Watch channel (auto-download new vids every 5 min)
```bash
yt-notes --watch "https://youtube.com/feeds/videos.xml?channel_id=UC123" -o ./auto --interval 300
```

### Quiet mode
```bash
yt-notes big-playlist --quiet
```

See `yt-notes --help` for more options.

## Demo

<iframe src="https://www.loom.com/embed/e352c38ea8e244c093d81f7d300c8d1f" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: relative; top: 0; left: 0; width: 100%; max-with: 700px: height: 450px;"></iframe>


## Development

1. Clone: `git clone https://github.com/iminierai-aig/yt-notes.git`
2. Install: `pip install -e .`
3. Run: `python -m yt-notes --help`
4. Build: `python -m build && twine upload dist/*`

Built with yt-dlp in ~24 hours. PRs for subtitle integration or AI summaries welcome!

## License

MIT — see [LICENSE](LICENSE).
