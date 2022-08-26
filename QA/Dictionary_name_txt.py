import os
import fnmatch
from collections import defaultdict


def getdic():
    dic_studiengänge = defaultdict(list)
    for path, dirs,files in os.walk('C:/Users/Alexa/OneDrive/Desktop/UE/Infoling-2/txt'):
        for f in fnmatch.filter(files, '*.txt'):
            dic_studiengänge[os.path.basename(path)].append(f)
    return dic_studiengänge