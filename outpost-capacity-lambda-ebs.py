# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import boto3
import os


def lambda_handler(event, context):
    # Get Details of event
    alarm_name = event["detail"]['alarmName']
    
    new_state = event['detail']['state']['value']
    InstanceType = alarm_name.split('-')[-1]
    print ('{} is in state {}'.format(alarm_name,new_state))
    print ('TriggerChild: ', InstanceType)

    # Create IAM client
    iam = boto3.resource('iam')
    client = boto3.client('iam')
    
    #Get Environment Variables
    policy_arn = os.environ["policy_arn"]
    policy_name = os.environ["policy_name"]
    subnet_id = os.environ["subnet_id"]
    ebs_alarm_breached= os.environ['ebs_alarm_breached']
    
    # Getting the old/original version of the policy
    policy = iam.Policy(policy_arn)
    original_version = policy.default_version
    original_doc = boto3.client('iam').get_policy_version(PolicyArn = policy_arn,VersionId = str(original_version.version_id))
    print ('Policy: ',original_doc)
    try:
        list_of_blocked = original_doc['PolicyVersion']['Document']['Statement'][1]['Condition']['ForAnyValue:StringEquals']['ec2:InstanceType']
        print (list_of_blocked)
    except:
        list_of_blocked = []
        print ('No conditions found')
    # Get new state of alarm
    if new_state == 'OK':
        effect = 'Allow'
    elif new_state == 'ALARM':
    	effect = 'Deny'
        
    
    
    #Declare policy to allow EC2 actions when alarm is normal
    allow_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": effect,
                "Action": "ec2:CreateVolume",
                "Resource": [
                    "arn:aws:ec2:*:*:subnet/" + subnet_id,
                    "arn:aws:ec2:*:*:network-interface/*",
                    "arn:aws:ec2:*:*:instance/*",
                    "arn:aws:ec2:*:*:volume/*",
                    "arn:aws:ec2:*::image/ami-*",
                    "arn:aws:ec2:*:*:key-pair/*",
                    "arn:aws:ec2:*:*:security-group/*"
                ]
            },
	        {
	            "Sid": "Instances",
	            "Effect": effect,
	            "Action": "ec2:RunInstances",
	            "Resource": [
	                "arn:aws:ec2:*::image/ami-*",
	                "arn:aws:ec2:*:*:subnet/"+subnet_id,
	                "arn:aws:ec2:*:*:key-pair/*",
	                "arn:aws:ec2:*:*:instance/*",
	                "arn:aws:ec2:*:*:volume/*",
	                "arn:aws:ec2:*:*:security-group/*",
	                "arn:aws:ec2:*:*:network-interface/*"
	            ]
	        }
        ]
    }

    
    #create new policy version
    response = client.create_policy_version(
        PolicyArn= policy_arn,
        PolicyDocument= json.dumps(allow_policy),
        SetAsDefault= True
    )
    
    print(response)
    print(original_version.version_id)
    
    #delete old policy version
    response = client.delete_policy_version(
        PolicyArn= policy_arn,
        VersionId= str(original_version.version_id)
    ) 
    
    print(response)
    
    return {
        'statusCode': 200
    }
