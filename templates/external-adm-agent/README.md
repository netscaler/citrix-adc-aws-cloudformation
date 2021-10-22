## CloudFormation Template description

This template provisions a Citrix External ADM agent in AWS, as well as registers it with the ADM service.

This template provisions a 1nic Citrix External ADM.

## Pre-requisites

> If VPC, subnets, iGateway do not already exists and ADCs are to be provisioned on fresh resources, refer [vpc-infra](../../../vpc-infra/) to create the prequisite infra

The CloudFormation template requires sufficient IAM previliges to create IAM roles, beyond normal EC2 full privileges.

The user of this template also needs to [accept the terms and subscribe to the AWS Marketplace product](https://aws.amazon.com/marketplace/pp/prodview-wuhs2ryexcf6e) before using this CloudFormation template.

The following should be present
*VPC connected to Internet Gateway

* 1 Subnetwork: Management side Subnet
* 1 unallocated EIP, if user wants to use EIP for management
* EC2 KeyPair

## Quick Launch Links

|Region|CFT|
|--|--|
|**US East (N. Virginia)** us-east-1|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|
|**US East (Ohio)** us-east-2|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|
|**US West (N. California)** us-west-1|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|
|**US West (Oregon)** us-west-2|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|
|**Canada (Central)** ca-central-1|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ca-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|
|**Asia Pacific (Hong Kong)** ap-east-1|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|
|**Asia Pacific (Mumbai)** ap-south-1|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|
|**Asia Pacific (Tokyo)** ap-northeast-1|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|
|**Asia Pacific (Seoul)** ap-northeast-2|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|
|**Asia Pacific (Singapore)** ap-southeast-1|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|
|**Asia Pacific (Sydney)** ap-southeast-2|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|
|**Europe (Frankfurt)** eu-central-1|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|
|**Europe (Ireland)** eu-west-1|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|
|**Europe (London)** eu-west-2|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|
|**Europe (Paris)** eu-west-3|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-3#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|
|**Europe (Stockholm)** eu-north-1|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-north-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|
|**South America (São Paulo)** sa-east-1|[![launch-button-logo](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=sa-east-1#/stacks/new?templateURL=https://s3.amazonaws.com/citrixadc-automation/templates/external-adm-agent/external-adm-agent.yaml)|

## Additional Links

* **Install Citrix ADM Agent agent on AWS**: <https://docs.citrix.com/en-us/citrix-application-delivery-management-service/getting-started/install-agent-on-aws.html>
* **Getting Started with Citrix ADM service**: <https://docs.citrix.com/en-us/citrix-application-delivery-management-service/getting-started/install-agent-on-aws.html>
