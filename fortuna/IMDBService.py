import json
import os
import sys


from PyMovieDb import IMDB

# Add the parent directory of both folders to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.file_mover import  get_all_video_files, is_video_file
from util.file_namer import get_cleaned_names_for_movie_files
from util.JsonDatabase import JsonDatabase
from IMDBCacheConstants import *


db = JsonDatabase(IMDB_DB_FILE_PATH)


def get_movie_files_by_filters(filters):
    filter_dict = _get_filter_map(filters)



def _get_filter_map(filters):
    keys = []
    values = []

    separated_filters = filters.split(',')
    for filter in separated_filters:
        key, value = filter.split(':')

        if key not in IMDB_CACHE_KEY_LIST:
            print(f"Invalid filter key: {key}")
            continue

        keys.append(key)
        values.append(value)

    return dict(zip(keys, values))


def get_info_by_source_dir(source_dir):
    return db.search_by_key(SOURCE_DIR_KEY, source_dir)


def get_info(file_path):
    if is_video_file(file_path):
        _get_movie_info(file_path)
    else:
        _get_movie_info_from_a_dir(file_path)


def _get_movie_info_from_a_dir(directory):
    filenames = get_all_video_files(directory)

    for filename in filenames:
        _get_movie_info(filename)


def _get_movie_info(filename, imdb_client=None):
    imdb_cache = _search_imdb_cache_for_movie(db, filename)

    if len(imdb_cache) == 0:
        imdb = imdb_client if imdb_client is not None else IMDB()

        clean_move_name = get_cleaned_names_for_movie_files([filename])
        clean_movie_name_without_info = clean_move_name[0]['new'].split(' (')[0]
        movie_year = clean_move_name[0]['new'].split(' (')[1].split(')')[0] if ' (' in clean_move_name[0]['new'] else\
            None

        imdb_response = imdb.get_by_name(
            clean_movie_name_without_info,
            year=int(movie_year) if movie_year is not None else None
        )

        res = json.loads(imdb_response)

        if 'status' in res:
            print(f"Failed to get info for {filename} with response from IMDB: {res['status']} - {res['message']}")
            return

        file_dir = os.path.join(os.getcwd(), os.path.dirname(filename))
        imdb_cache = [_map_imdb_response_to_db_format(res, file_dir, filename)]
        db.add(imdb_cache[0])

    for movie in imdb_cache:
        _print_info(movie)


def _map_imdb_response_to_db_format(imdb_response, source_dir, filename):
    return {
        TITLE_KEY: imdb_response["name"],
        YEAR_KEY: imdb_response["datePublished"].split("-")[0] if imdb_response["datePublished"] is not None else "?",
        DESCRIPTION_KEY: imdb_response["description"] if imdb_response["description"] is not None else "",
        DIRECTOR_KEY: _map_director_to_db_format(imdb_response["director"]),
        RATING_KEY: imdb_response["rating"]["ratingValue"] if imdb_response["rating"] is not None else "?",
        GENRE_KEY: _map_list_to_string(imdb_response["genre"]),
        KEYWORDS_KEY: imdb_response["keywords"],
        POSTER_URL_KEY: imdb_response["poster"],
        SOURCE_DIR_KEY: source_dir,
        FILENAME_KEY: filename
    }


def _map_list_to_string(list):
    return ', '.join(list)


def _map_director_to_db_format(directors):
    director_string = ""
    for director in directors:
        director_string += f"{director['name']}, "

    return director_string[:-2]


def _search_imdb_cache_for_movie(db, filename):
    key = db.search_by_key(FILENAME_KEY, filename)
    return key


def _print_info(movie_details):
    title = movie_details[TITLE_KEY]
    year = movie_details[YEAR_KEY]
    description = movie_details[DESCRIPTION_KEY]
    desc_print = f'\n\t- {description}' if description != "" else "<No description found>"
    rating = f'{movie_details[RATING_KEY]}',
    director = f" , dir: {movie_details[DIRECTOR_KEY]}," if movie_details[DIRECTOR_KEY] is not None else ""
    genre = f'\n\t- Genres: {movie_details[GENRE_KEY]}' if movie_details[GENRE_KEY] is not None else ""
    keywords = f'\n\t- Keywords: {movie_details[KEYWORDS_KEY]}' if movie_details[KEYWORDS_KEY] is not None else ""
    filepath = f'\n\t- Filepath: {os.path.join(movie_details[SOURCE_DIR_KEY], movie_details[FILENAME_KEY])}'

    print(f'* {title} ({year}) {director} [{rating}/10] {desc_print} {genre} {keywords} {filepath}')
