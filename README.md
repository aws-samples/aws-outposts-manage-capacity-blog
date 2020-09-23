## Manage AWS Outposts Capacity Using Amazon CloudWatch and AWS Lambda

![Image of Solution](https://github.com/aws-samples/aws-outposts-manage-capacity-blog/blob/master/SolutionDiagram.png)


### Overview of solution
We use integrations between services in the AWS Outposts home region with the services deployed on the AWS Outpost to accomplish our goal. AWS Outposts provides available and utilized capacity metrics in Amazon CloudWatch. We do condition monitoring on these metrics based on thresholds that are defined by administrators to generate alarms that create an Amazon CloudWatch Event. For our use case, events trigger fan-out actions to multiple destinations to inform (via Amazon Simple Notification Service) and act (via an AWS Lambda function) on the condition. We act on the event by updating the permissions (policy) associated with administrators in AWS Identity and Access Management (IAM). If our threshold has been exceeded, we remove the capability to create more resources by updating an AWS IAM policy, to reserve that capacity in the event of a failure. Once our threshold normalizes, we return the privilege to the administrators. 


### Prerequisites
For this walkthrough, you should have the following prerequisites: 
- An AWS account 
- An AWS Outposts fully configured 
- An AWS IAM Role that you used to assign privileges to your AWS Outposts administrators 
- An AWS Virtual Private Cloud (VPC) subnet associated with your AWS Outposts 
- An S3 bucket in the same AWS region as your AWS Outposts. Please refer to the AWS Region Table for more information. 

### The suggested sequence of steps is as follows:
- Create AWS IAM Policies
- Launch AWS CloudFormation stack (from repository)
- Review created resources.

### Create AWS IAM Policies

#### EC2 Sample
````
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Action": "ec2:RunInstances",
            "Resource": [
                "arn:aws:ec2:*:*:subnet/",
                "arn:aws:ec2:*:*:network-interface/*",
                "arn:aws:ec2:*:*:instance/*",
                "arn:aws:ec2:*:*:volume/*",
                "arn:aws:ec2:*::image/ami-*",
                "arn:aws:ec2:*:*:key-pair/*",
                "arn:aws:ec2:*:*:security-group/*"
            ]
        }
    ]
 }

````
#### EBS Sample
````
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Action": "ec2:CreateVolume",
            "Resource": [
                "arn:aws:ec2:*:*:subnet/",
                "arn:aws:ec2:*:*:network-interface/*",
                "arn:aws:ec2:*:*:instance/*",
                "arn:aws:ec2:*:*:volume/*",
                "arn:aws:ec2:*::image/ami-*",
                "arn:aws:ec2:*:*:key-pair/*",
                "arn:aws:ec2:*:*:security-group/*"
            ]
        }
    ]
 }

````

### Launch AWS CloudFormation stack
Create an AWS CloudFormation stack using the outposts-manage-capacity.yaml template that is included in your local clone of the repository. 


#### Parameters
Provide all necessary parameters using the descriptions below:
| Parameter | Description |
|-----------|-------------|
| AdminIAMPolicyArnEBS       |  ARN of EC2 IAM Policy associated with AWS Outposts administrators and that will be managed by solution           |
| AdminIAMPolicyArnEC2        | ARN of EBS IAM Policy associated with AWS Outposts administrators and that will be managed by solution            |
| Bucket       | An S3 bucket with the code from the Github repository            |
| Email       |  Email address or mailing list to send capacity notifications to.           |
| Subnet    |   Subnet associated to the AWS Outpost were capacity will be managed          |
| ComputeThreshold     |  Capacity threshold to use to generate alarms and restrict creating compute resources.           |
| StorageThreshold    |  Capacity threshold to use to generate alarms and restrict creating storage resources.           |
| OutpostId     |   The Id of your AWS Outpost          |

### Review Resources
Review the resources created by CloudFormation and validate your work. 

### Validate your work
To validate your work, assign the IAM policy created for Amazon EC2 and Amazon EBS to the IAM users or IAM roles assigned to your AWS Outposts administrators. Once assigned, use one of these IAM principals to create enough EC2 or EBS resources on your AWS Outpost to breach the thresholds you have established. This will depend on your AWS Outposts configuration and the capacity it is populated with. When capacity is exceeded, your administrators should receive an error similar to the below when attempting to create resources as well as an email notifying of the condition. You can also circumvent this by using the 'Set_Alarm_State' function through the SDK/CLI to modify the state of your target alarms.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

