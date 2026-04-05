import csv
import os
import sys

from InquirerPy import prompt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from util.logger import info, error
from constants import TIMESTAMPS_FOLDER
from string_util import extract_text_from_parenthesis
from file_util import open_csv_in_editor, create_folders_in_home_folder_from_path
from constants import START_TIME_FIELD, END_TIME_FIELD, IGNORE_SUBS_FIELD, TITLE_FIELD


def find_batch_file_by_name(filename):
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
    folder_path = create_folders_in_home_folder_from_path(TIMESTAMPS_FOLDER)
    file_path = os.path.join(folder_path, filename + '.csv')
    header = [START_TIME_FIELD, END_TIME_FIELD, IGNORE_SUBS_FIELD, TITLE_FIELD]
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)

    open_csv_in_editor(file_path)


def list_files_in_batch_file_folder():
    batch_files = get_batch_files_in_batch_file_folder()
    for file in batch_files:
        print(f"  - {os.path.splitext(file)[0]}")


def open_batch_file(filename):
    template_filepath = os.path.join(os.path.expanduser("~"), TIMESTAMPS_FOLDER, filename + '.csv')
    if os.path.exists(template_filepath):
        open_csv_in_editor(template_filepath)
    else:
        error(f"File {filename}.csv does not exist in the timestamps folder.")


def find_video_file_in_folder_using_batch_file_name(video_filenames, batch_file_name):
    match_string = extract_text_from_parenthesis(batch_file_name)[0]
    if not match_string:
        error(f"Batch file name {batch_file_name} does not contain any parenthetical text to match video file name to.")
        return None

    matching_video_files = [video for video in video_filenames if match_string in video]
    if not matching_video_files:
        error(f"No video files found matching batch file name {batch_file_name} with match string {match_string}.")
        return None
    elif len(matching_video_files) > 1:
        error(f"Multiple video files found matching batch file name {batch_file_name} with match string {match_string}. Please make sure the batch file name uniquely identifies the video file.")
        return None

    return matching_video_files[0]


def select_batch_file_via_menu():
    files = get_batch_files_in_batch_file_folder()
    if not files:
        info("No batch files found in the timestamps folder.")
        return None
    return show_batch_files_selection_menu([os.path.splitext(f)[0] for f in files],
                                               menu_msg="Select batch file to open:")


def get_all_batch_files_for_series(series_name):
    info(f"Searching for batch files for series {series_name}")
    files = get_batch_files_in_batch_file_folder()
    series_files = []
    for file in files:
        if series_name in file:
            series_files.append(file)
    return series_files


def get_batch_files_in_batch_file_folder():
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


def show_batch_files_selection_menu(batch_files, menu_msg):
    options = [
        {
            'type': 'list',
            'name': 'batch_file',
            'message': menu_msg,
            'choices': batch_files,
        }
    ]

    return prompt(options)['batch_file']


def show_batch_files_checklist_menu(batch_files, menu_msg):
    options = [
        {
            'type': 'checkbox',
            'name': 'batch_files_to_delete',
            'message': menu_msg,
            'choices': batch_files,
        }
    ]

    return prompt(options)['batch_files_to_delete']
