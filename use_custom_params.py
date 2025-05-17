#!/usr/bin/env python3
import os
import argparse
from bottle_counter import BottleCounter

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
    parser = argparse.ArgumentParser(description="Use custom parameters for bottle counting")
    parser.add_argument("-p", "--params", default="bottle_counter_params.txt", 
                        help="Path to parameters file (default: bottle_counter_params.txt)")
    parser.add_argument("-i", "--image", help="Path to input image file")
    parser.add_argument("-v", "--video", help="Path to input video file")
    parser.add_argument("-c", "--camera", type=int, default=0, help="Camera device index (default: 0)")
    args = parser.parse_args()
    
    # Check if parameters file exists
    if not os.path.isfile(args.params):
        print(f"Error: Parameters file '{args.params}' not found. Run tune_params.py first.")
        return
    
    # Load parameters
    params = load_parameters(args.params)
    if params is None:
        return
    
    # Create counter with custom parameters
    counter = BottleCounter()
    
    # Update counter parameters
    counter.min_radius = params.get('min_radius', counter.min_radius)
    counter.max_radius = params.get('max_radius', counter.max_radius)
    counter.min_distance = params.get('min_distance', counter.min_distance)
    counter.param1 = params.get('param1', counter.param1)
    counter.param2 = params.get('param2', counter.param2)
    
    print(f"Using custom parameters: {params}")
    
    # Process input
    if args.image:
        counter.process_image(args.image)
    elif args.video:
        counter.process_video(args.video)
    else:
        counter.process_video(args.camera)

if __name__ == "__main__":
    main() 