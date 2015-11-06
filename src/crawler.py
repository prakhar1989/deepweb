from subprocess import Popen, PIPE
from itertools import chain
from bing import get_restricted_results
import os
from config import logger
from starter import readQueryFile
from hashlib import md5
import re

# path to the cache folder
CACHE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), os.pardir, 'cache'
    )
)

# path to the results folder
RESULTS_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), os.pardir, 'results'
    )
)


def getPageContent(url):
    # returns the content from the webpage associated with the url
    # Checks the cache first and if not found, downloads the page
    # from the internet

    url = url.encode("ascii", "ignore")
    # create folder if it doesnt exist
    if not os.path.exists(CACHE_PATH):
        os.makedirs(CACHE_PATH)
    logger("Fetching " + url)
    filename = os.path.join(CACHE_PATH, md5(url.encode("ascii", "ignore")).hexdigest())
    content = None
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            content = f.read()
    else:
        p = Popen(["lynx", "--dump", url], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        content, err = p.communicate()
        if content:
            with open(filename,'w') as f:
                    f.write(content)
    return content


def getWords(url):
    # returns a set of words from a the content of a url
    content = getPageContent(url)
    if content:
        end = content.find("\nReferences\n")
        content = content[:end] if end > 0 else content
        text = re.sub(r'\[(.*?)\]', '', re.sub(r'\n', "", content))
        words = set([w.lower() for w in re.split(r'\W+', text) if str.isalpha(w)])
        return words
    return []

def writeToFile(wordMap, filename, categoryData):
    # builds a content summary file with the associated filename.
    # takes as input the category data read from the data files
    # and map of word document frequencies

    # create folder if it doesn't exist
    if not os.path.exists(RESULTS_PATH):
        os.makedirs(RESULTS_PATH)
    filename = os.path.join(RESULTS_PATH, filename)
    webTotalMap = {}
    for cat in categoryData:
        for k, v in categoryData[cat].iteritems():
            webTotalMap[k] = v.get("count")
    with open(filename, 'w') as f:
        for word, count in sorted(wordMap.iteritems()):
            matches = -1 if word not in webTotalMap else webTotalMap[word]
            f.write("{0}#{1}#{2}\n".format(word, float(count), float(matches)))


def getContentSummary(database, category, documents, categoryData):
    # generates the content summary for a database and category.
    # takes as input a set of documents, the primary category additionally.
    wordList = [getWords(d) for d in documents]
    dfMap = dict()
    vocabulary = reduce(lambda a, b: a.union(b), wordList, set())
    for word in vocabulary:
        matchCount = sum([1 for l in wordList if word in l])
        dfMap[word] = matchCount
    writeToFile(dfMap, "{0}-{1}.txt".format(category, database), categoryData)
    return dfMap
