from django.urls import path
from .views import DocumentListAPI

urlpatterns = [
    path("upload", DocumentListAPI.as_view(), name="list_document_api"),
]
