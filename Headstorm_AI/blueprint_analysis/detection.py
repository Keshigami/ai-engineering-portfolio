import os
from roboflow import Roboflow
from PIL import Image, ImageDraw
import numpy as np

class BlueprintDetection:
    """Detection module using Roboflow API"""
    
    def __init__(self, api_key=None, project_id=None, version=None):
        self.api_key = api_key or os.getenv("ROBOFLOW_API_KEY")
        self.project_id = project_id or os.getenv("ROBOFLOW_PROJECT_ID", "blueprint-elements")
        self.version = version or os.getenv("ROBOFLOW_VERSION", "1")
        
        self.enabled = False
        if self.api_key:
            try:
                rf = Roboflow(api_key=self.api_key)
                project = rf.workspace().project(self.project_id)
                self.model = project.version(self.version).model
                self.enabled = True
                print(f"Roboflow Detection Enabled: {self.project_id} (v{self.version})")
            except Exception as e:
                print(f"Roboflow Initialization Failed: {e}")
        else:
            print("Roboflow API Key not found. Running in Mock/Heuristic mode.")

    def detect(self, image):
        """Detect elements using Roboflow or Mock fallback"""
        if not self.enabled:
            return self._mock_detect(image)
        
        # Real Roboflow Inference
        prediction = self.model.predict(image, confidence=40, overlap=30).json()
        return prediction.get("predictions", [])

    def _mock_detect(self, image):
        """Fallback mock detections for demo purposes with variety"""
        import random
        if hasattr(image, 'size'):
            w, h = image.size
        else:
            h, w = image.shape[:2]
            
        classes = ["door", "window", "column", "staircase"]
        mocks = []
        
        # Always generate at least 3-5 interesting elements for the demo
        for _ in range(random.randint(3, 6)):
            mocks.append({
                "x": random.randint(int(w*0.1), int(w*0.9)),
                "y": random.randint(int(h*0.1), int(h*0.9)),
                "width": random.randint(40, 100),
                "height": random.randint(40, 100),
                "class": random.choice(classes),
                "confidence": random.uniform(0.82, 0.98)
            })
        return mocks

    def visualize(self, image, predictions):
        """Draw detections on image with class-specific styling"""
        if not hasattr(image, 'convert'):
            image = Image.fromarray(image)
        
        draw = ImageDraw.Draw(image)
        
        # Color mapping for professional look
        colors = {
            "door": "#FF3B30",
            "window": "#007AFF",
            "column": "#4CD964",
            "staircase": "#FFCC00"
        }

        for pred in predictions:
            color = colors.get(pred["class"], "red")
            
            # Roboflow returns center x, y
            x0 = pred["x"] - pred["width"] / 2
            y0 = pred["y"] - pred["height"] / 2
            x1 = pred["x"] + pred["width"] / 2
            y1 = pred["y"] + pred["height"] / 2
            
            # Thick lines for visibility
            draw.rectangle([x0, y0, x1, y1], outline=color, width=4)
            
            # Background for text
            label = f"{pred['class']} {pred['confidence']:.2f}"
            draw.rectangle([x0, y0 - 20, x0 + 100, y0], fill=color)
            draw.text((x0 + 5, y0 - 18), label, fill="white")
            
        return image
