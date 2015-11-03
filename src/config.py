import base64

#========Bing Parameters===========
BING_KEY = "Byygq1zI2KKyssKp8UvVe3DV/v6Aa0FEsKrE+pqDa0s"
BING_ID = "0c3454d3-67ce-4558-b4ac-1e95f964cdf5"
ENCODED_KEY = base64.b64encode("{0}:{1}".format(BING_KEY, BING_KEY))

TAXONOMY = {
    "Root": ["Computers", "Health", "Sports"],
    "Computers": ["Hardware", "Programming"],
    "Sports": ["Basketball", "Soccer"],
    "Health": ["Diseases", "Fitness"]
}

def logger(s, highlight=False):
    if highlight:
        print "[LOG]"
        print "[LOG]"
        print "[LOG] " + s
        print "[LOG]"
        print "[LOG]"
    else:
        print "[LOG] " + s[:80] + " ..."
