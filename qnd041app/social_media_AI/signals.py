from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

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
        "scheduled_date": instance.scheduled_date.isoformat() if instance.scheduled_date else None,
    }

@receiver(post_save, sender=InstagramPost)
def ig_post(sender, instance, created, **kwargs):
    # 1. Validación de seguridad: solo si está programado y tiene fecha
    if instance.status == "scheduled" and instance.scheduled_date:
        try:
            payload = serialize(instance)
            ahora = timezone.now()

            if instance.scheduled_date > ahora:
                # PROGRAMADO: Uso correcto de kwargs
                task_instagram_post.apply_async(
                    kwargs={"payload": payload},
                    eta=instance.scheduled_date
                )
                print(f"📌 [Signal] Post {instance.id} programado para {instance.scheduled_date}")
            else:
                # INMEDIATO: Debes pasarlo como keyword argument para que coincida con la tarea
                task_instagram_post.delay(payload=payload)
                print(f"🚀 [Signal] Ejecución inmediata para el post {instance.id}")
        
        except Exception as e:
            # Importante: evitar que un error en el signal rompa el guardado en el Admin
            print(f"❌ [Signal Error] No se pudo procesar el post {instance.id}: {e}")
            
    elif created and instance.status == "draft":
        print(f"📝 [Signal] Post {instance.id} guardado como borrador.")


@receiver(post_save, sender=InstagramCarouselPost)
def ig_carousel(sender, instance, created, **kwargs):
    if instance.status == "scheduled" and instance.scheduled_date:
        try:
            payload = serialize(instance)
            ahora = timezone.now()

            if instance.scheduled_date > ahora:
                # PROGRAMADO
                task_instagram_carousel.apply_async(
                    kwargs={"payload": payload},
                    eta=instance.scheduled_date
                )
                print(f"📌 [Signal] Carousel {instance.id} programado para {instance.scheduled_date}")
            else:
                # INMEDIATO
                task_instagram_carousel.delay(payload=payload)
                print(f"🚀 [Signal] Ejecución inmediata para carousel {instance.id}")

        except Exception as e:
            print(f"❌ [Signal Error] No se pudo procesar el carousel {instance.id}: {e}")

    elif created and instance.status == "draft":
        print(f"📝 [Signal] Carousel {instance.id} guardado como borrador.")
        


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