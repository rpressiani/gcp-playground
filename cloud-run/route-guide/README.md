# Route Guide
https://github.com/grpc-ecosystem/grpc-cloud-run-example/tree/master/python

https://github.com/GoogleCloudPlatform/serverless-expeditions/tree/main/terraform-serverless

https://github.com/grpc-ecosystem/grpc-cloud-run-example/tree/master/python

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud builds submit
```

PROJECT_ID=$(gcloud config get-value project)
REGION=us-central1
SERVICE_NAME=route-guide
gcloud run deploy --image gcr.io/${PROJECT_ID}/route-guide
gcloud run deploy ${SERVICE_NAME} \
    --image gcr.io/${PROJECT_ID}/${SERVICE_NAME} \
    --region=${REGION} \
    --allow-unauthenticated

ENDPOINT=$(\
  gcloud run services list \
  --project=${PROJECT_ID} \
  --region=${REGION} \
  --platform=managed \
  --format="value(status.address.url)" \
  --filter="metadata.name=${SERVICE_NAME}") 
ENDPOINT=${ENDPOINT#https://} && echo ${ENDPOINT}

```bash
grpcurl \
    -plaintext \
    -proto route_guide.proto \
    -d '{   "lo": {     "latitude": 400000000,     "longitude": -750000000   },   "hi": {     "latitude": 420000000,     "longitude": -730000000   } }' \
    localhost:50051 \
    RouteGuide.ListFeatures
```

```bash
grpcurl \
    -proto src/route_guide.proto \
    -d '{   "lo": {     "latitude": 400000000,     "longitude": -750000000   },   "hi": {     "latitude": 420000000,     "longitude": -730000000   } }' \
    ${ENDPOINT}:443 \
    RouteGuide.ListFeatures
```

gcloud run services delete ${SERVICE_NAME} --region=${REGION} --quiet

## Terraform

tf init

$ SERVICE_ACCOUNT_NAME=terraform-sa

SA needs run.services.setIamPolicy -> cloud run admin

gcloud iam service-accounts keys create service_account_keys.json \
    --iam-account=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com

