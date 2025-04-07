from google.cloud import discoveryengine
from google.api_core.client_options import ClientOptions
from commons.domain.constants.env_variables import PROJECT_ID, DATA_STORE_ID, DATA_STORE_LOCATION, DOCUMENT_BUCKET
from commons.domain.constants.domain_constants import DEFAULT_GLOBAL_LOCATION
from commons.domain.utils.utils import generate_gcs_uri

class DataStoreEngineClient:
    def __init__(self, company_folder: str):

        self.project_id = PROJECT_ID
        self.location = DATA_STORE_LOCATION
        self.data_store_id = DATA_STORE_ID

        self.gcs_uri = generate_gcs_uri(DOCUMENT_BUCKET, f"{company_folder}/raw")
        self.data_store_client = self._get_data_store_client()
        self.parent = self._get_parent_branch()

    def _get_client_options(self):
        if self.location != DEFAULT_GLOBAL_LOCATION:
            return ClientOptions(
                api_endpoint=f"{self.location}-discoveryengine.googleapis.com"
            )
        return None

    def _get_data_store_client(self):
        
        return discoveryengine.DocumentServiceClient(
            client_options=self._get_client_options()
        )

    def _get_parent_branch(self):
        return self.data_store_client.branch_path(
            project=self.project_id,
            location=self.location,
            data_store=self.data_store_id,
            branch="default_branch",
        )


    def upload_files_from_bucket(self) -> None:

        try:
            source_documents = [f"{self.gcs_uri}/*"]
            request = discoveryengine.ImportDocumentsRequest(
                parent=self.parent,
                gcs_source=discoveryengine.GcsSource(
                    input_uris=source_documents, data_schema="content"
                ),
                reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
            )

            self.data_store_client.import_documents(request=request)

        except Exception as e:
            raise e

    def delete_file(
                    self, 
                    document_name: str) -> None:
        
        try:
            target_uri = f"{self.gcs_uri}/{document_name}"

            request = discoveryengine.ListDocumentsRequest(parent=self.parent)
            list_response = self.data_store_client.list_documents(request=request)

            document_id = self.get_document_id_by_uri(
                list_response.documents, target_uri
            )

            if document_id:
                datastore_document_name = self.data_store_client.document_path(
                    project=self.project_id,
                    location=self.location,
                    data_store=self.data_store_id,
                    branch="default_branch",
                    document=document_id,
                )

                self.data_store_client.delete_document(name=datastore_document_name)
        except Exception as e:
            raise e
    def get_document_id_by_uri(self, documents, target_uri):
        matching_docs = [doc.id for doc in documents if doc.content.uri == target_uri]
        return matching_docs[0] if matching_docs else None