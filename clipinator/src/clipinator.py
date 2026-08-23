import os
import os.path
import subprocess
import sys

import click
from send2trash import send2trash

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from constants import CLIPS_PARENT_FOLDER, TIMESTAMPS_FOLDER, MEDIA_PLAYER
from util.logger import info, error, warning
from batch_files import show_batch_files_checklist_menu, \
    get_batch_files_in_batch_file_folder
from batch_files import (select_batch_file_via_menu,
                         get_all_batch_files_for_series,
                         find_video_file_in_folder_using_batch_file_name,
                         list_files_in_batch_file_folder,
                         generate_clips_csv_file_template,
                         find_batch_file_by_name,
                         open_batch_file_in_editor,
                         show_batch_files_selection_menu)
from substitles import get_tmp_subtitles_filepath, get_subtitle_file_path, show_subtitle_selection_menu, find_fonts
from clips import clip_video, clip_multiple_clips_from_a_video, get_tmp_audio_path, get_default_output_dir, get_clips_from_csv_file


def _cleanup_temp_files():
    for tmp_path in [get_tmp_audio_path(), get_tmp_subtitles_filepath()]:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception as e:
                print(f"!!!Failed to remove temporary file: {e}!!!")
                print(f"!!!Temporary file is located at {tmp_path}!!!")


def open_video_with_medial_player(video_files):
    info(f"Playing...")
    with open(os.devnull, 'w') as devnull:
        subprocess.call([MEDIA_PLAYER] + video_files, stdout=devnull, stderr=devnull)


@click.group()
def clipinator_cli():
    """Clipinator - Video clipping tool."""
    pass


@clipinator_cli.command()
@click.argument('input_file_path', type=click.Path(exists=True))
@click.argument('start_time', type=str)
@click.argument('end_time', type=str)
@click.argument('clip_name', type=str)
@click.option('-o', '--output-dir', default=get_default_output_dir(),
              help="Output directory. Creates a new directory if it doesn't exist.")
@click.option('-s', '--subtitles', default='', type=click.Path(),
              help="Path to the subtitles file (.srt)")
@click.option('-es', '--embedded-subtitles', type=int, default=None,
              help="Use subtitles embedded in the video file. Value is the index of the subtitle stream (default: 0)")
@click.option('-pf', '--pick-font', is_flag=True, default=False,
              help="If subtitles were added using -s or -es then this flag allows you to pick a custom font from all the available (.ttf) files on your system to use for the subtitles. First option generates an image with samples of all the available fonts.")
@click.option('-ea', '--embedded-audio', type=int, default=None,
              help="Use audio embedded in the video file. Value is the index of the audio stream")
@click.option('-p', '--play', is_flag=True, help="Play the generated clip after creation.")
def clip(input_file_path, start_time, end_time, clip_name, output_dir, subtitles, embedded_subtitles, pick_font,  embedded_audio,
         play):
    """Clip a single segment from a video file."""
    _cleanup_temp_files()

    custom_font_filepath = show_subtitle_selection_menu(
        find_fonts(), menu_msg="Select a subtitle file:"
    ) if (subtitles != '' or embedded_subtitles is not None) and pick_font else None

    try:
        subtitles_file_path = get_subtitle_file_path(embedded_subtitles, subtitles, input_file_path)
        clip_filepath = clip_video(input_file_path, clip_name, start_time, end_time, output_dir, subtitles_file_path, embedded_audio, custom_font_filepath)

        _cleanup_temp_files()
        if play:
            open_video_with_medial_player([clip_filepath])

    except Exception as e:
        error(f"An error occurred while processing the video file.\n\t{e}")


@clipinator_cli.command()
@click.argument('input_file_path', type=click.Path(exists=True))
@click.option('-o', '--output-dir', default=get_default_output_dir(),
              help="Output directory. Creates a new directory if it doesn't exist.")
@click.option('-s', '--subtitles', default='', type=click.Path(),
              help="Path to the subtitles file (.srt)")
@click.option('-es', '--embedded-subtitles', type=int, default=None,
              help="Use subtitles embedded in the video file. Value is the index of the subtitle stream")
@click.option('-pf', '--pick-font', is_flag=True, default=False,
              help="If subtitles were added using -s or -es then this flag allows you to pick a custom font from all the available (.ttf) files on your system to use for the subtitles. First option generates an image with samples of all the available fonts.")
@click.option('-ea', '--embedded-audio', type=int, default=None,
              help="Use audio embedded in the video file. Value is the index of the audio stream")
@click.option('-p', '--play', is_flag=True, help="Open the output folder in the media player after creation.")
def batch_clip(input_file_path, output_dir, subtitles, embedded_subtitles, pick_font, embedded_audio, play):
    """Clip multiple segments from a video using a CSV timestamps file. A menu will be shown to select the timestamps batch file."""
    _cleanup_temp_files()
    timestamps_file = select_batch_file_via_menu()

    custom_font = show_subtitle_selection_menu(
        find_fonts(), menu_msg="Select a subtitle file:"
    ) if (subtitles != '' or embedded_subtitles is not None) and pick_font else None

    if not timestamps_file:
        error("You don't have any timestamp files to process.")
        return
    try:
        subtitles_file_path = get_subtitle_file_path(embedded_subtitles, subtitles, input_file_path)
        timestamps_filepath = find_batch_file_by_name(timestamps_file)
        batch_name = os.path.basename(timestamps_file).split('.')[0]

        clips_filepaths = clip_multiple_clips_from_a_video(
            input_file_path,
            get_clips_from_csv_file(timestamps_filepath),
            batch_name,
            output_dir,
            subtitles_file_path,
            embedded_audio,
            custom_font
        )
        try:
            send2trash(timestamps_filepath)
            print(f"Moved {timestamps_filepath} to trash")
        except Exception as e:
            print(f"Failed to move {timestamps_filepath} to trash: because\n\t {e}")

        _cleanup_temp_files()
        if play:
            open_video_with_medial_player(clips_filepaths)
    except Exception as e:
        error(f"An error occurred while processing batch file {timestamps_file}: because of error:")
        print(e)



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
    list_files_in_batch_file_folder()


