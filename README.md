# Photo Gallery Application

A cloud-native photo gallery application built with Flask, AWS S3, MySQL, and Kubernetes. The application allows users to upload and view photos, storing them in S3 and maintaining metadata in MySQL.

## Architecture

- *Frontend*: Flask web application
- *Backend Storage*: AWS S3 for photos, MySQL for metadata
- *Infrastructure*: AWS (managed via Terraform)
- *Container Orchestration*: Kubernetes (managed via Helm)
- *CI/CD*: GitHub Actions

## Prerequisites

- AWS Account
- Docker
- Kubernetes
- Helm
- Terraform
- Python 3.9+


# Manual operations to run the project:
1. Create S3 bucket for terraform state 'djans-backend-state' with Bucket Versioning.
2. Update SSH key of the lab in repository secrets.
3. Update Bastion role to EMR_EC2_DefaultRole (existing role).
4. Grant Admin permissions to EMR_EC2_DefaultRole (AdministratorAccess).
5. SSH to Bastion & create GH runner on Bastion.
6. Run terraform.
7. Goto http://public_IP_of_K8S_EC2:30080 (i.e. http://34.201.3.118:30080)


# Access to DB
1. mysql -u root -p
2. Enter the password: mysecurepassword
3. SHOW DATABASES;
4. USE photoDB;
5. SHOW TABLES;
6. SELECT * FROM photos;


# Set up GitHub Secrets:
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - DOCKER_HUB_USERNAME
   - DOCKER_HUB_PASSWORD
   - GIT_PAT
   - GIT_USERNAME
   - GIT_EMAIL
   - EC2_SSH_KEY

## Application Components

### Flask Application
- Photo upload functionality
- Gallery view with presigned URLs
- MySQL database integration
- S3 storage integration

