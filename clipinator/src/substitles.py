import os
import re
import shlex
import sys

from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

TMP_SUBTITLES_PATH = os.path.join(os.getcwd(), "tmp_subtitle.srt")


def parse_html_to_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()


def remove_empty_lines_at_and_of_subtitle_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    filtered_lines = []
    for i in range(len(lines)):
        if lines[i].strip():
            filtered_lines.append(lines[i])
        else:
            if i == len(lines) - 1:
                continue

            if lines[i + 1].strip().isdigit() and i + 2 < len(lines) and "-->" in lines[i + 2]:
                filtered_lines.append(lines[i])

    with open(file_path, 'w') as file:
        file.writelines(filtered_lines)


def get_tmp_subtitles_filepath():
    return TMP_SUBTITLES_PATH


def get_subtitle_file_path(embedded_subtitles, subtitles, input_file_path):
    if embedded_subtitles is not None:
        video_path = input_file_path
        os.system(
            f"ffmpeg -i {shlex.quote(video_path)} -map 0:s:{embedded_subtitles}  -scodec subrip -loglevel error {shlex.quote(TMP_SUBTITLES_PATH)}")
        _remove_font_size_from_subtitle_file(TMP_SUBTITLES_PATH)
        return TMP_SUBTITLES_PATH
    return subtitles


def _remove_font_size_from_subtitle_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    content = re.sub(r'<font\b[^>]*\bsize="\d+"[^>]*>', lambda m: re.sub(r'\bsize="\d+"', '', m.group(0)), content)

    with open(file_path, 'w') as file:
        file.write(content)


