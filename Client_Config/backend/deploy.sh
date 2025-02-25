#!/bin/bash

# Exit on any error
set -e

# Configuration
PROJECT_ID=$(gcloud config get-value project)
IMAGE_NAME="client-config-backend"
REGION="us-central1"
SERVICE_NAME="client-config-backend"

# Replace PROJECT_ID in config.yaml
sed -i "s|gcr.io/PROJECT_ID/client-config-backend|gcr.io/${PROJECT_ID}/${IMAGE_NAME}|g" config.yaml

# Build the Docker image
echo "Building Docker image..."
docker build -t gcr.io/${PROJECT_ID}/${IMAGE_NAME} .

# Push the image to Google Container Registry
echo "Pushing image to Google Container Registry..."
docker push gcr.io/${PROJECT_ID}/${IMAGE_NAME}

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run services replace config.yaml --region=${REGION}

# Make the service public
echo "Making the service public..."
gcloud run services add-iam-policy-binding ${SERVICE_NAME} \
  --member="allUsers" \
  --role="roles/run.invoker" \
  --region=${REGION}

echo "Deployment completed successfully!"
echo "Service URL: $(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --format='value(status.url)')" 