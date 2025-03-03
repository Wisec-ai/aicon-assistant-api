from django.urls import path
from .views import DocumentListAPI

urlpatterns = [
    path("", DocumentListAPI.as_view(), name="list_document_api"),
]
