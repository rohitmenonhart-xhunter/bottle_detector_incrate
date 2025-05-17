#!/usr/bin/env python3
import cv2
import argparse

def extract_frame(video_path, output_path="frame.jpg", frame_number=0):
    """Extract a frame from a video file"""
    # Open video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return False
    
    # Get total frame count
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames in video: {total_frames}")
    
    if frame_number >= total_frames:
        frame_number = total_frames // 2  # Use middle frame if requested frame is out of range
        print(f"Frame number out of range, using middle frame: {frame_number}")
    
    # Set position to requested frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    # Read frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame")
        cap.release()
        return False
    
    # Save frame
    cv2.imwrite(output_path, frame)
    print(f"Frame saved to {output_path}")
    
    # Clean up
    cap.release()
    return True

def main():
    parser = argparse.ArgumentParser(description="Extract a frame from a video file")
    parser.add_argument("-v", "--video", required=True, help="Path to input video file")
    parser.add_argument("-o", "--output", default="frame.jpg", help="Path to output image file")
    parser.add_argument("-f", "--frame", type=int, default=0, help="Frame number to extract (default: 0)")
    args = parser.parse_args()
    
    extract_frame(args.video, args.output, args.frame)

if __name__ == "__main__":
    main() 