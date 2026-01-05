# Clipinator

A video clipping tool that allows you to extract segments from video files with optional subtitle support.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Clipinator uses a command-based CLI structure.

### Commands Overview

```bash
clipinator --help
```

### Clip a Single Segment

Extract a single clip from a video file:

```bash
clipinator clip <INPUT_FILE> <START_TIME> <END_TIME> <CLIP_NAME> [OPTIONS]
```

**Arguments:**
- `INPUT_FILE` - Path to the source video file
- `START_TIME` - Start time of the clip (format: `HH:MM:SS` or `MM:SS`)
- `END_TIME` - End time of the clip (format: `HH:MM:SS` or `MM:SS`)
- `CLIP_NAME` - Name for the output clip (use `[folder]` prefix to organize into subfolders)

**Options:**
- `-o, --output-dir` - Output directory (default: `~/Videos/Clips`)
- `-s, --subtitles` - Path to an external subtitles file (.srt)
- `-es, --embedded-subtitles` - Index of embedded subtitle stream to use
- `-ea, --embedded-audio` - Index of embedded audio stream to use

**Examples:**

```bash
# Basic clip
clipinator clip movie.mkv 10:30 12:45 "Funny Scene"

# With subtitles
clipinator clip movie.mkv 10:30 12:45 "Funny Scene" -s subtitles.srt

# Using embedded subtitles (stream index 0)
clipinator clip movie.mkv 10:30 12:45 "Funny Scene" -es 0

# Organize into subfolders using [brackets]
clipinator clip movie.mkv 10:30 12:45 "[Action][Chase]Car Scene"
```

### Batch Clip from CSV

Extract multiple clips using a CSV timestamps file:

```bash
clipinator batch-clip <VIDEO_FILE>  [OPTIONS]
```

A menu will prompt you to select a timestamps CSV file from `~/Videos/Clips/Timestamps/`.

**Arguments:**
- `INPUT_FILE` - Path to the source video file
**Options:**
- `-o, --output-dir` - Output directory (default: `~/Videos/Clips`)
- `-s, --subtitles` - Path to an external subtitles file (.srt)
- `-es, --embedded-subtitles` - Index of embedded subtitle stream to use
- `-ea, --embedded-audio` - Index of embedded audio stream to use

**Example:**

```bash
clipinator batch-clip movie.mkv my_timestamps -es 0
```

### Create a Timestamps Template

Generate a new CSV template file for batch clipping:

```bash
clipinator template <FILENAME>
```

This creates a CSV file in `~/Videos/Clips/Timestamps/` and opens it in the default editor.

**Example:**

```bash
clipinator template my_movie_clips
```

### Manage Batch Files

Commands to manage timestamp CSV files.

#### List All Timestamp Files

```bash
clipinator batch-files list
```

#### Open a Timestamp File

```bash
clipinator batch-files open <FILENAME>
```

**Example:**

```bash
clipinator batch-files open my_timestamps
```

## CSV Timestamps Format

The CSV file should have the following columns:

| Column | Description |
|--------|-------------|
| `start_time` | Start time of the clip (HH:MM:SS or MM:SS) |
| `end_time` | End time of the clip (HH:MM:SS or MM:SS) |
| `ignore_subs` | Set to `y` to skip subtitles for this clip |
| `title` | Name for the clip (supports `[folder]` prefixes) |

**Example CSV:**

```csv
start_time,end_time,ignore_subs,title
00:10:30,00:12:45,n,Funny Scene
00:45:00,00:47:30,y,Action Scene No Subs
01:20:00,01:22:15,n,[Best Moments]Epic Fight
```

## Folder Organization

Use square brackets in clip names to organize clips into subfolders:

- `[Category]Clip Name` → saves to `Category/Clip Name.mp4`
- `[Category][Subcategory]Clip Name` → saves to `Category/Subcategory/Clip Name.mp4`
