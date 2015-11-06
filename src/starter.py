import time
import sys
import bing
import crawler
from config import TAXONOMY, logger, getEncodedKey
from collections import defaultdict
import os

BING_KEY = None

# path to the data folder
DATA_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), os.pardir, 'data'
    )
)

def readQueryFile(filename):
    # generates a category -> query mapping associated 
    # with a filename
    mapping  = defaultdict(list)
    with open(os.path.join(DATA_PATH, filename)) as f:
        for line in f:
            terms = line.split()
            category = terms[0]
            query = " ".join(terms[1:])
            mapping[category].append(query)
    return mapping

def buildQueryUrlMap(database, filename):
    # returns a list of unique urls for a given database.
    logger("Collecting data for " + filename)
    cache = {}
    queriesMappings = readQueryFile(filename)
    for keyword, queries in queriesMappings.iteritems():
        cache[keyword] = {}
        for query in queries:
            results = bing.get_restricted_results(database, query, BING_KEY)[0]
            cache[keyword][query] = {
                "count": int(results.get('WebTotal')),
                "urls": [r["Url"] for r in results.get('Web')]
            }
    return cache

def classifyDb(database, Tc=100, Ts=0.6):
    # classifies a database based on values of
    # threshold and specificity
    categories, categoryData = ["Root"], {}
    for cat in categories:
        logger("Analyzing " + cat + " category")
        filename = cat.lower() + ".txt"
        keywords = TAXONOMY.get(cat)
        if keywords:
            queryUrlMap = buildQueryUrlMap(database, filename)
            categoryData.update(queryUrlMap)
            keywordCount = {k: sum([q["count"] for q in
                                    queryUrlMap[k].itervalues()]) for k in keywords}

            N = float(sum(keywordCount.values()))
            for k, v in keywordCount.items():
                logger("Coverage for {0} : {1}, Specificity: {2}".format(k, str(v), str(v/N)))
                if v >= Tc and v/N >= Ts:
                    logger(">>>>>> Adding " + k + " to category <<<<<<")
                    categories.append(k)
    return (categories, categoryData)


def getUniqueDocs(keywords, categoryData):
    # gets a list of keywords and returns a set of doc urls
    # that have for those keywords
    combinedDocs = set()
    for k in keywords:
        urls = [x['urls'] for x in categoryData[k].values()]
        uniqueUrls = reduce(lambda a, b: a.union(b), urls, set())
        combinedDocs = combinedDocs.union(uniqueUrls)
    return combinedDocs

def buildContentSummary(categories, categoryData, database):
    # builds the content summary for a database
    iters = 2 if len(categories) > 1 else 1
    keywords = [TAXONOMY.get(cat) for cat in categories[:iters]]
    for i in range(iters):
        keys = reduce(list.__add__, keywords[i:])
        urls = getUniqueDocs(keys, categoryData)
        logger("Building the content summary for " + categories[i] + \
               ". Total docs to fetch: " + str(len(urls)), highlight=True)
        crawler.getContentSummary(database, categories[i], urls, categoryData)

def runner(database, Tc, Ts):
    # the program runner
    categories, categoryData = classifyDb(database, Tc, Ts)
    logger(">>>>>> Categorization complete: {0}<<<<<<< ".format("/".join(categories)), highlight=True)
    buildContentSummary(categories, categoryData, database)
    logger("Process Complete.")
    logger("Results generated in " + crawler.RESULTS_PATH)

if __name__ == "__main__":
    database = raw_input("Enter database: ").strip()
    Tc = int(raw_input("Enter Tc (leave blank for 100): ") or 100)
    Ts = float(raw_input("Enter Ts (leave blank for 0.6): ") or 0.6)
    key = raw_input("Enter BING account key (leave blank to use author's key): ")
    BING_KEY = getEncodedKey(None if key else key)
    runner(database, Tc, Ts)
