from wagtail import hooks
from .viewsets import ConversationViewSet

@hooks.register('register_admin_viewset')
def register_conversation_viewset():
    return ConversationViewSet('conversations')