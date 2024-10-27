import json
import os
import sys

from PyMovieDb import IMDB

# Add the parent directory of both folders to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.file_namer import get_cleaned_names_for_movie_files


def get_movie_info(movie_name):
    imdb = IMDB()
    clean_move_name = get_cleaned_names_for_movie_files([movie_name])
    clean_movie_name_without_info = clean_move_name[0]['new'].split(' (')[0]
    movie_year = clean_move_name[0]['new'].split(' (')[1].split(')')[0]

    imdb_response = imdb.get_by_name(
        clean_movie_name_without_info,
        year=int(movie_year) if movie_year is not None else None
    )

    res = json.loads(imdb_response)

    if 'status' in res:
        print(f"Failed to get info for {movie_name} with response from IMDB: {res['status']} - {res['message']}")
    else:
        _print_info(res)


def _print_info(movie_details):
    name = movie_details["name"]
    year = movie_details["datePublished"].split("-")[0]
    description = movie_details["description"] if movie_details["description"] is not None else ""
    desc_print = f'\n\t{description}' if description is not None else ""
    rating = movie_details["rating"]["ratingValue"] if movie_details["rating"] is not None else ""

    print(f'- {name} ({year})  [{rating}/10] {desc_print}')
