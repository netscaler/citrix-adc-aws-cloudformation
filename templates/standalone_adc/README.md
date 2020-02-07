## CloudFormation Template description
This template   Launches required number of Citrix ADCs. By default Customer Licensed (BYOL) ADC will be launched with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary.

The output of the CloudFormation template includes:

- `InstanceIDsWithIPs`: Instances created with their IPs in `{IP:InstanceID}` format

## Input
The `*` against any parameter in the CFT implies it as a mandatory field.
For eg., `VPC ID*` is a mandatory field

## Pre-requisites
The CloudFormation template requires sufficient permissions to create IAM roles, beyond normal EC2 full privileges. The use must have already subscribed to the AMI to be launched (default AMI launched will be [Citrix ADC (formerly NetScaler) VPX - Customer Licensed](https://aws.amazon.com/marketplace/pp/B00AA01BOE) before using this CloudFormation template.

<p>The following should be present</p>

- VPC connected to Internet Gateway
- Enough EIPs
    - How much EIPs?
	    - 2 EIPs for one Citrix ADC (One for Management, Another for CLient)
- 3 Subnetworks
	- Management side Subnet
	- Client side Subnet
	- Servers side Subnet



## Quick Launch Links

- **US East (Ohio)** (us-east-2): [![This template   Launches required number of Citrix ADCs. By default Customer Licensed (BYOL) ADC will be launched with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary.](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=CitrixADC-1&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **US East (N. Virginia)** (us-east-1): [![This template   Launches required number of Citrix ADCs. By default Customer Licensed (BYOL) ADC will be launched with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary.](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=CitrixADC-1&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **US West (N. California)** (us-west-1): [![This template   Launches required number of Citrix ADCs. By default Customer Licensed (BYOL) ADC will be launched with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary.](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/new?stackName=CitrixADC-1&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **US West (Oregon)** (us-west-2): [![This template   Launches required number of Citrix ADCs. By default Customer Licensed (BYOL) ADC will be launched with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary.](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=CitrixADC-1&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **Asia Pacific (Mumbai)** (ap-south-1): [![This template   Launches required number of Citrix ADCs. By default Customer Licensed (BYOL) ADC will be launched with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary.](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?stackName=CitrixADC-1&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **Asia Pacific (Seoul)** (ap-northeast-2): [![This template   Launches required number of Citrix ADCs. By default Customer Licensed (BYOL) ADC will be launched with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary.](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?stackName=CitrixADC-1&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **Asia Pacific (Singapore)** (ap-southeast-1): [![This template   Launches required number of Citrix ADCs. By default Customer Licensed (BYOL) ADC will be launched with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary.](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?stackName=CitrixADC-1&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **Asia Pacific (Sydney)** (ap-southeast-2): [![This template   Launches required number of Citrix ADCs. By default Customer Licensed (BYOL) ADC will be launched with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary.](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=CitrixADC-1&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **Asia Pacific (Tokyo)** (ap-northeast-1): [![This template   Launches required number of Citrix ADCs. By default Customer Licensed (BYOL) ADC will be launched with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary.](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=CitrixADC-1&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **Canada (Central)** (ca-central-1): [![This template   Launches required number of Citrix ADCs. By default Customer Licensed (BYOL) ADC will be launched with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary.](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/new?stackName=CitrixADC-1&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **EU (Frankfurt)** (eu-central-1): [![This template   Launches required number of Citrix ADCs. By default Customer Licensed (BYOL) ADC will be launched with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary.](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=CitrixADC-1&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **EU (Ireland)** (eu-west-1): [![This template   Launches required number of Citrix ADCs. By default Customer Licensed (BYOL) ADC will be launched with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary.](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=CitrixADC-1&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **EU (London)** (eu-west-2): [![This template   Launches required number of Citrix ADCs. By default Customer Licensed (BYOL) ADC will be launched with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary.](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?stackName=CitrixADC-1&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)
- **South America (Sao Paulo)** (sa-east-1): [![This template   Launches required number of Citrix ADCs. By default Customer Licensed (BYOL) ADC will be launched with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary.](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?stackName=CitrixADC-1&templateURL=https://s3.amazonaws.com/netscaler-cft-templates/cft-create-multiple-byol-vpx.template)




## Additional Links:
- **Citrix ADC on AWS** : https://www.citrix.com/en-in/products/citrix-adc/resources/netscaler-on-aws.html
- **VPX installation in AWS** : https://docs.citrix.com/en-us/netscaler/12/deploying-vpx/install-vpx-on-aws.html
- **NetScaler Overview** : https://www.citrix.com/products/netscaler-adc/resources/netscaler-vpx.html
