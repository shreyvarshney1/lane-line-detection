# Lane Detection in Videos

This project is a lane detection system that processes video frames to detect lane lines using OpenCV and MoviePy. It applies color selection, edge detection, region masking, and Hough Transform to detect lanes on roads. The output is a video with highlighted lane lines.

## Features

- Detects lane lines in videos with common road lane colors (white and yellow).
- Processes each frame to detect lane edges and highlights lanes using line averaging.
- Efficiently applies Hough Transform to detect lane lines.
- Exports processed videos with lane lines overlaid.

## Installation

### Prerequisites

1. **Python 3.x**
2. **Required Libraries**: Install the dependencies using `pip`:
   ```bash
   pip install opencv-python-headless moviepy numpy
   ```

### Project Structure
- `test_videos/`: Folder containing input videos.
- `output_videos/`: Folder where processed videos are saved.
- `lane_detection.py`: The main script that processes the videos.

## Usage

1. **Place Videos**:
   - Add your video files (e.g., `challenge.mp4`, `solidWhiteRight.mp4`, `solidYellowLeft.mp4`) in the `test_videos` folder.

2. **Run the Script**:
   - Run the main Python file to process the videos:
   ```bash
   python lane_detection.py
   ```

3. **View Output**:
   - Processed videos with lane lines will be saved in the `output_videos` folder, with filenames prefixed by `output_`.

## Code Explanation

The core functionality is split across six main parts:

1. **HSL Color Selection**:
   - Selects white and yellow colors using HSL color space masking to focus on lane colors.

2. **Canny Edge Detection**:
   - Converts the image to grayscale, applies Gaussian blur to reduce noise, and uses Canny edge detection to highlight edges.

3. **Region of Interest Selection**:
   - Masks the region of interest (a trapezoidal area) where lanes are typically located on the road.

4. **Averaging and Drawing Lane Lines**:
   - Averages detected lines on the left and right to create smooth lane lines. Draws the lane lines on a blank image.

5. **Frame Processing**:
   - Combines color selection, edge detection, region masking, and line detection for each frame.

6. **Video Processing**:
   - Processes the input video frame by frame and exports the final video with lane lines highlighted.

## Example

To process a video called `challenge.mp4`, ensure it’s in the `test_videos` folder, then run the script. The output will be saved in `output_videos/output_challenge.mp4`.

## License

This project is licensed under the MIT License. See `LICENSE` for more details.
