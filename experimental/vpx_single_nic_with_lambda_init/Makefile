all: package-lambda

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  package-lambda      to package the lambda function"
	@echo "  update-lambda       to update the lambda function in AWS. May be mismatched to the region deployed"


vpx-bootstrap.zip: handler.py 
	zip  -r9 vpx-bootstrap.zip handler.py 

package-lambda: vpx-bootstrap.zip
	@echo "create/update lambda deployment package (vpx-bootstrap.zip)"

update-lambda:  package-lambda
	@echo "update lambda deployment package"
	aws s3 cp ${PWD}/vpx-bootstrap.zip s3://vpx-lambda-functions
