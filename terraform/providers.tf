terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.0.0" # This pulls the official Databricks provider
    }
  }
}

provider "databricks" {
  # We leave this completely empty! 
  # Terraform is smart enough to automatically look for the 
  # DATABRICKS_HOST and DATABRICKS_TOKEN environment variables 
  # that we locked into GitHub Actions earlier. No hardcoding here!
}