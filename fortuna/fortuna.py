import argparse
import os
import random
import subprocess
from enum import Enum

from art import tprint

from IMDBService import get_info

MEDIA_PLAYER = 'vlc'


class ActionType(Enum):
    PLAY = "PLAY"
    SHOW_INFO = "SHOW_INFO"


def get_all_folders(directory):
    return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]


def get_video_files(directory):
    all_files = os.listdir(directory)
    video_files = [file for file in all_files if file.endswith(('.mp4', '.mkv', '.avi'))]
    return video_files


def pick_random_video(items, number_of_videos):
    return random.sample(items, number_of_videos)


def open_video_with_medial_player(video_files):
    tprint(f"Playing...")
    subprocess.call([MEDIA_PLAYER] + video_files)


def play_movie(dir, number_of_videos):
    movies = None
    movies = get_video_files(dir)
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


def play(source, number_of_videos, video_type):
    if video_type == "MOVIE":
        play_movie(source, number_of_videos)
    elif video_type == "SERIES":
        play_series(source, number_of_videos)


def main(file_path, video_type, action, number_of_videos):
    if action == ActionType.PLAY:
        play(file_path, number_of_videos, video_type, filter)
    elif action == ActionType.SHOW_INFO:
        get_info(file_path)


if __name__ == "__main__":
    medium = "MOVIE"

    parser = argparse.ArgumentParser(description="Open a random video file from within a directory")
    parser.add_argument("dir", help="The source directory")
    parser.add_argument("-s", "--series", action="store_true", help="Expects series organized in seasons folders")
    parser.add_argument("-n", "--number", type=int, default=1, help="Number of random videos to open")
    parser.add_argument("-i", "--info", action="store_true", help="Get movie info")

    args = parser.parse_args()
    if args.series:
        medium = "SERIES"

    action = ActionType.PLAY if not args.info else ActionType.SHOW_INFO
    filter = args.filter if (action == ActionType.PLAY and args.filter) else ""

    main(args.dir, medium, action, args.number)

