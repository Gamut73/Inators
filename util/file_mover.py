import os
import shutil


def remove_source_dir(source_dir):
    try:
        shutil.rmtree(source_dir)
        print("\t- Successfully removed source directory")
    except OSError as e:
        print("\t- Error: %s - %s." % (e.filename, e.strerror))


def move_movie(source_dir):
    movie_dir = os.path.expanduser("~/Videos/Eiga")

    os.makedirs(movie_dir, exist_ok=True)
    movie_filepath = movie_dir

    if (is_video_file(source_dir)):
        shutil.move(source_dir, movie_dir)
        movie_filepath = os.path.join(movie_dir, os.path.basename(source_dir))
    else:
        for filename in os.listdir(source_dir):
            if is_video_file(filename) and not is_sample_video(filename):
                shutil.move(os.path.join(source_dir, filename), movie_dir)
                movie_filepath = os.path.join(movie_dir, filename)

    print("\t- Successfully moved movie")
    return movie_filepath


def get_all_video_files(source_dir):
    video_files = []
    for filename in os.listdir(source_dir):
        if is_video_file(filename) and not is_sample_video(filename):
            video_files.append(os.path.join(source_dir, filename))
    return video_files


def is_video_file(filename):
    return filename.endswith((".mp4", ".mkv", ".avi"))

def is_sample_video(filename):
    return filename.lower().find("sample") != -1

def _move_subtitles_from_subfolder(source_dir, subtitle_dir):
    for filename in os.listdir(source_dir):
        if filename.endswith(".srt"):
            shutil.move(os.path.join(source_dir, filename), subtitle_dir)


def _write_source_dir_as_name_with_underscores(source_path):
    source_folders = source_path.split(os.sep)
    result = ""
    black_list = [".", "sub", "subtitles", "subs", "download", "downloads"]  # replace with your actual blacklist

    for folder in source_folders:
        if folder and folder.lower() not in black_list:
            folder_with_underscores = folder.replace(" ", "_")
            if result:
                result += "_" + folder_with_underscores
            else:
                result = folder_with_underscores

    return result


def move_subtitles(source_dir):
    subtitle_dir = os.path.expanduser("~/Videos/Eiga/Subtitles")
    subtitle_dir = os.path.join(subtitle_dir, _write_source_dir_as_name_with_underscores(source_dir))
    print(subtitle_dir)

    potential_subtitle_folders = ['subs', 'Subs', 'subtitles', 'Subtitles', 'subtitle', 'Subtitle', 'sub', 'Sub']

    for folder in potential_subtitle_folders:
        sub_source_folder = os.path.join(source_dir, folder)
        if os.path.exists(sub_source_folder):
            os.makedirs(subtitle_dir, exist_ok=True)
            _move_subtitles_from_subfolder(sub_source_folder, subtitle_dir)

    print("\t- Successfully moved subtitles")