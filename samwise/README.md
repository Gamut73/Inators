# Samwise

Samwise is a Python script that helps with the organization of your local movie/series/anime collection. It automates the process of moving movies and subtitles to the correct directories and removing the source directory after the move.

## Usage

1. Ensure that `samwise.py` and `file_mover.py` are in the same directory.
2. Run the `samwise.py` script with the desired action and source directories as command line arguments.

Here is an example of how to use the script:

```bash
python samwise.py move_movie_downloads /path/to/source/directory
```

In this example, `move_movie_downloads` is the action to perform and `/path/to/source/directory` is the source directory to process.

## Actions

Currently, the script supports the following actions:

- `move_movie_downloads` or `mmd`: Moves movies and subtitles from the source directories to the correct directories and removes the source directories.

## Functions

The script uses the following functions from `file_mover.py`:

- `move_subtitles(source_dir)`: Moves subtitles from the source directory to the correct directory.
- `move_movie(source_dir)`: Moves movies from the source directory to the correct directory.
- `remove_source_dir(source_dir)`: Removes the source directory.

## Requirements

- Python 3
- `os` and `shutil` Python libraries

## TODO

Please replace the paths in `file_mover.py` with the configs or env_vars or something that match your system configuration.