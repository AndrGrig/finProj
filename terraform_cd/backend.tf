terraform {
  backend "s3" {
    bucket         = "djans-backend-state"
    key            = "terraform/state/terraform.tfstate"
    region         = "us-east-1"  
    encrypt        = true
  }
}