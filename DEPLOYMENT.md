# Deployment Guide - IBM Cloud Code Engine

This guide explains how to deploy the Product Inventory API to IBM Cloud Code Engine.

## Prerequisites

1. IBM Cloud account
2. IBM Cloud CLI installed
3. Docker installed (for local testing)
4. Code Engine plugin for IBM Cloud CLI

## Install IBM Cloud CLI and Code Engine Plugin

```bash
# Install IBM Cloud CLI (if not already installed)
# Visit: https://cloud.ibm.com/docs/cli?topic=cli-getting-started

# Install Code Engine plugin
ibmcloud plugin install code-engine
```

## Login to IBM Cloud

```bash
ibmcloud login
```

## Option 1: Deploy Using IBM Cloud Code Engine (Recommended)

### Step 1: Create a Code Engine Project

```bash
# Create a new project
ibmcloud ce project create --name product-inventory-api

# Select the project
ibmcloud ce project select --name product-inventory-api
```

### Step 2: Build and Deploy from Source

```bash
# Deploy directly from source code
ibmcloud ce application create \
  --name product-inventory-api \
  --build-source . \
  --strategy dockerfile \
  --port 8080 \
  --min-scale 1 \
  --max-scale 5 \
  --cpu 0.25 \
  --memory 0.5G
```

### Step 3: Get the Application URL

```bash
ibmcloud ce application get --name product-inventory-api
```

The output will show the URL where your API is accessible.

## Option 2: Deploy Using Container Registry

### Step 1: Build Docker Image Locally

```bash
# Build the Docker image
docker build -t product-inventory-api:latest .

# Test locally
docker run -p 8080:8080 product-inventory-api:latest
```

Visit http://localhost:8080/docs to test locally.

### Step 2: Push to IBM Cloud Container Registry

```bash
# Login to IBM Cloud Container Registry
ibmcloud cr login

# Create a namespace (if you don't have one)
ibmcloud cr namespace-add product-inventory

# Tag the image
docker tag product-inventory-api:latest \
  us.icr.io/product-inventory/product-inventory-api:latest

# Push the image
docker push us.icr.io/product-inventory/product-inventory-api:latest
```

### Step 3: Deploy to Code Engine

```bash
# Create a Code Engine project (if not exists)
ibmcloud ce project create --name product-inventory-api
ibmcloud ce project select --name product-inventory-api

# Deploy the application
ibmcloud ce application create \
  --name product-inventory-api \
  --image us.icr.io/product-inventory/product-inventory-api:latest \
  --registry-secret icr-secret \
  --port 8080 \
  --min-scale 1 \
  --max-scale 5 \
  --cpu 0.25 \
  --memory 0.5G
```

## Configuration Options

### Environment Variables

You can set environment variables during deployment:

```bash
ibmcloud ce application update \
  --name product-inventory-api \
  --env KEY=VALUE
```

### Scaling Configuration

```bash
# Update scaling settings
ibmcloud ce application update \
  --name product-inventory-api \
  --min-scale 0 \
  --max-scale 10 \
  --cpu 0.5 \
  --memory 1G
```

### Auto-scaling based on requests

```bash
ibmcloud ce application update \
  --name product-inventory-api \
  --concurrency 100 \
  --concurrency-target 80
```

## Monitoring and Logs

### View Application Status

```bash
ibmcloud ce application get --name product-inventory-api
```

### View Logs

```bash
# View recent logs
ibmcloud ce application logs --name product-inventory-api

# Follow logs in real-time
ibmcloud ce application logs --name product-inventory-api --follow
```

### View Application Events

```bash
ibmcloud ce application events --name product-inventory-api
```

## Testing the Deployed API

Once deployed, test your API:

```bash
# Get the application URL
APP_URL=$(ibmcloud ce application get --name product-inventory-api --output json | jq -r '.status.url')

# Test the root endpoint
curl $APP_URL

# Test get product by ID
curl $APP_URL/product/g265-tf85

# Test list products
curl $APP_URL/product

# Access API documentation
echo "API Docs: $APP_URL/docs"
```

## Updating the Application

### Update from Source

```bash
ibmcloud ce application update \
  --name product-inventory-api \
  --build-source .
```

### Update from New Image

```bash
# Build and push new image
docker build -t us.icr.io/product-inventory/product-inventory-api:v2 .
docker push us.icr.io/product-inventory/product-inventory-api:v2

# Update application
ibmcloud ce application update \
  --name product-inventory-api \
  --image us.icr.io/product-inventory/product-inventory-api:v2
```

## Cleanup

### Delete Application

```bash
ibmcloud ce application delete --name product-inventory-api
```

### Delete Project

```bash
ibmcloud ce project delete --name product-inventory-api
```

## Cost Optimization

- Set `--min-scale 0` to scale to zero when not in use
- Use appropriate CPU and memory settings
- Monitor usage with IBM Cloud monitoring tools

## Troubleshooting

### Application Not Starting

```bash
# Check logs
ibmcloud ce application logs --name product-inventory-api --tail 100

# Check events
ibmcloud ce application events --name product-inventory-api
```

### Port Issues

Ensure the Dockerfile exposes port 8080 and the application listens on the PORT environment variable.

### Image Pull Errors

Ensure you have created the registry secret:

```bash
ibmcloud ce registry create --name icr-secret \
  --server us.icr.io \
  --username iamapikey \
  --password <your-api-key>
```

## Additional Resources

- [IBM Cloud Code Engine Documentation](https://cloud.ibm.com/docs/codeengine)
- [Code Engine CLI Reference](https://cloud.ibm.com/docs/codeengine?topic=codeengine-cli)
- [Container Registry Documentation](https://cloud.ibm.com/docs/Registry)

## Support

For issues with the API, check the logs and events. For IBM Cloud issues, consult IBM Cloud support.