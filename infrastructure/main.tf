terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
  backend "s3" {
    bucket = "sns-challenge-terraform-state"
    key    = "terraform.tfstate"
    region = "eu-central-1"
  }
}

provider "aws" {
  region = var.region
}

resource "aws_vpc" "vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_security_group" "sg" {
  name        = "sg"
  description = "Security group for AWS lambda and AWS RDS connection"
  vpc_id      = aws_vpc.vpc.id
  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["127.0.0.1/32"]
    self = true
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}

resource "aws_subnet" "subnets" {
  for_each = var.networks
  vpc_id     = aws_vpc.vpc.id
  cidr_block = each.value.cidr_block
  availability_zone = "${var.region}${each.value.availability_zone}"
}

resource "aws_db_subnet_group" "dbsubnet" {
  name       = "main"
  subnet_ids = values(aws_subnet.subnets)[*].id

  tags = {
    Name = "My DB subnet group"
  }
}

resource "aws_db_instance" "MysqlForLambda" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "mysql"
  instance_class       = "db.t2.micro"
  name                 = "ChallengeDB"
  username             = var.db_username
  password             = var.db_password
  db_subnet_group_name = aws_db_subnet_group.dbsubnet.id
  vpc_security_group_ids = [aws_security_group.sg.id]
  final_snapshot_identifier = "someid"
  skip_final_snapshot  = true
}

data "archive_file" "lambda" {
  type = "zip"
  source_dir ="lambda"
  output_path = "app.zip"
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda-vpc-execution-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "test-attach" {
    role       = aws_iam_role.lambda_role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_lambda_function" "test_lambda" {
  filename         = "app.zip"
  function_name    = "AWSLambdaExecutionCounter"
  role             = "arn:aws:iam::${var.account_id}:role/lambda-vpc-execution-role"
  handler          = "app.handler"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256(data.archive_file.lambda.output_path)
  vpc_config {
      subnet_ids = values(aws_subnet.subnets)[*].id
      security_group_ids = [aws_security_group.sg.id]
  }
  environment {
    variables = {
      rds_endpoint = aws_db_instance.MysqlForLambda.endpoint
      db_username = var.db_username
      db_password = var.db_password
    }
  }
}

resource "aws_api_gateway_rest_api" "PassengersAPI" {
  name        = "PassengersAPI"
  description = "This is my API for the RDS."
}

resource "aws_api_gateway_resource" "PassengersResource" {
  rest_api_id = aws_api_gateway_rest_api.PassengersAPI.id
  parent_id   = aws_api_gateway_rest_api.PassengersAPI.root_resource_id
  path_part   = "passengers"
}

resource "aws_api_gateway_method" "PassengersMethod" {
  rest_api_id   = aws_api_gateway_rest_api.PassengersAPI.id
  resource_id   = aws_api_gateway_resource.PassengersResource.id
  http_method   = "ANY"
  authorization = "NONE"
}


resource "aws_api_gateway_integration" "integration" {
  rest_api_id             = aws_api_gateway_rest_api.PassengersAPI.id
  resource_id             = aws_api_gateway_resource.PassengersResource.id
  http_method             = aws_api_gateway_method.PassengersMethod.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:eu-central-1:lambda:path/2015-03-31/functions/${aws_lambda_function.test_lambda.arn}/invocations"
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.test_lambda.arn
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html

  source_arn = "${aws_api_gateway_rest_api.PassengersAPI.execution_arn}/*/*/*"
}

resource "aws_api_gateway_deployment" "dev" {
  depends_on = [aws_api_gateway_integration.integration]
  rest_api_id = aws_api_gateway_rest_api.PassengersAPI.id
  stage_name = "dev"
}
