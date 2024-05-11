import argparse
from file_mover import move_subtitles, move_movie, remove_source_dir
from file_namer import clean_movie_names_in_dir


def move_movie_downloads(source_dirs):
    for source_dir in source_dirs:
        print(f"* Processing Movie In: {source_dir}")
        move_subtitles(source_dir)
        move_movie(source_dir)
        remove_source_dir(source_dir)


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
