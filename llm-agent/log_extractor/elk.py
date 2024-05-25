# implement the elk log extractor
from elasticsearch import Elasticsearch
import json
import time

class ELKLogExtractor:
    def __init__(self):
        self.cache = []
        self.cache_time = 0
        self.cloud_id = "9b78dc4b87cb480bb9388eabc314c9f0:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQ0MDkyMzRiMmE4YTk0MjRjYTQyZjA3NTYwYzFjMjkyNCRkMmU4ZjVmNTA5MzY0ZWJhYmQ1ZWQ1NTc4MTI2NjVkZA=="
        self.username = "elastic"
        self.pwd = "kpfk5RF8BrIUrTi3I8Ov7S8B"
        self.es = Elasticsearch(
            cloud_id=self.cloud_id,
            basic_auth=(self.username, self.pwd),
        )
    
    def get_logs_for_last_5_minutes(self):
        if len(self.cache) == 0 or time.time() - self.cache_time > 300:
            self.cache = self.get_logs()
            self.cache_time = time.time()
        return self.cache
        
    def get_logs(self, time_range=5):
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