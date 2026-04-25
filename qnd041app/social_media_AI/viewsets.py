from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.viewsets.base import ViewSetGroup
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

class InstagramPostViewSet(ModelViewSet):
    model = InstagramPost
    menu_label = "Instagram Post"
    icon = "mobile-alt"
    menu_order = 200
    add_to_admin_menu = False

    list_display = ( 
        "prompt",
        "caption",
        "image_thumb",
        "categories",
        "scheduled_date",
        "created_by",
    )
    search_fields = ("caption",)


# 🔥 IMPORTANTE: instancia (NO clase)
instagram_post_viewset = InstagramPostViewSet()
 


class InstagramCarouselViewSet(ModelViewSet):
    model = InstagramCarouselPost

    menu_label = "Instagram Carousels"
    icon = "mobile-alt"
    menu_order = 200
    add_to_admin_menu = False  # 👈 importante
    list_display = (
        "caption",
        "scheduled_date",
        "created_by",
    )
    search_fields = ("caption",)

    form_fields = [
        "image_size",
        "category",
        "caption",
        "copy",
        "hashtags",
        "scheduled_date",
        "created_by",
    ]

instagram_carousel_post_viewset = InstagramCarouselViewSet()

class InstagramReelViewSet(ModelViewSet):
    model = InstagramReel

    menu_label = "Instagram Reels"
    icon = "mobile-alt"
    menu_order = 200
    add_to_admin_menu = False  # 👈 importante
    list_display = (
        "title",
        "caption",
        "scheduled_date",
        "created_by",
    )
    search_fields = ("caption",)
    # 🔥 ESTE ES EL FIX
    form_fields = [
        "title",
        "video",
        "caption",
        "hashtags",
        "scheduled_date",
        "created_by",
    ]
instagram_reel_post_viewset = InstagramReelViewSet()


class FacebookPostViewSet(ModelViewSet):
    model = FacebookImagePost

    menu_label = "Facebook Post"
    icon = "mobile-alt"
    menu_order = 200
    add_to_admin_menu = False  # 👈 importante
    list_display = (
        "post_type",
        "link",
        "scheduled_date",
        "created_by",
    )
    search_fields = ("post_type",)


    form_fields = [
        "post_type",
        "message",
        "link",
        "scheduled_date",
        "created_by",
    ]

facebook_post_viewset = FacebookPostViewSet()

class FacebookVideoPostViewSet(ModelViewSet):
    model = FacebookVideoPost
    menu_label = "Facebook reels"
    icon = "mobile-alt"
    menu_order = 200
    add_to_admin_menu = False

    list_display = (
        "message",
        "scheduled_date",
        "created_by",
    )

    search_fields = ("message",)

    form_fields = [
        "message",
        "video",
        "link",
        "scheduled_date",
        "created_by",
    ]


class FacebookCarouselPostViewSet(ModelViewSet):
    model = FacebookCarouselPost
    menu_label = "Facebook Carousels"
    icon = "mobile-alt"
    menu_order = 300
    add_to_admin_menu = False

    list_display = (
        "message",
        "scheduled_date",
        "created_by",
    )

    search_fields = ("message",)

    form_fields = [
        "message",
        "link",
        "scheduled_date",
        "created_by",
    ]



class TwitterPostViewSet(ModelViewSet):
    model = TwitterPost
    menu_label = " Twitter(X) Post"
    icon = "mobile-alt"
    menu_order = 300
    add_to_admin_menu = False

    list_display = (
        "text",
        "scheduled_date",
        "created_by",
    )

    search_fields = ("text",)

    form_fields = [
        "text",
        "scheduled_date",
        "created_by",
    ]


class LinkedInPostViewSet(ModelViewSet):
    model = LinkedInPost
    menu_label = " LinkedIn Post"
    icon = "mobile-alt"
    menu_order = 300
    add_to_admin_menu = False

    list_display = (
        "content",
        "scheduled_date",
        "created_by",
    )

    search_fields = ("content",)

    form_fields = [
        "content",
        "scheduled_date",
        "created_by",
    ]






class SocialMediaGroup(ViewSetGroup):
    menu_label = "Social Media (+AI)"
    icon = "mobile-alt"
    menu_order = 200
    items = (
        InstagramPostViewSet(),
        FacebookPostViewSet(),
        LinkedInPostViewSet(),
        TwitterPostViewSet(),
        InstagramCarouselViewSet(),
        FacebookCarouselPostViewSet(),
        InstagramReelViewSet(),
        FacebookVideoPostViewSet(),
    )