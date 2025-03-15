# Fortuna

Goddess: Fortuna is the goddess of fortune and the personification of luck in Roman religion.

Script: Fortuna helps you make entertainment decisions by randomly selecting a movie or TV show for you to watch. It can
also handle series organized in seasons folders. In the future, it will also choose what you watch for you based on your
preferences that you wouldn't otherwise be able to express without the use of natural language.

# Usage

`python3 fortuna.py <directory>`

If you expect series organized in seasons folders, use the `-s` or `--series` flag:

`python3 fortuna.py <directory> -s`

# Arguments

- `<directory>`: The source directory where the media files are located.
- `-s` or `--series`: Use this flag if you expect series organized in seasons folders when playing.
- `-n` or `--number`: The number of videos to play. Default is 1.
- `-i` or `--info`: Get movie info. The value is a movie file or a directory containing movie files.
- `-f` or `--filters`: Filter for cached movies. The forma is `field:value,field:value`. You can use multiple filters by
  separating them with a comma. For example: `genre:comedy,keywords:japanese`. Use the `-lf` or `--list_fields` flag to
  see all fields you can filter by.
- `-l` or `--list`: List all cached movies that have information. Can be filtered using the `-f` or `--filters` flag.
- `-lf` or `--list_fields`: Without arguments, lists all fields you can filter by. When provided with a field name (e.g., `-lf genre`), displays counts of all unique values for that field in the IMDB cache. For example, running `python fortuna.py -lf genre` will show all unique genre values and how many movies match each genre, like:
  ```
  Values for 'genre':
  - action: 22
  - comedy: 12
  - fantasy: 10
  - scifi: 1
  ```
  The matching is case insensitive, so "Comedy" and "comedy" are counted as the same value.