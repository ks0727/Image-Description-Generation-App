import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

from PIL import Image

class ReviewGenerator:
    def __init__(self, model_path="Salesforce/blip-image-captioning-base"):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.processor = BlipProcessor.from_pretrained(model_path)
        self.model = BlipForConditionalGeneration.from_pretrained(model_path)

    def generate(self, image, prompt=""):
        if not isinstance(image,Image.Image):
            image = Image.open(image)
        inputs = self.processor(images=image, text=prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(**inputs,max_new_tokens=1000)
        generated_text = self.processor.decode(outputs[0], skip_special_tokens=True)
        return generated_text[len(prompt):]

