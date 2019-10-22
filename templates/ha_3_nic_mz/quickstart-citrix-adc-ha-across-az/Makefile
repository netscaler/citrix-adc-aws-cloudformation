all: help

#upload-quickstart

#test-master

#test-workload
QSS3BucketName= "georgen-test"
QSS3KeyPrefix="quickstart-citrix-adc-ha-across-az"
AWS_REGION=us-east-1


help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "\tsync-bucket	creates ${QSS3BucketName} bucket in ${AWS_REGION} aws region and creates a copy of quickstart code in this S3 bucket"

lint:
	cfn-lint templates/*.yaml

create-bucket:
	@echo "Creating bucket: ${QSS3BucketName}"
	aws s3 mb s3://${QSS3BucketName}

ziplambda:
	cd functions/source/ha-across-az/ && 7z -tzip a lambda-ha-3-nic-mz.zip lambda-ha-3-nic-mz.py
	mv functions/source/ha-across-az/lambda-ha-3-nic-mz.zip functions/packages/ha-across-az

sync-bucket:
	@echo "syncing quickstart contents to s3 bucket"
	aws s3api put-object --bucket ${QSS3BucketName} --key ${QSS3KeyPrefix}/
	aws s3 sync . s3://${QSS3BucketName}/${QSS3KeyPrefix} --exclude Makefile --delete



