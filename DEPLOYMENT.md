# Cloud Run Deployment Instructions

## Option 1: Deploy via Google Cloud Console

1. **Go to Google Cloud Console** → **Cloud Run**
2. **Click on your existing service** (cyberchicmodels-api)
3. **Click "Edit & Deploy New Revision"**
4. **In the Container section:**
   - Select "Deploy one revision from an existing container image"
   - OR select "Continuously deploy new revisions from a source repository"

## Option 2: Deploy from Source Repository

1. **Push this code to GitHub repository**
2. **In Cloud Run Console:**
   - Click "Edit & Deploy New Revision"
   - Select "Continuously deploy new revisions from a source repository"
   - Connect to your GitHub repository
   - Select the branch with this code
   - Set build configuration:
     - Build Type: Dockerfile
     - Source Location: /Dockerfile

## Option 3: Build and Deploy with gcloud (if authenticated)

```bash
# Build the container image
gcloud builds submit --tag gcr.io/cyberchicmodels-ai/cyberchicmodels-api

# Deploy to Cloud Run
gcloud run deploy cyberchicmodels-api \
  --image gcr.io/cyberchicmodels-ai/cyberchicmodels-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --add-cloudsql-instances cyberchicmodels-ai:us-central1:cyberchicmodels-db \
  --set-env-vars DB_USER=cyberchic-admin,DB_PASS=_;,aGyNq1]}3=i4:,DB_NAME=cyberchicmodels-db,CLOUD_SQL_CONNECTION_NAME=cyberchicmodels-ai:us-central1:cyberchicmodels-db
```

## Environment Variables Required

- `DB_USER`: cyberchic-admin
- `DB_PASS`: _;,aGyNq1]}3=i4:
- `DB_NAME`: cyberchicmodels-db
- `CLOUD_SQL_CONNECTION_NAME`: cyberchicmodels-ai:us-central1:cyberchicmodels-db

## Cloud SQL Connection

Make sure the Cloud Run service has the Cloud SQL connection configured:
- Instance: cyberchicmodels-ai:us-central1:cyberchicmodels-db
