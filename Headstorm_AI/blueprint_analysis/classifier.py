"""
Blueprint Classifier Module
Uses EfficientNet-B0 for classifying blueprint types
"""
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import os

class BlueprintClassifier:
    """Classifies blueprints into categories: floor_plan, elevation, section, site_plan"""
    
    CLASSES = ['elevation', 'floor_plan', 'section', 'site_plan']
    
    def __init__(self, model_path=None, device=None):
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self._build_model()
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        
        self.model.to(self.device)
        self.model.eval()
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    
    def _build_model(self):
        """Build EfficientNet-B0 model with custom classifier"""
        model = models.efficientnet_b0(weights='DEFAULT')
        num_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.Linear(num_features, len(self.CLASSES))
        )
        return model
    
    def load_model(self, path):
        """Load trained weights"""
        state_dict = torch.load(path, map_location=self.device)
        self.model.load_state_dict(state_dict)
        print(f"Model loaded from {path}")
    
    def save_model(self, path):
        """Save model weights"""
        torch.save(self.model.state_dict(), path)
        print(f"Model saved to {path}")
    
    def predict(self, image):
        """
        Predict blueprint type
        Args:
            image: PIL Image or path to image
        Returns:
            dict with 'class' and 'confidence' and 'probabilities'
        """
        if isinstance(image, str):
            image = Image.open(image).convert('RGB')
        elif not isinstance(image, Image.Image):
            image = Image.fromarray(image).convert('RGB')
        
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(input_tensor)
            probs = torch.softmax(outputs, dim=1)[0]
            
        conf, pred_idx = torch.max(probs, 0)
        
        return {
            'class': self.CLASSES[pred_idx.item()],
            'confidence': conf.item(),
            'probabilities': {cls: probs[i].item() for i, cls in enumerate(self.CLASSES)}
        }

    def train_mode(self):
        """Set model to training mode"""
        self.model.train()
        return self
    
    def eval_mode(self):
        """Set model to evaluation mode"""
        self.model.eval()
        return self


if __name__ == "__main__":
    # Quick test
    classifier = BlueprintClassifier()
    print(f"BlueprintClassifier initialized on {classifier.device}")
    print(f"Classes: {classifier.CLASSES}")
