import requests
import time
import sys
import bing
import shelve
from collections import defaultdict
import os

# Hack for turning off SSLWarning on CLIC machines :|
requests.packages.urllib3.disable_warnings()


def getFileName(category):
    return category.lower() + '.txt'

def getQueryCount(site, query):
    results = bing.get_restricted_results(site, query)
    # TODO: try / catch
    return (site, query, int(results[0].get('WebTotal')))


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

def buildMap(database, filename, keyword):
    cache = {}
    queriesMappings = readQueryFile(filename)
    for query in queriesMappings[keyword]:
        time.sleep(1)
        result = getQueryCount(database, query)
        cache[query] = result[-1]
    return cache

if __name__ == "__main__":
    #print getQueryCount("fifa.com", "premiership")
    #print getQueryCount("hardwarecentral.com", "avi file")
    #print getQueryCount("fifa.com", "avi file")
    d = shelve.open('results')
    print d.keys()
    d.close()
