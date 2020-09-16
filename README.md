## Manage AWS Outposts Capacity Using Amazon CloudWatch and AWS Lambda

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
- Launch AWS CloudFormation stack
- Review created resources.


### Parameters
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


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

