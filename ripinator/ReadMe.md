# Ripinator

Ripinator is a command-line tool that extracts audio tracks and subtitles from video files using FFmpeg.

## Dependencies

- Python 3.x
- FFmpeg
- MediaInfo CLI tool

Install FFmpeg and MediaInfo on your system:
```bash
# Ubuntu/Debian
sudo apt install ffmpeg mediainfo

# macOS (with Homebrew)
brew install ffmpeg mediainfo

# Windows (with Chocolatey)
choco install ffmpeg mediainfo
```

## How to Use

### Extract Audio
```bash
# Extract first audio track (starts at 0)
python ripinator.py video.mp4 --audio

# Extract specific audio track by index
python ripinator.py video.mp4 --audio 1
```

### Extract Subtitles
```bash
# Extract first subtitle track (starts at 0)
python ripinator.py video.mp4 --subtitle

# Extract specific subtitle track by index
python ripinator.py video.mp4 --subtitle 2
```

### List Available Streams
```bash
# Show all audio and subtitle streams in the video (When extracting using this info, remember that indexing starts at 0)
python ripinator.py video.mp4 --list-streams
```

### Output Files
- Audio files are saved as `filename_audio.mp3`
- Subtitle files are saved as `filename_subtitle.srt`