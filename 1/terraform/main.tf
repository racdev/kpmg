module "three-tier" {
    source = "./three-tier"

    instance_ami_id = data.aws_ami.amazon_linux.id
}