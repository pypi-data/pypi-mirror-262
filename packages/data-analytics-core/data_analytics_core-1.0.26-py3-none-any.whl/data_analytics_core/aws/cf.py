"""
AWS_CF Class
containing all the needed AWS CloudFormation actions and the client itself.
"""
import os
import json
import boto3
import yaml
# custom imports
from data_analytics_core.localstack.boto_client_moks.localstack_clients import boto3_client_localstack


class AmazonWebServicesCF:
    def __init__(self, region_name="eu-central-1"):
        # env aws connections generation
        self.region_name = region_name
        if os.getenv("LOCALSTACK_ENDPOINT_URL"):
            self.cf_client = boto3_client_localstack(service_name="cloudformation", region_name=region_name)
        else:
            self.cf_client = boto3.client('cloudformation', region_name=region_name)

    def create_resource(self, resource_name: str, path_to_file: str,
                        role_arn: str = None, tags: list[dict] = None, file_format_yaml: bool = True):
        if file_format_yaml:
            with open(path_to_file, 'r') as yaml_file:
                self.cf_client.create_stack(
                    StackName=resource_name,
                    TemplateBody=str(yaml.safe_load(yaml_file)),
                    RoleARN=role_arn,
                    OnFailure="ROLLBACK",
                    Tags=tags
                )
        else:
            with open(path_to_file, 'r') as json_file:
                self.cf_client.create_stack(
                    StackName=resource_name,
                    TemplateBody=str(json.load(json_file)),
                    RoleARN=role_arn,
                    OnFailure="ROLLBACK",
                    Tags=tags
                )
