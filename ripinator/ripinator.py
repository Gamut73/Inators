import argparse
import os
import re
import shlex
import subprocess
import sys
from enum import Enum

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class RipType(Enum):
    NON = 0
    AUDIO = 1
    SUBTITLE = 2


class MediaInfoSection(Enum):
    AUDIO = 'Audio'
    TEXT = 'Text'


def _remove_font_size_from_subtitle_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    content = re.sub(r'<font\b[^>]*\bsize="\d+"[^>]*>', lambda m: re.sub(r'\bsize="\d+"', '', m.group(0)), content)

    with open(file_path, 'w') as file:
        file.write(content)


def _get_subtitle_from_video(video_path, subtitle_path, subtitle_index):
    os.system(
        f"ffmpeg -i {shlex.quote(video_path)} -map 0:s:{subtitle_index}  -scodec subrip {shlex.quote(subtitle_path)}")
    _remove_font_size_from_subtitle_file(subtitle_path)


def _get_audio_from_video(video_path, audio_path, audio_index):
    os.system(
        f"ffmpeg -i {shlex.quote(video_path)} -map 0:a:{audio_index} -ab 160k -ac 2 -ar 44100 -vn {shlex.quote(audio_path)}")


def _get_media_info(media_filepath):
    mediainfo_cli_output = subprocess.run(
        ['mediainfo', media_filepath],
        capture_output=True,
        text=True,
        check=True
    )

    sections = _parse_mediainfo_sections_for_streams(mediainfo_cli_output.stdout)
    for section in sections:
        print(f"{section}\n-------------------------")


def _parse_mediainfo_sections_for_streams(mediainfo_text):
    sections = mediainfo_text.strip().split('\n\n')
    matching_sections = []

    for section in sections:
        if not section.strip():
            continue

        lines = section.strip().split('\n')
        if not lines:
            continue

        heading = lines[0].strip()

        for media_section in MediaInfoSection:
            if media_section.value in heading:
                matching_sections.append(section.strip())
                break

    return matching_sections


def main(file_path, rip_type, index):
    new_file = os.path.splitext(file_path)[0]
    if rip_type == RipType.AUDIO:
        new_file = new_file + "_audio.mp3"
        _get_audio_from_video(file_path, new_file, index)
    else:
        new_file = new_file + "_subtitle.srt"
        _get_subtitle_from_video(file_path, new_file, index)


if __name__ == "__main__":
    rip_type = RipType.NON
    index = 0

    parser = argparse.ArgumentParser(description='Rip audio or subtitles from a video file.')
    parser.add_argument('file_path', type=str, help='File path of the video')
    parser.add_argument('-a', '--audio', nargs='?', const=0, type=int,
                        help='Rip audio from video. Optionally specify the audio index to rip (default is 0)')
    parser.add_argument('-s', '--subtitle', nargs='?', const=0, type=int,
                        help='Rip subtitles from video. Optionally specify the subtitle index to rip (default is 0)')
    parser.add_argument('-ls', '--list-streams', action='store_true', help='List audio streams in the video')

    args = parser.parse_args()

    if args.subtitle is not None:
        rip_type = RipType.SUBTITLE
        index = args.subtitle
    elif args.audio is not None:
        rip_type = RipType.AUDIO
        index = args.audio
    elif args.list_streams:
        _get_media_info(args.file_path)
    else:
        print("Please specify either --audio or --subtitle option.")

    if rip_type != RipType.NON:
        main(args.file_path, rip_type, index)
