from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny  # Importante
from django.utils import timezone
from .models import Conversation, Message, LeadTemperatureChoices
from .models import WhatsAppConversation, WhatsAppMessage, LeadTemperatureChoices
from .models import FacebookConversation, FacebookMessage, LeadTemperatureChoices

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




class WebhookWhatsAppMessageAPIView(APIView):
    """
    Endpoint para recibir y almacenar mensajes y estados de temperatura desde n8n (WhatsApp).
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        platform = data.get("platform", "whatsapp")
        whatsapp_phone_number = data.get("platform_user_id") # O 'whatsapp_phone_number'
        contact_name = data.get("contact_name", "")
        message_content = data.get("content")
        sender_type = data.get("sender_type", "user")
        
        ai_temperature = data.get("temperature")
        should_convert = data.get("should_convert_ticket", False)

        if not whatsapp_phone_number or not message_content:
            return Response(
                {"error": "Faltan parámetros obligatorios (platform_user_id/whatsapp_phone_number, content)"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1. Obtener o crear conversación de WhatsApp
        conversation, created = WhatsAppConversation.objects.get_or_create(
            whatsapp_phone_number=whatsapp_phone_number,
            defaults={"platform": platform, "contact_name": contact_name}
        )
        
        if contact_name and not conversation.contact_name:
            conversation.contact_name = contact_name
            conversation.save(update_fields=['contact_name'])

        # 2. Registrar el mensaje en la tabla hija
        WhatsAppMessage.objects.create(
            conversation=conversation,
            sender_type=sender_type,
            content=message_content,
            timestamp=timezone.now()
        )

        # 3. Actualizar temperatura evaluada por la IA
        if ai_temperature in [choice[0] for choice in LeadTemperatureChoices.choices]:
            conversation.temperature = ai_temperature

        # 4. Convertir a ticket si corresponde
        if should_convert and not conversation.converted_to_ticket:
            conversation.convert_to_ticket()
        else:
            conversation.save()

        return Response({
            "status": "success",
            "conversation_id": conversation.id,
            "temperature": conversation.temperature,
            "is_hot": conversation.is_hot,
            "converted_to_ticket": conversation.converted_to_ticket
        }, status=status.HTTP_200_OK)




class WebhookFacebookMessageAPIView(APIView):
    """
    Endpoint para recibir y almacenar mensajes y estados de temperatura desde n8n (Facebook Messenger).
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        platform = data.get("platform", "facebook")
        facebook_psid = data.get("platform_user_id") # Corresponde al PSID de Facebook
        contact_name = data.get("contact_name", "")
        message_content = data.get("content")
        sender_type = data.get("sender_type", "user")
        
        ai_temperature = data.get("temperature")
        should_convert = data.get("should_convert_ticket", False)

        if not facebook_psid or not message_content:
            return Response(
                {"error": "Faltan parámetros obligatorios (platform_user_id/facebook_psid, content)"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1. Obtener o crear conversación de Facebook
        conversation, created = FacebookConversation.objects.get_or_create(
            facebook_psid=facebook_psid,
            defaults={"platform": platform, "contact_name": contact_name}
        )
        
        if contact_name and not conversation.contact_name:
            conversation.contact_name = contact_name
            conversation.save(update_fields=['contact_name'])

        # 2. Registrar el mensaje en la tabla hija
        FacebookMessage.objects.create(
            conversation=conversation,
            sender_type=sender_type,
            content=message_content,
            timestamp=timezone.now()
        )

        # 3. Actualizar temperatura evaluada por la IA
        if ai_temperature in [choice[0] for choice in LeadTemperatureChoices.choices]:
            conversation.temperature = ai_temperature

        # 4. Convertir a ticket si corresponde
        if should_convert and not conversation.converted_to_ticket:
            conversation.convert_to_ticket()
        else:
            conversation.save()

        return Response({
            "status": "success",
            "conversation_id": conversation.id,
            "temperature": conversation.temperature,
            "is_hot": conversation.is_hot,
            "converted_to_ticket": conversation.converted_to_ticket
        }, status=status.HTTP_200_OK)