import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Conversation, Message


from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def whatsapp_verify(request):

    verify_token = settings.WHATSAPP_BUSINESS_API

    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == verify_token:
        return JsonResponse(int(challenge), safe=False)

    return JsonResponse(
        {"error": "Invalid token"},
        status=403
    )



@csrf_exempt
def whatsapp_webhook(request):

    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:

        data = json.loads(request.body)

        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        if "messages" not in value:
            return JsonResponse({"status": "ignored"})

        message_data = value["messages"][0]

        phone = message_data["from"]
        message_text = message_data["text"]["body"]

        # nombre usuario
        contacts = value.get("contacts", [])
        username = contacts[0]["profile"]["name"] if contacts else "Unknown"

        # convertir formato Ecuador
        if not phone.startswith("+"):
            phone = f"+{phone}"

        # buscar o crear conversación
        conversation, created = Conversation.objects.get_or_create(
            phone=phone,
            defaults={
                "username": username,
                "interaction_type": "info",
                "sentiment": "neutral"
            }
        )

        # guardar mensaje usuario
        Message.objects.create(
            conversation=conversation,
            role="user",
            content=message_text
        )

        return JsonResponse({
            "status": "received"
        })

    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
        