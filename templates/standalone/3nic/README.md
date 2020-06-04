## CloudFormation Template description

This template provisions two Citrix ADC VPX in two different AWS Availability Zones and configures them as High-Availabile. This template also gives an option to allocate Pooled License to Citrix ADCs while provisioning.
This template   Launches required number of Citrix ADCs. By default Customer Licensed (BYOL) ADC will be launched with 3 ENIs associated to 3 VPC subnets (Management, Client, Server).

This template provisions a 3nic Citrix ADC VPX.
This template also gives an option to allocate Pooled License to Citrix ADCs while provisioning.
This template creates the below resources:
- IAM Role required for HA configuration
- 3 Security Groups
	- Management Security Group for management (NSIP) interfaces
	- Client Security Group for client (VIP) interfaces
	- Server Security Group for server (SNIP) interfaces
- 3 Elastic Network Interfaces (3 for each Citrix ADCs)
	- Management interface (eth0) 
	- Client interface (eth1) 
	- Server interface (eth2) 
- 1 Elastic IP for Management interface `User has option not to create these EIPs`

## Pre-requisites
> If VPC, subnets, iGateway do not already exists and ADCs are to be provisioned on fresh resources, refer [vpc-infra](../../../vpc-infra/) to create the prequisite infra
The CloudFormation template requires sufficient IAM previliges to create IAM roles, beyond normal EC2 full privileges. The user of this template also needs to [accept the terms and subscribe to the AWS Marketplace product](https://aws.amazon.com/marketplace/pp/B00AA01BOE/) before using this CloudFormation template.
<p>The following should be present</p>
- VPC connected to Internet Gateway
- 3 Subnetworks (3 each in every availability zone)
	- Management side Subnet
	- Client side Subnet
	- Servers side Subnet
- 1 unallocated EIP
- EC2 KeyPair



## Quick Launch Links
|Region|CFT|
|--|--|
|**US East (N. Virginia)** us-east-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|
|**US East (Ohio)** us-east-2|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|
|**US West (N. California)** us-west-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|
|**US West (Oregon)** us-west-2|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|
|**Canada (Central)** ca-central-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|
|**Asia Pacific (Hong Kong)** ap-east-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|
|**Asia Pacific (Mumbai)** ap-south-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|
|**Asia Pacific (Tokyo)** ap-northeast-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|
|**Asia Pacific (Seoul)** ap-northeast-2|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|
|**Asia Pacific (Singapore)** ap-southeast-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|
|**Asia Pacific (Sydney)** ap-southeast-2|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|
|**Europe (Frankfurt)** eu-central-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|
|**Europe (Ireland)** eu-west-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|
|**Europe (London)** eu-west-2|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|
|**Europe (Paris)** eu-west-3|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-3#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|
|**Europe (Stockholm)** eu-north-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-north-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|
|**South America (São Paulo)** sa-east-1|[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/standalone/3nic/standalone-3nic-adc.yaml)|

## Additional Links:
- **Citrix ADC VPX on AWS**: https://docs.citrix.com/en-us/citrix-adc/13/deploying-vpx/deploy-aws.html
- **Deploy a Citrix ADC VPX standalone instance on AWS**:https://docs.citrix.com/en-us/citrix-adc/13/deploying-vpx/deploy-aws/launch-vpx-for-aws-ami.html
- **Citrix ADC Overview** : https://www.citrix.com/en-in/products/citrix-adc/
