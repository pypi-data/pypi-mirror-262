import logging

from google.protobuf.json_format import MessageToDict

from spaceone.core.connector import BaseConnector
from spaceone.core import pygrpc
from spaceone.core.utils import parse_endpoint
from spaceone.core.error import *

__all__ = ['IdentityConnector']
_LOGGER = logging.getLogger(__name__)


class IdentityConnector(BaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'endpoint' not in self.config:
            raise ERROR_WRONG_CONFIGURATION(key='endpoint')

        if len(self.config['endpoint']) > 1:
            raise ERROR_WRONG_CONFIGURATION(key='too many endpoint')

        for (k, v) in self.config['endpoint'].items():
            e = parse_endpoint(v)
            self.client = pygrpc.client(endpoint=f'{e.get("hostname")}:{e.get("port")}', version=k)

    def get_service_account(self, service_account_id, domain_id):
        response = self.client.ServiceAccount.get({
            'service_account_id': service_account_id,
            'domain_id': domain_id
        }, metadata=self.transaction.get_connection_meta())

        return self._change_message(response)

    def list_service_accounts(self, query, domain_id):
        response = self.client.ServiceAccount.list({
            'query': query,
            'domain_id': domain_id
        }, metadata=self.transaction.get_connection_meta())

        return self._change_message(response)

    def get_project(self, project_id, domain_id):
        response = self.client.Project.get({
            'project_id': project_id,
            'domain_id': domain_id
        }, metadata=self.transaction.get_connection_meta())

        return self._change_message(response)

    def list_projects(self, query, domain_id):
        response = self.client.Project.list({
            'query': query,
            'domain_id': domain_id
        }, metadata=self.transaction.get_connection_meta())

        return self._change_message(response)

    @staticmethod
    def _change_message(message):
        return MessageToDict(message, preserving_proto_field_name=True)
