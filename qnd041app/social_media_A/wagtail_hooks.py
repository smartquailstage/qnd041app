from wagtail import hooks
from .viewsets import SocialMediaGroup


@hooks.register("register_admin_viewset")
def register_viewsets():
    return SocialMediaGroup()