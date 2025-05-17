#!/usr/bin/env python3
import cv2
import numpy as np
import os
import argparse
from bottle_counter import BottleCounter

def process_video_and_save(input_video, output_video, min_radius=15, max_radius=60, min_distance=20, param1=30, param2=30):
    """Process a video and save the results with bottle detection"""
    # Create bottle counter with custom parameters
    counter = BottleCounter()
    counter.min_radius = min_radius
    counter.max_radius = max_radius
    counter.min_distance = min_distance
    counter.param1 = param1
    counter.param2 = param2
    
    # Open input video
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print(f"Error: Could not open video {input_video}")
        return False
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Video properties: {width}x{height}, {fps} fps, {total_frames} frames")
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    frame_count = 0
    max_bottles = 0
    
    # Process video
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Process frame
        result, bottle_count = counter.process_frame(frame)
        if bottle_count > max_bottles:
            max_bottles = bottle_count
            
        # Add frame number
        frame_count += 1
        text = f"Frame: {frame_count}/{total_frames}"
        cv2.putText(result, text, (20, height - 20), counter.font, counter.font_scale, (255, 255, 255), counter.thickness)
        
        # Write frame to output video
        out.write(result)
        
        # Display progress
        if frame_count % 10 == 0:
            print(f"Processing: {frame_count}/{total_frames} frames ({frame_count/total_frames*100:.1f}%)")
    
    # Clean up
    cap.release()
    out.release()
    
    print(f"Processing complete. Maximum bottles detected: {max_bottles}")
    print(f"Result saved to {output_video}")
    return True

def load_parameters(params_file):
    """Load parameters from a file"""
    params = {}
    try:
        with open(params_file, 'r') as f:
            for line in f:
                key, value = line.strip().split(' = ')
                params[key] = int(value)
        return params
    except Exception as e:
        print(f"Error loading parameters: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Process video with bottle detection and save results")
    parser.add_argument("-i", "--input", required=True, help="Path to input video file")
    parser.add_argument("-o", "--output", default="result.mp4", help="Path to output video file")
    parser.add_argument("-p", "--params", help="Path to parameters file (optional)")
    args = parser.parse_args()
    
    # Check if parameters file exists
    if args.params and os.path.isfile(args.params):
        # Load parameters
        params = load_parameters(args.params)
        if params:
            print(f"Using custom parameters: {params}")
            process_video_and_save(
                args.input, 
                args.output,
                min_radius=params.get('min_radius', 15),
                max_radius=params.get('max_radius', 60),
                min_distance=params.get('min_distance', 20),
                param1=params.get('param1', 30),
                param2=params.get('param2', 30)
            )
    else:
        # Use default parameters
        print("Using default parameters")
        process_video_and_save(args.input, args.output)

if __name__ == "__main__":
    main() 