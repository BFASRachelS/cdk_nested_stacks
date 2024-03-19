#!/usr/bin/env python3
import os

import aws_cdk as cdk

app = cdk.App()
from cdk_nested_stacks.cdk_nested_stacks_api_gateway_stack import CdkNestedStacksApiGatewayStack

# Creating the whole application based on Nested stacks
CdkNestedStacksApiGatewayStack(app, "CdkNestedStacksApiGatewayStack")

app.synth()
