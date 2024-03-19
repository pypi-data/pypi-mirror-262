import logging
import os
import pandas as pd
from typing import Optional

from .http_client import HttpClient

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

ACHO_TOKEN = os.environ.get("ACHO_PYTHON_SDK_TOKEN") or ""
BASE_URL = os.environ.get("ACHO_PYTHON_SDK_BASE_URL") or ""
ACHO_CLIENT_TIMEOUT = 30

class View():

    def __init__(self, http_client: HttpClient, project_id: Optional[int] = None, view_id: Optional[int] = None):
        self.http = http_client
        self.project_id = project_id
        self.view_id = view_id
        return
    
    def __str__(self) -> str:
        return f"View {self.view_id} of Project {self.project_id}"
    
    async def download(self, options = {}, destination = os.getcwd()):
        payload = {
            'proj_id': self.project_id,
            'view_id': self.view_id,
            'options': options,
        }
        resp = await self.http.call_api(path=f"/project/get-csv-links", http_method="POST", json=payload)
        if not os.path.exists(destination):
            os.makedirs(destination)
        # destination_path = os.path.join(destination, filename)
        result = resp.get('signedUrls', [])
        return result
    
    async def export_to_df(self, options = {}):
        urls = await self.download(options)
        aggregated_results = pd.DataFrame()

        for url in urls:
            # Adjust the chunksize parameter as needed to control memory usage
            for chunk in pd.read_json(url, lines=True, compression='gzip', chunksize=10000):
                # Process the chunk: perform operations like filtering, aggregations, etc.
                # This example assumes a simple operation, but you would replace this with whatever operation you need
                processed_chunk = chunk # This is where you'd apply operations

                # Update aggregated results with processed chunk
                # This might involve concatenation, summation, or any other form of aggregation depending on your need
                aggregated_results = pd.concat([aggregated_results, processed_chunk])

        return aggregated_results