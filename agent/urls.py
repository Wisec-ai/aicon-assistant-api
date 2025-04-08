from django.urls import path
from .views.agent_conversation import AgentConversationAPI
from .views.session import SessionAPI

urlpatterns = [
    path("streaming-chat", AgentConversationAPI.as_view(), name="chat_api"),
    path("generate-session", SessionAPI.as_view(), name="session_api"),
]
