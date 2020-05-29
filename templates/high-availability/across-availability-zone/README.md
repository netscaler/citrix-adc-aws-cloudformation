## CloudFormation Template description
> If VPC, subnets, iGateway do not already exists and ADCs are to be provisioned on fresh resources, refer [vpc-infra](../../vpc-infra/) to create the prequisite infra

This template provisions two Citrix ADC VPX in two different AWS Availability Zones and configures them as High-Availabile. This template also gives an option to allocate Pooled License to Citrix ADCs while provisioning.
This template creates the below resources:
- IAM Role required for HA configuration
- 3 Security Groups
	- Management Security Group for management (NSIP) interfaces
	- Client Security Group for client (VIP) interfaces
	- Server Security Group for server (SNIP) interfaces
- 6 Elastic Network Interfaces (3 for each Citrix ADCs)
	- Primary Citrix ADC
		- Management interface (eth0) 
		- Client interface (eth1) 
		- Server interface (eth2) 
	- Secondary Citrix ADC
		- Management interface (eth0) 
		- Client interface (eth1) 
		- Server interface (eth2) 
- 3 Elastic IPs `User has option not to create these EIPs`
	- Management EIP for Primary Citrix ADC
	- Management EIP for Secondary Citrix ADC
	- Client EIP for VIP `<--This EIP gets migrated from Primary to Secondary (new-primary) upon HA failover`



## Pre-requisites
The CloudFormation template requires sufficient IAM previliges to create IAM roles, beyond normal EC2 full privileges. The user of this template also needs to [accept the terms and subscribe to the AWS Marketplace product](https://aws.amazon.com/marketplace/pp/B00AA01BOE/) before using this CloudFormation template.
<p>The following should be present</p>

- VPC connected to Internet Gateway
- 6 Subnetworks (3 each in every availability zone)
	- Primary VPX Subnets
		- Management side Subnet
		- Client side Subnet
		- Servers side Subnet
	- Secondary VPX Subnets
		- Management side Subnet
		- Client side Subnet
		- Servers side Subnet
- 3 unallocated EIPs


## Network architecture
![Citrix HA Across AZ](https://docs.citrix.com/en-us/netscaler/media/aws-hainc.png)


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

- **HA Across AZs**: https://docs.citrix.com/en-us/netscaler/12-1/deploying-vpx/deploy-aws/high-availability-different-zones.html
- **VPX installation in AWS** : https://docs.citrix.com/en-us/netscaler/12/deploying-vpx/install-vpx-on-aws.html
- **NetScaler Overview** : https://www.citrix.com/products/netscaler-adc/resources/netscaler-vpx.html
