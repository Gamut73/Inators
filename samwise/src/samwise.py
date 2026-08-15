import os
import sys

import click

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from util.file_namer import clean_list_of_movie_files, clean_series_dir
from util.file_mover import move_subtitles, move_movie, remove_source_dir, is_video_file
from util.logger import error, info

@click.group()
def samwise_cli():
    """Samwise - CLI tool for organising local movie/series/anime collections."""
    pass


@samwise_cli.command('mm')
@click.argument('source_dirs', type=click.Path(exists=True), nargs=-1, required=True)
def move_movies(source_dirs):
    """Move movies and subtitles to the correct directories."""
    newly_moved_movies = []

    for source_dir in source_dirs:
        info(f"* Processing Movie: {source_dir}")
        try:
            movie_filepath = move_movie(source_dir)
            newly_moved_movies.append(movie_filepath)
            if not is_video_file(source_dir):
                move_subtitles(source_dir)
                remove_source_dir(source_dir)
        except Exception as e:
            error(f"An error occurred while processing movie {source_dir}: because of error: {e}")

    clean_list_of_movie_files(newly_moved_movies)


def _get_video_files(directory):
    all_files = os.listdir(directory)
    video_files = [file for file in all_files if file.endswith(('.mp4', '.mkv', '.avi'))]
    return video_files


@samwise_cli.command('cmn')
@click.argument('path', type=click.Path(exists=True), required=True)
def clean_movie_names(path):
    """Clean movie names in the given files or directories."""
    if os.path.isdir(path):
        video_filepaths = _get_video_files(path)
        clean_list_of_movie_files(video_filepaths)
    elif os.path.isfile(path):
        clean_list_of_movie_files([path])


@samwise_cli.command('csd')
@click.argument('filepaths', type=click.Path(exists=True), nargs=-1, required=True)
def clean_series(filepaths):
    """Clean series directory names."""
    for filepath in filepaths:
        clean_series_dir(filepath)


if __name__ == "__main__":
    samwise_cli()
