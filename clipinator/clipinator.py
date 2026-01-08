import csv
import os.path
import re
import shlex

import click
from bs4 import BeautifulSoup
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from send2trash import send2trash

from constants import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.logger import debug, info, error
from batch_files_menus import show_batch_files_selection_menu, show_batch_files_checklist_menu

TIMESTAMPS_FOLDER = 'Videos/Clips/Timestamps'
CSV_FILE_EDITOR = 'libreoffice'
DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Videos", "Clips")

TMP_AUDIO_PATH = os.path.join(os.getcwd(), "tmp_audio.mp3")
TMP_SUBTITLES_PATH = os.path.join(os.getcwd(), "tmp_subtitle.srt")


def _cleanup_temp_files():
    for tmp_path in [TMP_AUDIO_PATH, TMP_SUBTITLES_PATH]:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception as e:
                print(f"!!!Failed to remove temporary file: {e}!!!")
                print(f"!!!Temporary file is located at {tmp_path}!!!")


def clip_video(input_file_path, clip_name, start_time, end_time, output_dir, subtitles_filepath, audio_track_index):
    info(f"Clipping from {start_time} to {end_time} and saving it as {clip_name}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    og_vid_name = os.path.basename(input_file_path)
    clip_save_file_path = _build_clip_file_path(clip_name, og_vid_name, output_dir)

    video_clip = VideoFileClip(input_file_path)
    if subtitles_filepath != '':
        video_clip = _add_subtitles(video_clip, subtitles_filepath, video_clip.size[1])

    if audio_track_index is not None:
        video_clip = _set_alternative_audio_track(video_clip, input_file_path, audio_track_index)

    video_clip = video_clip.subclip(_convert_time_to_seconds(start_time), _convert_time_to_seconds(end_time))
    video_clip.write_videofile(clip_save_file_path)


def clip_multiple_clips_from_a_video(input_file_path, clips, clips_parent_folder_name, output_dir, subtitles_file_path,
                                     audio_track_index):
    clean_clips_parent_folder_name = clips_parent_folder_name.split('(')[0].strip()
    clips_parent_folder = os.path.join(output_dir, clean_clips_parent_folder_name)
    for clip in clips:
        subs_filepath = subtitles_file_path
        if 'ignore_subs' in clip and clip[IGNORE_SUBS_FIELD].lower() == 'y':
            info(f"Ignoring subtitles for clip {clip[TITLE_FIELD]}")
            subs_filepath = ''
        clip_video(input_file_path, clip[TITLE_FIELD], clip[START_TIME_FIELD], clip[END_TIME_FIELD],
                   clips_parent_folder, subs_filepath, audio_track_index)


def get_clips_from_csv_file(filepath):
    with open(filepath, 'r') as file:
        csv_reader = csv.DictReader(file)
        clips = []
        for row in csv_reader:
            clip = {
                START_TIME_FIELD: row[START_TIME_FIELD],
                END_TIME_FIELD: row[END_TIME_FIELD],
                TITLE_FIELD: row[TITLE_FIELD],
            }
            if IGNORE_SUBS_FIELD in row:
                clip[IGNORE_SUBS_FIELD] = row[IGNORE_SUBS_FIELD].strip()
            else:
                clip[IGNORE_SUBS_FIELD] = 'n'
            clips.append(clip)
    return clips


def _find_timestamps_file_in_timestamps_folder(filename):
    timestamps_folder = os.path.join(os.path.expanduser("~"), TIMESTAMPS_FOLDER)
    if os.path.exists(timestamps_folder):
        file_path = os.path.join(timestamps_folder, filename + '.csv')
        if os.path.exists(file_path):
            return file_path
        else:
            error(f"File {filename}.csv does not exist in the timestamps folder.")
    else:
        error(f"The timestamps folder does not exist at {timestamps_folder}.")


def generate_clips_csv_file_template(filename):
    folder_path = _create_folders_in_home(TIMESTAMPS_FOLDER)
    file_path = os.path.join(folder_path, filename + '.csv')
    header = [START_TIME_FIELD, END_TIME_FIELD, IGNORE_SUBS_FIELD, TITLE_FIELD]
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)

    _open_csv_editor(file_path)


def _set_alternative_audio_track(clip, video_filepath, audio_track_index):
    if not os.path.exists(TMP_AUDIO_PATH):
        os.system(f"ffmpeg -i {shlex.quote(video_filepath)} -map 0:a:{audio_track_index} -ab 160k -ac 2 -ar 44100 -vn -loglevel error {shlex.quote(TMP_AUDIO_PATH)}")

    audio_clip = AudioFileClip(TMP_AUDIO_PATH)
    info("Using alternative audio track with index ", audio_track_index)
    return clip.set_audio(audio_clip)


