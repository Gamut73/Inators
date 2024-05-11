import os
import json
import google.generativeai as genai

def _rename_file(filepath, new_filename):
    os.rename(filepath, new_filename)

def _get_movies_in_dir(dir):
    filenames = os.listdir(dir)
    return [filename for filename in filenames if filename.endswith((".mp4", ".mkv", ".avi"))]

def _build_json_object_for_rename_response(response):
    response_lines = response.split("\n")
    return [_build_json_object_for_rename_response_line(response_line) for response_line in response_lines]

def _build_json_object_for_rename_response_line(response_line):
    old_name, new_name = response_line.split("||")
    return {"old": old_name, "new": new_name}
    

def _build_clean_movie_names_in_dir_prompt(filenames):
    prompt = """
    Below are file names. Clean them up so that they are in the format of '<Movie Title: Subtitle (Year)>'. Put each 
    on a line with <old-name>||<new-name> Here is an example:
    For the filenames:
    2004 - Survive Style 5+.mkv 
    Akira (1988) 2160p HDR 5.1 Eng - Jpn x265 10bit Phun Psyz.mkv
    Europa.Europa.1990.1080p.BluRay.x264-[YTS.LT].mp4
    You answer should be:
    2004 - Survive Style 5+.mkv||Survive Style 5+ (2004).mkv
    Akira (1988) 2160p HDR 5.1 Eng - Jpn x265 10bit Phun Psyz.mkv||Akira (1988).mkv
    Europa.Europa.1990.1080p.BluRay.x264-[YTS.LT].mp4||Europa Europa (1990).mp4
    Here are the file name(s) to clean up: 
    """
    for filename in filenames:
        prompt += filename + "\n"

    return prompt


def clean_movie_names_in_dir(dir):
    genai.configure(api_key="YOUR_API_KEY")
    text_model = genai.GenerativeModel('gemini-pro')

    print(f"* Finding all the movies in the directory: {dir}")
    movie_titles = _get_movies_in_dir(dir)    
    
    print('* Cleaning up movie names')
    prompt = _build_clean_movie_names_in_dir_prompt(movie_titles)
    
    response = text_model.generate_content(prompt)
    clean_titles = _build_json_object_for_rename_response(response.text)
    print('* Renaming movies')
    for clean_title in clean_titles:
        _rename_file(os.path.join(dir, clean_title['old']), os.path.join(dir, clean_title['new']))
        print(f"\t- {clean_title['old']} --> {clean_title['new']}")
    print('* Done :-)')    