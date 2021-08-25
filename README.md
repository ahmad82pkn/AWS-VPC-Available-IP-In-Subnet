# Available-IP-In-Subnet

This Code will help monitor number of free ip in each subnet across all accounts/region/vpc and alert if they decrease below specified threshold. 


PLEASE NOTE, YOU CAN DEPLOY THIS CODE DIRECTLY FROM AWS CONSOLE -> Search for Available-ip and change region

https://ap-southeast-2.console.aws.amazon.com/lambda/home?region=ap-southeast-2#/create/function



####INSTRUCTIONS##### Please follow steps to update the code as per your account numbers/arn info at specified locations.

1- In Lambda python code account list accountlist=['1234','5678'] update it with destination account numbers in which you want this lambda to find if any subnet in those accounts have less than 10 free IP. You can include source account number as well in which lambda will be deployed if you want to scan available ip in source account as well For example accountlist=['1234','5678',5555']

2- In Lambda python code regionlist add all regions where you want this scan to happen

3- Create an SNS topic in source/central account where lambda will be deployed and subscribe your email ID to receive notifications.

4- In Lambda Code, Replace SNS Topic ARN to source/central account SNS ARN in which Lambda will be deployed topicArn = 'arn:aws:sns:REGION:ACCOUNT NUMBER:NotifyMe'

5- Create an EC2 Role with name "available-ip-checker-dest" in each destination account in which this lambda will try to run describe_subnets API call.

6- Create a Lambda Role in Source/Central account Name this role "available-ip-checker"

7- For role "available-ip-checker-dest" in each destination account add below permission to run describe subnets API . Further that role in remote account should have trust relationship with source/central account in which Lambda will be deployed , so that Lambda can assume the role.

following permissions policy should be added to the role "available-ip-checker-dest" in each destination account

    { "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Action": [ "ec2:DescribeSubnets" ], "Resource": "*" } ] }

####Following Trust relation should be created in the role "available-ip-checker-dest" in each destination account

    { "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Principal": { "AWS": [ "arn:aws:iam::ACCOUNTNUMBER:role/available-ip-checker"-----> Replace account number/role ARN to central/source account where lambda will be deployed (role must be created in source account before updating trust relation) ] }, "Action": "sts:AssumeRole" } ] }

8- In Source/Central account role "available-ip-checker" add below permissions.

    { "Version": "2012-10-17",

    "Statement": [ { "Sid": "AllowPublishToMyTopic", "Effect": "Allow", "Action": "sns:Publish", "Resource": "arn:aws:sns:REGION:ACCOUNT NUMBER:NotifyMe"---> Update SNS topic ARN },

    { "Effect": "Allow", "Sid": "AllowToAssumeRoleInDestinationAccountsToMonitor", "Action": "sts:AssumeRole", "Resource": [ "arn:aws:iam::ACCOUNT NUMBER:role/available-ip-checker-dest", ---> Update Role ARN to each Destination account ROLE ARN Created in step 5 "arn:aws:iam::ACCOUNT NUMBER:role/available-ip-checker-dest" ---> Update Role ARN to each Destination account ROLE ARN Created in step 5

    ]
    },

    { "Effect": "Allow", "Sid": "LambdaBasicExecution", "Action": [ "logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents" ], "Resource": "*" } ] }

9- Go to your Lambda Function Config in AWS console and change execution rolename to "available-ip-checker"

10- Add cloudwatch Event Cronjob to schedule lambda execution as per your required frequency Per hour/Per day etc
