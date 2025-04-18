import argparse
import csv
import os.path
import re
import shlex

from bs4 import BeautifulSoup
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from send2trash import send2trash

TIMESTAMPS_FOLDER = 'Videos/Clips/Timestamps'
CSV_FILE_EDITOR = 'libreoffice'

TMP_AUDIO_PATH = os.path.join(os.getcwd(), "tmp_audio.mp3")
TMP_SUBTITLES_PATH = os.path.join(os.getcwd(), "tmp_subtitle.srt")


def clip_video(input_file_path, clip_name, start_time, end_time, output_dir, subtitles_filepath, audio_track_index):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    og_vid_name = os.path.basename(input_file_path)
    clip_save_file_path = _build_clip_file_path(clip_name, og_vid_name, output_dir)

    clip = VideoFileClip(input_file_path)
    if subtitles_filepath != '':
        clip = _add_subtitles(clip, subtitles_filepath, clip.size[1])

    if audio_track_index is not None and audio_track_index != 0:
        clip = _set_alternative_audio_track(clip, input_file_path, audio_track_index)

    clip = clip.subclip(_convert_time_to_seconds(start_time), _convert_time_to_seconds(end_time))
    clip.write_videofile(clip_save_file_path)


def clip_multiple_clips_from_a_video(input_file_path, clips, clips_parent_folder_name, output_dir, subtitles_file_path):
    clean_clips_parent_folder_name = clips_parent_folder_name.split('(')[0].strip()
    clips_parent_folder = os.path.join(output_dir, clean_clips_parent_folder_name)
    for clip in clips:
        clip_video(input_file_path, clip['title'], clip['start'], clip['end'], clips_parent_folder, subtitles_file_path)


def get_clips_from_csv_file(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        clips = []
        for row in csv_reader:
            clips.append({
                'start': row['start'],
                'end': row['end'],
                'title': row['title'],
            })
    return clips


def generate_clips_csv_file_template(filename):
    folder_path = _create_folders_in_home(TIMESTAMPS_FOLDER)
    file_path = os.path.join(folder_path, filename + '.csv')
    header = ['start', 'end', 'title']
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)

    _open_csv_editor(file_path)


def _set_alternative_audio_track(clip, video_filepath, audio_track_index):
    os.system(f"ffmpeg -i {shlex.quote(video_filepath)} -map 0:a:{audio_track_index} -ab 160k -ac 2 -ar 44100 -vn -loglevel error {shlex.quote(TMP_AUDIO_PATH)}")

    audio_clip = AudioFileClip(TMP_AUDIO_PATH)
    return clip.set_audio(audio_clip)

def _get_filename_from_path(file_path):
    file_name_with_extension = os.path.basename(file_path)
    return os.path.splitext(file_name_with_extension)[0]


def _parse_html_to_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()


def _add_subtitles(video_clip, subtitles_file_path, video_height):
    print("Subtitles file path: ", subtitles_file_path)
    generator = lambda txt: TextClip(
        _parse_html_to_text(txt),
        font='Dejavu-Sans-Bold',
        fontsize=int(video_height * 0.08),
        color='white',
        method='caption',
        stroke_color='black',
        stroke_width=1,
        align='South',
        size=video_clip.size
    )

    _remove_trailing_empty_lines(subtitles_file_path)
    subtitle_clip = SubtitlesClip(subtitles_file_path, generator)
    return CompositeVideoClip((video_clip, subtitle_clip.set_position(('center', 'bottom'))), size=video_clip.size)


def _remove_trailing_empty_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    while lines and lines[-1].strip() == '':
        lines.pop()

    with open(file_path, 'w') as file:
        file.writelines(lines)


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


def _get_subtitle_file_path(embedded_subtitles, subtitles):
    if embedded_subtitles is not None:
        video_path = args.input_file_path
        os.system(
            f"ffmpeg -i {shlex.quote(video_path)} -map 0:s:{embedded_subtitles}  -scodec subrip -loglevel error {shlex.quote(TMP_SUBTITLES_PATH)}")
        _remove_font_size_from_subtitle_file(TMP_SUBTITLES_PATH)
        return TMP_SUBTITLES_PATH
    return subtitles


if __name__ == "__main__":
    default_output_dir = os.path.join(os.path.expanduser("~"), "Videos", "Clips")

    parser = argparse.ArgumentParser(description='Clip a video')
    parser.add_argument('input_file_path', nargs='?', default='', help="Name of the input file")
    parser.add_argument('start_time', nargs='?',
                        default='',
                        help="Start time of the clip in the format hh:mm:ss (e.g 10 is ten seconds, 00:10 is ten seconds, 21:00 is twenty one minutes, 00:21:00 is also twenty one minutes)")
    parser.add_argument('end_time', nargs='?', default='', help="End time of the clip in the same format as start time")
    parser.add_argument('clip_name', nargs='?', default='', help="Name of the clip")

    parser.add_argument('-o', '--output_dir', default=default_output_dir,
                        help="Output directory. Creates a new directory if it doesn't exist. Default is the current directory")

    parser.add_argument('-s', '--subtitles', default='', help="Path to the subtitles file (.srt)")
    parser.add_argument('-es', '--embedded_subtitles', nargs='?', const=0, type=int,
                        help="Use subtitles embedded in the video file. Value is the index of the subtitle stream to "
                             "use (default is 0)")

    parser.add_argument('-ea', '--embedded_audio', nargs='?', const=0, type=int, help="Use audio embedded in the "
                                                                                      "video file. Value is the index "
                                                                                      "of the audio stream to use ("
                                                                                      "default is 0)")

    parser.add_argument('-f', '--file', help="CSV file path containing clip details")
    parser.add_argument('-t', '--template',
                        help="Value is the filename of a csv that will be generated with the template for the clips")

    args = parser.parse_args()

    subtitles_file_path = _get_subtitle_file_path(args.embedded_subtitles, args.subtitles)
    if args.file:
        clip_multiple_clips_from_a_video(
            args.input_file_path,
            get_clips_from_csv_file(args.file),
            os.path.basename(args.file).split('.')[0],
            args.output_dir,
            subtitles_file_path
        )
        try:
            send2trash(args.file)
            print(f"Moved {args.file} to trash")
        except Exception as e:
            print(f"Failed to move {args.file} to trash: because\n\t {e}")
    elif args.template:
        generate_clips_csv_file_template(args.template)
    else:
        clip_video(args.input_file_path, args.clip_name, args.start_time, args.end_time, args.output_dir,
                   subtitles_file_path, args.embedded_audio)

    if os.path.exists(TMP_SUBTITLES_PATH):
        try:
            os.remove(TMP_SUBTITLES_PATH)
        except Exception as e:
            print(f"!!!Failed to remove temporary subtitle file: because\n\t {e}!!!")
            print(f"!!!Temporary subtitle file is located at {TMP_SUBTITLES_PATH}!!!")

    if os.path.exists(TMP_AUDIO_PATH):
        try:
            os.remove(TMP_AUDIO_PATH)
        except Exception as e:
            print(f"!!!Failed to remove temporary subtitle file: because\n\t {e}!!!")
            print(f"!!!Temporary subtitle file is located at {TMP_AUDIO_PATH}!!!")
