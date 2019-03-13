#!/usr/bin/env python

import os
import pprint
import json

from parsl.execution_provider.execution_provider_base import ExecutionProvider
import boto3
from botocore.exceptions import ClientError


WORKER_USERDATA = '''#!/bin/bash
export JAVA=/usr/local/bin/jdk1.7.0_51/bin
export SWIFT=/usr/local/bin/swift-trunk/bin
export PATH=$JAVA:$SWIFT:$PATH
export WORKER_LOGGING_LEVEL=TRACE
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
sudo pip3 install ipyparallel
sudo pip3 install parsl
'''

EC2_LOCATIONS = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']

DEFAULT_LOCATION = 'us-east-2'

NEW_LINE = '''
'''

translate_table = {'PD': 'PENDING',
                   'R': 'RUNNING',
                   'CA': 'CANCELLED',
                   'CF': 'PENDING',  # (configuring),
                   'CG': 'RUNNING',  # (completing),
                   'CD': 'COMPLETED',
                   'F': 'FAILED',  # (failed),
                   'TO': 'TIMEOUT',  # (timeout),
                   'NF': 'FAILED',  # (node failure),
                   'RV': 'FAILED',  # (revoked) and
                   'SE': 'FAILED'}  # (special exit state


class EC2(ExecutionProvider):

    def __init__(self, config):

        self.config = self.read_configs(config)
        self.sitename = self.config['site']
        self.session = self.create_session(self.config)
        self.client = self.session.client('ec2')
        self.ec2 = self.session.resource('ec2')
        if self.config['logfile']:
            self.logger = open(self.config['logfile'], 'a')
        else:
            self.logger = open('awsprovider.log')
        self.instances = []
        self.vpc_id = 0
        self.sg_id = 0
        self.sn_ids = []

    def _read_conf(self, config_file):
        # cfile = open(config_file, 'r').read()
        # config = {}
        # for line in cfile.split('\ns'):
        #     # Checking if empty line or comment
        #     if line.startswith('#') or not line:
        #         continue
        #     temp = line.split('=')
        #     config[temp[0]] = temp[1].strip('\r')
        config = json.loads(config_file)
        return config

    def pretty_configs(self, configs):
        printer = pprint.PrettyPrinter(indent=4)
        printer.pprint(configs)

    def read_configs(self, config_file):
        config = self._read_conf(config_file)
        return config

    def create_session(self, config={}):
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
                                            aws_secret_access_key=credentials['AWSSecretKey'],)
            return session
        elif os.path.isfile(os.path.expanduser('~/.aws/credentials')):
            cred_lines = open(os.path.expanduser(
                '~/.aws/credentials')).readlines()
            credentials = {'AWS_Username': cred_lines[0],
                           'AWSAccessKeyId': cred_lines[1].split(' = ')[1],
                           'AWSSecretKey': cred_lines[2].split(' = ')[1]}
            config.update(credentials)
            session = boto3.session.Session()
            return session
        elif (os.getenv("AWS_ACCESS_KEY_ID") is not None
              and os.getenv("AWS_SECRET_ACCESS_KEY") is not None):
            session = boto3.session.Session(aws_access_key_id=credentials['AWSAccessKeyId'],
                                            aws_secret_access_key=credentials['AWSSecretKey'],)
            return session
        else:
            print("Cannot find credentials")
            exit(-1)

    def create_vpc(self):
        # Create the VPC
        vpc = self.ec2.create_vpc(
            CidrBlock='172.32.0.0/16',
            AmazonProvidedIpv6CidrBlock=False,
        )
        # Create an Internet Gateway and attach it to the VPC
        internet_gateway = self.ec2.create_internet_gateway()
        internet_gateway.attach_to_vpc(VpcId=vpc.vpc_id)  # Returns None
        # Route Table
        route_table = self.config_route_table(vpc, internet_gateway)

        availability_zones = self.client.describe_availability_zones()
        for num, zone in enumerate(availability_zones['AvailabilityZones']):
            if zone['State'] == "available":
                subnet = vpc.create_subnet(
                    CidrBlock='172.32.{}.0/20'.format(16 * num),
                    AvailabilityZone=zone['ZoneName'])
                # Associate it with subnet
                route_table.associate_with_subnet(SubnetId=subnet.id)
                self.sn_ids.append(subnet.id)
            else:
                print(("{} unavailable".format(zone['ZoneName'])))
        # Security groups
        sg = self.security_group(vpc)
        self.vpc_id = vpc.id
        return vpc

    def security_group(self, vpc):
        sg = vpc.create_security_group(
            GroupName="private-subnet",
            Description="security group for remote executors")

        ip_ranges = [{
            'CidrIp': '172.32.0.0/16'
        }]
        """
        Allows all ICMP in, all tcp and udp in within vpc
        """
        inPerms = [{
            'IpProtocol': 'TCP',
            'FromPort': 0,
            'ToPort': 65535,
            'IpRanges': ip_ranges,
        }, {
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
        """
        Allows all TCP out, all tcp and udp out within vpc
        """
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
        route_table = vpc.create_route_table()
        route_ig_ipv4 = route_table.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=internet_gateway.internet_gateway_id)
        return route_table

    # vpc = create_vpc(ec2, client)
    # print(vpc.id)

    def scale_out(self, size, instance_type, subnet=None):
        for i in range(size):
            spin_up_instance(instance_type, subnet)

    def scale_in(self, size):
        raise NotImplemented

    def spin_up_instance(self, client=self.client,
                         instance_type=self.config['instancetype'], subnet=self.sn_ids[0]):
        instance = ec2.create_instances(ImageId='<ami-image-id>', MinCount=self.config['minNodeCount'], MaxCount=self.config['maxNodeCount'])

    def get_instance_state(self, client=self.client,
                           instance_ids=self.instances):
        pass

    def submit(self, client=self.client):
        pass

    def status(self, client=self.client):
        pass

    def cancel(self, client=self.client, instances=self.instances):
        pass

    def show_summary(self):
        print((
            "EC2 Summary:\nVPC IDs: {}\nSubnet IDs: {}\nSecurity Group ID: {}\nInstance IDs: {}\n".format(
                self.vpc_id,
                self.sn_ids,
                self. sg_id,
                self.instances)))


if __name__ == '__main__':
    conf = '''{"site": "EC2",
            "instancetype": "t2.nano"
            "minNodeCount":1
            "maxNodeCount":5
            }'''
    provider = EC2(conf)
    vpc = provider.create_vpc()
    provider.show_summary()
