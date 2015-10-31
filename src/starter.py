import requests
import time
import sys
import bing
import shelve
from collections import defaultdict
import os

# Hack for turning off SSLWarning on CLIC machines :|
requests.packages.urllib3.disable_warnings()

# open db
p = os.path.dirname(os.path.abspath('__file__'))
d = shelve.open('results', flag='r')
try:
    data = d["data"]
finally:
    d.close()

taxonomy = {
    "Root": ["Computers", "Health", "Sports"],
    "Computers": ["Hardware", "Programming"],
    "Sports": ["Basketball", "Soccer"],
    "Health": ["Diseases", "Fitness"]
}

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

def classifyDb(database, Tc=100, Ts=0.6):
    if database not in data:
        raise KeyError(database +  " not found")
    results = data[database]
    summary = {k:sum(v.values()) for k, v in results.iteritems()}
    categories = ["Root"]
    for cat in categories:
        keywords = taxonomy.get(cat)
        if keywords:
            N = float(sum([summary[c] for c in keywords]))
            for keyword in keywords:
                if summary[keyword] > Tc and summary[keyword]/N > Ts:
                    categories.append(keyword)
    return "/".join(categories)

if __name__ == "__main__":
    database = raw_input("Enter database: ").strip()
    Tc = int(raw_input("Enter Tc (leave blank for 100): ") or 100)
    Ts = float(raw_input("Enter Ts (leave blank for 0.6): ") or 0.6)
    print database, "is classified as", classifyDb(database, Tc, Ts)
