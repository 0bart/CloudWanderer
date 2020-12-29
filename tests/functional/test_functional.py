import unittest
import logging
import botocore
from cloudwanderer import CloudWanderer
from cloudwanderer.storage_connectors import DynamoDbConnector


class TestFunctional(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.basicConfig(level='debug')

    def setUp(self):
        self.storage_connector = DynamoDbConnector(
            endpoint_url='http://localhost:8000',
            client_args={
                'config': botocore.config.Config(
                    max_pool_connections=100,
                )
            }
        )
        self.wanderer = CloudWanderer(storage_connectors=[self.storage_connector])

    def test_write_resources(self):
        self.storage_connector.init()
        self.wanderer.write_resources(exclude_resources=['image', 'snapshot', 'policy'], concurrency=128, client_args={
            'config': botocore.config.Config(
                max_pool_connections=100,
            )
        })

    def test_write_resources_in_region(self):
        self.storage_connector.init()
        self.wanderer.write_resources_in_region(exclude_resources=['image', 'snapshot', 'policy'])

    def test_write_custom_resource_definition(self):
        self.storage_connector.init()
        self.wanderer.write_resources_of_service_in_region('lambda', exclude_resources=['images', 'snapshots'])

    def test_read_all(self):
        for x in self.storage_connector.read_all():
            print(x)

    def test_read_resource_of_type(self):
        vpcs = self.storage_connector.read_resources(service='ec2', resource_type='vpc')

        print(list(vpcs))

    def test_read_all_resources_in_account(self):
        vpc = next(self.storage_connector.read_resources(service='ec2', resource_type='vpc'))
        print([str(x.urn) for x in self.storage_connector.read_resources(account_id=vpc.urn.account_id)])

    def test_read_resource_of_type_in_account(self):
        vpc = list(self.storage_connector.read_resources(service='ec2', resource_type='vpc'))[0]
        print([str(x.urn) for x in self.storage_connector.read_resources(
            service='ec2', resource_type='vpc', account_id=vpc.urn.account_id)])

    def test_write_resource_attributes(self):
        self.storage_connector.init()
        self.wanderer.write_resource_attributes()

    def test_write_resource_attributes_in_region(self):
        self.wanderer.write_resource_attributes_in_region('ec2')
