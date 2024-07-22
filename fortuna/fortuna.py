import os
import random
import subprocess
import argparse

MEDIA_PLAYER = 'vlc'


def get_all_folders(directory):
    return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]


def get_video_files(directory):
    all_files = os.listdir(directory)
    video_files = [file for file in all_files if file.endswith(('.mp4', '.mkv', '.avi'))]
    return video_files


def pick_random_video(items, number_of_videos):
    return random.sample(items, number_of_videos)


def open_video_with_medial_player(video_files):
    print(video_files)
    subprocess.call([MEDIA_PLAYER] + video_files)


def get_movie(dir, number_of_videos):
    video_files = get_video_files(dir)
    if not video_files:
        print('<<No Videos Found Within This Directory>>')
    else:
        video_files = pick_random_video(video_files, number_of_videos)
        open_video_with_medial_player(video_files)


def get_series(directory, number_of_videos):
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


def main(directory, video_type, number_of_videos):
    if video_type == "MOVIE":
        get_movie(directory, number_of_videos)
    elif video_type == "SERIES":
        get_series(directory, number_of_videos)


if __name__ == "__main__":
    medium = "MOVIE"

    parser = argparse.ArgumentParser(description="Open a random video file from within a directory")
    parser.add_argument("dir", help="The source directory")
    parser.add_argument("-s", "--series", action="store_true", help="Expects series organized in seasons folders")
    parser.add_argument("-n", "--number", type=int, default=1, help="Number of random videos to open")

    args = parser.parse_args()
    if args.series:
        medium = "SERIES"

    main(args.dir, medium, args.number)
