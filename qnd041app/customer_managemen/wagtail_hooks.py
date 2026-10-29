from wagtail import hooks
from .viewsets import OmnichannelGroup

@hooks.register('register_admin_viewset')
def register_omnichannel_group():
    return OmnichannelGroup()