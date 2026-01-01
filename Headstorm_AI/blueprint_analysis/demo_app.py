"""
Blueprint Analysis Demo Application
Interactive Gradio interface for blueprint analysis
"""
import gradio as gr
import numpy as np
from PIL import Image
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .blueprint_analyzer import BlueprintAnalyzer


def create_demo():
    """Create Gradio demo interface"""
    
    # Initialize analyzer
    model_path = os.path.join(os.path.dirname(__file__), "blueprint_classifier.pth")
    if not os.path.exists(model_path):
        model_path = None
        print("Note: No trained model found. Using pretrained weights.")
    
    analyzer = BlueprintAnalyzer(model_path=model_path)
    
    def analyze_blueprint(image):
        """Process uploaded blueprint"""
        if image is None:
            return None, "Please upload an image"
        
        # Run analysis
        results = analyzer.analyze(image, include_visualization=True)
        
        # Generate report
        report = analyzer.generate_report(results)
        
        # Get visualization
        vis = results.get('visualization')
        
        return vis, report
    
    def get_classification_details(image):
        """Get detailed classification results"""
        if image is None:
            return "Upload an image first"
        
        result = analyzer.classifier.predict(image)
        
        output = "## Classification Results\n\n"
        output += f"**Predicted Type:** {result['class']}\n\n"
        output += f"**Confidence:** {result['confidence']:.1%}\n\n"
        output += "### All Probabilities:\n"
        
        sorted_probs = sorted(result['probabilities'].items(), 
                             key=lambda x: x[1], reverse=True)
        for cls, prob in sorted_probs:
            bar = "█" * int(prob * 20)
            output += f"- {cls}: {prob:.1%} {bar}\n"
        
        return output
    
    def get_text_details(image):
        """Get OCR text extraction results"""
        if image is None:
            return "Upload an image first"
        
        results = analyzer.ocr.extract_text(image)
        
        output = "## Extracted Text\n\n"
        output += f"**Total Regions:** {len(results)}\n\n"
        
        # Group by type
        by_type = {}
        for r in results:
            t = r['type']
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(r)
        
        for text_type, items in by_type.items():
            output += f"### {text_type.replace('_', ' ').title()} ({len(items)})\n"
            for item in items[:10]:
                conf = item['confidence']
                output += f"- \"{item['text']}\" (conf: {conf:.2f})\n"
            if len(items) > 10:
                output += f"- ... and {len(items) - 10} more\n"
            output += "\n"
        
        return output
    
    def get_segmentation_details(image):
        """Get segmentation results"""
        if image is None:
            return "Upload an image first"
        
        results = analyzer.segmentation.segment(image)
        
        output = "## Segmentation Results\n\n"
        output += f"**Rooms Detected:** {len(results['rooms'])}\n"
        output += f"**Wall Segments:** {len(results['walls'])}\n\n"
        
        output += "### Room Details\n"
        for i, room in enumerate(results['rooms'][:10]):
            output += f"- **Room {i+1}:** Area = {room.area:.0f} px², "
            output += f"Center = {room.center}, "
            output += f"BBox = {room.bounding_box}\n"
        
        if len(results['rooms']) > 10:
            output += f"- ... and {len(results['rooms']) - 10} more rooms\n"
        
        return output

    def get_detection_details(image):
        """Get AI detection results"""
        if image is None:
            return "Upload an image first"
        
        results = analyzer.detection.detect(image)
        
        output = "## AI Detection Results (Roboflow)\n\n"
        output += f"**Elements Detected:** {len(results)}\n\n"
        
        for pred in results:
            output += f"- **{pred['class']}**: Confidence: {pred['confidence']:.2f}, "
            output += f"Size: {pred['width']}x{pred['height']}\n"
        
        return output
    
    # Build interface
    with gr.Blocks(title="Blueprint Analyzer", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🏗️ Blueprint Analysis System
        
        Upload an architectural blueprint to analyze its type, extract text/dimensions, 
        and detect rooms & structural elements.
        
        **Capabilities:**
        - 📋 **Classification**: Floor Plan, Elevation, Section, Site Plan
        - 📝 **OCR**: Extract dimensions, room labels, and annotations
        - 🏠 **Segmentation**: Detect rooms and wall structures
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                input_image = gr.Image(type="pil", label="Upload Blueprint")
                analyze_btn = gr.Button("🔍 Analyze Blueprint", variant="primary")
            
            with gr.Column(scale=1):
                output_image = gr.Image(type="pil", label="Analyzed Result")
        
        with gr.Row():
            report_output = gr.Textbox(label="Analysis Report", lines=20, max_lines=30)
        
        with gr.Accordion("Detailed Results", open=False):
            with gr.Tabs():
                with gr.Tab("Classification"):
                    class_output = gr.Markdown()
                    class_btn = gr.Button("Get Classification Details")
                
                with gr.Tab("Text Extraction"):
                    text_output = gr.Markdown()
                    text_btn = gr.Button("Get OCR Details")
                
                with gr.Tab("Segmentation"):
                    seg_output = gr.Markdown()
                    seg_btn = gr.Button("Get Segmentation Details")
                
                with gr.Tab("AI Detection"):
                    det_output = gr.Markdown()
                    det_btn = gr.Button("Get AI Detection Details")
        
        # Event handlers
        analyze_btn.click(
            fn=analyze_blueprint,
            inputs=[input_image],
            outputs=[output_image, report_output]
        )
        
        class_btn.click(
            fn=get_classification_details,
            inputs=[input_image],
            outputs=[class_output]
        )
        
        text_btn.click(
            fn=get_text_details,
            inputs=[input_image],
            outputs=[text_output]
        )
        
        seg_btn.click(
            fn=get_segmentation_details,
            inputs=[input_image],
            outputs=[seg_output]
        )
        
        det_btn.click(
            fn=get_detection_details,
            inputs=[input_image],
            outputs=[det_output]
        )
        
        gr.Markdown("""
        ---
        **Technologies:** PyTorch (EfficientNet-B0) | EasyOCR | OpenCV | Gradio
        
        *Built for HeadstormAI Computer Vision Engineer Portfolio*
        """)
    
    return demo


if __name__ == "__main__":
    demo = create_demo()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=True,
        show_error=True
    )
