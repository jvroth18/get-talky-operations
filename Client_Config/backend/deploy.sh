#!/bin/bash

# Configuration
PROJECT_ID="talky-conversational-ai"
REGION="us-central1"
SERVICE_NAME="get-talky-backend-dev"
VPC_CONNECTOR="vpc-connector"
DB_USER_SECRET="get-talky-db-user"
DB_PASS_SECRET="get-talky-db-password"

# Build the container
echo "Building container..."
gcloud builds submit --tag gcr.io/${PROJECT_ID}/${SERVICE_NAME}

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
  --image gcr.io/${PROJECT_ID}/${SERVICE_NAME} \
  --platform managed \
  --region ${REGION} \
  --project ${PROJECT_ID} \
  --vpc-connector ${VPC_CONNECTOR} \
  --set-env-vars "INSTANCE_CONNECTION_NAME=${PROJECT_ID}:${REGION}:get-talky-db" \
  --set-secrets "DB_USER=${DB_USER_SECRET}:latest,DB_PASS=${DB_PASS_SECRET}:latest" \
  --ingress internal-and-cloud-load-balancing

echo "Deployment completed!"