def _get_filename_from_path(file_path):
    file_name_with_extension = os.path.basename(file_path)
    return os.path.splitext(file_name_with_extension)[0]


def _parse_html_to_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()


def _add_subtitles(video_clip, subtitles_file, video_height):
    print("Subtitles file path: ", subtitles_file)
    txt_clip_generator = lambda txt: TextClip(
        _parse_html_to_text(txt),
        font='Dejavu-Sans-Bold',
        fontsize=int(video_height * 0.06),
        color='white',
        method='caption',
        stroke_color='black',
        stroke_width=1,
        align='South',
        size=video_clip.size
    )

    _remove_all_empty_lines(subtitles_file)
    subtitle_clip = SubtitlesClip(subtitles_file, txt_clip_generator)
    return CompositeVideoClip((video_clip, subtitle_clip.set_position(('center', 'bottom'))), size=video_clip.size)


def _remove_all_empty_lines(file_path):
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


def _create_folders_in_home(path):
    home_dir = os.path.expanduser("~")
    full_path = os.path.join(home_dir, path)
    os.makedirs(full_path, exist_ok=True)
    return full_path


def _open_csv_editor(file_path):
    os.system(CSV_FILE_EDITOR + ' \"' + file_path + '\"')


def _build_clip_file_path(clip_name, og_vid_name, output_dir):
    file_path = output_dir

    save_path_as_list = _get_save_path_as_list(clip_name)
    clip_name_without_group = save_path_as_list[-1]

    if len(save_path_as_list) > 1:
        for group_name in save_path_as_list[:-1]:
            file_path = os.path.join(file_path, group_name)
            os.makedirs(file_path, exist_ok=True)

    og_vid_name_without_ext = os.path.splitext(og_vid_name)[0]

    return os.path.join(file_path, clip_name_without_group + " (" + og_vid_name_without_ext + ").mp4")


def _get_save_path_as_list(input_string):
    substrings = re.findall(r'\[(.*?)\]', input_string)
    cleaned_string = re.sub(r'\[.*?\]', '', input_string)
    substrings.append(cleaned_string)

    return substrings


def _convert_time_to_seconds(time):
    while (time.count(":") != 2):
        time = "00:" + time

    time_split = time.split(":")
    return int(time_split[0]) * 3600 + int(time_split[1]) * 60 + int(time_split[2])


def _remove_font_size_from_subtitle_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    content = re.sub(r'<font\b[^>]*\bsize="\d+"[^>]*>', lambda m: re.sub(r'\bsize="\d+"', '', m.group(0)), content)

    with open(file_path, 'w') as file:
        file.write(content)


def _get_subtitle_file_path(embedded_subtitles, subtitles, input_file_path):
    if embedded_subtitles is not None:
        video_path = input_file_path
        os.system(
            f"ffmpeg -i {shlex.quote(video_path)} -map 0:s:{embedded_subtitles}  -scodec subrip -loglevel error {shlex.quote(TMP_SUBTITLES_PATH)}")
        _remove_font_size_from_subtitle_file(TMP_SUBTITLES_PATH)
        return TMP_SUBTITLES_PATH
    return subtitles


def _list_files_in_timestamps_folder():
    batch_files = _get_batch_files_in_timestamps_folder()
    for file in batch_files:
        print(f"  - {os.path.splitext(file)[0]}")


def _get_batch_files_in_timestamps_folder():
    folder_path = os.path.join(os.path.expanduser("~"), TIMESTAMPS_FOLDER)
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)
        if files:
            filenames_to_print = [f for f in files if f.endswith('.csv')]
            filenames_to_print.sort()
            return filenames_to_print
    else:
        error(f"The timestamps folder does not exist at {folder_path}. Creating it now.")
        os.makedirs(folder_path)
        return []


def open_template_file(filename):
    template_filepath = os.path.join(os.path.expanduser("~"), TIMESTAMPS_FOLDER, filename + '.csv')
    if os.path.exists(template_filepath):
        _open_csv_editor(template_filepath)
    else:
        error(f"File {filename}.csv does not exist in the timestamps folder.")


def _select_batch_file_via_menu():
    files = _get_batch_files_in_timestamps_folder()
    if not files:
        info("No batch files found in the timestamps folder.")
        return None
    return show_batch_files_selection_menu([os.path.splitext(f)[0] for f in files],
                                               menu_msg="Select batch file to open:")


@click.group()
def clipinator_cli():
    """Clipinator - Video clipping tool."""
    pass


