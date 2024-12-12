output "vpc_id" {
  value = aws_vpc.main.id
}

output "subnet_id" {
  value = aws_subnet.main.id
}

output "ec2_public_ip" {
  value = aws_instance.k8s_node.public_ip
  description = "Public IP address of the EC2 instance"
}

output "ec2_instance_id" {
  value = aws_instance.k8s_node.id
}

output "s3_bucket_name" {
  value = aws_s3_bucket.photos_bucket.id
}

output "mysql_volume_id" {
  value = aws_ebs_volume.mysql_volume.id
}