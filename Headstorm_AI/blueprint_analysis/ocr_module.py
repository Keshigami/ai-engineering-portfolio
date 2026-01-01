"""
OCR Module for Blueprint Text Extraction
Uses EasyOCR for multi-orientation text detection
"""
import cv2
import numpy as np
import re

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    print("Warning: EasyOCR not available, using fallback")

class BlueprintOCR:
    """Extract text from blueprints including dimensions and labels"""
    
    def __init__(self, languages=['en']):
        self.languages = languages
        self.reader = None
        if EASYOCR_AVAILABLE:
            self.reader = easyocr.Reader(languages, gpu=False)
    
    def extract_text(self, image):
        """
        Extract all text from blueprint image
        Args:
            image: numpy array (BGR) or PIL Image
        Returns:
            list of dicts with 'text', 'bbox', 'confidence'
        """
        if hasattr(image, 'convert'):  # PIL Image
            image = np.array(image.convert('RGB'))
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if not EASYOCR_AVAILABLE or self.reader is None:
            return self._fallback_ocr(image)
        
        # Preprocess for better OCR
        processed = self._preprocess(image)
        
        # Run OCR
        results = self.reader.readtext(processed)
        
        extracted = []
        for bbox, text, conf in results:
            extracted.append({
                'text': text,
                'bbox': bbox,
                'confidence': conf,
                'type': self._classify_text(text)
            })
        
        return extracted
    
    def _preprocess(self, image):
        """Preprocess image for better OCR results"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(binary, None, 10, 7, 21)
        
        return denoised
    
    def _classify_text(self, text):
        """Classify extracted text type"""
        text = text.strip()
        
        # Dimension patterns (e.g., 10'-6", 3.5m, 1200mm)
        dimension_patterns = [
            r"\d+['\"]",  # feet/inches
            r"\d+\.?\d*\s*(m|mm|cm|ft|in)",  # metric/imperial
            r"\d+\s*[xX]\s*\d+",  # dimensions like 10x12
            r"\d+'-\d+\"",  # feet-inches format
        ]
        for pattern in dimension_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return 'dimension'
        
        # Room labels
        room_keywords = ['bedroom', 'bath', 'kitchen', 'living', 'dining', 
                        'garage', 'office', 'closet', 'hall', 'entry', 'porch']
        if any(kw in text.lower() for kw in room_keywords):
            return 'room_label'
        
        # Scale indicators
        if 'scale' in text.lower() or re.search(r'1:\d+', text):
            return 'scale'
        
        return 'annotation'
    
    def _fallback_ocr(self, image):
        """Fallback when EasyOCR not available - basic text detection"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Find text-like regions using MSER
        mser = cv2.MSER_create()
        regions, _ = mser.detectRegions(gray)
        
        detected = []
        for region in regions[:20]:  # Limit to first 20 regions
            x, y, w, h = cv2.boundingRect(region.reshape(-1, 1, 2))
            if w > 10 and h > 5 and h < 100:
                detected.append({
                    'text': '[Text Region Detected]',
                    'bbox': [[x, y], [x+w, y], [x+w, y+h], [x, y+h]],
                    'confidence': 0.5,
                    'type': 'unknown'
                })
        
        return detected
    
    def extract_dimensions(self, image):
        """Extract only dimension annotations"""
        all_text = self.extract_text(image)
        return [t for t in all_text if t['type'] == 'dimension']
    
    def extract_room_labels(self, image):
        """Extract only room labels"""
        all_text = self.extract_text(image)
        return [t for t in all_text if t['type'] == 'room_label']
    
    def visualize(self, image, results):
        """Draw OCR results on image"""
        if hasattr(image, 'convert'):  # PIL Image
            image = np.array(image.convert('RGB'))
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        output = image.copy()
        
        colors = {
            'dimension': (0, 255, 0),    # Green
            'room_label': (255, 0, 0),   # Blue
            'scale': (0, 255, 255),      # Yellow
            'annotation': (128, 128, 128) # Gray
        }
        
        for result in results:
            bbox = np.array(result['bbox']).astype(int)
            color = colors.get(result['type'], (128, 128, 128))
            
            cv2.polylines(output, [bbox], True, color, 2)
            
            # Draw text label
            x, y = bbox[0]
            cv2.putText(output, result['text'][:20], (x, y-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        
        return output


if __name__ == "__main__":
    ocr = BlueprintOCR()
    print(f"BlueprintOCR initialized (EasyOCR available: {EASYOCR_AVAILABLE})")
