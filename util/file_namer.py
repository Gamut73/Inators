import os
import sys
from pathlib import Path

#TODO: Destroy the monster that this file has become


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.file_namer_llm_prompts import (build_clean_series_folder_name_prompt,
                                         build_clean_subdir_names_prompt,
                                         build_clean_episode_names_prompt,
                                         build_clean_movie_names_in_dir_prompt)
from util.llm_client import *


def clean_series_dir(directory):
    if not os.path.isdir(directory):
        print(f"{directory} is not a directory.")
        return

    directory = _clean_series_folder_name(directory)

    subdirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    if len(subdirs) > 1:
        _clean_subdir_names(directory, subdirs)

        for subdir in subdirs:
            subdir_path = os.path.join(directory, subdir)
            video_files = _get_movies_in_dir(subdir_path)
            if len(video_files) > 1:
                _clean_episode_names(subdir_path, video_files)
    else:
        video_files = _get_movies_in_dir(directory)
        if len(video_files) > 1:
            _clean_episode_names(directory, video_files)
    print('* Done :-)')


def _clean_series_folder_name(directory):
    prompt = build_clean_series_folder_name_prompt(directory)
    response = make_llm_request(prompt)
    clean_titles = _build_json_object_for_rename_response(response)

    clean_title = clean_titles[0]
    new_dirname = clean_title['new']
    print(f"- {clean_title['old']} --> {clean_title['new']}")
    os.rename(clean_title['old'], new_dirname)

    return new_dirname


def _clean_subdir_names(directory, subdirs):
    prompt = build_clean_subdir_names_prompt(subdirs)
    response = make_llm_request(prompt)
    clean_titles = _build_json_object_for_rename_response(response)

    for clean_title in clean_titles:
        print(f"- {clean_title['old']} --> {clean_title['new']}")
        new_dirname = os.path.join(directory, clean_title['new'])
        os.rename(os.path.join(directory, clean_title['old']), new_dirname)


def _clean_episode_names(subdir_path, video_files):
    prompt = build_clean_episode_names_prompt(video_files)
    response = make_llm_request(prompt)
    clean_titles = _build_json_object_for_rename_response(response)

    for clean_title in clean_titles:
        print(f"- {clean_title['old']} --> {clean_title['new']}")
        new_filename = os.path.join(subdir_path, clean_title['new'])
        os.rename(os.path.join(subdir_path, clean_title['old']), new_filename)

    response = make_llm_request(prompt)
    return (response.text
            .replace("```", "")
            .rstrip())


def _rename_file(filepath, new_filename):
    os.rename(filepath, new_filename)


def _get_movies_in_dir(directory):
    filenames = os.listdir(directory)
    return [os.path.join(directory, filename) for filename in filenames if filename.endswith((".mp4", ".mkv", ".avi"))]


def _build_json_object_for_rename_response(response):
    response_lines = response.strip().splitlines()
    return [_build_json_object_for_rename_response_line(response_line) for response_line in response_lines]


def _build_json_object_for_rename_response_line(response_line):
    old_name, new_name = response_line.split("||")
    return {"old": old_name, "new": new_name}


def get_cleaned_names_for_movie_files(movie_names):
    prompt = build_clean_movie_names_in_dir_prompt(movie_names)
    response = make_llm_request(prompt)
    clean_titles = _build_json_object_for_rename_response(response.rstrip())

    return clean_titles


def clean_list_of_movie_files(movie_files):
    clean_titles = get_cleaned_names_for_movie_files(movie_files)

    for clean_title in clean_titles:
        new_filename = os.path.join(os.path.dirname(clean_title['old']), clean_title['new'])
        _rename_file(clean_title['old'], new_filename)
        print(f"- {clean_title['old']} --> {clean_title['new']}")
    print('* Done :-)')


def clean_movie_names_in_dir(directory):
    print(f"* Finding all the movies in the directory: {directory}")
    movie_files = _get_movies_in_dir(directory)

    clean_list_of_movie_files(movie_files)


def clean_movie_name(filepath):
    clean_list_of_movie_files([filepath])


def _load_dotenv():
    script_dir = Path(__file__).parent
    load_dotenv(script_dir / 'local.env')
