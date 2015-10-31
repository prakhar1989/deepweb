from subprocess import Popen, PIPE
from bing import get_restricted_results
from config import logger
from starter import readQueryFile
import re

def getUrls(database, filename="root.txt"):
    logger("Building unique sample urls for: " + database)
    queries = reduce(list.__add__, readQueryFile(filename).itervalues())
    urls = set()
    for query in queries:
        results = get_restricted_results(database, query)[0]["Web"]
        urls = urls.union(set([r["Url"] for r in results]))
    return urls

def getPageContent(url):
    logger("Fetching " + url)
    p = Popen(["lynx", "--dump", url], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    return output if not err else None

def getWords(url):
    content = getPageContent(url)
    end = content.find("\nReferences\n")
    content = content[:end] if end > 0 else content
    text = re.sub(r'\[(.*?)\]', '', re.sub(r'\n', "", content))
    words = set([w.lower() for w in re.split(r'\W+', text) if str.isalpha(w)])
    return words

def writeToFile(wordMap, filename):
    with open(filename, 'w') as f:
        for word, count in sorted(wordMap.iteritems()):
            f.write("{0}#{1}#-1.0\n".format(word, count))

def getContentSummary(database, category, documents):
    dfMap = dict()
    wordList = [getWords(d) for d in documents]
    logger("Building content summary")
    vocabulary = reduce(lambda a, b: a.union(b), wordList, set())
    for word in vocabulary:
        matchCount = sum([1 for l in wordList if word in l])
        dfMap[word] = matchCount
    category = "Root" #TODO: Fix this
    writeToFile(dfMap, "{0}-{1}.txt".format(category, database))
    return dfMap