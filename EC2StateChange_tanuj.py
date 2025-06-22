import boto3
from datetime import datetime

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')

    instance_id = extract_instance_id(event)
    if not instance_id:
        return {
            'statusCode': 400,
            'body': 'Instance ID not found in event payload.'
        }

    user_identity = get_user_identity(event)
    launch_date = datetime.utcnow().strftime('%Y-%m-%d')

    tagging_result = tag_instance(
        ec2_client,
        instance_id,
        launch_date,
        user_identity
    )

    return tagging_result


def extract_instance_id(event):
    try:
        return event['detail']['instance-id']
    except KeyError:
        print("Missing instance-id in the event structure.")
        return None


def get_user_identity(event):
    try:
        return event['detail']['userIdentity']['arn']
    except KeyError:
        print("User identity not present in event; defaulting to 'Unknown'.")
        return "Unknown"


def tag_instance(client, instance_id, date, user_arn):
    tags = [
        {'Key': 'LaunchDate', 'Value': date},
        {'Key': 'LaunchedBy', 'Value': user_arn}
    ]
    
    try:
        client.create_tags(Resources=[instance_id], Tags=tags)
        print(f"Tags successfully applied to {instance_id}: {tags}")
        return {
            'statusCode': 200,
            'body': f'Tags applied to instance {instance_id}'
        }
    except Exception as error:
        print(f"Error applying tags to instance {instance_id}: {error}")
        return {
            'statusCode': 500,
            'body': f'Failed to tag instance {instance_id}'
        }
