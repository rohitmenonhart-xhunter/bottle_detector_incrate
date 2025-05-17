#!/usr/bin/env python3
import cv2
import numpy as np
import argparse
import os

def create_trackbars(window_name):
    """Create trackbars for parameter tuning"""
    cv2.createTrackbar('Min Radius', window_name, 15, 100, lambda x: None)
    cv2.createTrackbar('Max Radius', window_name, 60, 150, lambda x: None)
    cv2.createTrackbar('Min Distance', window_name, 20, 100, lambda x: None)
    cv2.createTrackbar('Param1', window_name, 30, 300, lambda x: None)
    cv2.createTrackbar('Param2', window_name, 30, 100, lambda x: None)
    cv2.createTrackbar('Method', window_name, 0, 2, lambda x: None)  # 0: Hough, 1: Contour, 2: Both

def get_trackbar_values(window_name):
    """Get current trackbar values"""
    min_radius = cv2.getTrackbarPos('Min Radius', window_name)
    max_radius = cv2.getTrackbarPos('Max Radius', window_name)
    min_distance = cv2.getTrackbarPos('Min Distance', window_name)
    param1 = cv2.getTrackbarPos('Param1', window_name)
    param2 = cv2.getTrackbarPos('Param2', window_name)
    method = cv2.getTrackbarPos('Method', window_name)
    
    return min_radius, max_radius, min_distance, param1, param2, method

def detect_bottles_hough(frame, min_radius, max_radius, min_distance, param1, param2):
    """Detect bottles using Hough Circle Transform"""
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    # Apply Hough Circle Transform
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=min_distance,
        param1=param1,
        param2=param2,
        minRadius=min_radius,
        maxRadius=max_radius
    )
    
    # Process detected circles
    bottles = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            x, y, r = circle
            bottles.append((x, y, r))
            
    return bottles

def detect_bottles_contour(frame, min_radius, max_radius):
    """Detect bottles using contour detection"""
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply blur and threshold
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    _, thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours by size and shape
    bottles = []
    for contour in contours:
        # Calculate area and perimeter
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        # Filter out small contours
        if area < 500:
            continue
            
        # Check circularity
        circularity = 4 * np.pi * (area / (perimeter * perimeter)) if perimeter > 0 else 0
        if circularity < 0.5:  # Not circular enough
            continue
            
        # Get bounding circle
        (x, y), radius = cv2.minEnclosingCircle(contour)
        if min_radius <= radius <= max_radius:
            bottles.append((int(x), int(y), int(radius)))
            
    return bottles

def main():
    parser = argparse.ArgumentParser(description="Tune bottle detection parameters")
    parser.add_argument("-i", "--image", required=True, help="Path to input image file")
    args = parser.parse_args()
    
    # Check if image exists
    if not os.path.isfile(args.image):
        print(f"Error: Image file '{args.image}' not found")
        return
    
    # Read image
    frame = cv2.imread(args.image)
    if frame is None:
        print(f"Error: Could not read image {args.image}")
        return
    
    # Create window and trackbars
    window_name = "Parameter Tuning"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    create_trackbars(window_name)
    
    print("Press 'q' to quit, 's' to save parameters")
    
    while True:
        # Get current parameter values
        min_radius, max_radius, min_distance, param1, param2, method = get_trackbar_values(window_name)
        
        # Process frame with current parameters
        result = frame.copy()
        
        if method == 0 or method == 2:  # Hough or Both
            bottles_hough = detect_bottles_hough(frame, min_radius, max_radius, min_distance, param1, param2)
            for (x, y, r) in bottles_hough:
                cv2.circle(result, (x, y), r, (0, 255, 0), 2)
                cv2.circle(result, (x, y), 2, (0, 0, 255), 3)
            
            if method == 0:
                bottle_count = len(bottles_hough)
                text = f"Bottles (Hough): {bottle_count}"
                cv2.putText(result, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        if method == 1 or method == 2:  # Contour or Both
            bottles_contour = detect_bottles_contour(frame, min_radius, max_radius)
            for (x, y, r) in bottles_contour:
                # Use blue color for contour method to distinguish
                cv2.circle(result, (x, y), r, (255, 0, 0), 2)
                cv2.circle(result, (x, y), 2, (0, 0, 255), 3)
            
            if method == 1:
                bottle_count = len(bottles_contour)
                text = f"Bottles (Contour): {bottle_count}"
                cv2.putText(result, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        if method == 2:
            hough_count = len(bottles_hough)
            contour_count = len(bottles_contour)
            text1 = f"Bottles (Hough): {hough_count}"
            text2 = f"Bottles (Contour): {contour_count}"
            cv2.putText(result, text1, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(result, text2, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        # Display parameter info
        param_text = f"Min Radius: {min_radius}, Max Radius: {max_radius}, Min Distance: {min_distance}"
        other_param_text = f"Param1: {param1}, Param2: {param2}"
        cv2.putText(result, param_text, (20, result.shape[0] - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(result, other_param_text, (20, result.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Show result
        cv2.imshow(window_name, result)
        
        # Handle key presses
        key = cv2.waitKey(100) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # Save parameters to a file
            with open("bottle_counter_params.txt", "w") as f:
                f.write(f"min_radius = {min_radius}\n")
                f.write(f"max_radius = {max_radius}\n")
                f.write(f"min_distance = {min_distance}\n")
                f.write(f"param1 = {param1}\n")
                f.write(f"param2 = {param2}\n")
            print(f"Parameters saved to bottle_counter_params.txt")
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 