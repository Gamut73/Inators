from PyMovieDb import IMDB
import sys
import os
import json

# Add the parent directory of both folders to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.file_namer import clean_list_of_movie_names


def get_movie_info(movie_name):
    imdb = IMDB()
    clean_move_name = clean_list_of_movie_names([movie_name])
    clean_movie_name_without_info = clean_move_name[0]['new'].split(' (')[0]

    movie_details = imdb.get_by_name(clean_movie_name_without_info)
    movie_details_json = json.loads(movie_details)
    print(movie_details_json["name"] + ": " + movie_details_json["description"])
