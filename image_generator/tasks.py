import os
import base64
import requests
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.files.storage import default_storage
from celery import shared_task
from .models import GeneratedImage


@shared_task(autoretry_for=(Exception,), max_retries=3, retry_backoff=True)
def generate_image_from_text(prompt):
    """ Generates image from prompt and save the image metadata in the model/db """
    
    api_key = str(os.getenv("STABILITY_API_KEY"))
    url = 'https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image'

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data={
        "text_prompts": [
            {
                "text": str(prompt),
                "weight": 0.5
            }
        ],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30,
    }
    
    try:
        response = requests.post(url,headers=headers, json=data, timeout=5)
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.RequestException:
        pass
       
    if response:
        response_data = response.json()

        if response.status_code == 200:
            for i, image in enumerate(response_data["artifacts"]):
                img_data = base64.b64decode(image["base64"])
                filename = f"image{i}_model_id_{GeneratedImage.objects.count() + 1}.jpg"
                file_path = f"{settings.MEDIA_ROOT}/{filename}"
                default_storage.save(file_path, ContentFile(img_data))

                # Save the image URL to the model
                image_url = f"{settings.MEDIA_URL}{filename}"
                GeneratedImage.objects.create(prompt=prompt, image_url=image_url)
            return image_url
    return None
