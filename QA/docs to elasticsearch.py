from haystack.document_stores import ElasticsearchDocumentStore
from txt_to_doc import getdocs


studiengänge_document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="studiengänge")

studiengänge_document_store.write_documents(getdocs())