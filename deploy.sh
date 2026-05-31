#!/bin/bash

# Get account ID automatically
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION="eu-west-1"
ECR_URL="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"

echo "Deploying JewelHub to EKS..."
echo "Account: $ACCOUNT_ID"
echo "Region: $REGION"

# Replace ACCOUNT_ID placeholder in all yaml files
find ./k8s -name "*.yaml" | xargs sed -i "s|ACCOUNT_ID|$ACCOUNT_ID|g"

echo "✅ Account ID replaced in all manifests"