terraform {
  # Here we configure the providers we need to run our configuration
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.18.0"
    }
  }

  # With this backend configuration we are telling Terraform that the
  # created state should be saved in some Google Cloud Bucket with some prefix
  backend "gcs" {}
}

# We define the "google" provider with the project and the general region + zone
provider "google" {
  credentials = file(var.credentials_file)
  project = var.project
  region  = var.region
  zone    = var.zone
}


# Enable the Compute Engine API
# Alternatively you can do this directly via the GCP GUI
resource "google_project_service" "compute" {
  project            = var.project
  service            = "compute.googleapis.com"
  disable_on_destroy = false
}

# Enable the Cloud Resource Manager API
# Alternatively you can do this directly via the GCP GUI
resource "google_project_service" "cloudresourcemanager" {
  project            = var.project
  service            = "cloudresourcemanager.googleapis.com"
  disable_on_destroy = false
}

# Here we define a very small compute instance
# The actual content of it isn't important its just here for show-case purposes
resource "google_compute_instance" "default" {
  name         = "terraform-test-instance"
  machine_type = "f1-micro"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network = "default"
  }

  # Before we can create a compute instance we have to enable the the Compute API
  depends_on = [
    google_project_service.cloudresourcemanager,
  google_project_service.compute]
}