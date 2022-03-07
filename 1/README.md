# Challenge #1

A 3 tier environment is a common setup. Use a tool of your choosing/familiarity create these resources. Please remember we will not be judged on the outcome but more focusing on the approach, style and reproducibility.

## [Terraform](./terraform)

Standard Terraform implementation using terraform registry modules to deploy a stack in AWS.
Core "threetier" terraform module that builds the stack

## [CDKTF](./cdktf)

Implementation using the [Hashicorp CDKTF](https://www.terraform.io/cdktf) and python and using terraform registry modules to deploy a stack in AWS.
Core "threetier" CDKTF Resource definition.

> **Note** Neither of these have been tested using a 'real world' AWS Account, although they do terraform plan successfully.