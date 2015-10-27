import os
from collections import defaultdict

def readQueryFile(filename):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/")
    mapping  = defaultdict(list)
    with open(path + filename) as f:
        for line in f:
            terms = line.split()
            category = terms[0]
            query = " ".join(terms[1:])
            mapping[category].append(query)
    return mapping

if __name__ == "__main__":
    root = readQueryFile("root.txt")
    print root["Computers"]


