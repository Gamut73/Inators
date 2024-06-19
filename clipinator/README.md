Clipinator is for getting a clip from a video file

# Requirements
moviepy python lib

# Usage
run ```clipinator.py -h```

# Grouping clips
You can group clips by specify providing a **clip_name** in the form: ```'{group_name}_X__{clip_name}```'
Essentially everything before **'\_X__'** is the group name and a folder will be created so that your file will be saved at
```{output_dir}/{group_name}/{clip_name}.mp4```