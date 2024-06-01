# implement the elk log extractor
from elasticsearch import Elasticsearch
import json
import time

class ELKLogExtractor:
    def __init__(self):
        self.cache = []
        self.cache_time = 0
        self.cloud_id = "afa9c5b77ec04ec19df5fc92fc8f9e98:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ3YjNiNGQyODA2ZDI0ZWNmOGVkY2NmMjMxMjIxZTcxYyQwNGExNTk3MzM4MDM0OWFhYTIzZjRkMTI2ZTY1Mzk0Mw=="
        self.username = "elastic"
        self.pwd = "REFEL26mONYXzLH0fyFw8GLV"
        self.es = Elasticsearch(
            cloud_id=self.cloud_id,
            basic_auth=(self.username, self.pwd),
        )
    
    def get_logs_for_last_5_minutes(self):
        if len(self.cache) == 0 or time.time() - self.cache_time > 300:
            self.cache = self.get_logs()
            self.cache_time = time.time()
        return self.cache
        
    def get_logs(self, time_range=20):
        result = self.es.search(index="filebeat-*", body={"query": {"range": {"@timestamp": {"gte": "now-" + str(time_range) + "m"}}}}, scroll="2m", size=100)
        # Initialize scroll_id and hits
        scroll_id = result['_scroll_id']
        all_hits = result['hits']['hits']

        # Paginate through all results
        while len(result['hits']['hits']):
            result = self.es.scroll(
                scroll_id=scroll_id,
                scroll='2m'  # Scroll timeout (keep the context alive for 2 minutes)
            )
            all_hits.extend(result['hits']['hits'])
            scroll_id = result['_scroll_id']

        # Clear the scroll context to free resources
        self.es.clear_scroll(scroll_id=scroll_id)
        return json.dumps(all_hits)