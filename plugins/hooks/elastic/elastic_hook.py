from typing import Any

from airflow.hooks.base import BaseHook
from airflow.plugins_manager import AirflowPlugin
from elasticsearch import Elasticsearch


class ElasticHook(BaseHook):
    """Simple Hook class to communicate with Elasticsearch."""

    def __init__(self, conn_id: str = 'elastic_default', *args, **kwargs):
        super().__init__(*args, **kwargs)

        conn = self.get_connection(conn_id=conn_id)

        conn_config = {}
        hosts = []

        if conn.host:
            hosts = conn.host.split(',')
        if conn.port:
            conn_config['port'] = int(conn.port)
        if conn.login:
            conn_config['http_auth'] = (conn.login, conn.password)

        self.es = Elasticsearch(hosts, **conn_config)
        self.index = conn.schema

    def info(self) -> Any:
        """Returns basic information about the cluster."""

        return self.es.info()

    def set_index(self, index: str) -> None:
        """Sets the index based on the supplied index parameter."""

        self.index = index

    def add_doc(self, index: str, body: dict, **kwargs) -> Any:
        """Ads new document to the selected index/folder."""

        self.set_index(index)
        result = self.es.index(index=index, body=body, **kwargs)

        return result


class AirflowElasticPlugin(AirflowPlugin):
    """Registers the plugin in the ariflow system."""

    name = 'elastic'
    hooks = [ElasticHook]
