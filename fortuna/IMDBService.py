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
from util.youtube_api_client import *
from util.logger import warning, info, error
from util.printer import print_table, TableData, TableColumn

db = JsonDatabase(IMDB_DB_FILE_PATH)


def get_movie_files_by_filters(filters):
    return [movie[FILENAME_KEY] for movie in get_movie_info_by_filters(filters)]


def get_movie_info_by_filters(filters):
    if filters is None:
        return db.get_all()

    movies = []
    filter_dict = _get_filter_map(filters)
    info(f"Searching for movies with filters: {filter_dict}")
    cached_movies = db.get_all()
    if filter_dict is None:
        error("Invalid filters, return all cached movies")
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
            error(f"Invalid filter key: {key}")
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
            info(f"Deleted {movie[FILENAME_KEY]} from the movies database.")


def _get_movie_info(filename, imdb_client=None):
    imdb_cache = _search_imdb_cache_for_movie(db, filename)

    if len(imdb_cache) == 0:
        imdb = imdb_client if imdb_client is not None else IMDB()

        clean_move_name = get_cleaned_names_for_movie_files([filename])
        clean_movie_name_without_info = clean_move_name[0]['new'].split(' (')[0]
        movie_year = clean_move_name[0]['new'].split(' (')[1].split(')')[0] if ' (' in clean_move_name[0]['new'] else \
            None

        try:
            movie_year = int(movie_year) if movie_year is not None else None
        except ValueError:
            warning(f"Could not parse year '{movie_year}' for movie '{clean_movie_name_without_info}'. Ignoring year ")
            movie_year = None

        imdb_response = imdb.get_by_name(
            clean_movie_name_without_info,
            year=movie_year
        )

        res = json.loads(imdb_response)

        if 'status' in res:
            warning(
                f"Failed to get info for {filename}. Consider renaming the file to make it "
                "easier for the IMDB api")
            return

        file_dir = os.path.join(os.getcwd(), os.path.dirname(filename))
        imdb_cache = [_map_imdb_response_to_db_format(res, file_dir, filename)]
        db.add(imdb_cache[0])

    print_movie_info(imdb_cache)


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


def print_movie_info(movie_details_list):
    table_data = TableData(
        columns=[
            TableColumn(name="Title", style="cyan", width=30),
            TableColumn(name="Year", style="green", width=10),
            TableColumn(name="Director", style="magenta", width=30),
            TableColumn(name="Rating", style="yellow", width=10),
            TableColumn(name="Description", style="white", width=50),
            TableColumn(name="Genre", style="blue", width=30),
            TableColumn(name="Keywords", style="red", width=30),
            TableColumn(name="YouTube Trailer", style="bright_blue", width=50),
            TableColumn(name="Filepath", style="bright_green", width=70)
        ],
        rows=[],
        title="Movie Information"
    )
    for movie_details in movie_details_list:
        title = movie_details[TITLE_KEY]
        year = movie_details[YEAR_KEY]
        description = movie_details[DESCRIPTION_KEY] if movie_details[DESCRIPTION_KEY] != "" else "<No description found>"
        rating = movie_details[RATING_KEY]
        director = movie_details[DIRECTOR_KEY] if movie_details[DIRECTOR_KEY] is not None else ""
        genre = movie_details[GENRE_KEY] if movie_details[GENRE_KEY] is not None else ""
        keywords = movie_details[KEYWORDS_KEY] if movie_details[KEYWORDS_KEY] is not None else ""
        filepath = os.path.join(movie_details[SOURCE_DIR_KEY], movie_details[FILENAME_KEY])
        youtube_link = movie_details[YOUTUBE_URL_KEY] if movie_details[YOUTUBE_URL_KEY] is not None else ""
        row = [
            title,
            year,
            director,
            rating,
            description,
            genre,
            keywords,
            youtube_link,
            filepath
        ]
        table_data.rows.append(row)

    print_table(table_data)


