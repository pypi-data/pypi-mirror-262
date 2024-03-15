from pydantic import BaseModel
from typing import Optional
import base64
import json
from typing import TypeVar, Type, Any
from collections.abc import Mapping
import os

# EXAMPLE INPUT
# {
#   "data": {
#     "identifier": "test-external-resources-iam-role",
#     "assume_role": {
#       "aws": null,
#       "service": [
#         "ec2.amazonaws.com"
#       ],
#       "federated": null
#     },
#     "inline_policy": "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Action\":[\"ec2:DescribeVpcs\"],\"Resource\":[\"*\"]}]}",
#     "output_resource_name": "test-external-resources",
#     "region": "us-east-1"
#   },
#   "provision": {
#     "provision_provider": "aws",
#     "provisioner": "ter-int-dev",
#     "provider": "aws-iam-role",
#     "identifier": "test-external-resources-iam-role",
#     "target_cluster": "app-sre-stage-01",
#     "target_namespace": "test-jpiriz",
#     "target_secret_name": "test-external-resources",
#     "module_provision_data": {
#       "tf_state_bucket": "test-external-resources-state",
#       "tf_state_region": "us-east-1",
#       "tf_state_dynamodb_table": "test-external-resources-lock",
#       "tf_state_key": "aws/ter-int-dev/aws-iam-role/test-external-resources-iam-role/terraform.state"
#     }
#   }
# }

class TerraformProvisionOptions(BaseModel):
    tf_state_bucket: str
    tf_state_region: str
    tf_state_dynamodb_table: str
    tf_state_key: str

class Provision(BaseModel):
    provision_provider: str  # aws
    provisioner: str  # ter-int-dev
    provider: str  # aws-iam-role
    identifier: str
    target_cluster: str
    target_namespace: str
    target_secret_name: Optional[str]

class Output(Provision):
    data: dict[str, Any]

class AppInterfaceProvision(Provision):
    module_provision_data: TerraformProvisionOptions

def read_input_data(b64data: str) -> dict[str, Any]:
    str_input = base64.b64decode(b64data.encode("utf-8")).decode("utf-8")
    data = json.loads(str_input)
    return data

T = TypeVar('T', bound=BaseModel)
def parse_model(model_class: Type[T], data: Mapping[str,Any]) -> T:
    input = model_class.model_validate(data)
    return input

def parse_base64_model(model_class: Type[T], b64data: str) -> T:
    data = read_input_data(b64data)
    return parse_model(model_class=model_class, data=data)

def parse_app_interface_provision(b64data: str) -> AppInterfaceProvision:
    data = read_input_data(b64data)
    provision: AppInterfaceProvision = parse_model(AppInterfaceProvision, data["provision"])
    return provision

def check_container_env() -> None:
    if "INPUT" not in os.environ:
        raise Exception("INPUT env var not present")
