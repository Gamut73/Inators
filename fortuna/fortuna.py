import os
import random
import subprocess
import argparse


def get_all_folders(directory):
    return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]


def get_video_files(directory):
    all_files = os.listdir(directory)
    video_files = [file for file in all_files if file.endswith(('.mp4', '.mkv', '.avi'))]
    return video_files


def pick_random_item(items):
    return random.choice(items)


def open_video_with_vlc(video_file):
    subprocess.call(['vlc', video_file])


def get_movie(dir):
    video_files = get_video_files(dir)
    if not video_files:
        print('<<No Videos Found Within This Directory>>')
    else:
        video_file = pick_random_item(video_files)
        open_video_with_vlc(video_file)


def get_series(directory):
    seasons = get_all_folders(directory)
    if not seasons:
        print(f'<<No Seasons Found Within {directory}>>')
    else:
        random_season = pick_random_item(seasons)
        episodes = get_video_files(os.path.join(directory, random_season))
        if not episodes:
            print(f'<<No Episodes Found Within Season {random_season}>>')
        else:
            random_episode = pick_random_item(episodes)
            open_video_with_vlc(os.path.join(directory, random_season, random_episode))


def main(directory, medium):
    if medium == "MOVIE":
        get_movie(directory)
    elif medium == "SERIES":
        get_series(directory)
    else:
        print("Invalid medium. Please choose MOVIE, SERIES, or EPISODE.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Open a random video file from within a directory")
    parser.add_argument("dir", help="The source directory")
    parser.add_argument("--medium", help="MOVIE (default), SERIES (season + episode), or EPISODE", default="MOVIE")

    args = parser.parse_args()
    main(args.dir, args.medium)