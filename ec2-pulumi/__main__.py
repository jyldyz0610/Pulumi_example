import pulumi
import pulumi_aws as aws

# VPC erstellen
vpc = aws.ec2.Vpc("my-vpc",
    cidr_block="10.0.0.0/16")

# Public Subnet erstellen
public_subnet = aws.ec2.Subnet("public-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True)

# Security Group für die EC2-Instanz erstellen
security_group = aws.ec2.SecurityGroup("web-sg",
    vpc_id=vpc.id,
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 22,
            "to_port": 22,
            "cidr_blocks": ["0.0.0.0/0"],
        },
        {
            "protocol": "tcp",
            "from_port": 80,
            "to_port": 80,
            "cidr_blocks": ["0.0.0.0/0"],
        },
    ])

# EC2-Instanz erstellen
instance = aws.ec2.Instance("web-server",
    instance_type="t2.micro",
    vpc_security_group_ids=[security_group.id],
    subnet_id=public_subnet.id,
    ami="ami-0f673487d7e5f89ca",  # Hier die AMI-ID einfügen
    user_data="""#!/bin/bash
        sudo yum update -y
        sudo yum install docker -y
        sudo service docker start
        sudo docker run -d -p 80:9898 --name podinfo stefanprodan/podinfo
    """)

# Öffentliche IP-Adresse der Instanz anzeigen
pulumi.export("instance_public_ip", instance.public_ip)
