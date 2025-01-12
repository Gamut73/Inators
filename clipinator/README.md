Clipinator is for getting a clip from a video file

# Usage

run ```clipinator.py -h```

# Grouping clips

You can group clips by specify providing a **clip_name** in the form: ```'[Group0]...[GroupN]{clip_name}```'
Essentially everything surrounded by "[]" is a folder will be created so that your file will be saved at
```{clips_dir}/<Group0>/.../<GroupN>/{clip_name}.mp4```
It is optional, i.e not including an groups will save the file at ```{clips_dir}/{clip_name}.mp4```

# CSV file

Input can be provided in a csv file and ran with the ```-f``` flag. For example:
```clipinator /path/to/video -f /path/to/csv/file.csv```
You can provide a csv file with the following format and headings:

```
start, end, title (Grouping rule still apply for each title exept all groups will have the same parent folder given by the csv filename)
```

and It will create a folder for the csv filename and save the clips(each row of the csv file) in that folder.
**Anything after an open parenthesis `(` will be ignored when the folder is created and is consider extra info for 
your benefit**

### Example

```clipinator ./"Peep Show S02E04.mp4" -f "Peep Show (S02E04).csv"```
will create a folder called `{clips_dir}/Peep Show` and save the clips in that folder

# Template

You can generate a template csv file in the format of the above csv file by running:
```clipinator -t <csv-file-name>```

- This will generate a csv file with the headings: `start`, `end`, `title`
- If the name has spaces wrap it in double quotes to avoid weirdness in the terminal

### Example

```clipinator -t "Peep Show [S01E04]"``` will create and open the file ```{clips_dir}/Timestamps/Peep Show [S01E04].csv```


# Subtitles
You can either provide a subtitle file with the ```-s``` flag and a .srt file as the value or use ```-es``` if the 
video has an embedded subtitle file that can be used.

# Requirements

See requirements.txt
