import re
from ..infrastructure.llm_service import LLMService, Example, GenapiLlmService

def clean_movie_name(filename):
    """
    This function cleans up a movie filename to remove extra strings so that it leaves in the format:
        "Movie Title (Year).ext"

    Args:
        filename: The filename of the movie.

    Returns:
        The cleaned filename.
    """

    cleaned_name = _remove_resolutions(filename)
    
    match = re.search(r"\d{4}", cleaned_name)
    if match:
        year = match.group()
        cleaned_name = f"{cleaned_name} ({year})"
    
    # Remove everything after the first year in parentheses
    cleaned_name = re.sub(r"\(\d+\)(.*)", "", filename)
    # Remove everything after a dot followed by a number (e.g., ".1080p")
    cleaned_name = re.sub(r"\.\d+", "", cleaned_name)
    # Remove everything inside square brackets
    cleaned_name = re.sub(r"\[.*?\]", "", cleaned_name)
    # Remove extra spaces
    cleaned_name = cleaned_name.strip()
    # Put the year in parentheses at the end, if it exists
    match = re.search(r"\d{4}", cleaned_name)
    if match:
        year = match.group()
        cleaned_name = f"{cleaned_name} ({year})"
    # Add extension back on
    return f"{cleaned_name}.{filename.split('.')[-1]}"

def _remove_resolutions(filename):
    return re.sub(r"\d+p", "", filename)


llmService: LLMService = GenapiLlmService()

# filenames = [
#     "2004 - Survive Style 5+.mkv",
#     "Akira (1988) 2160p HDR 5.1 Eng - Jpn x265 10bit Phun Psyz.mkv",
#     "Europa.Europa.1990.1080p.BluRay.x264-[YTS.LT].mp4",
#     "Gatto Nero, Gatto Bianco (1998) ITA sub ENG 1080p by PanzerB.mkv"
# ]

# for filename in filenames:
#     cleaned_filename = clean_movie_name(filename)
#     print(f"{filename} ||| {cleaned_filename}")