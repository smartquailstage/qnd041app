import requests
from celery import shared_task
from django.conf import settings
from .models import SocialAutomationPost


@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def send_post_to_n8n(self, post_id):
    try:
        post = SocialAutomationPost.objects.get(id=post_id)

        # Idempotencia: evitar doble envío
        if post.status not in ["pending", "error"]:
            return "Already processed"

        payload = {
            "id": post.id,
            "title": post.title,
            "prompt": post.prompt,
            "brand_voice": post.brand_voice,
            "platform": post.target_platform,
            "go_live_at": post.go_live_at.isoformat() if post.go_live_at else None,
            "secret": settings.N8N_SECRET,
        }

        response = requests.post(
            settings.N8N_WEBHOOK_URL,
            json=payload,
            timeout=15
        )

        if response.status_code == 200:
            post.status = "processing"
            post.save()
        else:
            raise Exception("Bad response from n8n")

    except Exception as exc:
        post.status = "error"
        post.save()
        raise self.retry(exc=exc)