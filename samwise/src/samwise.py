import os
import sys

import click

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from util.file_namer import clean_movie_names_in_dir, clean_list_of_movie_files, clean_movie_name, clean_series_dir
from util.file_mover import move_subtitles, move_movie, remove_source_dir, is_video_file


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
        print(f"* Processing Movie: {source_dir}")
        movie_filepath = move_movie(source_dir)
        newly_moved_movies.append(movie_filepath)
        if not is_video_file(source_dir):
            move_subtitles(source_dir)
            remove_source_dir(source_dir)

    clean_list_of_movie_files(newly_moved_movies)


@samwise_cli.command('cmn')
@click.argument('filepaths', type=click.Path(exists=True), nargs=-1, required=True)
def clean_movie_names(filepaths):
    """Clean movie names in the given files or directories."""
    for filepath in filepaths:
        if os.path.isdir(filepath):
            clean_movie_names_in_dir(filepath)
        else:
            clean_movie_name(filepath)


@samwise_cli.command('csd')
@click.argument('filepaths', type=click.Path(exists=True), nargs=-1, required=True)
def clean_series(filepaths):
    """Clean series directory names."""
    for filepath in filepaths:
        clean_series_dir(filepath)


if __name__ == "__main__":
    samwise_cli()
