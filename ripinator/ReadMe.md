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
# Extract first audio track (full duration)
python src/ripinator.py audio video.mp4

# Extract specific audio track by index
python src/ripinator.py audio video.mp4 --index 1

# Extract a clip between start and end timestamps (hh:mm:ss)
python src/ripinator.py audio video.mp4 --start 00:01:00 --end 00:02:30
```

### Extract Subtitles
```bash
# Extract first subtitle track (full duration)
python src/ripinator.py subtitle video.mp4

# Extract specific subtitle track by index
python src/ripinator.py subtitle video.mp4 --index 2

# Extract subtitles between start and end timestamps (hh:mm:ss)
python src/ripinator.py subtitle video.mp4 --start 00:01:00 --end 00:02:30
```

### List Available Streams
```bash
# Show all audio and subtitle streams in the video (indexing starts at 0)
python src/ripinator.py list-streams video.mp4
```

### Output Files
- Audio files are saved as `filename_audio.mp3` by default.
- Subtitle files are saved as `filename_subtitle.srt`.

### Audio Time Range Options
- `--start`: Start timestamp in `hh:mm:ss` format. Defaults to `00:00:00`.
- `--end`: End timestamp in `hh:mm:ss` format. Defaults to the video duration.
- Audio output is clipped to the range between `--start` and `--end`.

### Subtitle Time Range Options
- `--start`: Start timestamp in `hh:mm:ss` format. Defaults to `00:00:00`.
- `--end`: End timestamp in `hh:mm:ss` format. Defaults to the video duration.
- Subtitle output is clipped to the range between `--start` and `--end`.

