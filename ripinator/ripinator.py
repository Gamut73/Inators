import argparse
import os
import sys
from enum import Enum

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.file_mover import move_subtitles, move_movie, remove_source_dir, is_video_file

class RipType(Enum):
    AUDIO = 1
    SUBTITLE = 2

def _get_subtitle_from_video(video_path, subtitle_path):
    os.system(f"ffmpeg -i {video_path} -map 0:s:0 {subtitle_path}")

def _get_audio_from_video(video_path, audio_path):
    os.system(f"ffmpeg -i {video_path} -ab 160k -ac 2 -ar 44100 -vn {audio_path}")


def main(file_path, rip_type):
        new_file = os.path.splitext(file_path)[0]
        if rip_type == RipType.AUDIO:
            new_file = new_file + "_audio.mp3"
            _get_audio_from_video(file_path, new_file)
        else:
            new_file = new_file +  "_subtitle.srt"
            _get_audio_from_video(file_path, new_file)
        
if __name__ == "__main__":
    rip_type = RipType.AUDIO

    parser = argparse.ArgumentParser(description='Turn video clips into audio clips')
    parser.add_argument('file_path', type=str, help='File path of the video')
    parser.add_argument('-a', '--audio', action='store_true', help='Rip audio from video (Default)')
    parser.add_argument('-s', '--subtitle', action='store_true', help='Rip subtitles from video')

    args = parser.parse_args()

    if args.subtitle:
        rip_type = RipType.SUBTITLE

    main(args.file_path, rip_type)
