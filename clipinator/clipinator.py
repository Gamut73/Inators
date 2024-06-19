from moviepy.editor import *
import argparse
import os

def clip_video(input_file_path, clip_name, start_time, end_time, output_dir):
    if os.path.exists(output_dir) == False:
        os.makedirs(output_dir)

    og_vid_name = os.path.basename(input_file_path)
    og_vid_name_without_ext = os.path.splitext(og_vid_name)[0]
    clip = VideoFileClip(input_file_path)
    clip = clip.subclip(_convert_time_to_seconds(start_time), _convert_time_to_seconds(end_time))
    clip.write_videofile(os.path.join(output_dir, clip_name + " (" + og_vid_name_without_ext + ").mp4"))
    
def _convert_time_to_seconds(time):
    while (time.count(":") != 2):
        time = "00:" + time
        
    time_split = time.split(":")
    return int(time_split[0])*3600 + int(time_split[1])*60 + int(time_split[2])    
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= 'Clip a video')
    parser.add_argument('input_file_path', help="Name of the input file")
    parser.add_argument('start_time', help="Start time of the clip in the format hh:mm:ss (e.g 10 is ten seconds, 00:10 is ten seconds, 21:00 is twenty one minutes, 00:21:00 is also twenty one minutes)")
    parser.add_argument('end_time', help="End time of the clip in the same format as start time")        
    parser.add_argument('clip_name', help="Name of the clip")
    parser.add_argument('-o', '--output_dir', default='~/Videos/Clips', help="Output directory. Creates a new directory if it doesn't exist. Default is the current directory")
    
    args = parser.parse_args()
    clip_video(args.input_file_path, args.clip_name, args.start_time, args.end_time, args.output_dir)