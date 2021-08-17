# Available-IP-In-Subnet

This Code will help monitor number of free ip in each subnet across all accounts/region/vpc and alert if they decrease below specified threshold. 


####INSTRUCTIONS##### 

Please follow steps to update the code as per your account numbers/arn info at specified locations.


1- In account list accountlist=['1234','5678'] update it with destination account numbers in which you want this lambda to find if any subnet in those accounts have less than 10 free IP.
You can include source account number as well in which lambda will be deployed if you want to scan available ip in source account as well
For example accountlist=['1234','5678',5555']

2- In regionlist add all regions where you want this scan to happen

3- Creata a Role with name "available-ip-checker-dest" in each destination account in which this lambda will try to run describe_subnets API call. 
This role should have permission to run describe subnets API . Further that role in remote account should have trust relationship with source/central account in which Lambda will be deployed , 
so that Lambda can assume the role. 

following permissions policy should be added to the role "available-ip-checker-dest" in each destination account

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeSubnets"
            ],
            "Resource": "*"
        }
    ]
}

####Following Trust relation should be created in the role "available-ip-checker-dest" in each destination account

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "arn:aws:iam::ACCOUNTNUMBER:role/available-ip-checker"-----> Replace account number/role ARN to central/source account where lambda will be deployed (role must be created in source account before updating trust relation)
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}


4- Replace SNS Topic ARN to source/central account SNS ARN in which Lambda will be deployed
topicArn = 'arn:aws:sns:REGION:ACCOUNT NUMBER:NotifyMe'



5- Create an SNS topic in source/central account where lambda will be deployed and subscribe your email ID to receive notifications. 


6- Create a Lambda Role in Source/Central account with atleast below permissions. Name this role "available-ip-checker"

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowPublishToMyTopic",
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": "arn:aws:sns:REGION:ACCOUNT NUMBER:NotifyMe"---> Update SNS topic ARN
        },
        {

            "Effect": "Allow",
            "Sid": "AllowToAssumeRoleInDestinationAccountsToMonitor",
            "Action": "sts:AssumeRole",
            "Resource": [
                "arn:aws:iam::ACCOUNT NUMBER:role/available-ip-checker-dest",  ---> Update Role ARN to each Destination account ROLE ARN Created in step 5
                "arn:aws:iam::ACCOUNT NUMBER:role/available-ip-checker-dest"   ---> Update Role ARN to each Destination account ROLE ARN Created in step 5
                
                ]
        },
        {
            "Effect": "Allow",
            "Sid": "LambdaBasicExecution",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}





7- Go to your Lambda Function Config in AWS console and change execution rolename to "available-ip-checker"

8 Add cloudwatch Event Cronjob to schedule lambda execution as per your required frequency Per hour/Per day etc


