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
    return {
        "id": instance.id,
        "model": instance.__class__.__name__,
        "caption": getattr(instance, "caption", "") or getattr(instance, "message", ""),
        "scheduled_date": str(getattr(instance, "scheduled_date", None)),
        "created_by": getattr(instance.created_by, "id", None),
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