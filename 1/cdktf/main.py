#!/usr/bin/env python
from unicodedata import name
from constructs import Construct
from cdktf import App, TerraformStack, Token

from imports.aws import AwsProvider
from imports.aws.ec2 import DataAwsAmi, DataAwsAmiFilter
from threetier import ThreeTier

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        AwsProvider(self, 'Aws', region='eu-west-1')

        ami = DataAwsAmi(self, 'ami',
            most_recent=True,
            owners=["amazon"],
            filter=[
                DataAwsAmiFilter(
                    name="name",
                    values=["amzn-ami-hvm-*-x86_64-gp2"]
                )
            ]
        )

        # define resources here
        stack = ThreeTier(self, 'stack',
            ami_id=Token().as_string(ami.id)
            )


app = App()
MyStack(app, "three-tier")

app.synth()
