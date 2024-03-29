# For Internal and External Apps

## CloudFormation Template description

This template provisions two Citrix ADC VPX in two different AWS Availability Zones and configures them as High-Availabile using Private IP as well as Public IP.

The template creates the below resources:

* IAM Role required for HA configuration
* 3 Security Groups
  * Management Security Group for management (NSIP) interfaces
  * Client Security Group for client (VIP) interfaces
  * Server Security Group for server (SNIP) interfaces
* 6 Elastic Network Interfaces (3 for each Citrix ADCs)
  * Primary Citrix ADC
    * Management interface (eth0)
    * Client interface (eth1)
    * Server interface (eth2)
  * Secondary Citrix ADC
    * Management interface (eth0)
    * Client interface (eth1)
    * Server interface (eth2)
* 2 Elastic IPs `User has option not to create these EIPs`
  * Management EIP for Primary Citrix ADC
  * Management EIP for Secondary Citrix ADC
* Optional LB vserver

## Pre-requisites

> If VPC, subnets, iGateway do not already exists and ADCs are to be provisioned on fresh resources, refer [vpc-infra](../../../vpc-infra/) to create the prequisite infra

The CloudFormation template requires sufficient IAM previliges to create IAM roles, beyond normal EC2 full privileges. The user of this template also needs to [accept the terms and subscribe to the AWS Marketplace product](https://aws.amazon.com/marketplace/pp/B00AA01BOE/) before using this CloudFormation template.

The following should be present

* VPC
* 6 Subnetworks (3 each in every availability zone)
  * Primary VPX Subnets
    * Management side Subnet
    * Client side Subnet
    * Servers side Subnet
  * Secondary VPX Subnets
    * Management side Subnet
    * Client side Subnet
    * Servers side Subnet
* 2 optional unallocated EIPs, if the user is opting for EIPs for management interfaces
* 1 unallocated EIP, for public VIP
* 1 more unallocated EIP for ADMAgent, if provisioning of ADMAgent option is enabled.
* EC2 KeyPair

## Post-deployment steps

The users are required to change the password post deployment when asked.

## Network architecture

### ADC state after the deployment

![ADC State after the deployment](./state-of-adc-after-the-deployment.jpg)

## Quick Launch Links

|Region|CFT|
|--|--|
|**US East (N. Virginia)** us-east-1|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|
|**US East (Ohio)** us-east-2|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|
|**US West (N. California)** us-west-1|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|
|**US West (Oregon)** us-west-2|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|
|**Canada (Central)** ca-central-1|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|
|**Asia Pacific (Hong Kong)** ap-east-1|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|
|**Asia Pacific (Mumbai)** ap-south-1|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|
|**Asia Pacific (Tokyo)** ap-northeast-1|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|
|**Asia Pacific (Seoul)** ap-northeast-2|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|
|**Asia Pacific (Singapore)** ap-southeast-1|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|
|**Asia Pacific (Sydney)** ap-southeast-2|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|
|**Europe (Frankfurt)** eu-central-1|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|
|**Europe (Ireland)** eu-west-1|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|
|**Europe (London)** eu-west-2|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|
|**Europe (Paris)** eu-west-3|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-3#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|
|**Europe (Stockholm)** eu-north-1|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-north-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|
|**South America (São Paulo)** sa-east-1|[![cft-launch-button](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/across-availability-zone/for-internal-and-external-apps/ha-3nic-across-az-pipeip.yaml)|

## Additional Links

* [Citrix ADC VPX on AWS](https://docs.citrix.com/en-us/citrix-adc/13/deploying-vpx/deploy-aws.html)
* [Deploy a VPX high-availability pair with private IP addresses across different AWS zones](https://docs.citrix.com/en-us/citrix-adc/current-release/deploying-vpx/deploy-aws/vpx-ha-pip-different-aws-zones.html)
* [How High Availability on AWS works](https://docs.citrix.com/en-us/citrix-adc/13/deploying-vpx/deploy-aws/how-aws-ha-works.html)
* [Citrix ADC Overview](https://www.citrix.com/en-in/products/citrix-adc/)
