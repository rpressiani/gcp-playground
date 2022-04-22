# learn-terraform-gcp
Based on Terraform's tutorial [Build Infrastructure - Terraform GCP Example](https://learn.hashicorp.com/tutorials/terraform/google-cloud-platform-build).

## Setup
### Create service account
```bash
$ PROJECT_ID=$(gcloud config get-value project)
$ SERVICE_ACCOUNT_NAME=terraform-sa
$ gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME
$ gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member "serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --role "roles/editor"
```

### Download service account keys
```bash
$ gcloud iam service-accounts keys create service_account_keys.json \
    --iam-account=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com
```

## Format and validate the configuration
```bash
$ terraform fmt
$ terraform validate
```

## Create infrastructure
```bash
$ terraform apply
```

## Inspect state
```bash
$ terraform show
```

## Destroy
```bash
$ terraform destroy
```

