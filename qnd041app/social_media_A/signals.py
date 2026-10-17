from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    InstagramPost,
    InstagramCarouselPost,
    InstagramReel,
    FacebookImagePost,
    FacebookVideoPost,
    FacebookCarouselPost,
    TwitterPost,
    LinkedInPost,
)

from .tasks import (
    task_instagram_post,
    task_instagram_carousel,
    task_instagram_reel,
    task_facebook_image,
    task_facebook_video,
    task_facebook_carousel,
    task_twitter_post,
    task_linkedin_post,
)


def serialize(instance):
    """Serializa los datos comunes y específicos de cualquier post para n8n."""
    return {
        "id": instance.id,
        "model": instance.__class__.__name__,
        "status": getattr(instance, "status", "draft"),
        "caption": getattr(instance, "caption", "") or getattr(instance, "message", ""),
        "copy": getattr(instance, "copy", ""),
        "hashtags": getattr(instance, "hashtags", ""),
        "image_size": getattr(instance, "image_size", "square"),
        "scheduled_date": instance.scheduled_date.isoformat() if getattr(instance, "scheduled_date", None) else None,
        "created_by": instance.created_by.username if getattr(instance, "created_by", None) else None,
        
        # URL de la imagen si el modelo la soporta
        "image_url": instance.image.file.url if hasattr(instance, "image") and instance.image else None,
        
        # Cuenta asociada (si el modelo la tiene)
        "account_id": instance.account.account_id if hasattr(instance, "account") and instance.account else None,
        "account_name": instance.account.account_name if hasattr(instance, "account") and instance.account else None,
        
        # Categoría asociada
        "category_id": instance.categories.id if hasattr(instance, "categories") and instance.categories else (
            instance.category.id if hasattr(instance, "category") and instance.category else None
        ),
    }


@receiver(post_save, sender=InstagramPost)
def ig_post(sender, instance, created, **kwargs):
    if created:
        task_instagram_post.delay(serialize(instance))


@receiver(post_save, sender=InstagramCarouselPost)
def ig_carousel(sender, instance, created, **kwargs):
    if created:
        task_instagram_carousel.delay(serialize(instance))


@receiver(post_save, sender=InstagramReel)
def ig_reel(sender, instance, created, **kwargs):
    if created:
        task_instagram_reel.delay(serialize(instance))


@receiver(post_save, sender=FacebookImagePost)
def fb_image(sender, instance, created, **kwargs):
    if created:
        task_facebook_image.delay(serialize(instance))


@receiver(post_save, sender=FacebookVideoPost)
def fb_video(sender, instance, created, **kwargs):
    if created:
        task_facebook_video.delay(serialize(instance))


@receiver(post_save, sender=FacebookCarouselPost)
def fb_carousel(sender, instance, created, **kwargs):
    if created:
        task_facebook_carousel.delay(serialize(instance))


@receiver(post_save, sender=TwitterPost)
def twitter(sender, instance, created, **kwargs):
    if created:
        task_twitter_post.delay(serialize(instance))


@receiver(post_save, sender=LinkedInPost)
def linkedin(sender, instance, created, **kwargs):
    if created:
        task_linkedin_post.delay(serialize(instance))