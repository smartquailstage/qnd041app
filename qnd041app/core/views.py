# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SocialAutomationPost


@csrf_exempt
def social_callback(request):
    """
    Endpoint que recibe el callback de n8n después de generar contenido.
    """
    try:
        data = json.loads(request.body)

        post_id = data.get("id")
        if not post_id:
            return JsonResponse({"error": "Missing post id"}, status=400)

        post = SocialAutomationPost.objects.get(id=post_id)

        # Actualizamos campos si vienen
        post.generated_caption = data.get("caption", post.generated_caption)
        post.generated_image_url = data.get("image_url", post.generated_image_url)
        post.meta_post_id = data.get("meta_post_id", post.meta_post_id)
        post.status = data.get("status", post.status)

        post.save()

        return JsonResponse({"ok": True})

    except SocialAutomationPost.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)