import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import InstagramPost, InstagramReel, FacebookImagePost


MODEL_MAP = {
    "InstagramPost": InstagramPost,
    "InstagramReel": InstagramReel,
    "FacebookImagePost": FacebookImagePost,
}


@csrf_exempt
def n8n_webhook_callback(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    data = json.loads(request.body)

    model_name = data.get("model")
    object_id = data.get("id")
    status = data.get("status")  # sent | failed
    message = data.get("message", "")

    model = MODEL_MAP.get(model_name)

    if not model:
        return JsonResponse({"error": "Invalid model"}, status=400)

    try:
        obj = model.objects.get(id=object_id)

        obj.status = status
        obj.updated_at = timezone.now()
        obj.save(update_fields=["status", "updated_at"])

        return JsonResponse({"ok": True})

    except model.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)