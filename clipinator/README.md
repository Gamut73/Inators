Clipinator is for getting a clip from a video file

# Usage
run ```clipinator.py -h```

# Grouping clips
You can group clips by specify providing a **clip_name** in the form: ```'[Group0]...[GroupN]{clip_name}```'
Essentially everything surrounded by "[]" is a folder will be created so that your file will be saved at
```{output_dir}/<Group0>/.../<GroupN>/{clip_name}.mp4```
Not including an groups will save the file at ```{output_dir}/{clip_name}.mp4```

# CSV file
Input can be provided in a csv file and ran with the ```-f``` flag. For example:
```clipinator /path/to/video -f /path/to/csv/file.csv```
You can provide a csv file with the following format and headings:
```
start_time, end_time, clip_title (Grouping rule still apply)
```
and It will create a folder for the csv filename and save the clips(each row of the csv file) in that folder. The groupings above 1will still apply.

# Requirements
See requirements.txt
```