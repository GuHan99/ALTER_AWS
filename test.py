import boto3

if __name__ == "__main__":
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    print(response)
