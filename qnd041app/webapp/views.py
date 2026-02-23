# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SocialAutomationPost


@csrf_exempt
def social_callback(request):
    data = json.loads(request.body)

    post = SocialAutomationPost.objects.get(id=data["id"])

    post.generated_caption = data.get("caption")
    post.generated_image_url = data.get("image_url")
    post.meta_post_id = data.get("meta_post_id")
    post.status = data.get("status")

    post.save()

    return JsonResponse({"ok": True})