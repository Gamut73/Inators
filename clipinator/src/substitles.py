import os
import re
import shlex
import sys
import platform
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup
from InquirerPy import prompt
from PIL import Image, ImageDraw, ImageFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

TMP_SUBTITLES_PATH = os.path.join(os.getcwd(), "tmp_subtitle.srt")

def show_font_examples(
        font_name_filepath_pairs,
        example_phrase="I used to talk a lot once.\nIt didn't do me any good, so I stopped."
):
    block_width = 420
    block_height = 180
    padding = 20
    columns = 3
    font_size = 28
    background_color = (35, 35, 35)
    text_color = (255, 255, 255)

    rows = (len(font_name_filepath_pairs) + columns - 1) // columns
    image_width = columns * block_width
    image_height = rows * block_height

    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    for index, (font_name, font_filepath) in enumerate(font_name_filepath_pairs):
        column = index % columns
        row = index // columns
        x = column * block_width
        y = row * block_height

        draw.rectangle(
            [x, y, x + block_width - 1, y + block_height - 1],
            fill=background_color,
            outline=(80, 80, 80),
        )

        try:
            font = ImageFont.truetype(str(font_filepath), font_size)
            label_font = ImageFont.truetype(str(font_filepath), 18)
        except OSError:
            font = ImageFont.load_default()
            label_font = ImageFont.load_default()

        draw.text(
            (x + padding, y + padding),
            font_name,
            fill=text_color,
            font=label_font,
        )

        draw.multiline_text(
            (x + padding, y + padding + 40),
            example_phrase,
            fill=text_color,
            font=font,
            spacing=8,
        )

    image.show()
    return image

# TODO: Check if this is still needed since encoding support was added in moviepy
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


def show_subtitle_selection_menu(fonts, menu_msg):
    show_examples_option = {
        'name': 'Show examples',
        'value': 'show_examples',
    }

    options = [
        {
            'type': 'list',
            'name': 'subtitle_font',
            'message': menu_msg,
            'choices': [show_examples_option] + [
                {
                    'name': font_name,
                    'value': font_filepath,
                }
                for font_name, font_filepath in fonts
            ],
        }
    ]

    choice = prompt(options)['subtitle_font']
    if choice == 'show_examples':
        show_font_examples(fonts)
        return show_subtitle_selection_menu(fonts, menu_msg)
    return choice


def find_fonts():
    system = platform.system()

    if system == "Linux":
        return _font_filepaths_to_name_filepath_pairs(_find_linux_fonts())

    elif system == "Darwin":
        return _font_filepaths_to_name_filepath_pairs(_find_macos_fonts())

    elif system == "Windows":
        return _font_filepaths_to_name_filepath_pairs(_find_windows_fonts())

    raise RuntimeError(f"Unsupported OS: {system}")


def _font_filepaths_to_name_filepath_pairs(font_filepaths):
    return [
        (Path(font_filepath).stem, font_filepath)
        for font_filepath in font_filepaths
    ]


def _find_linux_fonts():
    result = subprocess.run(
        ["fc-list", "--format=%{file}\n"],
        capture_output=True,
        text=True,
        check=True,
    )

    return [
        Path(p)
        for p in result.stdout.splitlines()
        if p.lower().endswith(".ttf")
    ]


def _find_macos_fonts():
    directories = [
        Path.home() / "Library/Fonts",
        Path("/Library/Fonts"),
        Path("/System/Library/Fonts"),
    ]

    return _find_ttf_in_directories(directories)


def _find_windows_fonts():
    directories = [
        Path.home() / "AppData/Local/Microsoft/Windows/Fonts",
        Path("C:/Windows/Fonts"),
    ]

    return _find_ttf_in_directories(directories)


def _find_ttf_in_directories(directories):
    fonts = []

    for directory in directories:
        if directory.exists():
            fonts.extend(directory.rglob("*.ttf"))

    return sorted(set(fonts))


if __name__ == "__main__":
    for font in find_fonts():
        print(font)
