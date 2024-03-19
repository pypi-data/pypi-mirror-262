import asyncio
import logging
import os
import pandas as pd
from typing import Optional

from .http_client import HttpClient
from .view_client import View

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

ACHO_TOKEN = os.environ.get("ACHO_PYTHON_SDK_TOKEN") or ""
BASE_URL = os.environ.get("ACHO_PYTHON_SDK_BASE_URL") or ""
ACHO_CLIENT_TIMEOUT = 30

class Project():

    def __init__(self, token: Optional[str] = ACHO_TOKEN, base_url = BASE_URL, timeout = ACHO_CLIENT_TIMEOUT):
        self.http = HttpClient(token=token, base_url=base_url, timeout=timeout)
        self.project_id = None
        return
    
    def __str__(self) -> str:
        return f"Acho Python SDK Project Client"
    
    def set_current(self, project_id):
        self.project_id = project_id
        return
    
    async def list(self, options = {}):
        data = await self.http.call_api(path=f"/project/list", http_method="POST", json={})
        result = data.get('result', [])
        df_projects = pd.json_normalize(result)
        return df_projects
    
    async def list_views(self, options = {}):
        if self.project_id is None or not isinstance(self.project_id, int):
            try:
                self.project_id = int(self.project_id)
            except (ValueError, TypeError):
                logging.warning(f"Project ID is None or not resolvable to an integer: {self.project_id}, use set_current() to set a project ID")
            return
        data = await self.http.call_api(path=f"/project/{self.project_id}/views", http_method="GET")
        result = data.get('projectViewList', [])
        df_views = pd.json_normalize(result)
        return df_views
    
    async def view(self, view_id, options = {}):
        if self.project_id is None or not isinstance(self.project_id, int):
            try:
                self.project_id = int(self.project_id)
            except (ValueError, TypeError):
                logging.warning(f"Project ID is None or not resolvable to an integer: {self.project_id}, use set_current() to set a project ID")
            return
        
        if view_id is None or not isinstance(view_id, int):
            try:
                view_id = int(self.project_id)
            except (ValueError, TypeError):
                logging.warning(f"View ID is None or not resolvable to an integer: {view_id}")
            return
        
        view = View(http_client=self.http, project_id=self.project_id, view_id=view_id)
        return view
