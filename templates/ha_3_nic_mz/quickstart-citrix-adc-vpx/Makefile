all: help

#upload-quickstart

#test-master

#test-workload
QSS3BucketName=sumanth-citrix
QSS3KeyPrefix=$(notdir $(shell pwd))
AWS_REGION=us-east-1


help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "\tsync-bucket	creates ${QSS3BucketName} bucket in ${AWS_REGION} aws region and creates a copy of quickstart code in this S3 bucket"

create-bucket:
	@echo "Creating bucket: ${QSS3BucketName}"
	aws s3 mb s3://${QSS3BucketName}

sync-bucket:
	@echo "syncing quickstart contents to s3 bucket"
	aws s3api put-object --bucket ${QSS3BucketName} --key ${QSS3KeyPrefix}/
	aws s3 sync . s3://${QSS3BucketName}/${QSS3KeyPrefix} --exclude Makefile



