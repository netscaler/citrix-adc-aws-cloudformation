#!/bin/bash

PREFIX=n-cft-fn

regions=("us-east-1" "us-east-2" "us-west-1" "us-west-2" "eu-west-1" "eu-west-2" "eu-central-1" "ca-central-1" "ap-south-1" "ap-northeast-2" "ap-southeast-1" "ap-southeast-2" "ap-northeast-1" "sa-east-1")

for r in ${regions[@]}
do
    bucket=${PREFIX}-$r
    echo "Creating bucket $bucket"
    if [[ "$r" == "us-east-1" ]] 
    then
        aws s3api create-bucket --bucket $bucket --region $r 
    else
        aws s3api create-bucket --bucket $bucket --region $r --create-bucket-configuration LocationConstraint=$r
    fi
    aws --region=$r s3api put-bucket-acl --acl public-read --bucket $bucket
done
