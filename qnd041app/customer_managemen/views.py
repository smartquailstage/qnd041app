from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny  # Importante
from django.utils import timezone
from .models import Conversation, Message, LeadTemperatureChoices

class WebhookMessageAPIView(APIView):
    """
    Endpoint para recibir y actualizar datos desde n8n.
    """
    # Sobrescribimos la política de permisos global para permitir solicitudes de n8n
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        platform = data.get("platform")
        platform_user_id = data.get("platform_user_id")
        contact_name = data.get("contact_name", "")
        message_content = data.get("content")
        sender_type = data.get("sender_type", "user")
        
        ai_temperature = data.get("temperature")
        should_convert = data.get("should_convert_ticket", False)

        if not platform or not platform_user_id or not message_content:
            return Response(
                {"error": "Faltan parámetros obligatorios (platform, platform_user_id, content)"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1. Obtener o crear conversación
        conversation, created = Conversation.objects.get_or_create(
            platform=platform,
            platform_user_id=platform_user_id,
            defaults={"contact_name": contact_name}
        )
        
        if contact_name and not conversation.contact_name:
            conversation.contact_name = contact_name
            conversation.save(update_fields=['contact_name'])

        # 2. Registrar el mensaje en la base de datos
        Message.objects.create(
            conversation=conversation,
            sender_type=sender_type,
            content=message_content,
            timestamp=timezone.now()
        )

        # 3. Actualizar temperatura evaluada por la IA
        if ai_temperature in [choice[0] for choice in LeadTemperatureChoices.choices]:
            conversation.temperature = ai_temperature

        # 4. Convertir a ticket si la IA lo determina
        if should_convert and not conversation.converted_to_ticket:
            conversation.convert_to_ticket()
        else:
            conversation.save()  # Guarda cambios de temperatura y actualiza 'is_hot'

        return Response({
            "status": "success",
            "conversation_id": conversation.id,
            "temperature": conversation.temperature,
            "is_hot": conversation.is_hot,
            "converted_to_ticket": conversation.converted_to_ticket
        }, status=status.HTTP_200_OK)