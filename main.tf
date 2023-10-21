provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "ec2_instance" {
  count = 2

  ami           = "ami-0fc5d935ebf8bc3bc"
  instance_type = "t2.micro"
  key_name      = "Kislay-Key"

  iam_instance_profile = "EC2-SSM-Role"

  tags = {
    Name = "machine-${count.index + 1}"
    CreatedWith = "Terraform"
  }
}

# Use a local-exec provisioner to run the Python script on your local machine
resource "null_resource" "run_local_script" {
  depends_on = [aws_instance.ec2_instance]

  provisioner "local-exec" {
    command = "python insert_instance_info.py"
  }
}

# Use a null_resource to run the shell script on the remote EC2 instances
resource "null_resource" "run_shell_script" {
  count = 2

  triggers = {
    instance_ids = aws_instance.ec2_instance.*.id[count.index]
  }

}