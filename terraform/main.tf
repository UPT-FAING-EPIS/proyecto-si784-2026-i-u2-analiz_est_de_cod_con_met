terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configura la región por defecto
provider "aws" {
  region = "us-east-1"
}

# Ejemplo de un bucket S3 que simula infraestructura
resource "aws_s3_bucket" "example" {
  bucket_prefix = "analizador-estatico-"

  tags = {
    Name        = "Analizador Estático"
    Environment = "Dev"
  }
}
