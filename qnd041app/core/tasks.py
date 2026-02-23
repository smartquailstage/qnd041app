import requests
from celery import shared_task
from django.conf import settings
from .models import SocialAutomationPost


from celery import shared_task
from core.models import SocialAutomationPost
import requests
from django.conf import settings

@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def send_post_to_n8n(self, post_id):
    post = SocialAutomationPost.objects.get(id=post_id)

    # Idempotencia
    if post.status not in ["pending", "error"]:
        return "Already processed"

    payload = {
        "id": post.id,
        "title": post.prompt[:50],  # snippets no tienen title
        "prompt": post.prompt,
        "brand_voice": post.brand_voice,
        "platform": "both",  # o agrega un campo platform en tu modelo
        "go_live_at": post.scheduled_datetime.isoformat() if post.scheduled_datetime else None,
        "secret": settings.N8N_SECRET,
    }

    try:
        response = requests.post(
            settings.N8N_WEBHOOK_URL,
            json=payload,
            timeout=15
        )
        if response.status_code == 200:
            post.status = "processing"
        else:
            post.status = "error"
        post.save()
    except Exception as exc:
        post.status = "error"
        post.save()
        raise self.retry(exc=exc)