@clipinator_cli.command()
@click.argument('input_file_path', type=click.Path(exists=True))
@click.argument('start_time', type=str)
@click.argument('end_time', type=str)
@click.argument('clip_name', type=str)
@click.option('-o', '--output-dir', default=DEFAULT_OUTPUT_DIR,
              help="Output directory. Creates a new directory if it doesn't exist.")
@click.option('-s', '--subtitles', default='', type=click.Path(),
              help="Path to the subtitles file (.srt)")
@click.option('-es', '--embedded-subtitles', type=int, default=None,
              help="Use subtitles embedded in the video file. Value is the index of the subtitle stream (default: 0)")
@click.option('-ea', '--embedded-audio', type=int, default=None,
              help="Use audio embedded in the video file. Value is the index of the audio stream")
def clip(input_file_path, start_time, end_time, clip_name, output_dir, subtitles, embedded_subtitles, embedded_audio):
    """Clip a single segment from a video file."""
    _cleanup_temp_files()
    try:
        subtitles_file_path = _get_subtitle_file_path(embedded_subtitles, subtitles, input_file_path)
        clip_video(input_file_path, clip_name, start_time, end_time, output_dir, subtitles_file_path, embedded_audio)
    finally:
        _cleanup_temp_files()


@clipinator_cli.command()
@click.argument('input_file_path', type=click.Path(exists=True))
@click.option('-o', '--output-dir', default=DEFAULT_OUTPUT_DIR,
              help="Output directory. Creates a new directory if it doesn't exist.")
@click.option('-s', '--subtitles', default='', type=click.Path(),
              help="Path to the subtitles file (.srt)")
@click.option('-es', '--embedded-subtitles', type=int, default=None,
              help="Use subtitles embedded in the video file. Value is the index of the subtitle stream")
@click.option('-ea', '--embedded-audio', type=int, default=None,
              help="Use audio embedded in the video file. Value is the index of the audio stream")
def batch_clip(input_file_path, output_dir, subtitles, embedded_subtitles, embedded_audio):
    """Clip multiple segments from a video using a CSV timestamps file. A menu will be shown to select the timestamps batch file."""
    _cleanup_temp_files()
    timestamps_file = _select_batch_file_via_menu()
    if not timestamps_file:
        error("You don't have any timestamp files to process.")
        return
    try:
        subtitles_file_path = _get_subtitle_file_path(embedded_subtitles, subtitles, input_file_path)
        timestamps_filepath = _find_timestamps_file_in_timestamps_folder(timestamps_file)
        clip_multiple_clips_from_a_video(
            input_file_path,
            get_clips_from_csv_file(timestamps_filepath),
            os.path.basename(timestamps_file).split('.')[0],
            output_dir,
            subtitles_file_path,
            embedded_audio
        )
        try:
            send2trash(timestamps_filepath)
            print(f"Moved {timestamps_filepath} to trash")
        except Exception as e:
            print(f"Failed to move {timestamps_filepath} to trash: because\n\t {e}")
    finally:
        _cleanup_temp_files()


@clipinator_cli.command()
@click.argument('filename', type=str)
def template(filename):
    """Generate a CSV template file for batch clipping."""
    generate_clips_csv_file_template(filename)


@clipinator_cli.group('batch-files')
def batch_files():
    """
    Manage timestamp files. Actions include:
    - list: List all timestamp files in the timestamps folder.
    - open FILENAME: Open a timestamp CSV file in the default editor.
    """
    pass


@batch_files.command('list')
def list_batch_files():
    """List all timestamp files in the timestamps folder."""
    _list_files_in_timestamps_folder()


@batch_files.command('open')
def open_batch_file():
    """Open a timestamp CSV file in the default editor. A menu will be shown to select the file."""
    filename = _select_batch_file_via_menu()
    if filename:
        open_template_file(filename)


@batch_files.command('delete')
def delete_batch_files():
    """Delete timestamp CSV files. A checklist menu will be shown to select the files to delete. Use the space button to tick checkboxes."""
    files = _get_batch_files_in_timestamps_folder()
    if not files:
        info("No batch files found in the timestamps folder.")
        return
    files_to_delete = show_batch_files_checklist_menu(
        [os.path.splitext(f)[0] for f in files],
        menu_msg="Select batch files to delete:"
    )
    if not files_to_delete:
        info("No files selected for deletion.")
        return
    for filename in files_to_delete:
        file_path = _find_timestamps_file_in_timestamps_folder(filename)
        try:
            send2trash(file_path)
            info(f"Moved {file_path} to trash")
        except Exception as e:
            error(f"Failed to move {file_path} to trash: because\n\t {e}")


if __name__ == "__main__":
    clipinator_cli()
