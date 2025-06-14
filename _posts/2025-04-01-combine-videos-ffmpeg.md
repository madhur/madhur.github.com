---
layout: blog-post
title: "Combine videos using ffmpeg"
excerpt: "Combine videos using ffmpeg"
disqus_id: /2025/04/01/combine-videos-using-ffmpeg/
tags:
    - ffmpeg
---

I wanted to combine videos using the tool. I had two videos in 9x16 format and wanted to combine side by side.

With a little bit of trial and error, I was able to achieve this using [ffmpeg](https://ffmpeg.org/)

The exact command is 

```
ffmpeg -i video1.mp4 -i video2.mp4 -filter_complex "[0:v]scale=540:960:force_original_aspect_ratio=decrease,pad=540:960:(ow-iw)/2:(oh-ih)/2[v0];[1:v]scale=540:960:force_original_aspect_ratio=decrease,pad=540:960:(ow-iw)/2:(oh-ih)/2[v1];[v0][v1]hstack=inputs=2[v]" -map "[v]" -map 0:a -c:v libx264 -c:a aac output.mp4
```

## Breaking Down the Command

Let's understand what each part of this complex command does:

### Input Files
```bash
-i video1.mp4 -i video2.mp4
```
This specifies our two input videos. FFmpeg will reference them as `[0]` and `[1]` respectively.

### Filter Chain Explanation

The `-filter_complex` parameter contains several operations:

**1. Scale and Pad First Video:**
```bash
[0:v]scale=540:960:force_original_aspect_ratio=decrease,pad=540:960:(ow-iw)/2:(oh-ih)/2[v0]
```
- `scale=540:960`: Resize to 540x960 pixels
- `force_original_aspect_ratio=decrease`: Maintain aspect ratio, making the video smaller if needed
- `pad=540:960:(ow-iw)/2:(oh-ih)/2`: Add padding to center the video in a 540x960 frame
- `[v0]`: Label this processed video as "v0"

**2. Scale and Pad Second Video:**
```bash
[1:v]scale=540:960:force_original_aspect_ratio=decrease,pad=540:960:(ow-iw)/2:(oh-ih)/2[v1]
```
Same process for the second video, labeled as "v1".

**3. Horizontal Stack:**
```bash
[v0][v1]hstack=inputs=2[v]
```
- `hstack`: Horizontally stack the two processed videos
- `inputs=2`: Specify we're combining 2 video streams
- `[v]`: Label the final combined video

### Output Mapping and Encoding
```bash
-map "[v]" -map 0:a -c:v libx264 -c:a aac output.mp4
```
- `-map "[v]"`: Use our combined video stream
- `-map 0:a`: Use audio from the first video
- `-c:v libx264`: Encode video using H.264 codec
- `-c:a aac`: Encode audio using AAC codec


Its great that in Linux even without tools such as Adobe Premiere Pro, you can achieve so much.


