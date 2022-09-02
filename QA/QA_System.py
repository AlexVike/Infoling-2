from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import ElasticsearchRetriever
from haystack.nodes import FARMReader
from haystack.utils import print_answers
from haystack.pipelines import ExtractiveQAPipeline
import os
import fnmatch
from collections import defaultdict


def getdic():
    """
    It walks through the directory tree, and for each file in the tree, it adds the file to a list in a
    dictionary, where the key is the name of the directory the file is in
    
    Returns:
      A dictionary with the names of the folders as keys and the names of the files in the folders as
    values.
    """
    dic_studiengänge = defaultdict(list)
    for path, dirs, files in os.walk(f'{os.getcwd()}/txt'):
        for f in fnmatch.filter(files, '*.txt'):
            dic_studiengänge[os.path.basename(path)].append(f)
    return dic_studiengänge


mydic = getdic()


# Creating a pipeline for the study programs.
studiengänge_document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="studiengänge")
studiengänge_retriever = ElasticsearchRetriever(document_store=studiengänge_document_store)
studiengänge_reader = FARMReader(model_name_or_path="QA/Finetuning/my_model", use_gpu=True, num_processes=0)
studiengänge_pipe = ExtractiveQAPipeline(studiengänge_reader, studiengänge_retriever)

def pipe(user_input: str, studiengang):
    """
    The function takes a user input and a studiengang as parameters and returns the top 3 predictions
    for the studiengang
    
    Args:
      user_input (str): str = the user's input
      studiengang: the name of the study program
    
    Returns:
      The answer for the question
    """
    studiengang_prediction = studiengänge_pipe.run(query=user_input, params={"Retriever": {"top_k": 10}, "filters": {"name": mydic[f"{studiengang}"]}, "Reader": {"top_k": 3}})
    return studiengang_prediction