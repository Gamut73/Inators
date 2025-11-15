import os
import random
import subprocess
import sys


import click
from art import tprint

from IMDBCacheConstants import IMDB_CACHE_KEY_LIST
from IMDBService import get_movie_files_by_filters, get_movie_info_by_filters, print_movie_info, get_info

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.logger import debug, info, error
from enums import ActionType, ListType

MEDIA_PLAYER = 'vlc'


def get_field_value_counts(field_name):
    movies = get_movie_info_by_filters(None)
    value_counts = {}

    for movie in movies:
        if field_name in movie and movie[field_name]:
            if isinstance(movie[field_name], str) and ',' in movie[field_name]:
                values = [v.strip() for v in movie[field_name].split(',')]
                for value in values:
                    value_lower = value.lower()
                    value_counts[value_lower] = value_counts.get(value_lower, 0) + 1
            else:
                value_lower = movie[field_name].lower()
                value_counts[value_lower] = value_counts.get(value_lower, 0) + 1

    return value_counts


def get_all_folders(directory):
    return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]


def get_video_files(directory):
    all_files = os.listdir(directory)
    video_files = [file for file in all_files if file.endswith(('.mp4', '.mkv', '.avi'))]
    return video_files


def pick_random_video(items, number_of_videos):
    count = len(items) if len(items) < number_of_videos else number_of_videos
    return random.sample(items, count)


def open_video_with_medial_player(video_files):
    tprint(f"Playing...")
    with open(os.devnull, 'w') as devnull:
        subprocess.call([MEDIA_PLAYER] + video_files, stdout=devnull, stderr=devnull)


def _play_movie(dir, number_of_videos, movie_filters):
    movies = get_video_files(dir)
    if movie_filters is not None:
        movies_files_in_db_by_filters = get_movie_files_by_filters(movie_filters)
        base_names_cached_movies = [os.path.basename(movie) for movie in movies_files_in_db_by_filters]
        intersection = []
        for movie in movies:
            if os.path.basename(movie) in base_names_cached_movies:
                intersection.append(movie)
        movies = intersection
        info(f"Choosing from {len(movies)} movies that match the filters")
    if not movies:
        info('<<No Videos Found Within This Directory>>')
    else:
        movies_to_play = pick_random_video(movies, number_of_videos)
        open_video_with_medial_player(movies_to_play)


def _play_series(directory, number_of_videos):
    random_episodes = []
    seasons = get_all_folders(directory)
    if not seasons:
        info(f'<<No Seasons Found Within {directory}>>')
    else:
        for _ in range(number_of_videos):
            random_season = random.choice(seasons)
            episodes = get_video_files(os.path.join(directory, random_season))
            if not episodes:
                info(f'<<No Episodes Found Within Season {random_season}>>')
            else:
                random_episode = pick_random_video(episodes, 1)
                random_episodes.append(os.path.join(directory, random_season, random_episode[0]))

        open_video_with_medial_player(random_episodes)


def _play(source, number_of_videos, video_type, filters):
    if video_type == "MOVIE":
        _play_movie(source, number_of_videos, filters)
    elif video_type == "SERIES":
        _play_series(source, number_of_videos)


def list_field_values(field_name):
    if field_name:
        if field_name not in IMDB_CACHE_KEY_LIST:
            error(f"Field '{field_name}' is not valid. Available fields are:")
            for field in IMDB_CACHE_KEY_LIST:
                print(field)
        else:
            value_counts = get_field_value_counts(field_name)
            if not value_counts:
                info(f"No values found for field '{field_name}'")
            else:
                print(f"Values for '{field_name}':")
                for value, count in sorted(value_counts.items()):
                    print(f"- {value}: {count}")


def validate_filepath(ctx, param, value):
    action = ctx.params.get('action', '').upper()
    actions_requiring_filepath = [ActionType.PLAY.name, ActionType.INFO.name]
    if action in actions_requiring_filepath and not value:
        raise click.BadParameter('filepath is required when action is PLAY')
    return value


def validate_list_type(ctx, param, value):
    action = ctx.params.get('action', '').upper()
    folder = ctx.params.get('folder_path', '').upper()
    list_type = ctx.params.get('list_type', '').upper()
    debug(f"Validating list_type: action={action}, value={value}, folder={folder}, list_type={list_type}")
    if action == ActionType.LIST.name and not [value for value in ListType.__members__].count(value):
        raise click.BadParameter('list_type is required when action is LIST')
    return value


def validate_field_name(ctx, param, value):
    list_type = ctx.params.get('list_type', '').upper()
    if list_type == ListType.FIELD_VALUES and not [field.name for field in IMDB_CACHE_KEY_LIST].count(value):
        raise click.BadParameter(f"field_name must be one of {[field for field in IMDB_CACHE_KEY_LIST]}")
    return value


@click.group()
def fortuna_cli():
    """Fortuna - Random Movie/Series Picker and IMDB Movie Infol"""
    pass


@fortuna_cli.command()
@click.argument('folder_path', type=click.Path(exists=True))
@click.option('--number', '-n', default=1, help='Number of random videos to open (default: 1)')
@click.option('--series', '-s', is_flag=True, help='Expects series organized in seasons folders')
@click.option('--filters', '-f', type=str, default=None, help='Filter for cached movies')
def play(folder_path, number, series, filters):
    """Play random video(s) from a directory."""
    media_type = "SERIES" if series else "MOVIE"
    _play(folder_path, number_of_videos=number, video_type=media_type, filters=filters)


@fortuna_cli.command()
@click.argument('filepath', type=click.Path(exists=True))
def info(filepath):
    """Get Movie infor for a specific file or directory."""
    get_info(filepath)


@fortuna_cli.group('list')
def lists():
    """List various information."""
    pass


@lists.command()
@click.argument('folder_path', type=click.Path(exists=True), required=False)
@click.option('--filters', '-f', type=str, default=None, help='Filter for cached movies')
def media(folder_path, filters):
    """List all cached movies."""
    movies = get_movie_info_by_filters(filters)
    for movie in movies:
        print_movie_info(movie)


@lists.command()
def fields():
    """List all available fields you can filter by."""
    print("Available fields:")
    for field in IMDB_CACHE_KEY_LIST:
        print(f"- {field}")


@lists.command()
@click.argument('field_name', type=click.Choice([field for field in IMDB_CACHE_KEY_LIST], case_sensitive=False))
def field_values(field_name):
    """Get value counts for a specific field."""
    list_field_values(field_name)


if __name__ == "__main__":
    fortuna_cli()

