from PyMovieDb import IMDB


def get_movie_info(movie_name):
    imdb = IMDB()
    return imdb.get_by_name(movie_name)
