# gcs-backend

Based on Pascal Zwikirsch's [Getting started with Terraform on GCP from scratch](https://levelup.gitconnected.com/getting-started-with-terraform-on-gcp-from-scratch-f607df91c47).

## Backend

In this example, the Terraform backend, that is where the state snapshots are stored, is set to be a bucket in Google Cloud Storage. By default, the Terraform uses the `local` backend which stores the state snapshots in a plain file saved in the current working directory. By setting the backend to be in cloud, multiple users are allowed to access it which makes it easier when the infrastructure is managed by a team and not a single individual.

## Instructions

- Create GCP project and Terraform service account with `editor` role
- Create GCS bucket that will be used as backend
  
  ```bash
  $ PROJECT_ID=$(gcloud config get-value project)
  $ gsutil mb gs://$PROJECT_ID-terraform-state
  ```

-  Create `terraform.tfvars` where the project name and the credentials filepath will be set
-  Create `config.tfbackend` where the backend config parameters will be set

  ```terraform
  prefix      = "terraform/state"
  bucket      = "bucket_name"
  credentials = "../service_account_keys.json"
  ```

-  Initialize terraform and apply
