# batch-translation
Based on Google's Tutorial [Run a batch translation using the Cloud Translation connector](https://cloud.google.com/workflows/docs/tutorial-translation-connector)

## Setup
### Set project
```bash
gcloud projects list
gcloud config set project PROJECT_ID
```

### Enable required APIs

- Workflows API
  ```bash
  gcloud services enable workflows.googleapis.com
  ```


- Cloud Storage API
  ```bash
  gcloud services enable storage.googleapis.com
  ```

- Cloud Translation API
  ```bash
  gcloud services enable translate.googleapis.com
  ```

### Set default location
```bash
gcloud config set workflows/location REGION
```

### Create service account
```bash
GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
gcloud iam service-accounts create batch-translation-sa
```

### Add roles to service account
```bash
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member "serviceAccount:batch-translation-sa@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com" \
    --role "roles/logging.logWriter"

gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member "serviceAccount:batch-translation-sa@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com" \
    --role "roles/storage.admin"

gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member "serviceAccount:batch-translation-sa@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com" \
    --role "roles/cloudtranslate.user"

gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member "serviceAccount:batch-translation-sa@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com" \
    --role "roles/serviceusage.serviceUsageConsumer"
```
## Create an input Cloud Storage bucket and files 

### Create bucket
```bash
BUCKET_INPUT=${GOOGLE_CLOUD_PROJECT}-input-files
gsutil mb gs://${BUCKET_INPUT}
```

### Create input files
```bash
echo "Hello World\!" > file1.txt
gsutil cp file1.txt gs://${BUCKET_INPUT}
echo "Workflows connectors simplify calling services." > file2.txt
gsutil cp file2.txt gs://${BUCKET_INPUT}
```

## Deploy and execute the workflow

### Deploy workflow
```bash
gcloud workflows deploy batch-translation --source=workflow.yaml \
--service-account=batch-translation-sa@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com
```

### Execute workflow
```bash
gcloud workflows execute batch-translation
```

### View workflow status
```bash
gcloud workflows executions describe WORKFLOW_ID /
  --workflow batch-translation /
  --location us-central1
```

## Cleanup
### Delete workflow
```bash
gcloud workflows delete batch-translation
```
### Delete buckets created
```bash
gsutil rm -r gs://BUCKET_NAME
```

### Delete service account
```bash
gcloud iam service-accounts delete batch-translation-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com
```

