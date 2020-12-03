import json
import os
import urllib.request, urllib.parse

from collections import OrderedDict
from typing import List, Union, Dict


class SOLR:
    """
    Wrapper for the SOLR retrieval engine.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8983,
        cookie: dict = None,
        collection: str = "trec",
        file_number: int = 100,
        ir_model: str = "DFR",
    ):
        self.host = host
        if self.host is None:
            self.host = (
                os.environ["SOLR_HOST"] if "SOLR_HOST" in os.environ else "localhost"
            )

        self.port = port
        if self.port is None:
            self.port = (
                int(os.environ["SOLR_PORT"]) if "SOLR_PORT" in os.environ else 8983
            )

        self.cookie = cookie

        self.collection = collection
        if self.collection is None:
            self.collection = (
                os.environ["SOLR_COLLECTION"]
                if "SOLR_COLLECTION" in os.environ
                else "trec"
            )

        self.file_number = file_number
        if self.file_number is None:
            self.file_number = (
                int(os.environ["SOLR_FILENUMBER"])
                if "SOLR_FILENUMBER" in os.environ
                else 100
            )

        self.ir_model = ir_model
        if self.ir_model is None:
            self.ir_model = (
                os.environ["SOLR_IRMODEL"] if "SOLR_IRMODEL" in os.environ else "DFR"
            )

    def __rget(self, path: str = "select?", params: Union[Dict, None] = None):

        url = f"http://{self.host}:{str(self.port)}/solr/{self.collection}/{path}"

        def __format_param(key):
            values = params[key]
            if type(values) is not list:
                values = [values]

            return "&".join(map(lambda value: key + "=" + str(value), values))

        if len(params) > 0:
            url = f"{url}?{'&'.join(map(__format_param, params.keys()))}"

        request = urllib.request.urlopen(url)

        return json.load(request)["response"]["docs"]

    def query(
        self,
        query: str,
        fields: List[str] = None,
        rows: int = 15,
        sort: str = "score asc",
    ):

        params = {
            "fl": (
                urllib.parse.quote(" ".join(fields))
                if fields is not None
                else "docno%2Cscore%2Cdoctext&"
            ),
            "q": f"doctext%3A({query})",
            "rows": f"{rows}",
            "sort": urllib.parse.quote(sort),
        }

        return self.__rget(path="select", params=params)
