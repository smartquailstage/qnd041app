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


@receiver(post_save, sender=InstagramPost)
def ig_post(sender, instance, created, **kwargs):
    # Solo actuamos si el post se acaba de crear o si se marca como 'scheduled'
    if instance.status == "scheduled" and instance.scheduled_date:
        payload = serialize(instance)
        ahora = timezone.now()

        if instance.scheduled_date > ahora:
            # 1. PROGRAMADO: La tarea se queda en Redis hasta la fecha fijada
            task_instagram_post.apply_async(
                kwargs={"payload": payload},
                eta=instance.scheduled_date
            )
            print(f"📌 [Signal] Post {instance.id} programado para {instance.scheduled_date}")
        else:
            # 2. INMEDIATO: La fecha ya pasó o es para ahora mismo
            task_instagram_post.delay(payload)
            print(f"🚀 [Signal] Ejecución inmediata para el post {instance.id}")
            
    elif created and instance.status == "draft":
        # Opcional: Si quieres que al crear un borrador no pase nada, 
        # lo dejas pasar. La tarea se disparará cuando cambien el estado a 'scheduled'.
        print(f"📝 [Signal] Post {instance.id} guardado como borrador.")


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