@batch_files.command('open')
def open_batch_file():
    """Open a timestamp CSV file in the default editor. A menu will be shown to select the file."""
    filename = select_batch_file_via_menu()
    if filename:
        open_batch_file_in_editor(filename)


@batch_files.command('delete')
def delete_batch_files():
    """Delete timestamp CSV files. A checklist menu will be shown to select the files to delete. Use the space button to tick checkboxes."""
    files = get_batch_files_in_batch_file_folder()
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
        file_path = find_batch_file_by_name(filename)
        try:
            send2trash(file_path)
            info(f"Moved {file_path} to trash")
        except Exception as e:
            error(f"Failed to move {file_path} to trash: because\n\t {e}")


@batch_files.command('restore')
def restore_batch_file():
    """Restore a CSV timestamp file from the trash back to the timestamps folder."""
    from batch_files import get_csv_files_in_trash, restore_csv_from_trash
    files = get_csv_files_in_trash()
    if not files:
        info("No CSV files found in the trash.")
        return
    selected = show_batch_files_selection_menu(
        [os.path.splitext(f)[0] for f in files],
        menu_msg="Select a CSV file to restore:"
    )
    if not selected:
        return
    # Find the matching filename with extension
    match = next((f for f in files if os.path.splitext(f)[0] == selected), None)
    if match:
        try:
            dest = restore_csv_from_trash(match)
            info(f"Restored {match} to {dest}")
        except Exception as e:
            error(f"Failed to restore {match}: {e}")


@clipinator_cli.command('series-clip')
@click.argument('src_folder', type=click.Path(exists=True))
@click.argument('series_name', type=str)
def series_clip(src_folder, series_name):
    """"
    Clip multiple episodes from a Fseries
    :argument src_folder: The folder containing the videos files with episodes to clip
    :argument series_name: The name of the series.
    This will be used to find all the batch-files for each episode in TIMESTAMP_FOLDER. Whatever is in () in the batch file name will be used to match to the respective video file.
    e.g "Peep Show (S01E01)" will be matched to "Peep Show S01E01.mkv"
    """
    series_batch_files = get_all_batch_files_for_series(series_name)
    if not series_batch_files:
        error(f"No batch files found for series {series_name}. Make sure your batch files are named in the format 'Series Name (SXXEXX)' and that they are located in the timestamps folder.")
        return

    video_filenames = [f for f in os.listdir(src_folder) if f.lower().endswith(('.mp4', '.mkv', '.avi', '.mov'))]
    if not video_filenames:
        error(f"No video files found in source folder {src_folder}. Make sure the folder contains video files with extensions .mp4, .mkv, .avi or .mov.")
        return

    for batch_file in series_batch_files:
        video_file = find_video_file_in_folder_using_batch_file_name(video_filenames, batch_file)
        if not video_file:
            warning(f"Skipping batch file {batch_file} because no matching video file was found.")
            continue

        input_file_path = os.path.join(src_folder, video_file)
        info(f"Processing batch file {batch_file} with video file {video_file}")
        timestamps_filepath = find_batch_file_by_name(os.path.splitext(batch_file)[0])
        if not timestamps_filepath:
            warning(f"Skipping batch file {batch_file} because the timestamps file could not be found.")
            continue

        try:
            clip_multiple_clips_from_a_video(
                input_file_path,
                get_clips_from_csv_file(timestamps_filepath),
                os.path.basename(batch_file).split('.')[0],
                get_default_output_dir(),
                '',
                None
            )
            try:
                send2trash(timestamps_filepath)
                info(f"Moved {timestamps_filepath} to trash")
            except Exception as e:
                error(f"Failed to move {timestamps_filepath} to trash: because\n\t {e}")
        except Exception as e:
            error(f"An error occurred while processing batch file {batch_file}: because\n\t {e}")


@clipinator_cli.group('goto')
def goto():
    """
    Jump to the general clips folder or batch-files folder:
    """
    pass


@goto.command('clips')
def goto_clips():
    _goto_folder(CLIPS_PARENT_FOLDER)


@goto.command('batch-files')
def goto_batch_files():
    _goto_folder(TIMESTAMPS_FOLDER)


def _get_shell_path() -> str:
    return os.environ.get('SHELL', 'bash')

def _goto_folder(folder_path) -> None:
    target = os.path.abspath(os.path.join(os.path.expanduser("~"), folder_path))
    os.makedirs(target, exist_ok=True)
    os.chdir(target)
    os.system(_get_shell_path())


if __name__ == "__main__":
    clipinator_cli()
