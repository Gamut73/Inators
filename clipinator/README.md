Clipinator is for getting a clip from a video file

# Usage

run ```clipinator.py -h```

# Arguments

- `input_file_path`: Path to the input video file you want to clip.
- `start_time`: Start time of the clip in format hh:mm:ss. Flexible input:
  - `10` = ten seconds
  - `00:10` = ten seconds  
  - `21:00` = twenty-one minutes
  - `00:21:00` = twenty-one minutes
- `end_time`: End time of the clip using the same format as start time.
- `clip_name`: Name of the output clip file. Supports grouping with `[Group]` syntax.

Optional arguments:
- `-o, --output_dir`: Custom output directory for saving clips. Default is `~/Videos/Clips`.
- `-s, --subtitles`: Path to a subtitle file (.srt) to add to the clip.
- `-es, --embedded_subtitles [index]`: Extract and use subtitles embedded in the video file. 
  Optional index specifies which subtitle track to use (default: 0).
- `-ea, --embedded_audio [index]`: Use a specific audio track from the video file.
  Optional index specifies which audio track to use (default: 0).
- `-f, --file`: Name of the CSV file containing multiple clip definitions to process in batch. The script will search for the filename in the `Timestamps` directory.
  The original CSV file will be moved to trash after successful processing.
- `-t, --template`: Generate a CSV template file with the given name in `~/Videos/Clips/Timestamps/`.
- `-ltf, --list_timestamp_files`: List all timestamp files' names in the `Timestamps` directory.
- `-h, --help`: Show help message and exit.

# Grouping clips

You can group clips by specify providing a **clip_name** in the form: ```'[Group0]...[GroupN]{clip_name}```'
Essentially everything surrounded by "[]" is a folder will be created so that your file will be saved at
```{clips_dir}/<Group0>/.../<GroupN>/{clip_name}.mp4```
It is optional, i.e not including an groups will save the file at ```{clips_dir}/{clip_name}.mp4```

# CSV file

Input can be provided in a csv file and ran with the ```-f``` flag. For example:
```clipinator /path/to/video -f <name-of-csv-file-in-Timestamps-folder>```
You can provide a csv file with the following format and headings:

```
start, end, title (Grouping rule still apply for each title exept all groups will have the same parent folder given by the csv filename)
```

and It will create a folder for the csv filename and save the clips(each row of the csv file) in that folder.
**Anything after an open parenthesis `(` will be ignored when the folder is created and is consider extra info for 
your benefit**

### Example

```clipinator ./"Peep Show S02E04.mp4" -f "Peep Show (S02E04)"```
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
