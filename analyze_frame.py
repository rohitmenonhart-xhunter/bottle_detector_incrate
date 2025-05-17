#!/usr/bin/env python3
import cv2
import numpy as np
import argparse
import os
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

def analyze_frame(image_path, params_file=None, output_path=None):
    """Analyze a single frame with tuned parameters"""
    # Read image
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Error: Could not read image {image_path}")
        return
    
    # Create bottle counter
    counter = BottleCounter()
    
    # Load parameters if file is provided
    if params_file and os.path.isfile(params_file):
        params = load_parameters(params_file)
        if params:
            print(f"Using custom parameters: {params}")
            counter.min_radius = params.get('min_radius', counter.min_radius)
            counter.max_radius = params.get('max_radius', counter.max_radius)
            counter.min_distance = params.get('min_distance', counter.min_distance)
            counter.param1 = params.get('param1', counter.param1)
            counter.param2 = params.get('param2', counter.param2)
    
    # Process frame with both methods separately to compare
    # Hough Circles method
    bottles_hough = counter.detect_bottles_hough(frame)
    result_hough = frame.copy()
    for (x, y, r) in bottles_hough:
        cv2.circle(result_hough, (x, y), r, (0, 255, 0), 2)
        cv2.circle(result_hough, (x, y), 2, (0, 0, 255), 3)
    text_hough = f"Bottles (Hough): {len(bottles_hough)}"
    cv2.putText(result_hough, text_hough, (20, 40), counter.font, counter.font_scale, (0, 255, 0), counter.thickness)
    
    # Contour method
    bottles_contour = counter.detect_bottles_contour(frame)
    result_contour = frame.copy()
    for (x, y, r) in bottles_contour:
        cv2.circle(result_contour, (x, y), r, (255, 0, 0), 2)
        cv2.circle(result_contour, (x, y), 2, (0, 0, 255), 3)
    text_contour = f"Bottles (Contour): {len(bottles_contour)}"
    cv2.putText(result_contour, text_contour, (20, 40), counter.font, counter.font_scale, (255, 0, 0), counter.thickness)
    
    # Combined method (choosing the best)
    bottles = bottles_hough if len(bottles_hough) > len(bottles_contour) else bottles_contour
    result = frame.copy()
    for (x, y, r) in bottles:
        cv2.circle(result, (x, y), r, counter.circle_color, 2)
        cv2.circle(result, (x, y), 2, (0, 0, 255), 3)
    text = f"Bottles (Combined): {len(bottles)}"
    cv2.putText(result, text, (20, 40), counter.font, counter.font_scale, counter.text_color, counter.thickness)
    
    # Create a combined visualization
    h, w = frame.shape[:2]
    combined = np.zeros((h*2, w*2, 3), dtype=np.uint8)
    combined[0:h, 0:w] = frame  # Original in top-left
    combined[0:h, w:w*2] = result_hough  # Hough in top-right
    combined[h:h*2, 0:w] = result_contour  # Contour in bottom-left
    combined[h:h*2, w:w*2] = result  # Combined in bottom-right
    
    # Add labels
    cv2.putText(combined, "Original", (20, 30), counter.font, counter.font_scale, (255, 255, 255), counter.thickness)
    cv2.putText(combined, text_hough, (w+20, 30), counter.font, counter.font_scale, (0, 255, 0), counter.thickness)
    cv2.putText(combined, text_contour, (20, h+30), counter.font, counter.font_scale, (255, 0, 0), counter.thickness)
    cv2.putText(combined, text, (w+20, h+30), counter.font, counter.font_scale, counter.text_color, counter.thickness)
    
    # Save result if output path is provided
    if output_path:
        cv2.imwrite(output_path, combined)
        print(f"Analysis saved to {output_path}")
    
    # Display result
    cv2.namedWindow('Bottle Analysis', cv2.WINDOW_NORMAL)
    cv2.imshow('Bottle Analysis', combined)
    print("Press any key to exit")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description="Analyze a single frame with tuned parameters")
    parser.add_argument("-i", "--image", required=True, help="Path to input image file")
    parser.add_argument("-p", "--params", default="bottle_counter_params.txt", help="Path to parameters file")
    parser.add_argument("-o", "--output", help="Path to output image file (optional)")
    args = parser.parse_args()
    
    analyze_frame(args.image, args.params, args.output)

if __name__ == "__main__":
    main() 