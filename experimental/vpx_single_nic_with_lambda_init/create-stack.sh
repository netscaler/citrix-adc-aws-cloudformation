#!/bin/bash


# Sample invocation to create a single NIC VPX. You HAVE to customize ParameterValues to your environment
aws cloudformation create-stack --template-body file://ns.1nic.template --capabilities CAPABILITY_IAM --stack-name vpx-1nic-test --parameters  ParameterKey=Subnet,ParameterValue=subnet-a1b2c3d4 ParameterKey=VpcID,ParameterValue=vpc-1a2b3c4d ParameterKey=ImageName,ParameterValue=VpxStandard1000 ParameterKey=KeyName,ParameterValue=mykeyname
