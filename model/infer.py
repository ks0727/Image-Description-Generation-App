from model.blip_model import ReviewGenerator

review_generator = ReviewGenerator()

def generate_review(image):
    res = review_generator.generate(image)
    return res
