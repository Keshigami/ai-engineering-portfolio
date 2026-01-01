import cv2
import numpy as np
import easyocr
import json
from PIL import Image
import os

class MenuDigitizer:
    """Intelligent Menu Digitization Engine"""
    
    def __init__(self, languages=['en']):
        self.reader = easyocr.Reader(languages)
        print("MenuDigitizer Initialized (EasyOCR)")

    def process_menu(self, image_path):
        """Analyze menu and return structured JSON with spatial alignment"""
        results = self.reader.readtext(image_path)
        
        # 1. Group by Y-coordinate to find lines
        lines = []
        if not results:
            return {"restaurant": "Unknown", "categories": []}
            
        # Sort by Y-coordinate
        results.sort(key=lambda x: x[0][0][1])
        
        current_line = [results[0]]
        y_threshold = 15 # pixels to consider on the same line
        
        for i in range(1, len(results)):
            if abs(results[i][0][0][1] - results[i-1][0][0][1]) <= y_threshold:
                current_line.append(results[i])
            else:
                # Sort line horizontally
                current_line.sort(key=lambda x: x[0][0][0])
                lines.append(current_line)
                current_line = [results[i]]
        lines.append(current_line) # Add last line
        
        menu_data = {
            "restaurant": "Detected Restaurant", 
            "categories": []
        }
        
        current_category = None
        
        for line in lines:
            # Combine text on the same line
            line_text = " ".join([res[1] for res in line])
            
            # Category Detection (All caps, often standalone or centered)
            if line_text.isupper() and len(line_text) > 3:
                current_category = {"name": line_text, "items": []}
                menu_data["categories"].append(current_category)
                continue
                
            if not current_category:
                continue
                
            # Item and Price Extraction
            item_name = ""
            item_price = None
            
            for (bbox, text, prob) in line:
                if prob < 0.35: continue
                
                # Check if it looks like a price
                if "$" in text or (any(c.isdigit() for c in text) and "." in text):
                    item_price = text
                else:
                    item_name += " " + text
            
            if item_name.strip():
                item_entry = {"name": item_name.strip()}
                if item_price:
                    item_entry["price"] = item_price
                current_category["items"].append(item_entry)
        
        return menu_data

    def batch_analyze(self, folder_path):
        """Simulate processing 1000 menus for competitive intelligence"""
        files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg'))]
        print(f"🚀 Batch Engine: Found {len(files)} menus.")
        
        all_data = []
        for f in files[:5]: # Cap at 5 for demo speed
            print(f"📦 Processing: {f}")
            path = os.path.join(folder_path, f)
            data = self.process_menu(path)
            all_data.append(data)
            
        return all_data

if __name__ == "__main__":
    digitizer = MenuDigitizer()
    # Check if sample exists
    sample_path = "dataset/sample_menu_1.png"
    if not os.path.exists(sample_path):
        print("Run generate_samples.py first!")
    else:
        info = digitizer.process_menu(sample_path)
        print(json.dumps(info, indent=2))
