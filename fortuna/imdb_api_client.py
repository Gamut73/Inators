from PyMovieDb import IMDB


def find_movie_info_by_title(title, year=None):
    imdb = IMDB()
    if year is not None:
        response = imdb.get_by_name(title)
    else:
        response = imdb.get_by_name(title, year=year)
    if response.find("https://www.imdb.com/title/") == -1:
        response = response.replace("https://www.imdb.com/", "https://www.imdb.com/title/")
    return response


if __name__ == "__main__":
    movie_name = "Made in Hong Kong"
    movie_info = find_movie_info_by_title(movie_name)
    print(movie_info)
