PROD_S3Bucket=citrixadc-automation
DEV_S3Bucket=citrixadc-automation-dev
S3Key=lambda-citrixadc-awscft.zip

help:
	@echo "Please use \`make <target>\` where <target> is one of"
	@echo "\tpylintbarbarika	Run lint on lambda files"
	@echo "\tcfnlint			Run lint on CFTs"
	@echo "\tziplambda			Zips lambda deployment package"
	@echo "\tsync-bucket		Syncs the CFTs and lambda to \`$(S3Bucket)\` S3 bucket"

pylintsrcfiles:
	pyflakes `find functions/sources/barbarika/ -name "*.py"`
	pyflakes `find functions/sources/ -name "lambda*.py"`

ziplambda: pylintsrcfiles
	cd functions/sources/ && zip -r $(S3Key) *
	mv functions/sources/$(S3Key) functions/packages/$(S3Key)

cfnlint:
	cfn-lint `find templates -name "*.yaml" | grep -v aws-marketplace-cfts | grep -v secure_cloud_computing_architecture | grep -v autoscale | grep -v vpc-infra` -i W2506

prod-sync-bucket: cfnlint
	@echo "Have you zipped the latest lambda package? - Press Ctrl-C to cancel"
	read confirm
	# TODO: take `yes` as input and parse the input for confirmation
	@echo "Are you sure pushing TEMPLATES and LAMBDA to PRODUCTION S3 bucket `citrixadc-automation`? - Press Ctrl-C to cancel"
	read confirm
	@echo "Are you really sure? - Press Ctrl-C to cancel"
	read second_confirm
	@echo "Are you really sure? - Press Ctrl-C to cancel"
	read third_confirm
	aws s3 sync templates s3://$(PROD_S3Bucket)/templates
	aws s3 cp functions/packages/$(S3Key) s3://$(PROD_S3Bucket)/$(S3Key)

dev-sync-bucket: cfnlint
	aws s3 sync templates s3://$(DEV_S3Bucket)/templates
	aws s3 cp functions/packages/$(S3Key) s3://$(DEV_S3Bucket)/$(S3Key)

sync-s3-lambda: ziplambda
	aws s3 cp functions/packages/$(S3Key) s3://$(PROD_S3Bucket)/$(S3Key)

sync-s3-templates: cfnlint
	aws s3 sync templates s3://$(PROD_S3Bucket)/templates
