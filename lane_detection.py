import os
import cv2
import numpy as np
from moviepy.editor import VideoFileClip

# 1. HSL Color Selection
def HSL_color_selection(image):
    hls_image = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
    white_mask = cv2.inRange(hls_image, np.uint8([0, 200, 0]), np.uint8([255, 255, 255]))
    yellow_mask = cv2.inRange(hls_image, np.uint8([10, 0, 100]), np.uint8([40, 255, 255]))
    combined_mask = cv2.bitwise_or(white_mask, yellow_mask)
    return cv2.bitwise_and(image, image, mask=combined_mask)

# 2. Canny Edge Detection
def canny_detector(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    return cv2.Canny(blur, 50, 150)

# 3. Region of Interest
def region_selection(image):
    mask = np.zeros_like(image)
    height, width = image.shape[:2]
    polygon = np.array([[ (width * 0.1, height * 0.95), (width * 0.4, height * 0.6), 
                          (width * 0.6, height * 0.6), (width * 0.9, height * 0.95) ]], dtype=np.int32)
    cv2.fillPoly(mask, polygon, 255)
    return cv2.bitwise_and(image, mask)

# 4. Averaging and Drawing Lane Lines
def draw_lane_lines(image, lines, color=[255, 0, 0], thickness=10):
    line_image = np.zeros_like(image)
    left_line, right_line = [], []

    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1
            if slope < 0: left_line.append((slope, intercept))
            else: right_line.append((slope, intercept))
    
    def make_line(y1, y2, line_data):
        slope, intercept = np.mean(line_data, axis=0)
        x1, x2 = int((y1 - intercept) / slope), int((y2 - intercept) / slope)
        return (x1, y1), (x2, y2)
    
    y1, y2 = image.shape[0], int(image.shape[0] * 0.6)
    if left_line: cv2.line(line_image, *make_line(y1, y2, left_line), color, thickness)
    if right_line: cv2.line(line_image, *make_line(y1, y2, right_line), color, thickness)
    
    return cv2.addWeighted(image, 1.0, line_image, 1.0, 0.0)

# 5. Frame Processing
def frame_processor(image):
    color_select = HSL_color_selection(image)
    edges = canny_detector(color_select)
    region = region_selection(edges)
    lines = cv2.HoughLinesP(region, 1, np.pi / 180, threshold=20, minLineLength=20, maxLineGap=300)
    if lines is not None:
        return draw_lane_lines(image, lines)
    return image

# 6. Process Video
def process_video(input_path, output_path):
    input_video = VideoFileClip(input_path)
    processed = input_video.fl_image(frame_processor)
    processed.write_videofile(output_path, audio=False)

# Run the Code
if __name__ == "__main__":
    video_files = ["challenge.mp4", "solidWhiteRight.mp4", "solidYellowLeft.mp4"]
    input_folder, output_folder = "test_videos", "output_videos"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for video in video_files:
        input_path = os.path.join(input_folder, video)
        output_path = os.path.join(output_folder, f"output_{video}")
        print(f"Processing {video}...")
        process_video(input_path, output_path)
        print(f"Processed {video} saved as {output_path}")
