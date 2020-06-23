## CloudFormation Template description

This template provisions two Citrix ADC VPX in two different AWS Availability Zones and configures them as High-Availabile. This template also gives an option to allocate Pooled License to Citrix ADCs while provisioning.
This template:
- Provisions two CitrixADC and configure them in HA mode
- After deployment, each CitrixADC instance will have
  - 3 ENIs associated to same Management, Client and Server subnets
  - 2 EIPs for each CitrixADC instance for Management
  - 1 EIP for Client VIP >
	- 1 Client EIP for VIP `<--This EIP gets migrated from Primary to Secondary (new-primary) upon HA failover`
  - Required IAM Role


## Pre-requisites
> If VPC, subnets, iGateway do not already exists and ADCs are to be provisioned on fresh resources, refer [vpc-infra](../../vpc-infra/) to create the prequisite infra
The CloudFormation template requires sufficient IAM previliges to create IAM roles, beyond normal EC2 full privileges. The user of this template also needs to [accept the terms and subscribe to the AWS Marketplace product](https://aws.amazon.com/marketplace/pp/B00AA01BOE/) before using this CloudFormation template.
<p>The following should be present</p>

- VPC connected to Internet Gateway
- 3 Subnetworks (all in same availability zone)
    - Management side Subnet
    - Client side Subnet
    - Server side Subnet
- 3 unallocated EIPs
- EC2 KeyPair


## Network architecture
![Citrix HA Same AZ Private IP Migration](./citrix-adc-ha-same-zone-architecture.png)


## Quick Launch Links
|Region|CFT|
|--|--|
|**US East (N. Virginia)** us-east-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|
|**US East (Ohio)** us-east-2|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|
|**US West (N. California)** us-west-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|
|**US West (Oregon)** us-west-2|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|
|**Canada (Central)** ca-central-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|
|**Asia Pacific (Hong Kong)** ap-east-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|
|**Asia Pacific (Mumbai)** ap-south-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|
|**Asia Pacific (Tokyo)** ap-northeast-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|
|**Asia Pacific (Seoul)** ap-northeast-2|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|
|**Asia Pacific (Singapore)** ap-southeast-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|
|**Asia Pacific (Sydney)** ap-southeast-2|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|
|**Europe (Frankfurt)** eu-central-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|
|**Europe (Ireland)** eu-west-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|
|**Europe (London)** eu-west-2|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|
|**Europe (Paris)** eu-west-3|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-3#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|
|**Europe (Stockholm)** eu-north-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-north-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|
|**South America (São Paulo)** sa-east-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/high-availability/same-availability-zone/ha-3nic-same-az.yaml)|


## Additional Links:
- **Citrix ADC VPX on AWS**: https://docs.citrix.com/en-us/citrix-adc/13/deploying-vpx/deploy-aws.html
- **Deploy a high availability pair on AWS** : https://docs.citrix.com/en-us/citrix-adc/13/deploying-vpx/deploy-aws/vpx-aws-ha.html
- **How High Availability on AWS works** : https://docs.citrix.com/en-us/citrix-adc/13/deploying-vpx/deploy-aws/how-aws-ha-works.html
- **Citrix ADC Overview** : https://www.citrix.com/en-in/products/citrix-adc/
