1. Create S3 bucket for terraform state 'djans-backend-s3'
2. Update Bastion role to EMR_EC2_DefaultRole.
3. Grant Admin permissions to EMR_EC2_DefaultRole.
4. Create GH runner with terraform on Bastion.
5. Update SSH key of the lab in repository secrets.
6. Run terraform.
7. Manually update role of K8S EC2 to EMR-Role
8. Add the floowing JSON to EMR-Role:

{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
    		"Action": "s3:PutObject",
			"Resource": "arn:aws:s3:::djans-photos-bucket/*"
		},
		{
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::djans-photos-bucket"
        },
        {
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::djans-photos-bucket/*"
        }
	]
}
9. Goto public IP of K8S EC2/30080
