
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 3.0"

  name = var.vpc_name
  cidr = var.vpc_cidr

  azs              = ["${var.region}a", "${var.region}b", "${var.region}c"]
  private_subnets  = var.vpc_private_subnets
  public_subnets   = var.vpc_public_subnets
  database_subnets = var.vpc_database_subnets

  create_database_subnet_group       = true
  create_database_subnet_route_table = true

  tags = var.vpc_tags
}

module "alb_http_sg" {
  source  = "terraform-aws-modules/security-group/aws//modules/http-80"
  version = "~> 4.0"

  name        = "alb-http"
  vpc_id      = module.vpc.vpc_id
  description = "ALB Security group"

  ingress_cidr_blocks = ["0.0.0.0/0"]

  tags = var.sg_tags
}

module "asg_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 4.0"

  name        = "asg"
  description = "ASG security group"
  vpc_id      = module.vpc.vpc_id

  computed_ingress_with_source_security_group_id = [
    {
      rule                     = "http-80-tcp"
      source_security_group_id = module.alb_http_sg.security_group_id
    }
  ]
  number_of_computed_ingress_with_source_security_group_id = 1

  egress_with_source_security_group_id  = [
    {
      from_port                = 5432
      to_port                  = 5432
      protocol                 = "tcp"
      description              = "PostgreSQL access from ASG"
      source_security_group_id = module.db_sg.security_group_id
    }
  ]

  tags = var.sg_tags
}

module "db_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 4.0"

  name        = "db"
  description = "PostgreSQL security group"
  vpc_id      = module.vpc.vpc_id

  # ingress
  ingress_with_source_security_group_id  = [
    {
      from_port                = 5432
      to_port                  = 5432
      protocol                 = "tcp"
      description              = "PostgreSQL access from ASG"
      source_security_group_id = module.asg_sg.security_group_id
    }
  ]

  tags = var.sg_tags
} 

module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "~> 6.0"

  name = "alb"

  vpc_id          = module.vpc.vpc_id
  subnets         = module.vpc.public_subnets
  security_groups = [module.alb_http_sg.security_group_id]

  http_tcp_listeners = [
    {
      port               = 80
      protocol           = "HTTP"
      target_group_index = 0
    }
  ]

  target_groups = [
    {
      name             = "asg"
      backend_protocol = "HTTP"
      backend_port     = 80
      target_type      = "instance"
    },
  ]

  tags = var.alb_tags
}

module "asg" {
  source  = "terraform-aws-modules/autoscaling/aws"
  version = "~> 5.0"

  # Autoscaling group
  name = "asg"

  vpc_zone_identifier = module.vpc.private_subnets
  min_size            = 0
  max_size            = 5
  desired_capacity    = 2

  image_id      = var.instance_ami_id
  instance_type = var.instance_type

  security_groups = [module.asg_sg.security_group_id]

  target_group_arns = module.alb.target_group_arns

  tags = var.instance_tags
}

module "db" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 4.0"

  identifier = var.db_identifier

  # All available versions: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html#PostgreSQL.Concepts
  engine               = var.db_engine
  engine_version       = var.db_engine_version
  family               = var.db_family # DB parameter group
  major_engine_version = var.db_engine_major_version         # DB option group
  instance_class       = var.db_instance_class

  allocated_storage     = var.db_allocated_storage
  max_allocated_storage = var.db_max_allocated_storage

  # NOTE: Do NOT use 'user' as the value for 'username' as it throws:
  # "Error creating DB Instance: InvalidParameterValue: MasterUsername
  # user cannot be used as it is a reserved word used by the engine"
  db_name  = var.db_name
  username = var.db_username
  port     = var.db_port

  multi_az               = true
  db_subnet_group_name   = module.vpc.database_subnet_group
  vpc_security_group_ids = [module.db_sg.security_group_id]

  maintenance_window              = "Mon:00:00-Mon:03:00"
  backup_window                   = "03:00-06:00"
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  create_cloudwatch_log_group     = true

  backup_retention_period = 0
  skip_final_snapshot     = true
  deletion_protection     = false

  tags = var.db_tags
 
}
