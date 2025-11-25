#!/usr/bin/env python3
"""
YouTube Downloader & Notes CLI
Downloads videos, extracts chapters → Markdown notes
"""

import argparse
import sys
import json
from pathlib import Path
from yt_dlp import YoutubeDL
from loguru import logger
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# Logger config (like your PDF tool)
def setup_logger(quiet: bool = False):
    logger.remove()
    if quiet:
        logger.add(sys.stderr, level="ERROR")
    else:
        logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>")

def download_and_extract(url: str, output_dir: Path, audio_only: bool = False, notes_only: bool = False):
    """Core download logic using yt-dlp"""
    # Progress hook for download status
    def progress_hook(d):
        if d['status'] == 'downloading':
            console.print(f"Downloading: {d.get('filename', 'Unknown')}")
        elif d['status'] == 'finished':
            console.print(f"✓ Downloaded: {d['filename']}")
    
    ydl_opts = {
        'outtmpl': str(output_dir / '%(title)s.%(ext)s'),  # Output template
        'format': 'bestaudio/best' if audio_only else 'best[ext=mp4]/best[height<=720]/best',  # Format selection (single format, no merging)
        'writeinfojson': True,  # Extract metadata JSON
        'writesubtitles': True,  # Optional: Subs for notes
        'progress_hooks': [progress_hook],  # Add progress hook upfront
        'extractor_args': {
            'youtube': {
                'player_client': ['default'],  # Use default client to avoid JS runtime requirement and warnings
            }
        },
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        try:
            if notes_only:
                # Just extract info and generate notes, no download
                info = ydl.extract_info(url, download=False)
                generate_notes(info, output_dir)
                return
            
            # Download (this will extract info automatically)
            info = ydl.extract_info(url, download=True)
            
            # Generate notes post-download
            generate_notes(info, output_dir)
            
        except Exception as e:
            logger.error(f"✗ Download failed: {e}")
            return None

def generate_notes(info: dict, output_dir: Path):
    """Parse chapters → Markdown notes"""
    title = info.get('title', 'Untitled')
    description = info.get('description', '')
    chapters = info.get('chapters') or []
    
    md_content = [f"# {title}\n\n"]
    
    if description:
        md_content.append(f"{description}\n\n")
    
    if chapters:
        md_content.append("## Table of Contents\n")
        for i, chap in enumerate(chapters, 1):
            start = chap.get('start_time', 0)  # Seconds
            chap_title = chap.get('title', f"Chapter {i}")
            md_content.append(f"- [{chap_title}]({title}.mp4#t={int(start)}s)\n")  # Relative link
        md_content.append("\n")
    else:
        md_content.append("No chapters detected — full video notes.\n\n")
    
    md_content.append("## Full Transcript/Subtitles\n*(Add auto-gen later)*")
    
    notes_file = output_dir / f"{title}-notes.md"
    notes_file.write_text("".join(md_content))
    logger.success(f"Generated notes: {notes_file}")

def watch_channel(channel_rss: str, output_dir: Path, interval: int = 300):  # 5 min default
    """Watch mode: Poll RSS for new videos"""
    import feedparser  # Add to deps
    import time
    
    logger.info(f"Watching channel RSS: {channel_rss} (every {interval}s)")
    seen = set()
    
    while True:
        try:
            feed = feedparser.parse(channel_rss)
            if feed.bozo:  # Parse error
                logger.warning("RSS parse failed — skipping poll")
                return
            
            for entry in feed.entries:
                vid_id = entry.id  # Or link
                if vid_id not in seen:
                    logger.info(f"New video: {entry.title}")
                    download_and_extract(entry.link, output_dir)  # Download URL from entry.link
                    seen.add(vid_id)
            
            time.sleep(interval)
        except Exception as e:
            logger.error(f"Watch poll error: {e}")
            time.sleep(interval)  # Continue after error

def main():
    parser = argparse.ArgumentParser(
        description="YouTube Downloader & Notes CLI",
        epilog="""
Examples:
  %(prog)s https://youtube.com/watch?v=abc123
  %(prog)s https://youtube.com/playlist?list=PLxyz -o ./downloads
  %(prog)s --audio https://youtube.com/watch?v=abc123
  %(prog)s --notes-only https://youtube.com/watch?v=abc123
  %(prog)s --watch "https://youtube.com/feeds/videos.xml?channel_id=UC123" -o ./auto
        """
    )
    
    parser.add_argument("url", nargs="?", help="YouTube URL or playlist")
    parser.add_argument("-o", "--output", type=Path, default=Path("."), help="Output directory")
    parser.add_argument("--audio", action="store_true", help="Download audio only (MP3)")
    parser.add_argument("--notes-only", action="store_true", help="Extract notes without downloading")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode")
    parser.add_argument("--watch", help="Channel RSS URL for auto-download mode")
    parser.add_argument("--interval", type=int, default=300, help="Watch poll interval (seconds)")
    
    args = parser.parse_args()
    setup_logger(args.quiet)
    
    if args.watch:
        watch_channel(args.watch, args.output, args.interval)
        return 0
    
    if not args.url:
        parser.error("URL required (or use --watch)")
    
    args.output.mkdir(exist_ok=True)
    
    # Rich progress wrapper (like your PDF spinner)
    if not args.quiet:
        with Progress(SpinnerColumn(), TextColumn("[bold blue]Processing {task.description}"), transient=True) as progress:
            task = progress.add_task(args.url, total=None)
            download_and_extract(args.url, args.output, args.audio, args.notes_only)
            progress.update(task, completed=True)
    else:
        download_and_extract(args.url, args.output, args.audio, args.notes_only)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())