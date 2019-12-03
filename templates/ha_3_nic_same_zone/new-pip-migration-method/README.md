## CloudFormation Template description
This template:
- Provisions two CitrixADC and configure them in HA mode
- Each CitrixADC instance will have
  - 3 ENIs associated to same Management, Client and Server subnets
  - 1 EIPs for each CitrixADC instance for Management
  - Also creates required IAM Role


## Input
The `*` against any parameter in the CFT implies it as a mandatory field.
For eg., `VPC ID*` is a mandatory field

## Pre-requisites
The CloudFormation template requires sufficient permissions to create IAM roles, beyond normal EC2 full privileges. The user of this template also needs to [accept the terms and subscribe to the AWS Marketplace product](FIXME: Give 13.0.41.x BYOL product link) before using this CloudFormation template.
<p>The following should be present</p>

- VPC connected to Internet Gateway
- 3 Subnetworks (all in same availability zone)
    - Management side Subnet
    - Client side Subnet
    - Server side Subnet
- 2 unallocated EIPs to attach to Management interface of Primary and Secondary ADCs

## Output
The output of the CloudFormation template includes:
- `DummyIPs`: DO NOT use these IPs	
- `PrimaryADCInstanceID`: Primary Citrix ADC instance ID	
- `PrimaryPublicNSIP`: Primary CitrixADC EIP associated with Management	
- `PrimaryPrivateVIPs`: Primary Client side Private VIPs	
- `SecondaryADCInstanceID`: Primary Citrix ADC instance ID	
- `SecondaryPublicNSIP`: Secondary CitrixADC EIP associated with Management	
- `PrimaryPrivateSNIPs`: Primary Server side Private SNIPs


## Network architecture
![Citrix HA Same AZ Private IP Migration](https://docs.citrix.com/en-us/citrix-adc/media/aws-ha-pip-migration.png)


## Quick Launch Links

- **US East (Ohio)** (us-east-2): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone-pip-migration.template)
- **US East (N. Virginia)** (us-east-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone-pip-migration.template)
- **US West (N. California)** (us-west-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone-pip-migration.template)
- **US West (Oregon)** (us-west-2): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone-pip-migration.template)
- **Asia Pacific (Mumbai)** (ap-south-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone-pip-migration.template)
- **Asia Pacific (Seoul)** (ap-northeast-2): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone-pip-migration.template)
- **Asia Pacific (Singapore)** (ap-southeast-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone-pip-migration.template)
- **Asia Pacific (Sydney)** (ap-southeast-2): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone-pip-migration.template)
- **Asia Pacific (Tokyo)** (ap-northeast-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone-pip-migration.template)
- **Canada (Central)** (ca-central-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone-pip-migration.template)
- **EU (Frankfurt)** (eu-central-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone-pip-migration.template)
- **EU (Ireland)** (eu-west-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone-pip-migration.template)
- **EU (London)** (eu-west-2): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone-pip-migration.template)
- **South America (Sao Paulo)** (sa-east-1): [![Creates a HA pair with two instance of Netscaler with 3 ENIs associated to 3 VPC subnets (Management, Client, Server) on primary and 1 ENI for Management in secondary in the same availability zone](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/netscaler-cft-templates/ha_3_nic_same_zone-pip-migration.template)




## Additional Links:
- **How High Availability on AWS works** : https://docs.citrix.com/en-us/citrix-adc/13/deploying-vpx/deploy-aws/how-aws-ha-works.html
- **Deploy a high availability pair on AWS** : https://docs.citrix.com/en-us/citrix-adc/13/deploying-vpx/deploy-aws/vpx-aws-ha.html
- **Citrix ADC Overview** : https://www.citrix.com/en-in/products/citrix-adc/
