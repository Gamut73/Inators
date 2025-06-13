import json
import os
import sys

from PyMovieDb import IMDB

# Add the parent directory of both folders to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.file_mover import get_all_video_files, is_video_file
from util.file_namer import get_cleaned_names_for_movie_files
from util.JsonDatabase import JsonDatabase
from IMDBCacheConstants import *
from util.print_colors import PrintColors
from util.youtube_api_client import *

db = JsonDatabase(IMDB_DB_FILE_PATH)


def get_movie_files_by_filters(filters):
    return [movie[FILENAME_KEY] for movie in get_movie_info_by_filters(filters)]


def get_movie_info_by_filters(filters):
    if filters is None:
        return db.get_all()

    movies = []
    filter_dict = _get_filter_map(filters)
    print(f"Searching for movies with filters: {filter_dict}")
    cached_movies = db.get_all()
    if filter_dict is None:
        print("Invalid filters, return all cached movies")
        return cached_movies

    for movie in cached_movies:
        if all(movie.get(item[0], '') is not None and item[1].lower() in movie.get(item[0], '').lower() for item in
               filter_dict.items()):
            movies.append(movie)

    return movies


def _get_filter_map(filters):
    keys = []
    values = []

    separated_filters = filters.split(',')
    for filter in separated_filters:
        key, value = filter.split(':')

        if key not in IMDB_CACHE_KEY_LIST:
            print(f"Invalid filter key: {key}")
            continue

        keys.append(key.lower())
        values.append(value.lower())

    return dict(zip(keys, values))


def get_info_by_source_dir(source_dir):
    return db.search_by_key(SOURCE_DIR_KEY, source_dir)


def get_info(file_path):
    if is_video_file(file_path):
        _get_movie_info(file_path)
    else:
        _get_movie_info_from_a_dir(file_path)


def _get_movie_info_from_a_dir(directory, filters=None):
    filenames = get_all_video_files(directory)

    for filename in filenames:
        _get_movie_info(filename)

    _delete_movies_from_db_not_in_dir(filenames)


def _delete_movies_from_db_not_in_dir(movie_files):
    all_movies = db.get_all()
    for movie in all_movies:
        if movie[FILENAME_KEY] not in movie_files:
            db.delete_by_id(movie[ID_KEY])
            print(f"Deleted {PrintColors.apply_warning(movie[FILENAME_KEY])} from the movies database.")


def _get_movie_info(filename, imdb_client=None):
    imdb_cache = _search_imdb_cache_for_movie(db, filename)

    if len(imdb_cache) == 0:
        imdb = imdb_client if imdb_client is not None else IMDB()

        clean_move_name = get_cleaned_names_for_movie_files([filename])
        clean_movie_name_without_info = clean_move_name[0]['new'].split(' (')[0]
        movie_year = clean_move_name[0]['new'].split(' (')[1].split(')')[0] if ' (' in clean_move_name[0]['new'] else \
            None

        imdb_response = imdb.get_by_name(
            clean_movie_name_without_info,
            year=int(movie_year) if movie_year is not None else None
        )

        res = json.loads(imdb_response)

        if 'status' in res:
            print(
                f"{PrintColors.WARNING}Failed to get info for {filename}. Consider renaming the file to make it "
                f"easier for the IMDB api {PrintColors.ENDC}")
            return

        file_dir = os.path.join(os.getcwd(), os.path.dirname(filename))
        imdb_cache = [_map_imdb_response_to_db_format(res, file_dir, filename)]
        db.add(imdb_cache[0])

    for movie in imdb_cache:
        print_movie_info(movie)


def _map_imdb_response_to_db_format(imdb_response, source_dir, filename):
    return {
        TITLE_KEY: imdb_response["name"],
        YEAR_KEY: imdb_response["datePublished"].split("-")[0] if imdb_response["datePublished"] is not None else "?",
        DESCRIPTION_KEY: imdb_response["description"] if imdb_response["description"] is not None else "",
        DIRECTOR_KEY: _map_director_to_db_format(imdb_response["director"]),
        RATING_KEY: imdb_response["rating"]["ratingValue"] if imdb_response["rating"] is not None else "?",
        GENRE_KEY: _map_list_to_string(imdb_response["genre"]),
        KEYWORDS_KEY: imdb_response["keywords"] if imdb_response["keywords"] is not None else "",
        POSTER_URL_KEY: imdb_response["poster"],
        SOURCE_DIR_KEY: source_dir,
        FILENAME_KEY: filename,
        YOUTUBE_URL_KEY: "" #_build_youtube_link(imdb_response["name"]) TODO: Uncomment when rate limits are handled
    }


def _build_youtube_link(movie_name):
    result_id = get_first_youtube_search_video_result_id(movie_name + " trailer")
    if result_id is not None:
        return f"https://www.youtube.com/watch?v={result_id}"
    return "<Could not find a trailer on YouTube>"


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


def print_movie_info(movie_details):
    title = PrintColors.apply_header(movie_details[TITLE_KEY])
    title = PrintColors.apply_bold(title)
    year = f"({movie_details[YEAR_KEY]})"
    description = PrintColors.apply_bold(movie_details[DESCRIPTION_KEY])
    desc_print = f'\n\t- {description}' if description != "" else f"\n\t- <No description found>"
    rating = f'{movie_details[RATING_KEY]}'
    director = f" , {PrintColors.apply_underline('dir:')} {movie_details[DIRECTOR_KEY]}," if movie_details[
                                                                                                 DIRECTOR_KEY] is not None else ""
    genre = f'\n\t- {PrintColors.apply_underline("genre:")} {movie_details[GENRE_KEY]}' if movie_details[
                                                                                               GENRE_KEY] is not None else ""
    keywords = f'\n\t- {PrintColors.apply_underline("keywords:")} {movie_details[KEYWORDS_KEY]}' if movie_details[
                                                                                                        KEYWORDS_KEY] is not None else ""
    filepath = f'\n\t- {PrintColors.apply_underline("filepath:")} {os.path.join(movie_details[SOURCE_DIR_KEY], movie_details[FILENAME_KEY])}'

    youtube_link = f'\n\t- {PrintColors.apply_underline("youtube trailer:")} {movie_details[YOUTUBE_URL_KEY]}' if \
    movie_details[YOUTUBE_URL_KEY] is not None else ""

    print(f'\n* {title} {year} {director} [{rating}/10] {desc_print} {genre} {keywords} {youtube_link} {filepath}')
