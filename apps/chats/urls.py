from django.urls import path
from apps.chats.views import (
    ConversationListView,
    MessageListView,
    ConversationAssignView,
    ConversationResolveView,
)

app_name = "chats"

urlpatterns = [
    path("conversations/", ConversationListView.as_view(), name="conversation_list"),
    path(
        "conversations/<uuid:conversation_id>/messages/",
        MessageListView.as_view(),
        name="message_list",
    ),
    path(
        "conversations/<uuid:conversation_id>/assign/",
        ConversationAssignView.as_view(),
        name="conversation_assign",
    ),
    path(
        "conversations/<uuid:conversation_id>/resolve/",
        ConversationResolveView.as_view(),
        name="conversation_resolve",
    ),
]
