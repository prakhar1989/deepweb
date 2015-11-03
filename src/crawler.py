from subprocess import Popen, PIPE
from bing import get_restricted_results
import os
from config import logger
from starter import readQueryFile
from hashlib import md5
import re

CACHE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), os.pardir, 'cache'
    )
)

RESULTS_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), os.pardir, 'results'
    )
)


def getPageContent(url):
    logger("Fetching " + url)
    filename = os.path.join(CACHE_PATH, md5(url).hexdigest())
    #filename = "cache/" + md5(url).hexdigest()
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
    content = getPageContent(url)
    if content:
        end = content.find("\nReferences\n")
        content = content[:end] if end > 0 else content
        text = re.sub(r'\[(.*?)\]', '', re.sub(r'\n', "", content))
        words = set([w.lower() for w in re.split(r'\W+', text) if str.isalpha(w)])
        return words

def writeToFile(wordMap, filename):
    #filename = "results/" + filename
    filename = os.path.join(RESULTS_PATH, filename)
    with open(filename, 'w') as f:
        for word, count in sorted(wordMap.iteritems()):
            f.write("{0}#{1}#-1.0\n".format(word, count))

def getContentSummary(database, category, documents):
    dfMap = dict()
    wordList = [getWords(d) for d in documents]
    vocabulary = reduce(lambda a, b: a.union(b), wordList, set())
    for word in vocabulary:
        matchCount = sum([1 for l in wordList if word in l])
        dfMap[word] = matchCount
    writeToFile(dfMap, "{0}-{1}.txt".format(category, database))
    return dfMap
