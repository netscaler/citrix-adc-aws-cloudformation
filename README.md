
Citrix ADC (Formerly NetScaler) AWS Cloudformation templates
--------------------------------------

This is a repository for [Citrix ADC's](https://www.citrix.com/products/citrix-adc/) CloudFormation templates for deploying Citrix ADC in AWS (Amazon Web Services). 

>If you are looking for Ansible playbooks to deploy Citrix ADC services in AWS, click [here](https://github.com/citrix/citrix-ansible-aws)

## Citrix ADC VPX
Citrix ADC VPX is a virtual application delivery controller that combines the latest cloud-native features with a simple user experience. The Citrix ADC optimizes the user experience ensuring that applications are always available by using advanced L4-7 load balancing, traffic management and proven application acceleration such as HTTP compression and caching.

## Citrix ADC VPX in AWS
Citrix ADC VPX is available as Amazon Machine Images (AMI) in the [AWS Marketplace](https://aws.amazon.com/marketplace/seller-profile?id=fb9c6078-b60f-47f6-8622-49d5e1d5aca7). Before using a CloudFormation template to provision a Citrix ADC VPX in AWS, the AWS user has to accept the terms and subscribe to the AWS Marketplace product. Each edition of the Citrix ADC VPX in the Marketplace requires this step.

## About these CloudFormation templates
Each template in this repository has colocated documentation describing the usage and architecture of the template. The templates attempt to codify recommended deployment architecture of the Citrix ADC VPX, or to introduce the user to the Citrix ADC or to demonstrate a particular feature / edition / option. Users can re-use / modify or enhance the templates to suit their particular production and testing needs. Most templates require full EC2 permissions as well as permissions to create IAM roles.

## A note on AMI Ids
The CloudFormation templates contain AMI Ids that are specific to a particular release of the Citrix ADC VPX (e.g., release 12.0-56.20) and edition (e.g., Citrix ADC VPX Platinum Edition - 10 Mbps) OR Citrix ADC BYOL. To use a different version / edition of the Citrix ADC VPX with a CloudFormation template requires the user to edit the template and replace the AMI Ids.
> Latest Citrix ADC AWS-AMI-IDs can be found [here](https://github.com/citrix/citrix-adc-aws-cloudformation/blob/master/templates/README.md)

## Versioning
The master branch of the repository generally has the latest version of the template. Older released versions are tagged appropriately

## Support
For production issues with the templates, please contact Citrix Support through your normal support channels. If you have fixes / suggestions for improvements or requests, please raise an issue in this repository, by filling the detailed Bug Report.

## Further reading
- Deploy a Citrix ADC VPX standalone instance on AWS : https://docs.citrix.com/en-us/citrix-adc/12-1/deploying-vpx/deploy-aws/launch-vpx-for-aws-ami.html
- Citrix ADC 12.1 Documention : https://docs.citrix.com/en-us/citrix-adc/12-1/
- Citrix ADC Overview : https://www.citrix.com/products/citrix-adc/

