import requests
from elasticsearch import Elasticsearch, helpers

ES = Elasticsearch(
    hosts=["https://fz98j6ogqz:qez1c4u6k6@book-crawl-amazon-632909585.ap-southeast-2.bonsaisearch.net:443"], use_ssl=True)
if ES.ping():
    print("ES server connected")
def upload_detail_bunk(data):
    helpers.bulk(ES, data)