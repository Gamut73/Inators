import re


def extract_text_from_parenthesis(input_string):
    if not input_string:
        return []
    return [match.strip() for match in re.findall(r'\(([^()]*)\)', input_string)]


def filepath_to_list(input_string):
    substrings = re.findall(r'\[(.*?)\]', input_string)
    cleaned_string = re.sub(r'\[.*?\]', '', input_string)
    substrings.append(cleaned_string)

    return substrings


def convert_hms_timestamp_to_seconds(time):
    while time.count(":") != 2:
        time = "00:" + time

    time_split = time.split(":")
    return int(time_split[0]) * 3600 + int(time_split[1]) * 60 + int(time_split[2])