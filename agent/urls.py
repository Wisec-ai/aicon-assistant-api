from django.urls import path
from .views import AgentConversationAPI

urlpatterns = [
    path("", AgentConversationAPI.as_view(), name="chat_api"),
]
