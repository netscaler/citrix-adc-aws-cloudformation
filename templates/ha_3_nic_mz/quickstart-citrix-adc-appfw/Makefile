all: help

#upload-quickstart

#test-master

#test-workload
# See the following links before creating the bucket
# https://github.com/aws-quickstart/quickstart-linux-bastion/issues/35#issuecomment-524320027
# https://docs.aws.amazon.com/general/latest/gr/signature-version-2.html
QSS3BucketName= "your-own-bucket-name"
QSS3KeyPrefix="quickstart-citrix-adc-appfw"


help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "\tziplambda 		packages lambda function"
	@echo "\tsync-bucket	creates ${QSS3BucketName} bucket and creates a copy of quickstart code in this S3 bucket"

lint:
	cfn-lint templates/*.yaml

ziplambda:
	cd functions/source/appfw/ && 7z -tzip a lambda-appfw.zip lambda-appfw.py
	mv functions/source/appfw/lambda-appfw.zip functions/packages/appfw

sync-bucket:
	@echo "syncing quickstart contents to s3 bucket"
	aws s3api put-object --bucket ${QSS3BucketName} --key ${QSS3KeyPrefix}/
	aws s3 sync . s3://${QSS3BucketName}/${QSS3KeyPrefix} --exclude Makefile --delete



