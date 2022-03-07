variable "region" {
  description = "Name of AWS Region"
  type        = string
  default     = "eu-west-1"
}

variable "vpc_name" {
  description = "Name of VPC"
  type        = string
  default     = "dev-three-tier"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "vpc_azs" {
  description = "Availability zones for VPC"
  type        = list(string)
  default     = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
}

variable "vpc_private_subnets" {
  description = "Private subnets for VPC"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "vpc_public_subnets" {
  description = "Public subnets for VPC"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

variable "vpc_database_subnets" {
  description = "Database subnets for VPC"
  type        = list(string)
  default     = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]
}

variable "vpc_enable_nat_gateway" {
  description = "Enable NAT gateway for VPC"
  type        = bool
  default     = true
}

variable "vpc_tags" {
  description = "Tags to apply to resources created by VPC module"
  type        = map(string)
  default = {
    Terraform   = "true"
    Environment = "dev"
  }
}

variable "sg_tags" {
  description = "Tags to apply to resources created by SG module"
  type        = map(string)
  default = {
    Terraform   = "true"
    Environment = "dev"
  }
}

variable "alb_tags" {
  description = "Tags to apply to resources created by ALB module"
  type        = map(string)
  default = {
    Terraform   = "true"
    Environment = "dev"
  }
}

variable "instance_tags" {
  description = "Tags to apply to resources created by ASG module"
  type        = map(string)
  default = {
    Terraform   = "true"
    Environment = "dev"
  }
}

variable "db_tags" {
  description = "Tags to apply to resources created by RDS module"
  type        = map(string)
  default = {
    Terraform   = "true"
    Environment = "dev"
  }
}

variable "instance_ami_id" {
  description = "EC2 instance AMI ID"
  type        = string
}

variable "instance_type" {
  description = "EC2 Instancetype"
  type        = string
  default     = "t3.medium"
}

variable "db_identifier" {
  description = "DB Identifier"
  type        = string
  default     = "dev"
}

variable "db_engine" {
  description = "RDS DB Engine"
  type        = string
  default     = "postgres"
}

variable "db_engine_version" {
  description = "RDS DB Engine Version"
  type        = string
  default     = "14.1"
}

variable "db_family" {
  description = "RDS DB Family"
  type        = string
  default     = "postgres14"
}

variable "db_engine_major_version" {
  description = "RDS DB Engine major version"
  type        = string
  default     = "14"
}

variable "db_instance_class" {
  description = "RDS DB Instance class"
  type        = string
  default     = "db.t4g.medium"
}

variable "db_allocated_storage" {
  description = "RDS DB Storage"
  type        = string
  default     = "20"
}

variable "db_max_allocated_storage" {
  description = "RDS DB Max storage"
  type        = number
  default     = 100
}

variable "db_name" {
  description = "RDS DB Name"
  type        = string
  default     = "dev"
}

variable "db_username" {
  description = "RDS DB Username"
  type        = string
  default     = "devuser"
}

variable "db_port" {
  description = "RDS DB Port"
  type        = number
  default     = 5432
}