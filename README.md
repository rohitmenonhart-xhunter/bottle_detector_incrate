# Bottle Counter

A Python application that detects and counts bottles in a crate using computer vision techniques in real-time.

## Setup

1. Create and activate the virtual environment:
   ```
   # Create virtual environment
   python -m venv venv
   
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install opencv-python numpy imutils pillow
   ```

   Or using the requirements file:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Main Application

To run the main bottle detection application:

```
python bottle_counter.py [options]
```

Options:
- `-i, --image PATH`: Path to input image file
- `-v, --video PATH`: Path to input video file
- `-c, --camera INDEX`: Camera device index (default: 0)

Examples:
```
# Use webcam
python bottle_counter.py

# Use image file
python bottle_counter.py -i bottle_frame.jpg

# Use video file
python bottle_counter.py -v download.mp4
```

### Parameter Tuning

To fine-tune detection parameters using an image:

```
python tune_params.py -i IMAGE_PATH
```

This opens an interactive window with sliders to adjust parameters:
- Min Radius: Minimum radius of bottles to detect
- Max Radius: Maximum radius of bottles to detect
- Min Distance: Minimum distance between bottle centers
- Param1: Canny edge detector higher threshold
- Param2: Accumulator threshold for the Hough transform
- Method: Detection method (0: Hough, 1: Contour, 2: Both)

Controls:
- Press 's' to save parameters to a file (`bottle_counter_params.txt`)
- Press 'q' to quit

Example:
```
python tune_params.py -i bottle_frame.jpg
```

### Using Custom Parameters

To use previously saved parameters for detection:

```
python use_custom_params.py [options]
```

Options:
- `-p, --params PATH`: Path to parameters file (default: bottle_counter_params.txt)
- `-i, --image PATH`: Path to input image file
- `-v, --video PATH`: Path to input video file
- `-c, --camera INDEX`: Camera device index (default: 0)

Example:
```
python use_custom_params.py -v download.mp4 -p bottle_counter_params.txt
```

### Video Processing and Saving

To process a video and save the detection results to a new video file:

```
python save_results.py -i INPUT_VIDEO -o OUTPUT_VIDEO [-p PARAMS_FILE]
```

This processes the entire video file and saves the output with bottle detection visualized.

Example:
```
python save_results.py -i download.mp4 -o bottle_detection_result.mp4 -p bottle_counter_params.txt
```

### Frame Extraction

To extract a frame from a video file:

```
python extract_frame.py -v VIDEO_PATH [-o OUTPUT_PATH] [-f FRAME_NUMBER]
```

This is useful for extracting specific frames from video for parameter tuning or analysis.

Example:
```
python extract_frame.py -v download.mp4 -o bottle_frame.jpg -f 10
```

### Frame Analysis

To analyze a single frame with detailed visualization:

```
python analyze_frame.py -i IMAGE_PATH [-p PARAMS_FILE] [-o OUTPUT_PATH]
```

This creates a detailed visualization comparing the results of different detection methods:
- Top-left: Original image
- Top-right: Hough circle detection
- Bottom-left: Contour detection
- Bottom-right: Combined (best method) detection

Example:
```
python analyze_frame.py -i bottle_frame.jpg -p bottle_counter_params.txt -o bottle_analysis.jpg
```

## Sample Results

### Before Processing (Original Video)
The input video (`download.mp4`) contains a crate of bottles viewed from above:
![Original Video](https://github.com/rohitmenonhart-xhunter/bottle_detector_incrate/raw/main/download.mp4)

### After Processing (Detection Results)
The output video (`bottle_detection_result.mp4`) shows the bottles detected and counted in real-time:
![Processed Video with Detection](https://github.com/rohitmenonhart-xhunter/bottle_detector_incrate/raw/main/bottle_detection_result.mp4)

Our application detected a maximum of 28 bottles in the crate.

## Detection Methods

The application uses two detection methods:

1. **Hough Circle Transform**: Detects circular patterns in the image using OpenCV's `HoughCircles` function. Works well for clear, circular bottle caps.

2. **Contour Detection**: Detects bottle shapes based on contour analysis. This analyzes shapes in the image and filters based on size and circularity. Works well when bottles have distinct edges.

The application automatically selects the method that provides more detections for best results.

## Parameters

The main parameters for tuning:

- `min_radius`: Minimum radius of bottles (default: 15)
- `max_radius`: Maximum radius of bottles (default: 60)
- `min_distance`: Minimum distance between bottles (default: 20)
- `param1`: Canny edge detector threshold (default: 30)
- `param2`: Accumulator threshold (default: 30)

## Workflow Example

1. Extract a frame from your video:
   ```
   python extract_frame.py -v your_video.mp4 -o frame.jpg
   ```

2. Tune parameters using the extracted frame:
   ```
   python tune_params.py -i frame.jpg
   ```
   (Adjust parameters and press 's' to save)

3. Process the video with tuned parameters:
   ```
   python save_results.py -i your_video.mp4 -o result.mp4 -p bottle_counter_params.txt
   ```

4. Analyze a specific frame in detail:
   ```
   python analyze_frame.py -i frame.jpg -p bottle_counter_params.txt -o analysis.jpg
   ``` 