import argparse
import os

def _get_audio_from_video(video_path, audio_path):
    os.system(f"ffmpeg -i {video_path} -ab 160k -ac 2 -ar 44100 -vn {audio_path}")
    
def _get_list_of_videos(dir):
    videos = []
    for filename in os.listdir(dir):
        if filename.endswith((".mp4", ".mkv", ".avi")):
            videos.append(filename)
    return videos    

def _create_audio_clip_folder(dir):
    audio_dir = os.path.join(dir, "audio")
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

def main(dir):
    _create_audio_clip_folder(dir)
    videos = _get_list_of_videos(dir)
    
    for video in videos:
        print(f"Converting {video} to audio")
        video_path = os.path.join(dir, video)
        audio_path = os.path.join(dir, "audio", video.replace("mp4", "mp3"))
        _get_audio_from_video(video_path, audio_path)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Turn video clips into audio clips')
    parser.add_argument('dir', type=str, help='Directory containing videos')

    args = parser.parse_args()
    main(args.dir)