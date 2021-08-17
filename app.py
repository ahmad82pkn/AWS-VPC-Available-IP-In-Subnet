import boto3
import json

def lambda_handler(event, context):
        accountlist=['1234','5678']  # ---> Change Number 1 
        regionlist=['ap-southeast-2','us-east-1']  # --> Change Number 2
        notification = ""
        for account in accountlist:
            for region in regionlist:
                print("Account"+account+"Region:"+region)
                sts_connection = boto3.client('sts')
                acct_b = sts_connection.assume_role(
                    RoleArn="arn:aws:iam::"+str(account)+":role/available-ip-checker-dest",  # --> Change Number 3 only if your role name is different
                    RoleSessionName="cross_acct_lambda"
                )

                ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
                SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
                SESSION_TOKEN = acct_b['Credentials']['SessionToken']



                ec2 = boto3.client('ec2',region_name=region,aws_access_key_id=ACCESS_KEY,
                    aws_secret_access_key=SECRET_KEY,
                    aws_session_token=SESSION_TOKEN,)

                output_describe_subnets = ec2.describe_subnets( Filters=[{'Name': 'state', 'Values': ['available']}])
                print(output_describe_subnets)

                for eachsubnet in output_describe_subnets['Subnets']:
                    message = "Available IP's in Account Number: %s , Region: %s, VPC ID: %s , Subnet: %s is approaching ciritcal limit of %d" % (eachsubnet['OwnerId'],region,eachsubnet['VpcId'],eachsubnet['SubnetId'], eachsubnet['AvailableIpAddressCount'])
                    if eachsubnet['AvailableIpAddressCount']<10: # Feel free to change this number from 10 to any number on which you want to be alerted
                        print(message)
                        notification = notification+"\n"+message

        if notification:
            sns = boto3.client('sns')
            topicArn = 'arn:aws:sns:REGION:ACCOUNT NUMBER:NotifyMe'  # --> Change Number 4
            sns.publish(
                TopicArn = topicArn,
                Message = notification
            )


