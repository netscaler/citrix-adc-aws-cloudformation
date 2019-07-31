## CloudFormation Template description
This template -
- Creates a HA pair with two instance of Citrix ADC BYOL edition with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone.


## Input
The `*` against any parameter in the CFT implies it as a mandatory field.
For eg., `VPC ID*` is a mandatory field

## Pre-requisites
The CloudFormation template requires sufficient permissions to create IAM roles, beyond normal EC2 full privileges. The user of this template also needs to [accept the terms and subscribe to the AWS Marketplace product](https://aws.amazon.com/marketplace/pp/B00AA01BOE) before using this CloudFormation template.
<p>The following should be present</p>

- VPC connected to Internet Gateway
- 3 Subnetworks (all in same availability zone)
    - Management side Subnet
    - Client side Subnet
    - Server side Subnet
- 2 unallocated EIPs to attach to Management interface of Primary and Secondary ADCs

## Output
The output of the CloudFormation template includes:

- `IPAddressNSSec`: Elastic IP address of the Netscalar Secondary instance associated with Management
- `InstanceIdNSSec`: Instance Id of newly created Secondary Netscalar instance
- `InstanceIdNS`: Instance Id of newly created Primary Netscalar instance
- `IPAddressNS`: Elastic IP address of the Netscalar Primary instance associated with Management

## Network architecture
![Citrix HA Same AZ](https://docs.citrix.com/en-us/netscaler/media/ha-aws.png)


## Quick Launch Links

- **US East (Ohio)** (us-east-2): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone.template)
- **US East (N. Virginia)** (us-east-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone.template)
- **US West (N. California)** (us-west-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone.template)
- **US West (Oregon)** (us-west-2): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone.template)
- **Asia Pacific (Mumbai)** (ap-south-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone.template)
- **Asia Pacific (Seoul)** (ap-northeast-2): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone.template)
- **Asia Pacific (Singapore)** (ap-southeast-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone.template)
- **Asia Pacific (Sydney)** (ap-southeast-2): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone.template)
- **Asia Pacific (Tokyo)** (ap-northeast-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone.template)
- **Canada (Central)** (ca-central-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone.template)
- **EU (Frankfurt)** (eu-central-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone.template)
- **EU (Ireland)** (eu-west-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone.template)
- **EU (London)** (eu-west-2): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone.template)
- **South America (Sao Paulo)** (sa-east-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone.template)




## Additional Links:
- **Installing Citrix ADM agent on AWS**: https://docs.citrix.com/en-us/citrix-application-delivery-management-service/getting-started/install-agent-on-aws.html
- **VPX installation in AWS** : https://docs.citrix.com/en-us/netscaler/12/deploying-vpx/install-vpx-on-aws.html
- **Citrix ADC Overview** : https://www.citrix.com/products/netscaler-adc/resources/netscaler-vpx.html
