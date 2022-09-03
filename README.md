# Ein Question-Answer Ratgeber für Studiengänge an der Universität Regensburg

- [00-Requierements](https://github.com/AlexVike/Infoling-2/tree/main/Conda_pip_requierements)
- [01-HTML to txt](https://github.com/AlexVike/Infoling-2/tree/main/Hmtl%20to%20txt)
- [02-PDF to txt](https://github.com/AlexVike/Infoling-2/tree/main/pdf%20to%20txt)
- [03-Txt](https://github.com/AlexVike/Infoling-2/tree/main/txt)
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

## 01-Anforderungserhebung
In diesem Ordner sind alle Daten der durchgeführten Interviews, der Fokusgruppe und der Wettbewerbsanalyse zu finden. Diese Daten sind dazu genutzt worden, um die Bedürfnisse und die Pain Points der Nutzer zu erkennen. Dies stellte die Basis unserer Arbeit dar, auf der die App aufgebaut wurde.
- Interview: Beinhaltet die Vorabfragebögen und die Transkription der Interviews. Dabei wurden aus Datenschutzgründen die Namen entfernt. Daneben ist auch das Kategoriensystem des Leitfadens und der Interviewleitfaden zu finden. Der Interviewleitfaden basiert auf dem Kategoriensystem. Genauere Erläuterungen sind im Bericht zu finden. Abschließend ist in diesem Ordner die Kodierung der Interviews hochgeladen worden. Nur anhand dieser Daten konnten die Interviews ausgewertet werden.
- Wettbewerbsanalyse: Beinhaltet eine Feature-Matrix vom Apps, die Inhalte besitzen, die unserer Thematik entsprechen. Zusätzlich werden gute bzw. schlechte Features dieser Apps aufgezeigt, um daraufhin in der Wettbewerbsanalyse Schlussfolgerungen ziehen zu können.
- Fokusgruppe: Beinhaltet die ungeschnittene Audiodatei der Fokusgruppe. Zusätzlich kann hier eine bearbeitete Version dieser Audiodatei gefunden werden, die anstatt einer Stunde nur fünf Minuten lang ist. Neben den Audiodateien sind der Leitfaden, die Screenshots der Mural Boards und die Präsentation der Fokusgruppe hochgeladen worden.

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

```ruby
require 'redcarpet'
markdown = Redcarpet.new("Hello World!")
puts markdown.to_html
```
