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


def _get_video_duration(video_path):
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', video_path],
        capture_output=True, text=True, check=True
    )
    total_seconds = float(result.stdout.strip())
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def _get_audio_from_video(video_path, audio_path, audio_index, start_time, end_time):
    print(f"Extracting audio stream from start time: {start_time} to end time: {end_time}...")
    subprocess.run(
        [
            'ffmpeg', '-y',
            '-ss', start_time,
            '-to', end_time,
            '-i', video_path,
            '-map', f'0:a:{audio_index}',
            '-ab', '160k', '-ac', '2', '-ar', '44100',
            '-vn',
            audio_path,
        ],
        check=True
    )


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


def _validate_timestamp(ctx, param, value):
    if value is None:
        return value
    if not re.match(r'^\d{2}:\d{2}:\d{2}$', value):
        raise click.BadParameter("Timestamp must be in 'hh:mm:ss' format.")
    return value


@click.group()
def ripinator_cli():
    """Ripinator - CLI tool for extracting audio tracks and subtitles from video files."""
    pass


@ripinator_cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('-i', '--index', default=0, type=int,
              help="Index of the audio stream to rip (default: 0)")
@click.option('-s', '--start', default=None, type=str, callback=_validate_timestamp,
              help="Start time in 'hh:mm:ss' format (default: 00:00:00)")
@click.option('-e', '--end', default=None, type=str, callback=_validate_timestamp,
              help="End time in 'hh:mm:ss' format (default: duration of video)")
@click.option('-o', '--output-file', default=None, type=click.Path(),
              help="Output audio file path (default: <input_basename>_audio.mp3)")
def audio(file_path, index, start, end, output_file):
    """Rip an audio track from a video file."""
    output_file = output_file if output_file is not None else os.path.splitext(file_path)[0] + "_audio.mp3"
    start_time = start if start is not None else "00:00:00"
    end_time = end if end is not None else _get_video_duration(file_path)
    _get_audio_from_video(file_path, output_file, index, start_time, end_time)


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
