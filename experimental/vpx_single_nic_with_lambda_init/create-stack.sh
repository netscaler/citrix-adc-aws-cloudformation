#!/bin/bash

# Useful to get the AMI id. Note that there are several AMIs with the same product version. They are different by product code. Each product code 
# has a different license (E.g., 7rj9rmm05kihjjlsqkj6gni1x = 1000 Mbps Standard Edition)
aws ec2 describe-images --filters Name=name,Values="Citrix NetScaler and CloudBridge Connector*" --query 'Images[*].{Date:CreationDate,Description:Description,ID:ImageId,ProductCode:ProductCodes[0].ProductCodeId}' --output text | sort 

# Sample invocation to create a single NIC VPX. You HAVE to customize ParameterValues to your environment
aws cloudformation create-stack --template-body file://ns.1nic.template --capabilities CAPABILITY_IAM --stack-name vpx-create-lambda-test --parameters  ParameterKey=Subnet,ParameterValue=subnet-a1b2c3d4 ParameterKey=VpcID,ParameterValue=vpc-1a2b3c4d ParameterKey=AMI,ParameterValue=ami-1fda1867 ParameterKey=KeyName,ParameterValue=mykeyname
