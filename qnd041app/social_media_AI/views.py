import os
import requests
import json


from django.http import JsonResponse
from django.utils import timezone
from django.core.files.base import ContentFile
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from wagtail.images import get_image_model

from .models import InstagramPost, InstagramReel, FacebookImagePost


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from wagtail.images import get_image_model

from .models import InstagramPost


@api_view(['POST'])
@permission_classes([AllowAny])
def save_generated_image(request):

    data = request.data

    post_id = data.get("id")
    image_url = data.get("image")

    if not post_id or not image_url:
        return Response(
            {"error": "Missing data"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        post = InstagramPost.objects.get(id=post_id)

        # Descargar imagen
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()

        image_file = ContentFile(
            response.content,
            name=f"post_{post_id}.jpg"
        )

        ImageModel = get_image_model()

        wagtail_image = ImageModel.objects.create(
            title=f"Post {post_id} AI",
            file=image_file
        )

        post.image = wagtail_image
        post.generated_image_url = wagtail_image.file.url
        post.status = "completed"
        post.updated_at = timezone.now()
        post.save()

        return Response({
            "success": True,
            "image_id": wagtail_image.id
        })

    except InstagramPost.DoesNotExist:
        return Response(
            {"error": "Post not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


from .models import InstagramPost


@api_view(['POST'])
@permission_classes([AllowAny])
def instagram_webhook(request):

    data = request.data

    try:
        post = InstagramPost.objects.get(id=data.get("id"))

        post.caption = data.get("caption", "")
        post.copy = data.get("copy", "")
        post.hashtags = data.get("hashtags", "")
        post.status = "sent"
        post.updated_at = timezone.now()
        post.save()

        return Response({"success": True})

    except InstagramPost.DoesNotExist:
        return Response(
            {"error": "Post not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    


MODEL_MAP = {
    "InstagramPost": InstagramPost,
    "InstagramReel": InstagramReel,
    "FacebookImagePost": FacebookImagePost,
}


@api_view(['POST'])
@permission_classes([AllowAny])
def generic_callback(request):

    data = request.data

    model_name = data.get("model")
    object_id = data.get("id")
    status_value = data.get("status")

    model = MODEL_MAP.get(model_name)

    if not model:
        return Response(
            {"error": "Invalid model"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        obj = model.objects.get(id=object_id)

        obj.status = status_value
        obj.updated_at = timezone.now()
        obj.save()

        return Response({"success": True})

    except model.DoesNotExist:
        return Response(
            {"error": "Not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )