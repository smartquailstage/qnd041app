import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import InstagramPost, InstagramReel, FacebookImagePost,InstagramAccount


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



import requests
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from wagtail.images import get_image_model
from .models import InstagramPost, InstagramAccount, CategoryItem

Image = get_image_model()

@csrf_exempt
@require_POST
def n8n_instagram_webhook(type_self, request):
    
    auth_header = request.headers.get('Authorization', '')
    expected_token = f"Bearer {settings.N8N_SECRET}"
    
    if auth_header != expected_token:
        return JsonResponse({'error': 'No autorizado'}, status=401)

    try:
        import json
        data = json.loads(request.body)

        caption = data.get('caption', '')
        copy = data.get('copy', '')
        hashtags = data.get('hashtags', '')
        image_url = data.get('image_url', '') # URL externa enviada desde n8n
        account_id = data.get('account_id')
        category_id = data.get('category_id')
        scheduled_date = data.get('scheduled_date') # Formato ISO o YYYY-MM-DD HH:MM

        # Instanciar cuenta y categoría opcionales
        account = InstagramAccount.objects.filter(id=account_id).first() if account_id else None
        category = CategoryItem.objects.filter(id=category_id).first() if category_id else None

        # 1. Crear el post base
        post = InstagramPost.objects.create(
            caption=caption,
            copy=copy,
            hashtags=hashtags,
            account=account,
            categories=category,
            image_size='square', # Valor por defecto
            scheduled_date=scheduled_date,
            status='scheduled' if scheduled_date else 'draft'
        )

        # 2. Descargar y vincular la imagen si n8n provee una URL
        if image_url:
            response = requests.get(image_url)
            if response.status_code == 200:
                file_name = image_url.split('/')[-1].split('?')[0] or f"ig_post_{post.id}.jpg"
                image_file = ContentFile(response.content)
                
                # Crear imagen en el gestor nativo de Wagtail
                wagtail_image = Image(title=f"Auto n8n - Post {post.id}")
                wagtail_image.file.save(file_name, image_file, save=True)
                
                # Asignarla al post
                post.image = wagtail_image
                post.save()

        return JsonResponse({
            'success': True, 
            'message': 'Post de Instagram creado y sincronizado exitosamente',
            'post_id': post.id
        }, status=201)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)