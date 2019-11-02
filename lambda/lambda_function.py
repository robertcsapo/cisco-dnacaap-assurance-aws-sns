import boto3
import json
import os
from time import strftime


def lambda_handler(event, context):

    ''' S3 Settings '''
    s3 = boto3.client('s3')
    s3Filename = ("%s.txt" % strftime("%Y-%m-%d_%H-%M-%S"))

    ''' Deserialize payload to JSON '''
    try:
        data = json.loads(event['body'])
    except Exception:
        ''' Save non-JSON to S3 Bucket for Archive '''
        s3.put_object(Bucket=os.environ["S3BUCKET"], Key="Error-"+s3Filename, Body=(str(event)))
        return {
            'statusCode': 406,
            'body': json.dumps("Error - Can't load JSON from Body in the Payload")
        }

    ''' Validate the data from Cisco DNA Center '''
    try:
        data["domain"]
        data["details"]
        data["details"]["Type"]
        data["details"]["Assurance Issue Priority"]
        data["details"]["Device"]
        data["details"]["Assurance Issue Name"]

    except Exception:
        ''' Save Invalid JSON data to S3 Bucket for Archive '''
        s3.put_object(Bucket=os.environ["S3BUCKET"], Key="Error-"+s3Filename, Body=(str(event)))
        raise
        return {
            'statusCode': 406,
            'body': json.dumps("Error - Invalid data from Cisco DNA Center")
        }

    ''' Save JSON to S3 Bucket for Archive '''
    s3.put_object(Bucket=os.environ["S3BUCKET"], Key=s3Filename, Body=(bytes(json.dumps(event['body']).encode('UTF-8'))))

    ''' Amazon SNS Subject '''
    Subject = ("%s - %s - %s") % (data["domain"], data["details"]["Device"], data["details"]["Type"])

    ''' Amazon SNS Message - TODO Remove '''
    data["details"]["Assurance Issue Priority"]
    data["details"]["Device"]
    data["details"]["Assurance Issue Name"]
    data["ciscoDnaEventLink"]

    Message = "Severity - %s\nDevice - %s\nSummary - %s\nLink - %s" % (data["details"]["Assurance Issue Priority"], data["details"]["Device"], data["details"]["Assurance Issue Name"], data["ciscoDnaEventLink"])

    ''' Sending data to Amazon SNS Topic '''
    sns = boto3.client('sns')
    try:
        sns.publish(TopicArn=os.environ["SNSARN"], Subject=Subject[:100], Message=Message[:1600])
    except Exception as e:
        s3.put_object(Bucket=os.environ["S3BUCKET"], Key="snsError-"+s3Filename, Body=(str(e)))
        raise
        return {
            'statusCode': 500,
            'body': json.dumps("Error - Can't send to AWS SNS")
        }

    ''' Return to Cisco DNA Center with Success '''
    return {
        'statusCode': 200,
        'body': json.dumps("JSON Payload Received - Saved as %s and Sent to AWS SNS Topic %s" % (s3Filename, os.environ["SNSARN"]))
    }
