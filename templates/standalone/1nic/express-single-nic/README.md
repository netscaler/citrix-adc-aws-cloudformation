## NetScaler VPX Express 
NetScaler VPX Express is a free virtual application delivery controller (normal hourly AWS EC2 compute rates apply). This Amazon Machine Image (AMI) can be used for light production loads, testing and prototyping needs. 

## Pre-requisites
The CloudFormation template requires sufficient permissions to create IAM roles and lambda functions, beyond normal EC2 full privileges. The user of this template also needs to [accept the terms and subscribe to the AWS Marketplace product](https://aws.amazon.com/marketplace/pp/B0796LD46X/) before using this CloudFormation template.

## CloudFormation Template description
This CloudFormation template creates an instance of the VPX Express from the VPX Express AMI utilising a single VPC subnet. The CloudFormation template also provisions a lambda function that initializes the VPX instance. Initial configuration performed by the lambda function includes network interface configuration, VIP configuration and feature configuration. Further configuration can be performed by logging in to the GUI or via SSH (username: nsroot). The output of the CloudFormation template includes:

- `InstanceIdNS`. Instance Id of newly created VPX instance. This is the default password for the GUI / ssh access
- `ManagementURL`. Use this HTTPS URL to the Management GUI (uses self-signed cert) to login to the VPX and configure it further 
- `ManagementURL2`: Use this HTTP URL to the Management GUI (if your browser has problems with the self-signed cert) to login to the VPX 
- `PublicNSIp`: Use this public IP to ssh into the appliance 
- `PublicIpVIP`: The Public IP where load balanced applications can be accessed

## Network architecture
The CloudFormation template deploys the VPX in a single-NIC mode. The standard NetScaler IP addresses: NSIP (management IP), VIP (where load balanced applications are accessed) and SNIP (the IP used to send traffic to backend instances) are all provisioned on the single NIC and are drawn from the (RFC1918) address space of the provided VPC subnet.  The (RFC1918) NSIP is mapped to the Public IP of the VPX Instance and the RFC1918 VIP is mapped to a public Elastic IP. Note that if the VPX is restarted, the Public NSIP mapping is lost. In this case the NSIP is only accessible from within the VPC subnet, from another EC2 instance in the same subnet. Other possible architectures include 2 and 3-NIC configurations across multiple VPC subnets.

## Quick Launch Links

- US-East-1 region
    [![Create NetScaler VPX Express](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=NetScaler-12-VPX-Express&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/express.1nic.template)
- US-East-2 region
    [![Create NetScaler VPX Express](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=NetScaler-12-VPX-Express&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/express.1nic.template)
- US-West-1 region
    [![Create NetScaler VPX Express](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/new?stackName=NetScaler-12-VPX-Express&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/express.1nic.template)
- US-West-2 region
    [![Create NetScaler VPX Express](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=NetScaler-12-VPX-Express&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/express.1nic.template)
- CA-Central-1 region
    [![Create NetScaler VPX Express](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/new?stackName=NetScaler-12-VPX-Express&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/express.1nic.template)
- CA-Central-1 region
    [![Create NetScaler VPX Express](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/new?stackName=NetScaler-12-VPX-Express&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/express.1nic.template)
- EU-West-1 region
    [![Create NetScaler VPX Express](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=NetScaler-12-VPX-Express&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/express.1nic.template)
- EU-West-2 region
    [![Create NetScaler VPX Express](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?stackName=NetScaler-12-VPX-Express&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/express.1nic.template)
- EU-central-1 region
    [![Create NetScaler VPX Express](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=NetScaler-12-VPX-Express&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/express.1nic.template)
- AP-South-1 region
    [![Create NetScaler VPX Express](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?stackName=NetScaler-12-VPX-Express&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/express.1nic.template)
- AP-Northeast-1 region
    [![Create NetScaler VPX Express](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=NetScaler-12-VPX-Express&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/express.1nic.template)
- AP-Northeast-2 region
    [![Create NetScaler VPX Express](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?stackName=NetScaler-12-VPX-Express&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/express.1nic.template)
- AP-Southeast-1 region
    [![Create NetScaler VPX Express](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?stackName=NetScaler-12-VPX-Express&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/express.1nic.template)
- AP-Southeast-2 region
    [![Create NetScaler VPX Express](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=NetScaler-12-VPX-Express&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/express.1nic.template)
- SA-East-1 region
    [![Create NetScaler VPX Express](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?stackName=NetScaler-12-VPX-Express&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/express.1nic.template)


## Additional Links:

- VPX installation in AWS : https://docs.citrix.com/en-us/netscaler/12/deploying-vpx/install-vpx-on-aws.html
- NetScaler 12.0 Documention : https://docs.citrix.com/en-us/netscaler/12.html 
- NetScaler Overview : https://www.citrix.com/products/netscaler-adc/resources/netscaler-vpx.html
