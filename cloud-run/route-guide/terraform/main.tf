terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.25.0"
    }
  }
}

provider "google" {
  project     = var.project
  credentials = file(var.credentials_file)
}

locals {
  service_name = "route-guide"
}