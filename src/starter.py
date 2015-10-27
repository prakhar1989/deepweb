import requests
import sys
import bing

# Hack for turning off SSLWarning on CLIC machines :|
requests.packages.urllib3.disable_warnings()

def getQueryCount(site, query):
    results = bing.get_restricted_results(site, query)
    # TODO: try / catch
    return (site, query, int(results[0].get('WebTotal')))


if __name__ == "__main__":
    print getQueryCount("fifa.com", "premiership")
    print getQueryCount("hardwarecentral.com", "avi file")
    print getQueryCount("fifa.com", "avi file")



