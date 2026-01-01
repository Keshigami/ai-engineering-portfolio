import cv2
import numpy as np
import random
from PIL import Image, ImageDraw, ImageFont

def generate_synthetic_menu(output_path, restaurant_name="The Food Spot"):
    # Create a tall menu canvas
    W, H = 800, 1200
    img = Image.new('RGB', (W, H), color=(255, 255, 252)) # Slight off-white/paper color
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((W//2 - 100, 50), restaurant_name, fill=(0,0,0), font_size=40)
    
    categories = ["Appetizers", "Main Course", "Sides", "Drinks", "Desserts"]
    items = {
        "Appetizers": [("Calamari", 12.99), ("Garlic Bread", 6.50), ("Bruschetta", 9.00)],
        "Main Course": [("Ribeye Steak", 34.99), ("Grilled Salmon", 28.00), ("Pasta Carbonara", 19.50), ("Veggie Burger", 16.00)],
        "Sides": [("French Fries", 5.00), ("Cole Slaw", 4.00), ("Mashed Potatoes", 6.00)],
        "Drinks": [("Iced Tea", 3.00), ("Red Wine", 11.00), ("Craft Beer", 8.50)],
        "Desserts": [("Tiramisu", 9.00), ("Cheesecake", 8.00)]
    }
    
    y = 150
    for cat in categories:
        # Category Header
        draw.text((80, y), cat.upper(), fill=(150, 0, 0), font_size=25)
        y += 40
        
        for name, price in items[cat]:
            # Item Name
            draw.text((100, y), name, fill=(50, 50, 50), font_size=20)
            
            # Leader lines (dots)
            draw.text((350, y), "." * 40, fill=(200, 200, 200), font_size=15)
            
            # Price
            draw.text((650, y), f"${price:.2f}", fill=(0, 0, 0), font_size=20)
            y += 35
        
        y += 30 # Space between categories

    img.save(output_path)
    print(f"Generated synthetic menu: {output_path}")

if __name__ == "__main__":
    import os
    os.makedirs("dataset", exist_ok=True)
    generate_synthetic_menu("dataset/sample_menu_1.png", "Bistro 2026")
