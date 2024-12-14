resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "djans-vpc"
  }
}

resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.main.id
  cidr_block = var.subnet_cidr
  map_public_ip_on_launch = true
  tags = {
    Name = "djans-subnet"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "djans-gateway"
  }
}

resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "djans-route-table"
  }
}

resource "aws_route_table_association" "main" {
  subnet_id      = aws_subnet.main.id
  route_table_id = aws_route_table.main.id
}

resource "aws_security_group" "k8s_sg" {
  name        = "k8s-security-group"
  description = "Security group for K8s EC2 instance"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "k8s-security-group"
  }
}
resource "aws_instance" "k8s_node" {
  ami           = data.aws_ami.latest_amazon_linux.id
  instance_type = var.instance_type
  key_name      = var.key_name
  subnet_id     = aws_subnet.main.id
  vpc_security_group_ids = [aws_security_group.k8s_sg.id]

  tags = {
    Name = "K8s-EC2"
  }
}

resource "aws_ebs_volume" "mysql_volume" {
  availability_zone = "us-east-1c"
  size              = var.mysql_volume_size
  tags = {
    Name = "MySQL-Volume"
  }
}

resource "aws_volume_attachment" "mysql_attachment" {
  instance_id = aws_instance.k8s_node.id
  volume_id   = aws_ebs_volume.mysql_volume.id
  device_name = "/dev/xvdf"
}

resource "aws_s3_bucket" "photos_bucket" {
  bucket = var.bucket_name

  tags = {
    Name = "UI-Photos"
  }
}

data "aws_ami" "latest_amazon_linux" {
    most_recent = true
    filter {
        name   = "name"
        values = ["amzn2-ami-hvm-*-x86_64-gp2"]
    }

    owners      = ["amazon"]
}