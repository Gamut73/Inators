import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from constants import CSV_FILE_EDITOR
from string_util import filepath_to_list


def _get_filename_from_path(file_path):
    file_name_with_extension = os.path.basename(file_path)
    return os.path.splitext(file_name_with_extension)[0]


def create_folders_in_home_folder_from_path(path):
    home_dir = os.path.expanduser("~")  # TODO: Suppose HOME ought to be platform  dependent? BWGAFAWA?
    full_path = os.path.join(home_dir, path)
    os.makedirs(full_path, exist_ok=True)
    return full_path


def build_clip_file_path(clip_name, og_vid_name, output_dir):
    file_path = output_dir

    save_path_as_list = filepath_to_list(clip_name)
    clip_name_without_group = save_path_as_list[-1]

    if len(save_path_as_list) > 1:
        for group_name in save_path_as_list[:-1]:
            file_path = os.path.join(file_path, group_name)
            os.makedirs(file_path, exist_ok=True)

    og_vid_name_without_ext = os.path.splitext(og_vid_name)[0]

    return os.path.join(file_path, clip_name_without_group + " (" + og_vid_name_without_ext + ").mp4")


def open_csv_in_editor(file_path):
    os.system(CSV_FILE_EDITOR + ' \"' + file_path + '\"')
