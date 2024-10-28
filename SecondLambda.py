import boto3 

import json 

  

# Initialize the SNS client 

sns = boto3.client('sns') 

  

# The ARN of the SNS topic created for second lambda 

sns_topic_arn = 'arn:aws:sns:us-east-1:730335211444:SNSTopic1831444' 

  

def lambda_handler(event, context): 

    for record in event['Records']: 

        # Assuming the Rekognition and emotions results are in the message body 

        # as a JSON string, let's parse it 

        message_body = json.loads(record['body']) 

        rekognition_results = message_body['RekognitionResults'] 

         

        # Check the emotion analysis results 

        for face_detail in rekognition_results['FaceDetails']: 

            for emotion in face_detail['Emotions']: 

                if emotion['Type'] in ['ANGRY', 'FRUSTRATED'] and emotion['Confidence'] > 10: 

                    send_notification(emotion, message_body['ImageName']) 

  

def send_notification(emotion, image_name): 

    # Constructing the message 

    message = f"High confidence {emotion['Type']} emotion detected in image {image_name}." 

     

    # Publish the message to the SNS topic 

    sns.publish( 

        TopicArn=sns_topic_arn, 

        Message=message, 

        Subject='Emotion Detection Alert' 

    ) 

 