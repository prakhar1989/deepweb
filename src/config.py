import base64

#========Bing Parameters===========
BING_KEY = "KD9YWJna9o45c/lPuSlWp3+xVhhJpBd6N/qjfNVXTJ8="
BING_ID = "0c3454d3-67ce-4558-b4ac-1e95f964cdf5"

TAXONOMY = {
    "Root": ["Computers", "Health", "Sports"],
    "Computers": ["Hardware", "Programming"],
    "Sports": ["Basketball", "Soccer"],
    "Health": ["Diseases", "Fitness"]
}

def getEncodedKey(key):
    key = BING_KEY if not key else key
    return base64.b64encode("{0}:{1}".format(key, key))

def logger(s, highlight=False):
    if highlight:
        print "[LOG]"
        print "[LOG]"
        print "[LOG] " + s
        print "[LOG]"
        print "[LOG]"
    else:
        print "[LOG] " + s[:80] + " ..."
