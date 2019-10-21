## CloudFormation Template description
This template deploys a VPC, with 3 subnets (Management, client, server) for 2 Availability Zones.
It deploys an Internet Gateway, with a default  route on the public subnets.
This template also creates a HA pair across Availability Zones with two instance of Citrix ADC:
3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated
to 3 VPC subnets (Management, Client, Server) on secondary.
All the resource names created by this CFT will be prefixed with a tagName of the stackname.

The output of the CloudFormation template includes:

- `VPCID`: VPC ID
- `InstanceProfileName`: Instance Profile for ADCs
- `ManagementSecurityGroupID`: Security Group ID for Management ENIs
- `ClientSecurityGroupID`: Security Group ID for Client ENIs
- `ServerSecurityGroupID`: Security Group ID for Server ENIs
- `PrimaryManagementPublicEIP`: Primary Management Public EIP
- `PrimaryADCInstanceID`: Primary ADC Instance ID
- `PrimaryCitrixADCManagementURL`: HTTPS URL to the Management GUI of Primary CitrixADC (uses self-signed cert)
- `PrimaryCitrixADCManagementURL2`: HTTP URL to the Management GUI of Primary CitrixADC
- `PrimaryClientPublicEIP`: Primary Client Public EIP
- `PrimaryManagementPrivateNSIP`: Primary Management Private NSIP
- `PrimaryClientPrivateVIP`: Primary Client Private VIP
- `PrimaryManagementPublicSubnetID`: Primary Management Public Subnet ID
- `PrimaryClientPublicSubnetID`: Primary Client Public Subnet ID
- `PrimaryServerPrivateSubnetID`: Primary Server Private Subnet ID
- `SecondaryManagementPublicEIP`: Secondary Management Public EIP
- `SecondaryADCInstanceID`: Secondary ADC Instance ID
- `SecondaryCitrixADCManagementURL`: HTTPS URL to the Management GUI of Secondary CitrixADC (uses self-signed cert)
- `SecondaryCitrixADCManagementURL2`: HTTP URL to the Management GUI of Secondary CitrixADC
- `SecondaryManagementPrivateNSIP`: Secondary Management Private NSIP
- `SecondaryClientPrivateVIP`: Secondary Client Private VIP
- `SecondaryManagementPublicSubnetID`: Secondary Management Public Subnet ID
- `SecondaryClientPublicSubnetID`: Secondary Client Public Subnet ID
- `SecondaryServerPrivateSubnetID`: Secondary Server Private Subnet ID


## Pre-requisites
The CloudFormation template requires sufficient permissions to create IAM roles, beyond normal EC2 full privileges. The user of this template also needs to [accept the terms and subscribe to the AWS Marketplace product](https://aws.amazon.com/marketplace/pp/B00AA01BOE/) before using this CloudFormation template.
<p>The following should be present</p>

- Key Pair
- 3 unallocated EIPs
	- Primary Management
	- Client VIP
	- Secondary Management

## Network architecture
![Citrix HA Across AZ](https://docs.citrix.com/en-us/netscaler/media/aws-hainc.png)


## Quick Launch Links

- **US East (Ohio)** (us-east-2): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrix-aws-quickstart/quickstart-aws-ha-across-az/templates/ha-across-az-master.yaml.template)
- **US East (N. Virginia)** (us-east-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrix-aws-quickstart/quickstart-aws-ha-across-az/templates/ha-across-az-master.yaml.template)
- **US West (N. California)** (us-west-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrix-aws-quickstart/quickstart-aws-ha-across-az/templates/ha-across-az-master.yaml.template)
- **US West (Oregon)** (us-west-2): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrix-aws-quickstart/quickstart-aws-ha-across-az/templates/ha-across-az-master.yaml.template)
- **Asia Pacific (Mumbai)** (ap-south-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrix-aws-quickstart/quickstart-aws-ha-across-az/templates/ha-across-az-master.yaml.template)
- **Asia Pacific (Seoul)** (ap-northeast-2): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrix-aws-quickstart/quickstart-aws-ha-across-az/templates/ha-across-az-master.yaml.template)
- **Asia Pacific (Singapore)** (ap-southeast-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrix-aws-quickstart/quickstart-aws-ha-across-az/templates/ha-across-az-master.yaml.template)
- **Asia Pacific (Sydney)** (ap-southeast-2): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrix-aws-quickstart/quickstart-aws-ha-across-az/templates/ha-across-az-master.yaml.template)
- **Asia Pacific (Tokyo)** (ap-northeast-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrix-aws-quickstart/quickstart-aws-ha-across-az/templates/ha-across-az-master.yaml.template)
- **Canada (Central)** (ca-central-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrix-aws-quickstart/quickstart-aws-ha-across-az/templates/ha-across-az-master.yaml.template)
- **EU (Frankfurt)** (eu-central-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrix-aws-quickstart/quickstart-aws-ha-across-az/templates/ha-across-az-master.yaml.template)
- **EU (Ireland)** (eu-west-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrix-aws-quickstart/quickstart-aws-ha-across-az/templates/ha-across-az-master.yaml.template)
- **EU (London)** (eu-west-2): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrix-aws-quickstart/quickstart-aws-ha-across-az/templates/ha-across-az-master.yaml.template)
- **South America (Sao Paulo)** (sa-east-1): [![This template creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on secondary](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrix-aws-quickstart/quickstart-aws-ha-across-az/templates/ha-across-az-master.yaml.template)




## Additional Links:

- **HA Across AZs**: https://docs.citrix.com/en-us/citrix-adc/13/deploying-vpx/deploy-aws/high-availability-different-zones.html
- **VPX installation in AWS** : https://docs.citrix.com/en-us/citrix-adc/13/deploying-vpx/deploy-aws.html
- **Citrix ADC Overview** : https://www.citrix.com/products/citrix-adc/
