# Ein Question-Answer Ratgeber für Studiengänge an der Universität Regensburg

- [00-Requierements](https://github.com/AlexVike/Infoling-2/tree/main/Conda_pip_requierements)
- [01-HTML to txt](https://github.com/AlexVike/Infoling-2/tree/main/Hmtl%20to%20txt)
- [02-PDF to txt](https://github.com/AlexVike/Infoling-2/tree/main/pdf%20to%20txt)
- [03-Txt](https://github.com/AlexVike/Infoling-2/tree/main/txt)
- [04-QA](https://github.com/AlexVike/Infoling-2/tree/main/QA)
- [04-WSGI_App](https://github.com/AlexVike/Infoling-2/tree/main/wsgi_app)

## Instalation des Systems

Um das QA System benutzen zu können, muss man die [Requierements](https://github.com/AlexVike/Infoling-2/tree/main/Conda_pip_requierements) (etnweder conda, oder  pip) installieren. Daraufhin benötigt man die Datenbank. Um diese benutzen zu können muss zunächst [Docker](https://www.docker.com/products/docker-desktop/) installiert werden. Daraufhin kann [hier](https://hub.docker.com/r/alexvike/infoling2/tags) das Docker Image heruntergeladen werden. Nun muss die Datenbank über Docker gestartet werden. Falls der Vorgang Probleme macht kann mithilfe des [Codes](https://github.com/AlexVike/Infoling-2#elasticsearch) und Docker die Datenbank selbst erstellt werden. Sobald die Datenbank gestartet wurde, kann `main.py` ausgeführt werden. Mit dem Befehl `ipconfig` kann im Terminal die IPv4-Adresse überprüft werden. Diese kann im Browser eingegeben werden. Nun können Fragen gestellt werden.

## Scraping des Datensatzes
Als aller erstes musste der Datensatz für das Projekt gescraped werden. Dies erfolgte in 2 Schritten.

Zuerst wurden alle Links die für das Projekt in Frage kommen der [Universitätswebseite](https://www.uni-regensburg.de/studium/studienangebot/studiengaenge-a-z) in einer Liste abgespeichert. Wichtig war, dass es nur Studiengänge sind, die man Erststudium absolvieren kann.
```ruby
html = urlopen("https://www.uni-regensburg.de/studium/studienangebot/studiengaenge-a-z")
soup = BeautifulSoup(html.read(), 'lxml')
links = []
for link in soup.find_all('a'):
  if "schule/index.html" in str(link) or "-ba/index.html" in str(link) or "-bsc/index.html" in str(link):
     links.append(link.get('href'))
```

Mithilfe der Links kann nun der Inhalt der Webseiten gescraped werden. Da nur der Text wichtig ist werden die HTML Tags gelöscht. Daraufhin wird ein Ordner für die Webseite erstellt und die Text Datei darin gespeichert.
```ruby
for webseite in links:
  name = webseite.split("/")[-2]
  try:
    url = f"https://www.uni-regensburg.de{webseite}"
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
  except:
     url = f"{webseite}"
     html = urlopen(url).read()
     soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
  for script in soup(["script", "style"]):
      script.extract()    # rip it out

  
  text = soup.get_text().replace("nach oben", "") 

# break into lines and remove leading and trailing space on each
  lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
  chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
  text = '\n'.join(chunk for chunk in chunks if chunk)
  
   
#Creating a directory for each link and saving the text of the website in a txt file.
  directory = f"{name}"


  parent_dir = "C:/Users/Alexa/OneDrive/Desktop/Infolin2/txt"


  path = os.path.join(parent_dir, directory)

  if not os.path.isdir(path): 
    os.mkdir(path) 
  with open(f"{path}/{name}.txt", "w",encoding="utf-8" ) as file:
    file.write(f"{text}")
    file.flush()
```
Im zweiten Schritt wurden die Modulkataloge und Prüfungsordnungen der Studiengänge heruntergeladen. Da diese teilweise auf den verschiedenen Webseiten verteilt waren, wurden diese händisch heruntergeladen. Daraufhin wurde versucht mit dem `PDFToTextConverter()` von Haystack die PDFs umzuwandeln damit diese in das Doc-Format umgwandelt werden können, welches bei Haystack benötigt wird. Wegen der Formatierung mancher PDFs der Universität war dies jedoch nicht möglich. Aus diesen Grund wurde `pdfplumber` und `OCR` benutzt, um die PDFs in Textdateien umzuwandeln. Falls eine PDF Datei nicht von `pdfplumber` umgewandelt werden konnte wurde `OCR` verwendet.

`pdfplumber`:
```ruby
import pdfplumber as pdfp
import sys

pdf_path = getpdfspaths()
pdf_path = pdf_path[198:] # Ein Feher ist aufgetreten, bei der Konvertierung von einem PDF zu Text. Nach Behebung des Fehlers ab 198 nochmal durchgelaufen.
for abspath in pdf_path:
	print(f"scanning file {pdf_path.index(abspath)+1} of {len(pdf_path)}")
	pdfToString = ""
	with pdfp.open(abspath) as pdf:
		for page in pdf.pages:
			pdfToString += page.extract_text()
	size = sys.getsizeof(pdfToString)
	abspath_target ="/".join(abspath.split("/")[:-2])
	file_name = abspath.split("/")[-1].replace(".pdf", ".txt")
	if size > 500: # Bei einem PDF welches nicht mit pdfplumber konvertiert werden konnte, wird OCR verwendet.
    
		print(abspath_target+"/"+file_name)
		file = open(abspath_target+"/"+file_name,"w", encoding="utf-8")
		file.write("%s = %s\n" %("input_dictionary", pdfToString))
	
		file.close()
		
	
		
	else:
		print("Using OCR")
		ocr(abspath, abspath_target, file_name) 
```

`OCR`:
```ruby
# Quelle für OCR: https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/?ref=lbp

import platform
from tempfile import TemporaryDirectory
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

if platform.system() == "Windows":

  pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
  )

  # Windows also needs poppler_exe
  path_to_poppler_exe = Path(r"C:\Users\Alexa\OneDrive\Desktop\UE\Infoling-2\pdf to txt\poppler-22.04.0\Library\bin")
  
  
  out_directory = Path(r"~\Desktop").expanduser()
else:
  out_directory = Path("~").expanduser()  
  
  
  
def ocr(pdf, targetdir, targetfilename):
  ''' Main execution point of the program'''
  PDF_file = pdf
  image_file_list = []
  with TemporaryDirectory() as tempdir:
    # Create a temporary directory to hold our temporary images.

    """
    Part #1 : Converting PDF to images
    """

    if platform.system() == "Windows":
      pdf_pages = convert_from_path(
        PDF_file, 500, poppler_path=path_to_poppler_exe
      )
    else:
      pdf_pages = convert_from_path(PDF_file, 500)
    # Read in the PDF file at 500 DPI

    # Iterate through all the pages stored above
    for page_enumeration, page in enumerate(pdf_pages, start=1):
      # enumerate() "counts" the pages for us.

      # Create a file name to store the image
      filename = f"{tempdir}\page_{page_enumeration:03}.jpg"

      # Declaring filename for each page of PDF as JPG
      # For each page, filename will be:
      # PDF page 1 -> page_001.jpg
      # PDF page 2 -> page_002.jpg
      # PDF page 3 -> page_003.jpg
      # ....
      # PDF page n -> page_00n.jpg

      # Save the image of the page in system
      page.save(filename, "JPEG")
      image_file_list.append(filename)

    """
    Part #2 - Recognizing text from the images using OCR
    """

    with open(targetdir+"/"+targetfilename,"w", encoding="utf-8") as output_file:
      # Open the file in append mode so that
      # All contents of all images are added to the same file

      # Iterate from 1 to total number of pages
      for image_file in image_file_list:
        text = str(((pytesseract.image_to_string(Image.open(image_file)))))

        # The recognized text is stored in variable text
        # Any string processing may be applied on text
        # Here, basic formatting has been done:
        # In many PDFs, at line ending, if a word can't
        # be written fully, a 'hyphen' is added.
        # The rest of the word is written in the next line
        # Eg: This is a sample text this word here GeeksF-
        # orGeeks is half on first line, remaining on next.
        # To remove this, we replace every '-\n' to ''.
        # text = text.replace("-\n", "")

        # Finally, write the processed text to the file.
        output_file.write(text)

      # At the end of the with .. output_file block
      # the file is closed after writing all the text.
    # At the end of the with .. tempdir block, the
    # TemporaryDirectory() we're using gets removed!  
  # End of main function!
```

Nun wurden alle Textdateien in einem Ordner abegspeichert, damit diese im nächsten Schritt umgwandelt werden können, so dass sie der Datenbank übergeben werden können.
```ruby
import shutil

default_path = "C:/Users/Alexa/OneDrive/Desktop/UE/Infoling-2/txt"
pdfabspath = []
for item in os.listdir(default_path): #Fachordner = item
   if os.path.isdir(default_path + "/" + item): 
      for element in os.listdir(default_path + "/" + item): 
         if "txt" in element:
            src_path = default_path + "/" + item + "/" + element
            dst_path = "C:/Users/Alexa/OneDrive/Desktop/UE/Infoling-2/txt/1. all txt"
            shutil.copy(src_path, dst_path)
            print(default_path + "/" + item + "/" + element + ":wurde kopiert!")
```
## Elasticsearch
Die Textdateien sollen nun der Datenbank übergeben werden. Dafür werden sie zunächst mit `convert_files_to_docs()` zu Docs umgewandelt. Diese werden dann mit dem `PreProcessor()` weiterverarbeitet.

```ruby
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
    all_txt = convert_files_to_docs(dir_path="C:/Users/Alexa/OneDrive/Desktop/UE/Infoling-2/txt/1. all txt", encoding="utf-8")
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
```
Anschließend wird die Datenbank initialisiert und die Docs werden übergeben. Durch Docker wurde ein Docker-Image geladen und für die Datenbank ausgeführt .
```ruby
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.9.2
docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.9.2
```
```ruby
from haystack.document_stores import ElasticsearchDocumentStore
from txt_to_doc import getdocs


# Creating a document store and writing the documents to it.
studiengänge_document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="studiengänge")

studiengänge_document_store.write_documents(getdocs())
```

## QA-System
Nun wurde die Pipeline für das QA-System erstellt.
```ruby
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import ElasticsearchRetriever
from haystack.nodes import FARMReader
from haystack.utils import print_answers
from haystack.pipelines import ExtractiveQAPipeline

# Creating a pipeline for the study programs.
studiengänge_document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="studiengänge")
studiengänge_retriever = ElasticsearchRetriever(document_store=studiengänge_document_store)
studiengänge_reader = FARMReader(model_name_or_path="QA/Finetuning/my_model", use_gpu=True, num_processes=0)
studiengänge_pipe = ExtractiveQAPipeline(studiengänge_reader, studiengänge_retriever)
```
Damit das QA-System nur einen Studiengang übergeben bekommt wurde ein Dictionary erstellt. Der Ordner Name der Studiengänge dient dabei als Schlüssel und die Textdateien werden dem Schlüssel als Liste übergeben.

```ruby
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

```
```ruby
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
```

## Finetuning
Das Modell `deepset/gelectra-base-germanquad-distilled` wurde mit einem Datensatz, der mithilfe des [Annotationstools von Haystack](https://annotate.deepset.ai/) erstellt wurde, gefinetuned.
```ruby
from haystack.nodes import FARMReader


# Das Model deepset/gelectra-base-germanquad-distilled wird mit unseren Daten gefinetuned.
reader = FARMReader(model_name_or_path="deepset/gelectra-base-germanquad-distilled", use_gpu=True, num_processes=1)
data_dir = "QA/finetuning_data"

reader.train(data_dir=data_dir, train_filename="training_data_finetuning.json", use_gpu=True, n_epochs=1, save_dir="QA/my_model", num_processes=1)
# Das Model wird abgespeichert und für das Projekt verwendet.
reader.save(directory="QA/my_model")
new_reader = FARMReader(model_name_or_path="QA/my_model")
```

## Evaluation
Auch bei der Evaluation ist ein Datensatz, der mit dem [Annotationstool von Haystack](https://annotate.deepset.ai/) erstellt wurde, zum Einsatz gekommen. Die Ergebnisse der Evaluation und der Code können [hier](https://github.com/AlexVike/Infoling-2/blob/main/QA/Evaluation/Evaluation.ipynb) eingesehen werden.

## User Interface
Für ein einfaches User Interface wurde ein `Flask Webserver` erstellt. Zusätzlich wurde `Bootstrap` verwendet.

