from PyMovieDb import IMDB
import sys
import os

# Add the parent directory of both folders to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.file_namer import clean_list_of_movie_names


def get_movie_info(movie_name):
    imdb = IMDB()
    clean_move_name = clean_list_of_movie_names([movie_name])
    clean_movie_name_without_info = clean_move_name[0]['new'].split(' (')[0]
    year = clean_move_name[0]['new'].split(' (')[1].split(')')[0]
    return imdb.get_by_name(clean_movie_name_without_info)
