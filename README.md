## Manage AWS Outposts Capacity Using Amazon CloudWatch and AWS Lambda

### Overview of solution
We use integrations between services in the AWS Outposts home region with the services deployed on the AWS Outpost to accomplish our goal. AWS Outposts provides available and utilized capacity metrics in Amazon CloudWatch. We do condition monitoring on these metrics based on thresholds that are defined by administrators to generate alarms that create an Amazon CloudWatch Event. For our use case, events trigger fan-out actions to multiple destinations to inform (via Amazon Simple Notification Service) and act (via an AWS Lambda function) on the condition. We act on the event by updating the permissions (policy) associated with administrators in AWS Identity and Access Management (IAM). If our threshold has been exceeded, we remove the capability to create more resources by updating an AWS IAM policy, to reserve that capacity in the event of a failure. Once our threshold normalizes, we return the privilege to the administrators. 


### Prerequisites
For this walkthrough, you should have the following prerequisites: 
An AWS account An AWS Outposts fully configured 
An AWS IAM Role that you used to assign privileges to your AWS Outposts administrators 
An AWS Virtual Private Cloud (VPC) subnet associated with your AWS Outposts 
An S3 bucket in the same AWS region as your AWS Outposts. Please refer to the AWS Region Table for more information. 


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

