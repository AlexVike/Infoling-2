# Ein Question-Answer Ratgeber für Studiengänge an der Universität Regensburg

- [00-Requierements](https://github.com/AlexVike/Infoling-2/tree/main/Conda_pip_requierements)
- [01-HTML to txt](https://github.com/AlexVike/Infoling-2/tree/main/Hmtl%20to%20txt)
- [02-PDF to txt](https://github.com/AlexVike/Infoling-2/tree/main/pdf%20to%20txt)
- [03-Txt](https://github.com/AlexVike/Infoling-2/tree/main/txt)
- [04-QA](https://github.com/AlexVike/Infoling-2/tree/main/QA)
- [04-WSGI_App](https://github.com/AlexVike/Infoling-2/tree/main/wsgi_app)

Die Ordner und die Deliverables werden nun einzeln beschrieben:

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
Anschließend wird die Datenbank initialisiert und die Docs werden übergeben. Durch Docker wurde ein Docker-Image geladen und ausgeführt für die Datenbank.
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

## 02-Anforderungsspezifizierung
In diesem Ordner sind die Deliverables des Anforderungsdokument, der Hierarchischen Task Analyse und der Personas, User stories, Use-cases zu finden. In diesem Teil der Arbeit ist die Basis der Anforderungserhebung spezifiziert worden.
- Personas, User stories, Use-cases: Beinhaltet eine PDF-Datei mit allen Personas, User stories und Use-cases.
- Hierarchische Taskanalye: Beihnaltet die Schlüsseltasks und die Taskanalyse.
- Anforderungsdokument: Beinhaltet das Anforderungsdokument welches auf der Anforderungserhebung und der restlichen Anforderungsspezifizierung basiert. Aus diesem wird ersichtlich, welche Features die App beinhalten sollte. Jedoch sind nicht alle Anforderungen des Dokumentes übernommen worden. Die Gründe dafür sind im Bericht zu finden.

## 03-Iterativer Designprozess
In diesem Ordner sind drei Videos zu den unterschiedlichen Prototypen zu finden. In diesem Projekt wurden ein Paper-Prototype, ein Medium-Fidelity-Prototype und ein High-Fidelity-Prototype erstellt. Zusätzlich ist der High-Fidelity-Prototype anhand der UE-Tests verbessert worden. Genaue Erklärungen und Bilder der Prototypen sind im Bericht zu finden.
- Low-Fidelity-Prototype: Beinhaltet das Video des Prototypen.
- Medium-Fidelity-Prototype: Beinhaltet das Video des Prototypen.
- High-Fidelity-Prototype: Beinhaltet das Video des Prototypen.

## 04-Summative Evaluation
In diesem Ordner ist die Evaluation des High-Fidelity-Prototype zu finden. Mithilfe dieser Auswertung ist der High-Fidelity-Prototype verbessert worden. Mehr dazu in dem Bericht in 00-General.
- Evaluation des Prototypen: Beinhaltet die Vorabfragebögen der Teilnehmer der UE-Tests. Daneben ist exemplarisch eine Einverständniserklärung hochgeladen worden, die die Teilnehmer unterschrieben haben. Beobachter, Notizen und die Testunterlagen der UE-Tests sind hier zu finden. Diese zeigen die Vorbereitung auf die Tests und welche Notizen dabei entstanden sind. Mit diesen Notizen und den gesammelten Daten ist die Auswertung entstanden, die hier hochgeladen wurde.


