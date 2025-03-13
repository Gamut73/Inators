import argparse
import os
import random
import subprocess
from enum import Enum

from art import tprint

from IMDBService import get_info, get_movie_files_by_filters, get_movie_info_by_filters, print_movie_info
from IMDBCacheConstants import IMDB_CACHE_KEY_LIST

MEDIA_PLAYER = 'vlc'


class ActionType(Enum):
    PLAY = "PLAY"
    SHOW_INFO = "SHOW_INFO"
    LIST = "LIST"
    LIST_FIELDS = "LIST_FIELDS"


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


def play_movie(dir, number_of_videos, movie_filters):
    movies = get_video_files(dir)
    if movie_filters is not None:
        movies_files_in_db_by_filters = get_movie_files_by_filters(movie_filters)
        base_names_cached_movies = [os.path.basename(movie) for movie in movies_files_in_db_by_filters]
        intersection = []
        for movie in movies:
            if os.path.basename(movie) in base_names_cached_movies:
                intersection.append(movie)
        movies = intersection
        print(f"Choosing from {len(movies)} movies that match the filters")
    if not movies:
        print('<<No Videos Found Within This Directory>>')
    else:
        movies_to_play = pick_random_video(movies, number_of_videos)
        open_video_with_medial_player(movies_to_play)


def play_series(directory, number_of_videos):
    random_episodes = []
    seasons = get_all_folders(directory)
    if not seasons:
        print(f'<<No Seasons Found Within {directory}>>')
    else:
        for _ in range(number_of_videos):
            random_season = random.choice(seasons)
            episodes = get_video_files(os.path.join(directory, random_season))
            if not episodes:
                print(f'<<No Episodes Found Within Season {random_season}>>')
            else:
                random_episode = pick_random_video(episodes, 1)
                random_episodes.append(os.path.join(directory, random_season, random_episode[0]))

        open_video_with_medial_player(random_episodes)


def play(source, number_of_videos, video_type, filters):
    if video_type == "MOVIE":
        play_movie(source, number_of_videos, filters)
    elif video_type == "SERIES":
        play_series(source, number_of_videos)


def main(file_path, video_type, action, number_of_videos, filters):
    if action == ActionType.PLAY:
        play(file_path, number_of_videos, video_type, filters)
    elif action == ActionType.SHOW_INFO:
        get_info(file_path)
    elif action == ActionType.LIST:
        movies = get_movie_info_by_filters(filters)
        for movie in movies:
            print_movie_info(movie)
    elif action == ActionType.LIST_FIELDS:
        for field in IMDB_CACHE_KEY_LIST:
            print(field)


if __name__ == "__main__":
    medium = "MOVIE"
    action = ActionType.PLAY

    parser = argparse.ArgumentParser(description="Open a random video file from within a directory")
    parser.add_argument("dir", help="The source directory")
    parser.add_argument("-s", "--series", action="store_true", help="Expects series organized in seasons folders")
    parser.add_argument("-n", "--number", type=int, default=1, help="Number of random videos to open")
    parser.add_argument("-i", "--info", action="store_true", help="Get movie info")
    parser.add_argument("-f", "--filters", type=str, default=None, help="Filter for cached movies")
    parser.add_argument("-l", "--list", action="store_true", help="List all cached movies")
    parser.add_argument("-lf", "--list_fields", action="store_true", help="List all fields you can filter by")

    args = parser.parse_args()
    if args.series:
        medium = "SERIES"

    if args.info:
        action = ActionType.SHOW_INFO
    elif args.list:
        action = ActionType.LIST
    elif args.list_fields:
        action = ActionType.LIST_FIELDS

    filters = args.filters if (args.filters is not None) else None

    main(args.dir, medium, action, args.number, filters)

