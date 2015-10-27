"""
Contains all functions relating to getting queries from Bing.
Creating seperate files for different search engines allows for a decoupling
of the algorithm from the search engine.
"""
import requests
import config

def get_uri(query):
    url = "https://api.datamarket.azure.com/Bing/Search/Web?Query=%27{0}%27&$top=10&$format=json"
    return url.format(query)

def get_results(query, key=config.ENCODED_KEY):
    url = get_uri(query)
    headers = {'Authorization': 'Basic ' + key}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data.get('d').get('results')

def get_restricted_results(site_url, query, key=config.ENCODED_KEY):
    URL = "https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/v1/Composite?Query=%27site%3a{0}%20{1}%27&$top=10&$format=json"
    url = URL.format(site_url, query)
    headers = {'Authorization': 'Basic ' + key}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data.get('d').get('results')
