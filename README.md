Manual operations:
1. Create S3 bucket for terraform state 'djans-backend-s3'
2. Update SSH key of the lab in repository secrets.
3. Update Bastion role to EMR_EC2_DefaultRole (existing role).
4. SSH to Bastion & create GH runner on Bastion.
5. Grant Admin permissions to EMR_EC2_DefaultRole.
6. Add the following JSON to EMR-Role:

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
7. Run terraform.
8. Goto public IP of K8S_EC2/30080
