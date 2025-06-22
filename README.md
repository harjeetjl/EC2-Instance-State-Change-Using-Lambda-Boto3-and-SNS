# EC2 Instance State Monitoring and Notification System

This solution enables automated monitoring of Amazon EC2 instance state changes (e.g., `running`, `stopped`) using AWS Lambda and Amazon EventBridge. Upon detecting a change, the system triggers an email notification via Amazon SNS.

---

## System Architecture Overview

The architecture integrates the following AWS services:

- **AWS Lambda**: Executes notification logic on state-change events.
- **Amazon EventBridge**: Captures EC2 instance state-change notifications.
- **Amazon SNS**: Delivers email notifications to subscribed users.
- **AWS IAM**: Secures resources with the appropriate permission boundaries.

---

## Deployment Guide

### Step 1: SNS Configuration

1. Navigate to **Amazon SNS**.
2. Create a new **Standard** topic (e.g., `EC2StateChangeTopic_harjeet`).
3. Create a **subscription** for the topic:
   - Protocol: Email  
   - Endpoint: Enter your email address  
4. Confirm the subscription through the email verification link sent by SNS.

---

### Step 2: IAM Role Provisioning

1. Open the **IAM Console**, go to **Roles**, and select **Create Role**.
2. Choose **Lambda** as the use case.
3. Attach the following policies:
   - `AmazonEC2ReadOnlyAccess`
   - `AmazonSNSFullAccess`
   - `AWSLambdaBasicExecutionRole`
4. Grant additional permission to allow tag creation:
   - Create a new policy with the JSON below and attach it:
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": [
             "ec2:CreateTags"
           ],
           "Resource": "*"
         }
       ]
     }
     ```
5. Save the role as `LambdaEC2SNSRole`.

---

### Step 3: Lambda Function Setup

1. In the AWS Lambda Console, create a new function:
   - Name: `EC2StateChangeNotifier`
   - Runtime: Python 3.12
   - Execution Role: `LambdaEC2SNSRole`
2. Deploy the notification logic. Use the code file:
   [EC2StateChange_harjeet.py](https://github.com/harjeetjl/EC2-Instance-State-Change-Using-Lambda-Boto3-and-SNS/blob/main/EC2StateChange_harjeet.py)
3. Configure the Lambda environment:
   - Key: `SNS_TOPIC_ARN`
   - Value: ARN of the SNS topic created in Step 1

---

### Step 4: EventBridge Rule Creation

1. Go to **Amazon EventBridge > Rules > Create Rule**.
2. Define the rule as follows:
   - Name: `EC2StateChangeRule_harjeet`
   - Event Source: AWS event pattern  
   - Event Pattern:
     ```json
     {
       "source": ["aws.ec2"],
       "detail-type": ["EC2 Instance State-change Notification"],
       "detail": {
         "state": ["running", "stopped"]
       }
     }
     ```
3. Add the Lambda function (`EC2StateChangeNotifier`) as the target.
4. Complete the rule creation and enable it.

---

## Execution Test

To verify the implementation:

1. Navigate to the **EC2 Dashboard**.
2. Start or stop any instance.
3. Wait for the state transition to complete.
4. Check your inbox for an email from Amazon SNS indicating the instance state change and its ID.

---

## Additional Information

- The Lambda function can be extended to include additional instance metadata such as launch time, availability zone, or custom tags.
- To track more EC2 states (e.g., `pending`, `terminated`), modify the EventBridge rule accordingly.

---

## Screenshots

Ensure the following items are set up and working:

- SNS Topic with email subscription
![image](https://github.com/user-attachments/assets/6f4e6c1d-1f80-4683-ae41-8bcb4d549f61)

- IAM Role (`LambdaEC2SNSRole`) with correct policy attachments
![image](https://github.com/user-attachments/assets/3d431155-3195-4db9-b97d-4b2eea64a0aa)

- Lambda Function 
![image](https://github.com/user-attachments/assets/cad95682-78c4-40b9-b639-2c3e85bb57dd)

- Email notifications successfully triggered by instance state changes  
![image](https://github.com/user-attachments/assets/3f6a9ea5-c71f-49bb-8a52-6ab74132d4f4)
![image](https://github.com/user-attachments/assets/023fe3d5-b03b-4f47-b414-ada06601a3fa)


---

## Conclusion

This setup provides a robust notification mechanism for tracking EC2 instance lifecycle transitions in near real-time. It leverages native AWS services for event detection, automation, and messaging without requiring external infrastructure.
