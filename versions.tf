terraform {
  required_version = ">= 1.4.5"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.63.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 4.63.0"
    }

  }
}
