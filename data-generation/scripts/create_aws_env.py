import boto3
import json
import time
import logging
import os
import time


class AWSEnvCreator:
    config = {
        "AMIID": "ami-1d4e7a66",
        "AWSKeyName": "tyler_rsa",
        "nodeGranularity": "",
        "instancetype": "t2.micro",
        "AWSProfile": "tyler",
        "region": "us-east-1"
    }

    def __init__(self):
        """Initialize provider"""
        self.session = self.create_session(self.config)
        self.client = self.session.client(
            'ec2', region_name=self.config.get("region", "us-east-1"))
        self.ec2 = self.session.resource(
            'ec2', region_name=self.config.get("region", "us-east-1"))
        self.instances = []
        self.instance_states = {}
        self.vpc_id = 0
        self.sg_id = 0
        self.sn_ids = []
        self.logger = logging.getLogger(__name__)

    def xstr(self, string):
        return string if string else ""

    def create_vpc(self):
        """Create and configure VPC"""
        try:
            vpc = self.ec2.create_vpc(
                CidrBlock='10.0.0.0/16',
                AmazonProvidedIpv6CidrBlock=False,
            )
        except Exception as e:
            self.logger.error("{}\n".format(e))
        internet_gateway = self.ec2.create_internet_gateway()
        internet_gateway.attach_to_vpc(VpcId=vpc.vpc_id)  # Returns None
        self.internet_gateway = internet_gateway.id
        route_table = self.config_route_table(vpc, internet_gateway)
        self.route_table = route_table.id
        availability_zones = self.client.describe_availability_zones()
        for num, zone in enumerate(availability_zones['AvailabilityZones']):
            if zone['State'] == "available":
                subnet = vpc.create_subnet(
                    CidrBlock='10.0.{}.0/20'.format(16 * num),
                    AvailabilityZone=zone['ZoneName'])
                subnet.meta.client.modify_subnet_attribute(
                    SubnetId=subnet.id, MapPublicIpOnLaunch={"Value": False})
                route_table.associate_with_subnet(SubnetId=subnet.id)
                self.sn_ids.append(subnet.id)
            else:
                print(("{} unavailable".format(zone['ZoneName'])))
        # Security groups
        sg = self.security_group(vpc)
        self.vpc_id = vpc.id
        return vpc

    def spin_up_instance(self,  cmd_string, get_ip=False):
        """Starts an instance in the vpc in first available
        subnet. Starts up n instances at a time where n is
        node granularity from config"""
        escaped_command = self.xstr(cmd_string)
        command = "#!/bin/bash\nsed -i 's/us-east-2\.ec2\.//g' /etc/apt/sources.list\n" + \
            "\n{}".format(escaped_command)
        instance_type = self.config['instancetype']
        subnet = self.sn_ids[0]
        ami_id = self.config['AMIID']
        instance = self.ec2.create_instances(
            InstanceType=instance_type,
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            KeyName=self.config['AWSKeyName'],
            SubnetId=subnet,
            SecurityGroupIds=[self.sg_id],
            UserData=command)
        self.instances.append(instance[0].id)
        if get_ip:
            self.associate_ip(instance[0].id)
        self.logger.info(
            "Started up 1 instance. Instance type:{}".format(instance_type))
        return instance

    def associate_ip(self, instance, ttw=100):
        allocation = self.client.allocate_address(Domain='vpc')
        time.sleep(ttw)
        response = self.client.associate_address(AllocationId=allocation['AllocationId'],
                                                 InstanceId=instance)

    def shut_down_instance(self, instances=None):
        """Shuts down a list of instances if provided or the last
        instance started up if none provided"""
        if instances and len(self.instances > 0):
            term = self.client.terminate_instances(InstanceIds=instances)
            self.logger.info(
                "Shut down {} instances (ids:{}".format(
                    len(instances), str(instances)))
        elif len(self.instances) > 0:
            instance = self.instances.pop()
            term = self.client.terminate_instances(InstanceIds=[instance])
            self.logger.info("Shut down 1 instance (id:{})".format(instance))
        else:
            self.logger.warn("No Instances to shut down.\n")
            return -1
        return term

    def start_mongo_instance(self):
        """Set up a dynamodb instance in the VPC"""
        cmd_string = """sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo service mongod start"""
        return self.spin_up_instance(cmd_string)

    def security_group(self, vpc):
        """Create and configure security group.
        Allows all ICMP in, all tcp and udp in within vpc
        """
        sg = vpc.create_security_group(
            GroupName="private-subnet",
            Description="security group for remote executors")

        ip_ranges = [{
            'CidrIp': '10.0.0.0/16'
        }]

        # Allows all ICMP in, all tcp and udp in within vpc

        inPerms = [{
            'IpProtocol': 'TCP',
            'FromPort': 0,
            'ToPort': 65535,
            'IpRanges': ip_ranges,
        }, {
            'IpProtocol': 'TCP',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}],
        },
            {
            'IpProtocol': 'UDP',
            'FromPort': 0,
            'ToPort': 65535,
            'IpRanges': ip_ranges,
        }, {
            'IpProtocol': 'ICMP',
            'FromPort': -1,
            'ToPort': -1,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}],
        }]
        # Allows all TCP out, all tcp and udp out within vpc
        outPerms = [{
            'IpProtocol': 'TCP',
            'FromPort': 0,
            'ToPort': 65535,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}],
        }, {
            'IpProtocol': 'TCP',
            'FromPort': 0,
            'ToPort': 65535,
            'IpRanges': ip_ranges,
        }, {
            'IpProtocol': 'UDP',
            'FromPort': 0,
            'ToPort': 65535,
            'IpRanges': ip_ranges,
        }, ]

        sg.authorize_ingress(IpPermissions=inPerms)
        sg.authorize_egress(IpPermissions=outPerms)
        self.sg_id = sg.id
        return sg

    def config_route_table(self, vpc, internet_gateway):
        """Configure route table for vpc"""
        route_table = vpc.create_route_table()
        route_ig_ipv4 = route_table.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=internet_gateway.internet_gateway_id)
        return route_table

    def create_session(self, config={}):
        """Create boto3 session.
        If config contains ec2credentialsfile, it will use that file, if not,
        it will check for a ~/.aws/credentials file and use that.
        If not found, it will look for environment variables containing aws auth
        information. If none of those options work, it will let boto attempt to
        figure out who you are. if that fails, we cannot proceed"""
        if 'ec2credentialsfile' in config:
            config['ec2credentialsfile'] = os.path.expanduser(
                config['ec2credentialsfile'])
            config['ec2credentialsfile'] = os.path.expandvars(
                config['ec2credentialsfile'])

            cred_lines = open(config['ec2credentialsfile']).readlines()
            cred_details = cred_lines[1].split(',')
            credentials = {'AWS_Username': cred_lines[0],
                           'AWSAccessKeyId': cred_lines[1].split(' = ')[1],
                           'AWSSecretKey': cred_lines[2].split(' = ')[1]}
            config.update(credentials)
            session = boto3.session.Session(aws_access_key_id=credentials['AWSAccessKeyId'],
                                            aws_secret_access_key=credentials['AWSSecretKey'],
                                            profile_name=self.config.get("AWSProfile", None))
            return session
        elif os.path.isfile(os.path.expanduser('~/.aws/credentials')):
            cred_lines = open(os.path.expanduser(
                '~/.aws/credentials')).readlines()
            credentials = {'AWS_Username': cred_lines[0],
                           'AWSAccessKeyId': cred_lines[1].split(' = ')[1],
                           'AWSSecretKey': cred_lines[2].split(' = ')[1]}
            config.update(credentials)
            session = boto3.session.Session(
                profile_name=self.config.get("AWSProfile", None))
            return session
        elif (os.getenv("AWS_ACCESS_KEY_ID") is not None
              and os.getenv("AWS_SECRET_ACCESS_KEY") is not None):
            session = boto3.session.Session(aws_access_key_id=credentials['AWSAccessKeyId'],
                                            aws_secret_access_key=credentials['AWSSecretKey'],
                                            profile_name=self.config.get("AWSProfile", None))
            return session
        else:
            try:
                session = boto3.session.Session(
                    profile_name=self.config.get("AWSProfile", None))
                return session
            except Exception as e:
                self.logger.error("Credentials not found. Cannot Continue")
                exit(-1)


if __name__ == '__main__':
    c = AWSEnvCreator()
    c.create_vpc()
    c.spin_up_instance("echo hello", get_ip=True)
    c.start_mongo_instance()
