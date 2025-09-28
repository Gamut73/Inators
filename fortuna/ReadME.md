# Fortuna

![Fortuna-engraving-Hans-Sebald-Beham-1541](https://github.com/user-attachments/assets/2b2f77bd-1dc9-42d3-8c43-b926b8a7daf7)

Goddess: Fortuna is the goddess of fortune and the personification of luck in Roman religion.

Script: Fortuna helps you make entertainment decisions by randomly selecting a movie or TV show for you to watch. It can
also handle series organized in seasons folders. In the future, it will also choose what you watch for you based on your
preferences that you wouldn't otherwise be able to express without the use of natural language.

## Requirements
- Python 3.x
- VLC available on PATH (default media player). You can change the player by editing `MEDIA_PLAYER` in `fortuna.py`. (AT some point a config file will be added)
- Supported video files: `.mp4`, `.mkv`, `.avi`

## Quick Start
- Play random movies from a folder:
  - `python3 fortuna.py play <folder>`
- Play random episodes from a series (season folders inside the series folder):
  - `python3 fortuna.py play <folder> -s`
- List cached media and filter by IMDB fields:
  - `python3 fortuna.py list media -f "genre:comedy,keywords:japanese"`

## Commands

### Play
Play random video(s) from a directory.

- Syntax:
  - `python3 fortuna.py play <folder> [--number N] [--series] [--filters "field:value,field:value"]`
- Options:
  - `-n, --number`: Number of random videos to open (default: 1)
  - `-s, --series`: Treat the folder as a series directory containing season subfolders
  - `-f, --filters`: Filter cached movies using `field:value` pairs separated by commas
    - Example: `-f "genre:comedy,keywords:japanese"`
    - Matching is case-insensitive
- Examples:
  - One random movie: `python3 fortuna.py play ~/Videos/Movies`
  - Three random episodes from a show: `python3 fortuna.py play ~/Videos/Shows -s -n 3`
  - One random filtered movie: `python3 fortuna.py play ~/Videos/Movies -f "genre:comedy,year:1999"`

### List
List cached IMDB info and available fields.

- List media (optionally filtered):
  - `python3 fortuna.py list media [-f "field:value,field:value"]`
  - Prints cached movies that match the given filters.
- List all available fields you can filter by:
  - `python3 fortuna.py list fields`
- List value counts for a field (e.g., genres):
  - `python3 fortuna.py list field-values <field_name>`
  - Example:
    ```
    python3 fortuna.py list field-values genre
    Values for 'genre':
    - action: 22
    - comedy: 12
    - fantasy: 10
    - scifi: 1
    ```
  - Matching is case-insensitive.

## Filters
- Format: `field:value,field:value`
- Multiple filters are comma-separated.
- Use `python3 fortuna.py list fields` to see valid fields.
- Use `python3 fortuna.py list field-values <field_name>` to explore distinct values and counts.

## Series Folder Layout
If using `--series`, the directory should contain season subfolders:
```
/path/to/Show/
  Season 01/
    S01E01.mkv
    S01E02.mkv
  Season 02/
    S02E01.mkv
    ...
```

## Help
- CLI help: `python3 fortuna.py --help`
- Play help: `python3 fortuna.py play --help`
- List help: `python3 fortuna.py list --help`
