#!/usr/bin/env python3
import cv2
import numpy as np
import argparse
import os
import sys
from datetime import datetime

class BottleCounter:
    def __init__(self):
        # Detection parameters
        self.min_radius = 15
        self.max_radius = 60
        self.min_distance = 20
        self.param1 = 30  # Canny edge detector higher threshold
        self.param2 = 30  # Accumulator threshold
        
        # Visualization parameters
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.7
        self.thickness = 2
        self.text_color = (0, 255, 0)
        self.circle_color = (0, 255, 0)
        
    def detect_bottles_hough(self, frame):
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
            minDist=self.min_distance,
            param1=self.param1,
            param2=self.param2,
            minRadius=self.min_radius,
            maxRadius=self.max_radius
        )
        
        # Process detected circles
        bottles = []
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for circle in circles[0, :]:
                x, y, r = circle
                bottles.append((x, y, r))
                
        return bottles
    
    def detect_bottles_contour(self, frame):
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
            if self.min_radius <= radius <= self.max_radius:
                bottles.append((int(x), int(y), int(radius)))
                
        return bottles
    
    def process_frame(self, frame):
        """Process a frame and count bottles"""
        # Try both methods and use the one with better results
        bottles_hough = self.detect_bottles_hough(frame)
        bottles_contour = self.detect_bottles_contour(frame)
        
        # Choose method with more detections
        bottles = bottles_hough if len(bottles_hough) > len(bottles_contour) else bottles_contour
        
        # Draw circles around bottles
        result = frame.copy()
        for (x, y, r) in bottles:
            cv2.circle(result, (x, y), r, self.circle_color, 2)
            cv2.circle(result, (x, y), 2, (0, 0, 255), 3)
        
        # Display bottle count
        bottle_count = len(bottles)
        text = f"Bottles: {bottle_count}"
        cv2.putText(result, text, (20, 40), self.font, self.font_scale, self.text_color, self.thickness)
        
        return result, bottle_count
    
    def process_video(self, source=0):
        """Process video from webcam or file"""
        # Open video source
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            print(f"Error: Could not open video source {source}")
            return
            
        print("Press 'q' to quit, 's' to save the current frame")
        
        while True:
            # Read frame
            ret, frame = cap.read()
            if not ret:
                print("Video stream ended")
                break
                
            # Process frame
            result, count = self.process_frame(frame)
            
            # Show result
            cv2.imshow("Bottle Counter", result)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"bottle_count_{timestamp}.jpg"
                cv2.imwrite(filename, result)
                print(f"Saved frame as {filename}")
        
        # Clean up
        cap.release()
        cv2.destroyAllWindows()
    
    def process_image(self, image_path):
        """Process a single image file"""
        # Read image
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"Error: Could not read image {image_path}")
            return
            
        # Process frame
        result, count = self.process_frame(frame)
        
        # Show result
        cv2.imshow("Bottle Counter", result)
        print(f"Detected {count} bottles")
        print("Press any key to exit")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description="Count bottles in a crate using computer vision")
    parser.add_argument("-i", "--image", help="Path to input image file")
    parser.add_argument("-v", "--video", help="Path to input video file")
    parser.add_argument("-c", "--camera", type=int, default=0, help="Camera device index (default: 0)")
    args = parser.parse_args()
    
    counter = BottleCounter()
    
    if args.image:
        counter.process_image(args.image)
    elif args.video:
        counter.process_video(args.video)
    else:
        counter.process_video(args.camera)

if __name__ == "__main__":
    main() 