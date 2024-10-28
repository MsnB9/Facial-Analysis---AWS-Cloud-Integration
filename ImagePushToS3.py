import sys 

import boto3 

import time 

import os 

import json  # Import the JSON library to properly format the message body 

  

print(f"Running on Python: {sys.executable}") 

print(f"boto3 version: {boto3.__version__}") 

  

# Initialize boto3 client for S3 and SQS specifying the 'us-east-1' region 

s3_client = boto3.client('s3', region_name='us-east-1') 

sqs_client = boto3.client('sqs', region_name='us-east-1') 

  

# Define S3 bucket name and SQS queue name, and get its URL 

bucket_name = 'mybucket1831444' 

queue_name = 'myQueue1831444' 

queue_url_response = sqs_client.get_queue_url(QueueName=queue_name) 

queue_url = queue_url_response['QueueUrl'] 

  

# List of image filenames to upload 

image_files = ['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.jpg'] 

  

# Path to the directory containing images in the EC2 instance 

image_directory_path = '/home/ec2-user/images/' 

  

# Loop through each image file for uploading and processing it 

for image_file in image_files: 

    # Complete file path for uploading images 

    file_path = os.path.join(image_directory_path, image_file) 

     

    # Check if the image file exists before attempting to upload 

    if not os.path.isfile(file_path): 

        print(f"Error: The file {file_path} does not exist.") 

        continue 

  

    # Upload the image from EC2 to the S3 bucket 

    try: 

        s3_client.upload_file(file_path, bucket_name, image_file) 

        print(f"Uploaded {image_file} to S3 bucket {bucket_name}") 

         

        # Send message to SQS queue 

        message = { 

            'ImageName': image_file, 

            'BucketName': bucket_name 

        } 

        # Use json.dumps to convert the dictionary to a JSON formatted string 

        response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message)) 

        print(f"Sent message to SQS queue {queue_name}: {response['MessageId']}") 

  

    except Exception as e: 

        print(f"An error occurred: {e}") 

  

    # Adding a waiting time of 10 seconds before the next image upload 

    time.sleep(10) 