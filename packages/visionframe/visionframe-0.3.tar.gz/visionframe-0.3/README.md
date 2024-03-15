# visionframe

visionframe is a Python package that simplifies the process of extracting frames from videos using OpenCV and supervision.

## Installation

You can install visionframe using pip:

```bash
pip install visionframe
```

## Usage

To extract frames from videos, simply import the FrameExtractor class from visionframe and create an instance with the desired parameters. Then, call the extract_frames() method:

```python
from visionframe import FrameExtractor

VIDEO_DIR_PATH = "/path/to/videos"
IMAGE_DIR_PATH = "/path/to/images"
FRAME_STRIDE = 1

frame_extractor = FrameExtractor(video_dir_path=VIDEO_DIR_PATH, image_dir_path=IMAGE_DIR_PATH, frame_stride=FRAME_STRIDE)
frame_extractor.extract_frames()
```

Replace VIDEO_DIR_PATH with the directory path where your videos are located, IMAGE_DIR_PATH with the directory path where you want to save the extracted frames, and adjust FRAME_STRIDE as needed
