import logging 

import boto3 

from botocore.exceptions import ClientError 


def create_bucket(bucket_name, region=None): 

    try: 

        s3_client = boto3.client('s3', region_name=region if region else 'us-east-1') 

        # Auto to default region. 

        if region is None or region == 'us-east-1': 

#Creating s3 bucket and specifying region 

            s3_client.create_bucket(Bucket=bucket_name) 

        else: 

            location = {'LocationConstraint': region} 

            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location) 

    except ClientError as e: 

        logging.error(e) 

        return False 

    return True 


# Bucket name 

bucket_name = 'mybucket1831444'  # Specifying bucket name 


# Code to print the result, If bucket created or not 

if create_bucket(bucket_name): 

    print(f"Bucket {bucket_name} created successfully.") 

else: 

    print(f"Failed to create bucket {bucket_name}.") 