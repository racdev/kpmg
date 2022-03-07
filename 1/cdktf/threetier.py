import builtins

from constructs import Construct
from cdktf import Resource, Token

from imports.vpc import Vpc
from imports.autoscaling import Autoscaling
from imports.rds import Rds
from imports.alb import Alb
from imports.aws.vpc import SecurityGroup, SecurityGroupIngress, SecurityGroupEgress

class ThreeTier(Resource):
    def __init__(self, scope: Construct, ns: str, *, 
        ami_id: builtins.str,
        ):

        super().__init__(scope, ns)

        default_tags={'environment':'Dev','cdktf':'true'}

        vpc = Vpc(self, 'vpc', 
            name='threetier',
            cidr='10.0.0.0/16',
            azs=['eu-west-1a', 'eu-west-1b', 'eu-west-1c'],
            private_subnets=['10.0.1.0/24', '10.0.2.0/24', '10.0.3.0/24'],
            public_subnets=['10.0.101.0/24', '10.0.102.0/24', '10.0.103.0/24'],
            database_subnets=['10.0.201.0/24', '10.0.202.0/24', '10.0.203.0/24'],
            create_database_subnet_group=True,
            create_database_subnet_route_table=True,
            tags=default_tags
        )

        alb_sg = SecurityGroup(self, 'alb_sg',
            name='alb_sg',
            vpc_id=vpc.vpc_id_output,
            description='ALB Security Group',
            ingress=[
                SecurityGroupIngress(cidr_blocks=['0.0.0.0/0'],from_port=80,to_port=80,protocol='tcp',description='ingress from the internet')
            ],
            tags=default_tags
        )
        
        asg_sg = SecurityGroup(self, 'asg_sg',
            name='asg_sg',
            vpc_id=vpc.vpc_id_output,
            description='ASG Security Group',
            ingress=[
                SecurityGroupIngress(security_groups=Token().as_list(alb_sg.id),from_port=80,to_port=80,protocol='tcp',description='ingress from the ALB')
            ],
            tags=default_tags
        )
        
        db_sg = SecurityGroup(self, 'db_sg',
            name='db_sg',
            vpc_id=vpc.vpc_id_output,
            description='DB Security Group',
            ingress=[
                SecurityGroupIngress(security_groups=Token().as_list(asg_sg.id),from_port=5432,to_port=5432,protocol='tcp',description='ingress from the ASG instances')
            ],
            tags=default_tags
        )

        asg_sg.egress=[SecurityGroupEgress(security_groups=Token().as_list(db_sg.id),from_port=5432,to_port=5432,protocol='tcp',description='egress to the DB')]
        alb_sg.egress=[SecurityGroupEgress(security_groups=Token().as_list(asg_sg.id),from_port=80,to_port=80,protocol='tcp',description='egress to the ASG instances')]
        
        alb = Alb(self, 'alb',
            name='alb',
            vpc_id=Token().as_string(vpc.vpc_id_output),
            subnets=Token().as_list(vpc.public_subnets_output),
            security_groups=Token().as_list(alb_sg.id),
            http_tcp_listeners=[
                {
                    'port': 80,
                    'protocol': "HTTP",
                    'target_group_index': 0
                }
            ],
            target_groups=[
                {
                    'name': "asg",
                    'backend_protocol': "HTTP",
                    'backend_port': 80,
                    'target_type': "instance"
                }
            ],
            tags=default_tags
        )

        asg = Autoscaling(self, 'asg',
            name="asg",
            vpc_zone_identifier=Token().as_list(vpc.private_subnets_output),
            min_size=1,
            max_size=3,
            desired_capacity=2,
            image_id=ami_id,
            instance_type='t4.medium',
            security_groups=Token().as_list(asg_sg.id),
            target_group_arns=Token().as_list(alb.target_group_arns_output),
            tags=default_tags
        )

        rds = Rds(self, 'rds',
            identifier='db',
            engine='postgres',
            engine_version='14.1',
            family='postgres14',
            major_engine_version='14',
            instance_class='db.t4g.medium',
            allocated_storage='20',
            max_allocated_storage=100,
            db_name='dev',
            username='dbadmin',
            port='5432',
            multi_az=True,
            db_subnet_group_name=Token().as_string(vpc.database_subnet_group_name_output),
            vpc_security_group_ids=Token().as_list(db_sg.id),
            maintenance_window="Mon:00:00-Mon:03:00",
            backup_window="03:00-06:00",
            enabled_cloudwatch_logs_exports=["postgresql", "upgrade"],
            create_cloudwatch_log_group=True,
            backup_retention_period=0,
            skip_final_snapshot=True,
            deletion_protection=False,
            tags=default_tags
        )