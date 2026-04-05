import csv
import shlex

from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from util.logger import info
from substitles import parse_html_to_text, remove_empty_lines_at_and_of_subtitle_file
from file_util import build_clip_file_path
from string_util import convert_hms_timestamp_to_seconds
from constants import START_TIME_FIELD, END_TIME_FIELD, IGNORE_SUBS_FIELD, TITLE_FIELD


TMP_AUDIO_PATH = os.path.join(os.getcwd(), "tmp_audio.mp3")
DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Videos", "Clips")


def get_tmp_audio_path():
    return TMP_AUDIO_PATH


def get_default_output_dir():
    return DEFAULT_OUTPUT_DIR


def add_subtitles_to_clip(video_clip, subtitles_file, video_height):
    print("Subtitles file path: ", subtitles_file)
    txt_clip_generator = lambda txt: TextClip(
        parse_html_to_text(txt),
        font='Dejavu-Sans-Bold',
        fontsize=int(video_height * 0.06),
        color='white',
        method='caption',
        stroke_color='black',
        stroke_width=1,
        align='South',
        size=video_clip.size
    )

    remove_empty_lines_at_and_of_subtitle_file(subtitles_file)
    subtitle_clip = SubtitlesClip(subtitles_file, txt_clip_generator)
    return CompositeVideoClip((video_clip, subtitle_clip.set_position(('center', 'bottom'))), size=video_clip.size)


def clip_video(input_file_path, clip_name, start_time, end_time, output_dir, subtitles_filepath, audio_track_index):
    info(f"Clipping from {start_time} to {end_time} and saving it as {clip_name}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    og_vid_name = os.path.basename(input_file_path)
    clip_save_file_path = build_clip_file_path(clip_name, og_vid_name, output_dir)

    video_clip = VideoFileClip(input_file_path)
    if subtitles_filepath != '':
        video_clip = add_subtitles_to_clip(video_clip, subtitles_filepath, video_clip.size[1])

    if audio_track_index is not None:
        video_clip = set_alternative_audio_track(video_clip, input_file_path, audio_track_index)

    video_clip = video_clip.subclip(convert_hms_timestamp_to_seconds(start_time), convert_hms_timestamp_to_seconds(end_time))
    video_clip.write_videofile(clip_save_file_path)


def clip_multiple_clips_from_a_video(input_file_path, clips, clips_parent_folder_name, output_dir, subtitles_file_path,
                                     audio_track_index):
    clean_clips_parent_folder_name = clips_parent_folder_name.split('(')[0].strip()
    clips_parent_folder = os.path.join(output_dir, clean_clips_parent_folder_name)
    for clip in clips:
        subs_filepath = subtitles_file_path
        if 'ignore_subs' in clip and clip[IGNORE_SUBS_FIELD].lower() == 'y':
            info(f"Ignoring subtitles for clip {clip[TITLE_FIELD]}")
            subs_filepath = ''
        clip_video(input_file_path, clip[TITLE_FIELD], clip[START_TIME_FIELD], clip[END_TIME_FIELD],
                   clips_parent_folder, subs_filepath, audio_track_index)


def get_clips_from_csv_file(filepath):
    with open(filepath, 'r') as file:
        csv_reader = csv.DictReader(file)
        clips = []
        for row in csv_reader:
            clip = {
                START_TIME_FIELD: row[START_TIME_FIELD],
                END_TIME_FIELD: row[END_TIME_FIELD],
                TITLE_FIELD: row[TITLE_FIELD],
            }
            if IGNORE_SUBS_FIELD in row:
                clip[IGNORE_SUBS_FIELD] = row[IGNORE_SUBS_FIELD].strip()
            else:
                clip[IGNORE_SUBS_FIELD] = 'n'
            clips.append(clip)
    return clips


def set_alternative_audio_track(clip, video_filepath, audio_track_index):
    if not os.path.exists(TMP_AUDIO_PATH):
        os.system(f"ffmpeg -i {shlex.quote(video_filepath)} -map 0:a:{audio_track_index} -ab 160k -ac 2 -ar 44100 -vn -loglevel error {shlex.quote(TMP_AUDIO_PATH)}")

    audio_clip = AudioFileClip(TMP_AUDIO_PATH)
    info("Using alternative audio track with index " + str(audio_track_index))
    return clip.set_audio(audio_clip)
