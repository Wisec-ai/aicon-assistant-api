from django.urls import path
from .views import DocumentListAPI
from .views import DataStoreAPI

urlpatterns = [
    path("upload", DocumentListAPI.as_view(), name="list_document_api"),
    path("upload-data-store", DataStoreAPI.as_view(), name="upload_data_stor")
]
