"""
Segmentation Module for Blueprint Analysis
Detects walls, rooms, doors, and windows using OpenCV
"""
import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass
class Room:
    """Represents a detected room"""
    contour: np.ndarray
    area: float
    center: Tuple[int, int]
    bounding_box: Tuple[int, int, int, int]  # x, y, w, h

@dataclass
class Wall:
    """Represents a detected wall segment"""
    start: Tuple[int, int]
    end: Tuple[int, int]
    thickness: float

class BlueprintSegmentation:
    """Segment blueprint into structural elements"""
    
    def __init__(self):
        self.min_room_area = 1000  # Minimum pixels for room detection
        self.wall_thickness_range = (3, 30)  # Expected wall thickness in pixels
    
    def segment(self, image):
        """
        Full segmentation pipeline
        Args:
            image: numpy array (BGR) or PIL Image
        Returns:
            dict with 'rooms', 'walls', 'mask'
        """
        if hasattr(image, 'convert'):
            image = np.array(image.convert('RGB'))
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Preprocess
        processed = self._preprocess(image)
        
        # Detect walls
        wall_mask = self._detect_walls(processed)
        
        # Detect rooms (enclosed areas)
        rooms = self._detect_rooms(wall_mask)
        
        # Extract wall segments
        walls = self._extract_wall_segments(wall_mask)
        
        return {
            'rooms': rooms,
            'walls': walls,
            'wall_mask': wall_mask,
            'processed': processed
        }
    
    def _preprocess(self, image):
        """Convert to binary image highlighting walls"""
        # Grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Adaptive threshold - walls should be dark lines
        binary = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 15, 5
        )
        
        # Morphological operations to clean up
        kernel = np.ones((3, 3), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel, iterations=1)
        
        return cleaned
    
    def _detect_walls(self, binary):
        """Detect wall regions using morphological operations"""
        # Horizontal walls
        h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        h_walls = cv2.morphologyEx(binary, cv2.MORPH_OPEN, h_kernel)
        
        # Vertical walls
        v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
        v_walls = cv2.morphologyEx(binary, cv2.MORPH_OPEN, v_kernel)
        
        # Combine
        wall_mask = cv2.bitwise_or(h_walls, v_walls)
        
        # Dilate slightly to connect nearby segments
        wall_mask = cv2.dilate(wall_mask, np.ones((3, 3), np.uint8), iterations=1)
        
        return wall_mask
    
    def _detect_rooms(self, wall_mask) -> List[Room]:
        """Find enclosed room regions"""
        rooms = []
        
        # Invert to get room interiors
        room_mask = cv2.bitwise_not(wall_mask)
        
        # Find contours
        contours, hierarchy = cv2.findContours(
            room_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filter by area
            if area < self.min_room_area:
                continue
            
            # Skip if it's the outer boundary (too large)
            if area > 0.8 * (wall_mask.shape[0] * wall_mask.shape[1]):
                continue
            
            # Get bounding box and center
            x, y, w, h = cv2.boundingRect(contour)
            M = cv2.moments(contour)
            if M['m00'] > 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
            else:
                cx, cy = x + w // 2, y + h // 2
            
            rooms.append(Room(
                contour=contour,
                area=area,
                center=(cx, cy),
                bounding_box=(x, y, w, h)
            ))
        
        # Sort by area (largest first)
        rooms.sort(key=lambda r: r.area, reverse=True)
        
        return rooms
    
    def _extract_wall_segments(self, wall_mask) -> List[Wall]:
        """Extract individual wall line segments"""
        walls = []
        
        # Use probabilistic Hough transform
        lines = cv2.HoughLinesP(
            wall_mask, 1, np.pi/180, 
            threshold=50, minLineLength=30, maxLineGap=10
        )
        
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                
                # Estimate wall thickness at midpoint
                mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
                thickness = self._estimate_thickness(wall_mask, mid_x, mid_y)
                
                walls.append(Wall(
                    start=(x1, y1),
                    end=(x2, y2),
                    thickness=thickness
                ))
        
        return walls
    
    def _estimate_thickness(self, mask, x, y, max_search=30):
        """Estimate wall thickness at a point"""
        h, w = mask.shape
        
        # Search horizontally
        left = right = 0
        for i in range(1, max_search):
            if x - i >= 0 and mask[y, x - i] > 0:
                left = i
            else:
                break
        for i in range(1, max_search):
            if x + i < w and mask[y, x + i] > 0:
                right = i
            else:
                break
        
        return left + right + 1
    
    def visualize(self, image, results, show_rooms=True, show_walls=True):
        """Visualize segmentation results"""
        if hasattr(image, 'convert'):
            image = np.array(image.convert('RGB'))
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        output = image.copy()
        
        # Draw rooms
        if show_rooms:
            colors = [
                (255, 100, 100), (100, 255, 100), (100, 100, 255),
                (255, 255, 100), (255, 100, 255), (100, 255, 255),
                (200, 150, 100), (100, 200, 150), (150, 100, 200)
            ]
            
            for i, room in enumerate(results['rooms'][:9]):
                color = colors[i % len(colors)]
                
                # Draw filled contour with transparency
                overlay = output.copy()
                cv2.drawContours(overlay, [room.contour], -1, color, -1)
                cv2.addWeighted(overlay, 0.3, output, 0.7, 0, output)
                
                # Draw contour outline
                cv2.drawContours(output, [room.contour], -1, color, 2)
                
                # Label with room number
                cv2.putText(output, f"Room {i+1}", room.center,
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                cv2.putText(output, f"Room {i+1}", room.center,
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Draw walls
        if show_walls:
            for wall in results['walls'][:100]:  # Limit for performance
                cv2.line(output, wall.start, wall.end, (0, 0, 255), 2)
        
        return output


if __name__ == "__main__":
    segmentation = BlueprintSegmentation()
    print("BlueprintSegmentation initialized")
