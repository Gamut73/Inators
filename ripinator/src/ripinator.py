import os
import re
import shlex
import subprocess
import sys

import click

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class MediaInfoSection:
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

        for media_section_value in [MediaInfoSection.AUDIO, MediaInfoSection.TEXT]:
            if media_section_value in heading:
                matching_sections.append(section.strip())
                break

    return matching_sections


@click.group()
def ripinator_cli():
    """Ripinator - CLI tool for extracting audio tracks and subtitles from video files."""
    pass


@ripinator_cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('-i', '--index', default=0, type=int,
              help="Index of the audio stream to rip (default: 0)")
def audio(file_path, index):
    """Rip an audio track from a video file."""
    output_file = os.path.splitext(file_path)[0] + "_audio.mp3"
    _get_audio_from_video(file_path, output_file, index)


@ripinator_cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('-i', '--index', default=0, type=int,
              help="Index of the subtitle stream to rip (default: 0)")
def subtitle(file_path, index):
    """Rip subtitles from a video file."""
    output_file = os.path.splitext(file_path)[0] + "_subtitle.srt"
    _get_subtitle_from_video(file_path, output_file, index)


@ripinator_cli.command('list-streams')
@click.argument('file_path', type=click.Path(exists=True))
def list_streams(file_path):
    """List audio and subtitle streams in the video file."""
    _get_media_info(file_path)


if __name__ == "__main__":
    ripinator_cli()
