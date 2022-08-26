from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import ElasticsearchRetriever
from haystack.nodes import FARMReader
from haystack.utils import print_answers
from haystack.pipelines import ExtractiveQAPipeline
from Dictionary_name_txt import getdic


studiengänge_document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="studiengänge")
studiengänge_retriever = ElasticsearchRetriever(document_store=studiengänge_document_store)
studiengänge_reader = FARMReader(model_name_or_path="deepset/gelectra-base-germanquad-distilled", use_gpu=True, num_processes=0)
studiengänge_pipe = ExtractiveQAPipeline(studiengänge_reader, studiengänge_retriever)


mydic = getdic()

def pipe(user_input:str, user):
    studiengang_prediction = studiengänge_pipe.run(query = user_input, params={"Retriever": {"top_k": 10}, "filters": {"name": mydic[f"{user}"]}, "Reader": {"top_k": 5}})
    return studiengang_prediction


test = pipe("Wann kann Katholische Theologie, Mathematik und Rechtswissenschaft gewählt werden?", "archaeologie-ba")


print_answers(test) 
