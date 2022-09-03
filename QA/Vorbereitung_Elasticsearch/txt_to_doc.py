from haystack.utils import print_answers
from haystack.nodes import PreProcessor
from haystack.utils import convert_files_to_docs, print_answers


def getdocs():
    """
    The function takes all the txt files in the folder "1. all txt" and splits them into smaller
    documents of 200 sentences each. 
    
    The function returns a list of all the documents
    
    Returns:
      A list of documents
    """
    all_txt = convert_files_to_docs(dir_path="txt/1. all txt", encoding="utf-8")
    print(all_txt)

    txt_preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=False,
        split_by="sentence", # Dokument wird anhand von Sätzen getrennt
        split_length=200, # Nach 200 Sätzen erfolgt die Trennung -> ein Dokument besteht aus 200 Sätzen
        split_overlap = 2, # 2 Sätze Überlappung bei den einzelnen Dokumenten
        split_respect_sentence_boundary = False,
        language="de"
    )
    nested_docs = [txt_preprocessor.process(doc) for doc in all_txt]
    all_docs = [doc for x in nested_docs for doc in x]
    
    print(f"n_files_input: {len(all_txt)}\nn_docs_output: {len(all_docs)}")
    return all_docs
    
    
