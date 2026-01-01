"""
Blueprint Analyzer - Main Pipeline
Combines classification, OCR, and segmentation for complete blueprint analysis
"""
import cv2
import numpy as np
from PIL import Image
from pathlib import Path
import json
from datetime import datetime

from .classifier import BlueprintClassifier
from .ocr_module import BlueprintOCR
from .segmentation import BlueprintSegmentation
from .detection import BlueprintDetection


class BlueprintAnalyzer:
    """Complete blueprint analysis pipeline"""
    
    def __init__(self, model_path=None):
        """
        Initialize analyzer with all components
        Args:
            model_path: Path to trained classifier weights
        """
        self.classifier = BlueprintClassifier(model_path=model_path)
        self.ocr = BlueprintOCR(languages=['en'])  # English blueprints
        self.segmentation = BlueprintSegmentation()
        self.detection = BlueprintDetection()
        
        print("Blueprint Analyzer initialized:")
        print(f"  - Classifier: EfficientNet-B0 ({self.classifier.device})")
        print(f"  - OCR: EasyOCR (English)")
        print(f"  - Segmentation: OpenCV-based")
    
    def analyze(self, image, include_visualization=True):
        """
        Run complete analysis pipeline
        Args:
            image: PIL Image, numpy array, or path to image
            include_visualization: Whether to generate annotated output
        Returns:
            dict with all analysis results
        """
        # Load image if path
        if isinstance(image, (str, Path)):
            image = Image.open(image).convert('RGB')
        elif isinstance(image, np.ndarray):
            if len(image.shape) == 2:  # Grayscale
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            elif image.shape[2] == 4:  # RGBA
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
            elif image.shape[2] == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'image_size': image.size,
        }
        
        # 1. Classification
        try:
            classification = self.classifier.predict(image)
            results['classification'] = classification
        except Exception as e:
            results['classification'] = {'error': str(e)}
        
        # 2. OCR
        try:
            text_results = self.ocr.extract_text(image)
            results['ocr'] = {
                'total_text_regions': len(text_results),
                'dimensions': [t for t in text_results if t['type'] == 'dimension'],
                'room_labels': [t for t in text_results if t['type'] == 'room_label'],
                'annotations': [t for t in text_results if t['type'] == 'annotation'],
                'all_text': text_results
            }
        except Exception as e:
            results['ocr'] = {'error': str(e)}
        
        # 3. Segmentation
        try:
            seg_results = self.segmentation.segment(image)
            results['segmentation'] = {
                'num_rooms': len(seg_results['rooms']),
                'num_walls': len(seg_results['walls']),
                'rooms': [
                    {
                        'id': i + 1,
                        'area': room.area,
                        'center': room.center,
                        'bounding_box': room.bounding_box
                    }
                    for i, room in enumerate(seg_results['rooms'][:10])
                ]
            }
        except Exception as e:
            results['segmentation'] = {'error': str(e)}
        
        # 4. AI Detection (Roboflow)
        try:
            detections = self.detection.detect(image)
            results['detections'] = detections
        except Exception as e:
            results['detections'] = {'error': str(e)}
        
        # 5. Visualization
        if include_visualization:
            try:
                vis = self._create_visualization(image, results, seg_results, text_results, detections)
                results['visualization'] = vis
            except Exception as e:
                results['visualization'] = None
        
        return results
    
    def _create_visualization(self, image, results, seg_results, text_results, detections):
        """Create annotated visualization"""
        # Convert PIL to numpy
        img_np = np.array(image)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        
        # Draw segmentation
        output = self.segmentation.visualize(img_bgr, seg_results, 
                                             show_rooms=True, show_walls=False)
        
        # Draw OCR results
        output = self.ocr.visualize(output, text_results)
        
        # Draw AI Detections (Roboflow)
        if detections and not isinstance(detections, dict):
            # Convert back to PIL for detection visualization
            pill_img = Image.fromarray(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
            pill_img = self.detection.visualize(pill_img, detections)
            output = cv2.cvtColor(np.array(pill_img), cv2.COLOR_RGB2BGR)
        
        # Add classification label
        if 'classification' in results and 'class' in results['classification']:
            label = f"{results['classification']['class']} ({results['classification']['confidence']:.1%})"
            cv2.rectangle(output, (10, 10), (350, 50), (0, 0, 0), -1)
            cv2.putText(output, label, (20, 38), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Convert back to RGB
        output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        return Image.fromarray(output_rgb)
    
    def analyze_batch(self, image_paths, output_dir=None):
        """Analyze multiple images"""
        results = []
        for path in image_paths:
            print(f"Analyzing: {path}")
            result = self.analyze(path)
            result['source_path'] = str(path)
            results.append(result)
            
            if output_dir and result.get('visualization'):
                output_path = Path(output_dir) / f"analyzed_{Path(path).name}"
                result['visualization'].save(output_path)
                print(f"  Saved: {output_path}")
        
        return results
    
    def generate_report(self, results):
        """Generate analysis report"""
        report = []
        report.append("=" * 60)
        report.append("BLUEPRINT ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Timestamp: {results['timestamp']}")
        report.append(f"Image Size: {results['image_size']}")
        report.append("")
        
        # Classification
        if 'classification' in results:
            cls = results['classification']
            if 'error' not in cls:
                report.append("CLASSIFICATION:")
                report.append(f"  Type: {cls['class']}")
                report.append(f"  Confidence: {cls['confidence']:.1%}")
                report.append("  Probabilities:")
                for cls_name, prob in cls['probabilities'].items():
                    report.append(f"    - {cls_name}: {prob:.1%}")
            else:
                report.append(f"CLASSIFICATION ERROR: {cls['error']}")
        report.append("")
        
        # OCR
        if 'ocr' in results:
            ocr = results['ocr']
            if 'error' not in ocr:
                report.append("TEXT EXTRACTION:")
                report.append(f"  Total Regions: {ocr['total_text_regions']}")
                report.append(f"  Dimensions Found: {len(ocr['dimensions'])}")
                report.append(f"  Room Labels: {len(ocr['room_labels'])}")
                if ocr['dimensions']:
                    report.append("  Dimension Examples:")
                    for dim in ocr['dimensions'][:5]:
                        report.append(f"    - {dim['text']} (conf: {dim['confidence']:.2f})")
                if ocr['room_labels']:
                    report.append("  Room Labels:")
                    for room in ocr['room_labels'][:5]:
                        report.append(f"    - {room['text']}")
            else:
                report.append(f"OCR ERROR: {ocr['error']}")
        report.append("")
        
        # Segmentation
        if 'segmentation' in results:
            seg = results['segmentation']
            if 'error' not in seg:
                report.append("SEGMENTATION:")
                report.append(f"  Rooms Detected: {seg['num_rooms']}")
                report.append(f"  Wall Segments: {seg['num_walls']}")
                if seg['rooms']:
                    report.append("  Room Details:")
                    for room in seg['rooms'][:5]:
                        report.append(f"    - Room {room['id']}: {room['area']:.0f} px²")
            else:
                report.append(f"SEGMENTATION ERROR: {seg['error']}")
        
        # AI Detection
        if 'detections' in results:
            dets = results['detections']
            if not isinstance(dets, dict):
                report.append("AI DETECTION (Roboflow):")
                report.append(f"  Elements Detected: {len(dets)}")
                for det in dets:
                    report.append(f"    - {det['class']} (conf: {det['confidence']:.2f})")
            else:
                report.append(f"DETECTION ERROR: {dets.get('error')}")
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)


if __name__ == "__main__":
    # Test initialization
    analyzer = BlueprintAnalyzer()
    print("\nBlueprint Analyzer ready for analysis!")
