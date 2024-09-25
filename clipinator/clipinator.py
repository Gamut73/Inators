import argparse
import re

from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

def clip_video(input_file_path, clip_name, start_time, end_time, output_dir, subtitles_file_path):
    if os.path.exists(output_dir) == False:
        os.makedirs(output_dir)

    og_vid_name = os.path.basename(input_file_path)
    clip_save_file_path = _build_clip_file_path(clip_name, og_vid_name, output_dir)

    clip = VideoFileClip(input_file_path)
    if subtitles_file_path != '':
        clip = _add_subtitiles(clip, subtitles_file_path)

    clip = clip.subclip(_convert_time_to_seconds(start_time), _convert_time_to_seconds(end_time))
    clip.write_videofile(clip_save_file_path)


def _add_subtitiles(video_clip, subtitles_file_path):
    generator = lambda txt: TextClip(
        txt,
        font='Dejavu-Sans-Bold',
        fontsize=72,
        color='white',
        method='caption',
        stroke_color='black',
        stroke_width=2,
        align='South',
        size=video_clip.size
    )

    subtitle_clip = SubtitlesClip(subtitles_file_path, generator)
    return CompositeVideoClip((video_clip, subtitle_clip.set_position(('center', 'bottom'))), size=video_clip.size)



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
    # Find all substrings within square brackets
    substrings = re.findall(r'\[(.*?)\]', input_string)

    # Remove all substrings within square brackets from the input string
    cleaned_string = re.sub(r'\[.*?\]', '', input_string)

    # Append the cleaned string to the list of substrings
    substrings.append(cleaned_string)

    return substrings

def _convert_time_to_seconds(time):
    while (time.count(":") != 2):
        time = "00:" + time

    time_split = time.split(":")
    return int(time_split[0]) * 3600 + int(time_split[1]) * 60 + int(time_split[2])


if __name__ == "__main__":
    default_output_dir = os.path.join(os.path.expanduser("~"), "Videos", "Clips")

    parser = argparse.ArgumentParser(description='Clip a video')
    parser.add_argument('input_file_path', help="Name of the input file")
    parser.add_argument('start_time',
                        help="Start time of the clip in the format hh:mm:ss (e.g 10 is ten seconds, 00:10 is ten seconds, 21:00 is twenty one minutes, 00:21:00 is also twenty one minutes)")
    parser.add_argument('end_time', help="End time of the clip in the same format as start time")
    parser.add_argument('clip_name', help="Name of the clip")
    parser.add_argument('-o', '--output_dir', default=default_output_dir,
                        help="Output directory. Creates a new directory if it doesn't exist. Default is the current directory")
    parser.add_argument('-s', '--subtitles', default='', help="Path to the subtitles file (.srt)")

    args = parser.parse_args()
    clip_video(args.input_file_path, args.clip_name, args.start_time, args.end_time, args.output_dir, args.subtitles)
