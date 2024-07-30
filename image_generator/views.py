from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import generate_image_from_text


@api_view(['POST'])
def generate_images(request):
    """ Generates image and returns task_ids and status"""
    
    text = request.GET.get('prompt')
    if text:
        task = generate_image_from_text.apply_async(args=[text])
        return Response({"message": "Image generation started",'task_id': task.id, "status":status.HTTP_200_OK})
    
    prompts = ["A red flying dog", "A piano ninja", "A footballer kid"]
    task_ids = [generate_image_from_text.delay(prompt).id for prompt in prompts]
    return Response({"message": "Image generation started",'task_id':task_ids,"status":status.HTTP_200_OK})