import os
import random
import subprocess
import argparse


def get_video_files(dir):
    all_files = os.listdir(dir)
    video_files = [file for file in all_files if file.endswith(('.mp4', '.mkv', '.avi'))]
    return video_files


def pick_random_video(video_files):
    return random.choice(video_files)


def open_video_with_vlc(video_file):
    subprocess.call(['vlc', video_file])


def main(dir):
    video_files = get_video_files(dir)
    if not video_files:
        print('<<No Videos Found Within This Directory>>')
    else:
        video_file = pick_random_video(video_files)
        open_video_with_vlc(video_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Open a random video file from within a directory")
    parser.add_argument("dir", help="The source directory")

    args = parser.parse_args()
    main(args.dir)