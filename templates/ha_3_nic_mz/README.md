## CloudFormation Template description
This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary.The output of the CloudFormation template includes:

- `PrimaryVPXManagementURL`: HTTPS URL to the Management GUI of Primary VPX (uses self-signed cert)
- `PrimaryVPXManagementURL2`: HTTP URL to the Management GUI of Primary VPX
- `PrimaryInstanceIdNS`: Instance Id of newly created Primary VPX instance
- `PrimaryVPXPublicIpVIP`:  Elastic IP address of the Primary VPX instance associated with the VIP
- `PrimaryVPXNSIp`:  Private IP (NS IP) used for management of Primary VPX
- `PrimaryVPXPublicNSIp`:  Public IP (NS IP) used for management of Primary VPX
- `PrimaryVPXPrivateVIP`:  Private IP address of the Primary VPX instance associated with the VIP
- `PrimaryVPXSNIP`:  Private IP address of the Primary VPX instance associated with the SNIP
- `SecondaryVPXManagementURL`:  HTTPS URL to the Management GUI of Secondary VPX (uses self-signed cert)
- `SecondaryVPXManagementURL2`:  HTTP URL to the Management GUI of Secondary VPX
- `SecodnaryInstanceIdNS`:  Instance Id of newly created Secondary VPX instance
- `SecondaryVPXNSIp`:  Private IP (NS IP) used for management of Secondary VPX
- `SecondaryVPXPublicNSIp`:  Public IP (NS IP) used for management of Secondary VPX
- `SecondaryVPXPrivateVIP`:  Private IP address of the Secondary VPX instance associated with the VIP
- `SecondaryVPXSNIP`:  Private IP address of the Secondary VPX instance associated with the SNIP
- `SecurityGroup`:  Security group id that the VPX belongs to


## Pre-requisites
The CloudFormation template requires sufficient permissions to create IAM roles, beyond normal EC2 full privileges. The user of this template also needs to [accept the terms and subscribe to the AWS Marketplace product](https://aws.amazon.com/marketplace/pp/B00AA01BOE) before using this CloudFormation template.
<p>The following should be present</p>

- VPC connected to Internet Gateway
- 6 Subnetworks ( 3 each in every availability zone)
	- Primary VPX Subnets
		- Management side Subnet
		- Client side Subnet
		- Servers side Subnet
	- Secondary VPX Subnets
		- Management side Subnet
		- Client side Subnet
		- Servers side Subnet


## Network architecture
![Citrix HA Across AZ](https://docs.citrix.com/en-us/netscaler/media/aws-hainc.png)


## Quick Launch Links

- **US East (Ohio)** (us-east-2): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **US East (N. Virginia)** (us-east-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **US West (N. California)** (us-west-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **US West (Oregon)** (us-west-2): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **Asia Pacific (Mumbai)** (ap-south-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **Asia Pacific (Osaka-Local)** (ap-northeast-3): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-3#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **Asia Pacific (Seoul)** (ap-northeast-2): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **Asia Pacific (Singapore)** (ap-southeast-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **Asia Pacific (Sydney)** (ap-southeast-2): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **Asia Pacific (Tokyo)** (ap-northeast-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **Canada (Central)** (ca-central-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **China (Beijing)** (cn-north-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=cn-north-1#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **China (Ningxia)** (cn-northwest-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=cn-northwest-1#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **EU (Frankfurt)** (eu-central-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **EU (Ireland)** (eu-west-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **EU (London)** (eu-west-2): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **EU (Paris)** (eu-west-3): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-3#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **EU (Stockholm)** (eu-north-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-north-1#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)
- **South America (Sao Paulo)** (sa-east-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?stackName=NetScalerVPX-HAPair-MZ&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-ha-3-nic-mz.template)




## Additional Links:

- **HA Across AZs**: https://docs.citrix.com/en-us/netscaler/12-1/deploying-vpx/deploy-aws/high-availability-different-zones.html
- **VPX installation in AWS** : https://docs.citrix.com/en-us/netscaler/12/deploying-vpx/install-vpx-on-aws.html
- **NetScaler Overview** : https://www.citrix.com/products/netscaler-adc/resources/netscaler-vpx.html
