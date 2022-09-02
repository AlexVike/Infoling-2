from haystack.document_stores import ElasticsearchDocumentStore
from txt_to_doc import getdocs


# Creating a document store and writing the documents to it.
studiengänge_document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="studiengänge")

studiengänge_document_store.write_documents(getdocs())