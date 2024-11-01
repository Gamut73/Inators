import argparse

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.file_namer import clean_movie_names_in_dir, clean_list_of_movie_files
from util.file_mover import move_subtitles, move_movie, remove_source_dir, is_video_file


def move_movie_downloads(source_dirs):
    newly_moved_movies = []

    for source_dir in source_dirs:
        print(f"* Processing Movie: {source_dir}")
        movie_filepath = move_movie(source_dir)
        newly_moved_movies.append(movie_filepath)
        if not is_video_file(source_dir):
            move_subtitles(source_dir)
            remove_source_dir(source_dir)

    clean_list_of_movie_files(newly_moved_movies)

def main(source_dirs, action):
    if action == "move_movie_downloads" or action == "mmd":
        move_movie_downloads(source_dirs)
    elif action == "clean_movie_dir_names" or action == "cmdn":
        for source_dir in source_dirs:
            clean_movie_names_in_dir(source_dir)    
    else:
        print("Invalid action")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Move movie and subtitles to the correct directories')
    parser.add_argument('action', type=str, default='move', help='The action to perform[move_movie_downloads(mmd), clean_movie_dir_names(cmdn)]')
    parser.add_argument('source_dirs', type=str, nargs='+', help='The source directory(s) to process')

    args = parser.parse_args()
    main(args.source_dirs, args.action)
