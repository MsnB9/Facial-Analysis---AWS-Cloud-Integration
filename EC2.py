import boto3 

ec2_client = boto3.client('ec2') 

# Creating  Security Group to access ec2 through VM

sg_response = ec2_client.create_security_group( 

    GroupName='SecurityGroup2',  # Change to 'SecurityGroup2'

    Description='Allow SSH, HTTP, and HTTPS access' 

) 

security_group_id = sg_response['GroupId'] 

# Add Inbound Rules to the Security Group 

ec2_client.authorize_security_group_ingress( 

    GroupId=security_group_id, 

    IpPermissions=[ 

        # SSH access 

        { 

            'IpProtocol': 'tcp', 

            'FromPort': 22, 

            'ToPort': 22, 

            'IpRanges': [{'CidrIp': '0.0.0.0/0'}] 

        }, 

        # HTTP access 

        { 

            'IpProtocol': 'tcp', 

            'FromPort': 80, 

            'ToPort': 80, 

            'IpRanges': [{'CidrIp': '0.0.0.0/0'}] 

        }, 

        # HTTPS access 

        { 

            'IpProtocol': 'tcp', 

            'FromPort': 443, 

            'ToPort': 443, 

            'IpRanges': [{'CidrIp': '0.0.0.0/0'}] 

        } 

    ] 

) 

# Creation of EC2 instance and associate it with the Security Groups above
ec2_response = ec2_client.run_instances( 

    ImageId='ami-08e4e35cccc6189f4',  #AMI ID is correct and exist in AWS Learner lab

    InstanceType='t2.micro', 

    MaxCount=1, 

    MinCount=1, 

    KeyName='vockey1',  # Key pair for ec2 

    SecurityGroupIds=[security_group_id], 

    TagSpecifications=[ 

        { 

            'ResourceType': 'instance', 

            'Tags': [ 

                {'Key': 'Name', 'Value': 'instance1831444'}  # my  instance name with student ID 

            ] 

        } 

    ] 

) 
print(ec2_response) 