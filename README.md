# Cisco DNA Center Assurance Notifications to AWS SNS (email/sms)  
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/robertcsapo/cisco-dnacaap-assurance-aws-sns)![Website](https://img.shields.io/website/https/cisco-dnacaap-aws-s3-us-east-1.s3.amazonaws.com/cisco-dnacaap-aws-lambda.zip?down_color=red&down_message=offline&label=AWS%20S3%20Code&up_color=blue&up_message=online)

Forward events from Cisco DNA Center Platform API to Amazon Simple Notification Service (SNS).  
The Subscribers on AWS SNS can be Email, SMS, HTTPS or other AWS Services.  
https://aws.amazon.com/sns/faqs/

In this solution we'll focus on Email and SMS (optional) subscription of AWS SNS.

## Screenshot

### Quick Deployment Demo
![aws-demo](./img/cisco-dnacaap-aws-cf-demo.gif)
### AWS Cloudformation Template
![aws-cf](./img/cisco-dnacaap-aws-cf.png)
### Emails
_(Cisco DNA Center Issues sent as Email)_  
![aws-email](./img/cisco-dnacaap-aws-emails.png)
### SMS
_(Cisco DNA Center Issues sent as SMS)_  
![aws-sms](./img/cisco-dnacaap-aws-sms.jpg)

## Requirements
  - AWS Account (Free Tier https://aws.amazon.com/free/)
    - IAM Privileges to create Lambda, API Gateway, SNS, S3 and IAM Role
  - Cisco DNA Center 1.2.10+
    - Platform Bundle Enabled
  - Network Connectivity from Cisco DNA Center to Internet (AWS)
    - https/443
  - Subscriber Account
    - Email
    - Mobile Number (optional)

## TLDR (too long; didn't read) - Deployment

### AWS CloudFormation  
Supported Regions: **us-east-1,	us-west-2, ap-northeast-1, ap-southeast-1, ap-southeast-2, eu-north-1, eu-central-1, eu-west-1**  
(If more is needed, please raise an issue)
AWS SNS SMS Support: https://docs.aws.amazon.com/sns/latest/dg/sms_supported-countries.html

This will be created in your AWS Region
- AWS Lambda
  - Process JSON Payload from Cisco DNA Center and send it to S3/SNS
- API Gateway
  - Receive JSON Payload from Cisco DNA Center and send it to Lambda
- S3 Bucket
  - Storing JSON Payload from Cisco DNA-C for Archive purpose
- SNS
  - Delivering the Notifications from Cisco DNA-C (AWS Lambda) to Subscribers

### Deploying with Cloudformation Template (AWS CLI)

- Download github repo or **cisco-dnacaap-aws-cf.yaml**
- Run AWS CLI on your terminal
  - ```aws cloudformation deploy --template-file ./cisco-dnacaap-aws-cf.yaml --capabilities CAPABILITY_IAM --stack-name cisco-dnacaap-aws-notifications --parameter-overrides EmailSubscriber=your@email.tld --region us-west-2```
- Now Navigate to your **AWS Lambda**
- Your function is called **cisco-dnacaap-aws-lambda-$AWS-REGION**
- Click on your **API Gateway**
  - **API endpoint** - Here is your **AWS Lambda API Gateway URL** (see section in Cisco DNA Center Config)

### Deploying with Cloudformation Template (GUI)

- Download github repo or **cisco-dnacaap-aws-cf.yaml**
- Navigate to Cloudformation on your AWS Console
- Click **Create Stack**
  - Choose **Upload a Template file**
  - Drag and drop **cisco-dnacaap-aws-cf.yaml**
- Click **Next**
  - Choose **Stack Name** (eg. cisco-dnacaap-aws-notifications)
  - Choose your email account (needs to be valid) TODO
- Click **Next** (nothing required to fill out on this page)
- Accept IAM Checkbox (in the bottom)
  - **"I acknowledge that AWS CloudFormation might create IAM resources."**
- Click **Create stack**

Wait until the Stack is created (if something is stuck, cancel and try again).  
You'll receive an Email to confirm your AWS SNS Membership on Email and Accept.  
If you want to add more members then go to AWS SNS and choose **cisco-dnacaap-aws-sns-$AWS-REGION**

![aws-stack](./img/cisco-dnacaap-aws-stack-complete.png)

### Navigate to your AWS Lambda Function
- Click on your Function called **cisco-dnacaap-aws-lambda-$AWS-REGION**
- Click on your **API Gateway**
  - **API endpoint** - Here is your **AWS Lambda API Gateway URL** (see section in Cisco DNA Center Config)

![aws-lambda](./img/cisco-dnacaap-aws-lambda.png)

### Configuring Cisco DNA Center (GUI)
If you can't see the "Platform" tab on the top, then go to **Systems Settings** -> **Software Updates** -> **Installed Apps** to install "DNAC Platform"

- Click on **Bundles**
- Enable **Network Events for REST API Endpoint**
- Configure **Network Events for REST API Endpoint**
  - Choose **Create a new instance**
    - Set **Instance Name** (this can be changed if needed)
    - **Description** could be that it's pointing to your AWS Lambda
    - **REST End Point** points to your **AWS Lambda API Gateway URL** (see section in AWS deployment)
    - **Username/Password** - choose anything (we don't validate this in AWS)
- **"Success"** should be displayed and click on **"View Now"**
  - This takes you to **Developer Toolkit** -> **Integration Flows**
- Click on **Schedule to publish Network Events - REST Endpoint connector**
  - Choose any **Repeats/Run At Interval**
  - Click on **Resume** or **Schedule**
- Click on **Manage** -> **Configurations** (in the top)
  - **Event Settings**
    - Verify that all items that you prefer is marked and click **Save** (bottom corner)

![cisco-dnac](./img/cisco-dnacaap.png)

## Technologies & Frameworks Used
* Python3
* AWS
  - Lambda (Python)
  - SNS
  - S3
* Cisco DNA Center Platform API

## Authors & Maintainers

- Robert Csapo <rcsapo@cisco.com>

## License

This project is licensed to you under the terms of the [Cisco Sample
Code License](./LICENSE).
