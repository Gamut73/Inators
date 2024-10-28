Clipinator is for getting a clip from a video file

# Requirements
moviepy python lib

# Usage
run ```clipinator.py -h```

# Grouping clips
You can group clips by specify providing a **clip_name** in the form: ```'[Group0]...[GroupN]{clip_name}```'
Essentially everything surrounded by "[]" is a folder will be created so that your file will be saved at
```{output_dir}/<Group0>/.../<GroupN>/{clip_name}.mp4```
Not including an groups will save the file at ```{output_dir}/{clip_name}.mp4```

# CSV file
You can provide a csv file with the following format and headings:
```
start_time, end_time, clip_title (Grouping rule still apply)
```
and It will create a folder for the filename of the filepath you provided and save the clips(each row of the csv file) in that folder