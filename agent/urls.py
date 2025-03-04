from django.urls import path
from .views import AgentConversationAPI

urlpatterns = [
    path("streaming-chat", AgentConversationAPI.as_view(), name="chat_api"),
]
