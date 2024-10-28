import boto3 

import json 

  

# Initialize AWS clients 

rekognition = boto3.client('rekognition') 

dynamodb = boto3.client('dynamodb') 

sns = boto3.client('sns') 

  

# DynamoDB table name 

table_name = 'myDynamoDBTable1831444' 

  

# SNS Topic ARN 

sns_topic_arn = 'arn:aws:sns:us-east-1:730335211444:SNSTopic1831444' 

  

def lambda_handler(event, context): 

    # Debug: print the entire event that Lambda received from SQS 

    print("Event received by Lambda:", json.dumps(event)) 

     

    for record in event['Records']: 

        # Debug: print the raw message body of each SQS message 

        print("Raw message body:", record['body']) 

         

        # Parse the message from SQS 

        try: 

            message_body = json.loads(record['body']) 

        except json.JSONDecodeError as e: 

            print("JSON decode error:", e) 

            # If there is an error in parsing JSON, skip this record 

            continue 

         

        bucket = message_body.get('BucketName') 

        file_name = message_body.get('ImageName') 

  

        if not bucket or not file_name: 

            print("Bucket or Filename not found in the message body.") 

            continue 

         

        # Call Rekognition to analyze the image 

        rekognition_response = rekognition.detect_faces( 

            Image={ 

                'S3Object': { 

                    'Bucket': bucket, 

                    'Name': file_name 

                } 

            }, 

            Attributes=['ALL'] 

        ) 

         

        # Debug: print the response from Rekognition 

        print("Rekognition response:", json.dumps(rekognition_response)) 

         

        # Check the detected emotions and send notifications if necessary 

        for faceDetail in rekognition_response['FaceDetails']: 

            for emotion in faceDetail['Emotions']: 

                if emotion['Type'] in ['ANGRY', 'FRUSTRATED'] and emotion['Confidence'] > 10: 

                    send_sns_notification(file_name, emotion['Type']) 

         

         #  Results to store in DynamoDB table after images are uploaded 

        dynamodb.put_item( 

            TableName=table_name, 

            Item={ 

                'ImageName': {'S': file_name}, 

                'RekognitionResponse': {'S': json.dumps(rekognition_response)} 

            } 

        ) 

     

    return { 

        'statusCode': 200, 

        'body': json.dumps('Function executed successfully!') 

    } 

  

def send_sns_notification(file_name, emotion): 

    # Construct the message 

    message = f"Detected {emotion} emotion with high confidence in file {file_name}." 

     

    # Publish the message to the SNS topic 

    sns.publish( 

        TopicArn=sns_topic_arn, 

        Message=message, 

        Subject='Emotion Detection Alert' 

    ) 