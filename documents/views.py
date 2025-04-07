import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .domain.models.document_info import DocumentInfo
from .domain.models.data_store_info import DataStoreInfo
from .application.service import Service
from commons.domain.repository.data_store import DataStoreEngineClient

@method_decorator(csrf_exempt, name='dispatch')
class DocumentListAPI(APIView):

    authentication_classes = []     
    permission_classes = []
    throttle_classes = [AnonRateThrottle]

    def post(self, request):

        try:
            document_info = DocumentInfo(**request.data)
            company_sub_folder = f"{document_info.company_id}/raw"
            url = Service.generate_url(document_info.file_name, company_sub_folder)
            return Response(
                {
                    "status": "successful",
                    "url": url,
                    "details": "",
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {
                    "error": "Error uploading file to cloud storage",
                    "url": "",
                    "details": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

@method_decorator(csrf_exempt, name='dispatch')
class DataStoreAPI(APIView):

    authentication_classes = []     
    permission_classes = []
    throttle_classes = [AnonRateThrottle]

    def post(self, request):

        try:
            data_store_info = DataStoreInfo(**request.data)
            data_store_client = DataStoreEngineClient(data_store_info.company_id)
            data_store_client.upload_files_from_bucket()

            return Response(
                {
                    "status": "successful"
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {
                    "error": "Error uploading file to cloud storage",
                    "url": "",
                    "details": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )