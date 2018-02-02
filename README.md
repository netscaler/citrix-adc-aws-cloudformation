
Citrix NetScaler AWS Cloudformation templates
--------------------------------------

This is a repository for [Citrix NetScaler's](https://www.citrix.com/products/netscaler-adc/) CloudFormation templates for deploying Citrix NetScaler in AWS (Amazon Web Services). 

## Citrix NetScaler VPX
Citrix NetScaler VPX is a virtual application delivery controller that combines the latest cloud-native features with a simple user experience. The NetScaler optimizes the user experience ensuring that applications are always available by using advanced L4-7 load balancing, traffic management and proven application acceleration such as HTTP compression and caching.

## Citrix NetScaler VPX in AWS
Citrix NetScaler VPX is available as Amazon Machine Images (AMI) in the [AWS Marketplace](https://aws.amazon.com/marketplace/seller-profile?id=fb9c6078-b60f-47f6-8622-49d5e1d5aca7). Before using a CloudFormation template to provision a Citrix NetScaler VPX in AWS, the AWS user has to accept the terms and subscribe to the AWS Marketplace product. Each edition of the Citrix NetScaler VPX in the Marketplace requires this step.

## About these CloudFormation templates
Each template in this repository has colocated documentation describing the usage and architecture of the template. The templates attempt to codify recommended deployment architecture of the Citrix NetScaler VPX, or to introduce the user to the Citrix NetScaler or to demonstrate a particular feature / edition / option. Users can re-use / modify or enhance the templates to suit their particular production and testing needs. Most templates require full EC2 permissions as well as permissions to create IAM roles.

## A note on AMI Ids
The CloudFormation templates contain AMI Ids that are specific to a particular release of the Citrix NetScaler VPX (e.g., release 12.0-56.20) and edition (e.g., Citrix NetScaler VPX Platinum Edition - 10 Mbps). To use a different version / edition of the Citrix NetScaler VPX with a CloudFormation template requires the user to edit the template and replace the AMI Ids.

## Versioning
The master branch of the repository generally has the latest version of the template. Older released versions are tagged appropriately

## Support
For production issues with the templates, please contact Citrix Support through your normal support channels. If you have fixes / suggestions for improvements or requests, please raise an issue in this repository. 

## Further reading
- VPX installation in AWS : https://docs.citrix.com/en-us/netscaler/12/deploying-vpx/install-vpx-on-aws.html
- Citrix NetScaler 12.0 Documention : https://docs.citrix.com/en-us/netscaler/12.html 
- Citrix NetScaler Overview : https://www.citrix.com/products/netscaler-adc/resources/netscaler-vpx.html

