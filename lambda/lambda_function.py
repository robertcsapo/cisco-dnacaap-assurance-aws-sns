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

    try:
        data["title"]
        data["actualServiceId"]
        data["enrichmentInfo"]["issueDetails"]["issue"]
        data["enrichmentInfo"]["connectedDevice"]
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
    Subject = ("%s - %s") % (data["title"], data["actualServiceId"])

    ''' Amazon SNS Message '''
    for item in data["enrichmentInfo"]["issueDetails"]["issue"]:
        issueSeverity = item["issueSeverity"]
        issueSummary = item["issueSummary"]

    link = "N/A"
    for item in data["enrichmentInfo"]["connectedDevice"]:
        if item is not None:
            try:
                link = item["deviceDetails"]["cisco360view"]
                break
            except Exception:
                link = "N/A"
    ''' TODO - when Cisco DNA-C sends proper direct links in Assurance '''
    if link is not "N/A":
        link = link.split("/")
        link = ("https://%s/" % (link[2]))

    Message = "Severity - %s\nTitle - %s\nSummary - %s\nLink - %s" % (issueSeverity, data["title"], issueSummary, link)

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
        'body': json.dumps("JSON Payload Received and Saved as %s and Sent to AWS SNS Topic %s" % (s3Filename, os.environ["SNSARN"]))
    }
