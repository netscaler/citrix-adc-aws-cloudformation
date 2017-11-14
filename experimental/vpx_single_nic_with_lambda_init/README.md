# Single NIC Citrix NetScaler VPX CloudFormation Template
The template creates a single NIC Citrix NetScaler VPX in the supplied subnet and VPC. There is a helper lambda function that bootstraps the VPX to get it ready to receive traffic. After the stack is created by CloudFormation, you should have:
* a NetScaler VPX with a single NIC in the supplied subnet
* The NIC has 3 private IPs: the primary IP is the management (NSIP) IP, the other two are the Subnet IP (SNIP) and Virtual IP (VIP)
* VPX is configured with the required feature set.
* The VPX has two public IPs: an ephemeral one that is mapped to the primary private IP and an Elastic IP that is mapped to the VIP. Client traffic is directed to the Elastic IP which is then load balanced by the VPX. You can use SSH or a browser to connect to the ephemeral public IP in order to configure it

## Parameters
The Cloudformation template takes the following parameters:
* Subnet. This is the subnet id where you want the VPX to run in
* VpcID. This is the VPC id of the VPC where you want the VPX to run in
* AMI. This is the AMI id of the VPX
* KeyName. A keyname of a keypair that you own and have registered with AWS

## Outputs
The Cloudformation template outputs the following:
* InstanceIdNS: Instance Id of newly created VPX instance
* PublicIpVIP: Elastic IP address of the VPX instance associated with the VIP
* NSIp: Private IP (NS IP) used for management
* PublicNSIp: Public IP (NS IP) used for management
* PrivateVIP: Private IP address of the VPX instance associated with the VIP
* SNIP: Private IP address of the VPX instance associated with the SNIP

You can browse to http://PublicNSIp/ (or ssh to PublicNSIp) to continue configuring the appliance.


## Lambda function
The lambda function has been uploaded to a public S3 bucket called s3://vpx-bootstrap-functions. You can upload the function to a different S3 bucket and modify the CloudFormation template to point to the new bucket. The Makefile contain handy utilities to make the upload to S3 easy.

## Other utilities
`create_stack.sh` shows you how to obtain the AMI id from the command line and also to launch the stack from the command line.
