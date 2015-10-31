import time
import sys
import bing
import crawler
from config import TAXONOMY, logger
from collections import defaultdict
import os

def getFileForCategory(name):
    return name.lower() + ".txt"

def readQueryFile(filename):
    path = os.path.join(os.path.dirname(os.path.abspath('__file__')), "../data/")
    mapping  = defaultdict(list)
    with open(path + filename) as f:
        for line in f:
            terms = line.split()
            category = terms[0]
            query = " ".join(terms[1:])
            mapping[category].append(query)
    return mapping

def buildQueryUrlMap(database, filename):
    logger("Collecting data for " + filename)
    cache = {}
    queriesMappings = readQueryFile(filename)
    for keyword, queries in queriesMappings.iteritems():
        cache[keyword] = {}
        for query in queries:
            results = bing.get_restricted_results(database, query)[0]
            cache[keyword][query] = {
                "count": int(results.get('WebTotal')),
                "urls": [r["Url"] for r in results.get('Web')]
            }
    return cache

def classifyDb(database, Tc=100, Ts=0.6):
    categories, categoryData = ["Root"], {}
    for cat in categories:
        logger("Analyzing " + cat + " category")
        filename = getFileForCategory(cat)
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
    """ gets a list of keywords and returns a set of doc urls
    that have for those keywords """
    combinedDocs = set()
    for k in keywords:
        urls = [x['urls'] for x in categoryData[k].values()]
        uniqueUrls = reduce(lambda a, b: a.union(b), urls, set())
        combinedDocs = combinedDocs.union(uniqueUrls)
    return combinedDocs

def buildContentSummary(categories, categoryData, database):
    iters = 2 if len(categories) > 1 else 1
    keywords = [TAXONOMY.get(cat) for cat in categories[:iters]]
    for i in range(iters):
        keys = reduce(list.__add__, keywords[i:])
        urls = getUniqueDocs(keys, categoryData)
        logger("Building the content summary for " + categories[i] + \
               ". Total docs to fetch: " + str(len(urls)))
        crawler.getContentSummary(database, categories[i], urls)

def runner(database, Tc, Ts):
    categories, categoryData = classifyDb(database, Tc, Ts)
    logger(">>>>>> Categorization complete: {0}<<<<<<< ".format("/".join(categories)))
    buildContentSummary(categories, categoryData, database)
    logger("Process Complete")

if __name__ == "__main__":
    database = raw_input("Enter database: ").strip()
    Tc = int(raw_input("Enter Tc (leave blank for 100): ") or 100)
    Ts = float(raw_input("Enter Ts (leave blank for 0.6): ") or 0.6)
    runner(database, Tc, Ts)
