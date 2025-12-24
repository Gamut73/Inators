import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.llm_client import LLMPrompt, LLMPromptExample


def build_clean_series_folder_name_prompt(directory):
    return LLMPrompt(
        action="""
    Below is a series folder name. Clean it up so that it is in the format of '<Series Title: Subtitle (Year)>'. Then return  
    a line with <old-name>||<new-name> as output
    """,
        examples=[
            LLMPromptExample(
                input="""
    Allo Allo 1984 Season 1 to 3 Complete DVDRip x264 [i_c]
    Early Doors S01 720p Webrip x264 ANACKY99
    Game.Of.Thrones.S01.Season.1.1080p.5.1Ch.BluRay.ReEnc-DeeJayAhmed
    The.Story.of.Tokyo.Stories.S01.JAPANESE.WEBRip.x264-ION10
    """,
                output="""
    Allo Allo 1984 Season 1 to 3 Complete DVDRip x264 [i_c]||Allo Allo (1984)
    Early Doors S01 720p Webrip x264 ANACKY99||Early Doors
    Game.Of.Thrones.S01.Season.1.1080p.5.1Ch.BluRay.ReEnc-DeeJayAhmed||Game Of Thrones
    The.Men.Tokyo.Stories.S01.JAPANESE.WEBRip.x264-ION10|| The Men: Tokyo Stories
    """
            )
        ],
        payload=directory
    )


def build_clean_subdir_names_prompt(sub_dirs):
    return LLMPrompt(
        action="""
    Below are folder names. Rename them to season numbers in the format 'S01', 'S02', etc. Put each on a line with <old-name>||<new-name>
    """,
        examples=[
            LLMPromptExample(
                input="""
    Star Trek Season 1
    Star Trek Season 2
    Star Trek Season 3
    """,
                output="""
    Star Trek Season 1||S01
    Star Trek Season 2||S02
    Star Trek Season 3||S03
    """
            )
        ],
        payload=", ".join(sub_dirs)
    )


def build_clean_episode_names_prompt(video_files):
    return LLMPrompt(
        action="""
    Below are file names. Rename them to episode numbers in the format '<series-title> S<season>E<episode> <episode-title>.<ext>' 
    """,
        examples=[
            LLMPromptExample(
                input="""
    Midnight.Diner.Tokyo.Stories.S01E01.WEBRip.x264-ION10.mp4
    Midnight.Diner.Tokyo.Stories.S01E02.WEBRip.x264-ION10.mp4
    Midnight.Diner.Tokyo.Stories.S01E03.WEBRip.x264-ION10.mp4 
    """,
                output="""
                Midnight.Diner.Tokyo.Stories.S01E01.WEBRip.x264-ION10.mp4||Midnight Diner Tokyo Stories S01E01.mp4
    Midnight.Diner.Tokyo.Stories.S01E02.WEBRip.x264-ION10.mp4||Midnight Diner Tokyo Stories S01E02.mp4
    Midnight.Diner.Tokyo.Stories.S01E03.WEBRip.x264-ION10.mp4||Midnight Diner Tokyo Stories S01E03.mp4
                """
            )
        ],
        payload=", ".join([os.path.basename(video_file) for video_file in video_files])
    )


def build_clean_movie_names_in_dir_prompt(filenames):
    prompt = LLMPrompt(
        action="""
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
    """,
        examples=[
            LLMPromptExample(
                input="""
    2004 - Survive Style 5+.mkv||Survive Style 5+ (2004).mkv
    Akira (1988) 2160p HDR 5.1 Eng - Jpn x265 10bit Phun Psyz.mkv||Akira (1988).mkv
    Europa.Europa.1990.1080p.BluRay.x264-[YTS.LT].mp4||Europa Europa (1990).mp4
    Here are the file name(s) to clean up: 
    """,
                output="""
    2004 - Survive Style 5+.mkv||Survive Style 5+ (2004).mkv
    Akira (1988) 2160p HDR 5.1 Eng - Jpn x265 10bit Phun Psyz.mkv||Akira (1988).mkv
    Europa.Europa.1990.1080p.BluRay.x264-[YTS.LT].mp4||Europa Europa (1990).mp4
    Here are the file name(s) to clean up: 
    """,
            )
        ],
        payload=", ".join(filenames)
    )

    return prompt
