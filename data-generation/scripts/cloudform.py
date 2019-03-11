import boto3


def create_and_configure_vpc():  
    ec2 = boto3.resource('ec2')

    # Create the VPC
    vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16', AmazonProvidedIpv6CidrBlock=True)

    # Create an Internet Gateway and attach it to the VPC
    internet_gateway = ec2.create_internet_gateway()
    internet_gateway.attach_to_vpc(VpcId=vpc.vpc_id)# Returns None

    # Route Table
    route_table = config_route_table(vpc, internet_gateway)

    subnet=create_subnet(vpc)

    # Associate it with subnet
    route_table.associate_with_subnet(SubnetId=subnet.id)

    # Security groups
    sg = security_group(vpc)

    return vpc

def security_group(vpc):
    vpc.create_security_group(GroupName="private-subnet", Description="Swift-Seq VPC")

    ip_ranges = [{
        'CidrIp': '0.0.0.0/0'
    }]

    ip_v6_ranges = [{

        'CidrIpv6': '::/0'
    }]

    perms = [{
        'IpProtocol': 'TCP',
        'FromPort': 80,
        'ToPort': 80,
        'IpRanges': ip_ranges,
        'Ipv6Ranges': ip_v6_ranges
    }, {
        'IpProtocol': 'TCP',
        'FromPort': 443,
        'ToPort': 443,
        'IpRanges': ip_ranges,
        'Ipv6Ranges': ip_v6_ranges
    }, {
        'IpProtocol': 'TCP',
        'FromPort': 22,
        'ToPort': 22,
        'IpRanges': ip_ranges, # Remember to change this!
        'Ipv6Ranges': ip_v6_ranges # Remember to change this!
    }]

    sg.authorize_ingress(IpPermissions=perms)

def create_subnet(vpc):
     # Create a subnet in our VPC
    # Assign IPv6 block for subnet using CIDR provided by Amazon, except different size (must use /64)
    ipv6_subnet_cidr = vpc.ipv6_cidr_block_association_set[0]['Ipv6CidrBlock']
    ipv6_subnet_cidr = ipv6_subnet_cidr[:-2] + '64'
    subnet = vpc.create_subnet(CidrBlock='10.0.0.0/24', Ipv6CidrBlock=ipv6_subnet_cidr)
    return subnet


def config_route_table(vpc, internet_gateway):
    route_table = vpc.create_route_table()
    route_ig_ipv4 = route_table.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internet_gateway.internet_gateway_id)
    route_ig_ipv6 = route_table.create_route(DestinationIpv6CidrBlock='::/0', GatewayId=internet_gateway.internet_gateway_id)
    return route_table

create_and_configure_vpc()
