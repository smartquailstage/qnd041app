import requests
from celery import shared_task
from django.conf import settings


def send(webhook_key, payload):
    url = settings.N8N_WEBHOOKS_A.get(webhook_key)

    if not url:
        raise Exception(f"No webhook configured for {webhook_key}")

    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.text


# =========================
# INSTAGRAM POST
# =========================
@shared_task
def task_instagram_post(payload):
    return send("instagram_post", payload)


# =========================
# INSTAGRAM CAROUSEL
# =========================
@shared_task
def task_instagram_carousel(payload):
    return send("instagram_carousel", payload)


# =========================
# INSTAGRAM REEL
# =========================
@shared_task
def task_instagram_reel(payload):
    return send("instagram_reel", payload)


# =========================
# FACEBOOK IMAGE
# =========================
@shared_task
def task_facebook_image(payload):
    return send("facebook_image", payload)


# =========================
# FACEBOOK VIDEO
# =========================
@shared_task
def task_facebook_video(payload):
    return send("facebook_video", payload)


# =========================
# FACEBOOK CAROUSEL
# =========================
@shared_task
def task_facebook_carousel(payload):
    return send("facebook_carousel", payload)


# =========================
# TWITTER POST
# =========================
@shared_task
def task_twitter_post(payload):
    return send("twitter_post", payload)


# =========================
# LINKEDIN POST
# =========================
@shared_task
def task_linkedin_post(payload):
    return send("linkedin_post", payload)