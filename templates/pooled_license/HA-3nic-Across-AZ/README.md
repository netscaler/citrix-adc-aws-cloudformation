## CloudFormation Template description
> If you want to provision 2 ADCs in HA mode Across AZ, without allocating initial license, refer: https://github.com/citrix/netscaler-aws-cloudformation/tree/master/templates/ha_3_nic_mz

This template -
- Creates a HA pair with two instances of Citrix ADC with 3 Network Interfaces associated to 3 VPC subnets (Management, Client, Server) on primary and 3 Network Interfaces associated to 3 VPC subnets (Management, Client, Server) on secondary.
- Allocates user defined license to the above ADC pair

## Input
The `*` against any parameter in the CFT implies it as a mandatory field.
For eg., `VPC ID*` is a mandatory field

## Pre-requisites
The CloudFormation template requires sufficient permissions to create IAM roles, beyond normal EC2 full privileges. The user of this template also needs to [accept the terms and subscribe to the AWS Marketplace product](https://aws.amazon.com/marketplace/pp/B00AA01BOE) before using this CloudFormation template.
<p>The following should be present</p>

- VPC connected to Internet Gateway
- 6 Subnetworks (3 each in every Availability Zone)
	- Primary VPX Subnets
		- Management side Subnet
		  > NOTE: The Management Subnet CIDR should be different from that of VPC.
		- Client side Subnet
		- Server side Subnet
	- Secondary VPX Subnets
		- Management side Subnet
		- Client side Subnet
		- Server side Subnet
- 4 unallocated EIPs to attach to Management and Client interfaces of Primary and Secondary ADCs
- Rechable ADM/ ADM-Agent configured as license server

## Output
The output of the CloudFormation template includes:

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

## Network architecture
![Citrix HA Across AZ](https://docs.citrix.com/en-us/netscaler/media/aws-hainc.png)


## Quick Launch Links

- **US East (Ohio)** (us-east-2): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/license-cft-HA-3nic-Across-AZ.template)
- **US East (N. Virginia)** (us-east-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/license-cft-HA-3nic-Across-AZ.template)
- **US West (N. California)** (us-west-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/license-cft-HA-3nic-Across-AZ.template)
- **US West (Oregon)** (us-west-2): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/license-cft-HA-3nic-Across-AZ.template)
- **Asia Pacific (Mumbai)** (ap-south-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/license-cft-HA-3nic-Across-AZ.template)
- **Asia Pacific (Seoul)** (ap-northeast-2): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/license-cft-HA-3nic-Across-AZ.template)
- **Asia Pacific (Singapore)** (ap-southeast-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/license-cft-HA-3nic-Across-AZ.template)
- **Asia Pacific (Sydney)** (ap-southeast-2): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/license-cft-HA-3nic-Across-AZ.template)
- **Asia Pacific (Tokyo)** (ap-northeast-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/license-cft-HA-3nic-Across-AZ.template)
- **Canada (Central)** (ca-central-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/license-cft-HA-3nic-Across-AZ.template)
- **EU (Frankfurt)** (eu-central-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/license-cft-HA-3nic-Across-AZ.template)
- **EU (Ireland)** (eu-west-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/license-cft-HA-3nic-Across-AZ.template)
- **EU (London)** (eu-west-2): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/license-cft-HA-3nic-Across-AZ.template)
- **South America (Sao Paulo)** (sa-east-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/license-cft-HA-3nic-Across-AZ.template)




## Additional Links:

- **Pooled Capacity**: https://docs.citrix.com/en-us/citrix-application-delivery-management-service/manage-licenses/pooled-capacity.html
- **HA Across AZs**: https://docs.citrix.com/en-us/netscaler/12-1/deploying-vpx/deploy-aws/high-availability-different-zones.html
- **Installing Citrix ADM agent on AWS**: https://docs.citrix.com/en-us/citrix-application-delivery-management-service/getting-started/install-agent-on-aws.html
- **VPX installation in AWS** : https://docs.citrix.com/en-us/netscaler/12/deploying-vpx/install-vpx-on-aws.html
- **Citrix ADC Overview** : https://www.citrix.com/products/netscaler-adc/resources/netscaler-vpx.html
