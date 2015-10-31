"""
Contains all functions relating to getting queries from Bing.
Creating seperate files for different search engines allows for a decoupling
of the algorithm from the search engine.
"""
import config
import urllib2
import json

def get_restricted_results(site_url, query, key=config.ENCODED_KEY):
    query = query.replace(' ', '%20')
    URL = "https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/v1/Composite?Query=%27site%3a{0}%20{1}%27&$top=4&$format=json"
    url = URL.format(site_url, query)
    headers = {'Authorization': 'Basic ' + key}
    req = urllib2.Request(url, headers=headers)
    resp = urllib2.urlopen(req)
    data = json.loads(resp.read())
    return data.get('d').get('results')

if __name__ == "__main__":
    print get_restricted_results("fifa.com", "bayern")
