## CloudFormation Template description
This template -
- Creates required number of Citrix BYOL ADC with 3 ENIs each, associated to 3 VPC subnets (Management, Client, Server)
- Allocates user defined license to the above created ADCs

## Input
The `*` against any parameter in the CFT implies it as a mandatory field.
For eg., `VPC ID*` is a mandatory field

## Pre-requisites
The CloudFormation template requires sufficient permissions to create IAM roles, beyond normal EC2 full privileges. The user of this template also needs to [accept the terms and subscribe to the AWS Marketplace product](https://aws.amazon.com/marketplace/pp/B00AA01BOE) before using this CloudFormation template.
<p>The following should be present - </p>

- VPC connected to Internet Gateway
- 3 Subnetworks (in the same availability zones)
	- Management side Subnet
	- Client side Subnet
	- Server side Subnet
- Enough number of unallocated EIPs to attach to Management and Client interfaces of of each created ADC
> Each instance of ADC requires 2 EIPs - One for Management and the other for Client side
- Rechable ADM/ ADM-Agent configured as license server

## Output
The output of the CloudFormation template includes:

- `InstanceIDsWithIPs`: IPs of created BYOL ADCs with their respective EC2 instance-IDs in `{ip:instance}` format

## Quick Launch Links

- **US East (Ohio)** (us-east-2): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **US East (N. Virginia)** (us-east-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **US West (N. California)** (us-west-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **US West (Oregon)** (us-west-2): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **Asia Pacific (Mumbai)** (ap-south-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **Asia Pacific (Seoul)** (ap-northeast-2): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **Asia Pacific (Singapore)** (ap-southeast-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **Asia Pacific (Sydney)** (ap-southeast-2): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **Asia Pacific (Tokyo)** (ap-northeast-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **Canada (Central)** (ca-central-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **EU (Frankfurt)** (eu-central-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **EU (Ireland)** (eu-west-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **EU (London)** (eu-west-2): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **South America (Sao Paulo)** (sa-east-1): [![This template creates a HA pair with two instance of Citrix ADC with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)




## Additional Links:

- **HA Across AZs**: https://docs.citrix.com/en-us/netscaler/12-1/deploying-vpx/deploy-aws/high-availability-different-zones.html
- **VPX installation in AWS** : https://docs.citrix.com/en-us/netscaler/12/deploying-vpx/install-vpx-on-aws.html
- **NetScaler Overview** : https://www.citrix.com/products/netscaler-adc/resources/netscaler-vpx.html
