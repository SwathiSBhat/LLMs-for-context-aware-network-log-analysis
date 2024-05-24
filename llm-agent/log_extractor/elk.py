# implement the elk log extractor

def getlogs(timeframe, logtype):
    return [
        {"text": "Error: Unable to connect to the database. Retrying in 5 seconds.", "metadata": {"source": "log1"}},
        {"text": "Warning: High memory usage detected on server 2.", "metadata": {"source": "log2"}},
        {"text": "Info: User john_doe logged in from IP 192.168.1.1.", "metadata": {"source": "log3"}},
    ]
