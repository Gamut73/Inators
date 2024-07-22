# Fortuna

Goddess: Fortuna is the goddess of fortune and the personification of luck in Roman religion.

Script: Fortuna helps you make entertainment decisions by randomly selecting a movie or TV show for you to watch. It can also handle series organized in seasons folders. In the future, it will also choose what you watch for you based on your preferences that you wouldn't otherwise be able to express without the use of natural language.

# Usage
`python3 fortuna.py <directory>`

If you expect series organized in seasons folders, use the `-s` or `--series` flag:

`python3 fortuna.py <directory> -s`

# Arguments
- `<directory>`: The source directory where the media files are located.
- `-s` or `--series`: Use this flag if you expect series organized in seasons folders.
- '-n' or '--number': The number of videos to play. Default is 1.