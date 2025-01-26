# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage

from pathlib import Path
from PIL import Image
import os
import sys
sys.path.append("../")
from model.infer import generate_review


def index(request):
    return render(request, 'index.html')


def get_res(request):
    if request.method == "POST" and request.FILES.get('image'):
        image_file = request.FILES['image']
        
        file_name = default_storage.save(image_file.name, image_file)
        request.session['uploaded_image'] = file_name
        image_url = default_storage.url(file_name)

        image = Image.open(image_file)
        review = generate_review(image=image)

        return JsonResponse({"review": review, "image_url":image_url})

    return JsonResponse({"error": "Invalid request"}, status=400)
