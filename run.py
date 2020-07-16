import boto3
from botocore.exceptions import ClientError
import time


def start_aws(instances, state):
    ec2_init = boto3.client('ec2')
    try:
        ec2_init.start_instances(InstanceIds=[instances[state]], DryRun=True)
    except ClientError as err:
        if 'DryRunOperation' not in str(err):
            raise
    try:
        responce = ec2_init.start_instances(InstanceIds=[instances[state]], DryRun=False)
        # print(responce)
        # print('实例 %s 已经启动', instances[state])
    except ClientError as err:
        print(err)


def stop_aws(instances, state):
    ec2_init = boto3.client('ec2')
    try:
        ec2_init.stop_instances(InstanceIds=[instances[state]], DryRun=True)
    except ClientError as err:
        if 'DryRunOperation' not in str(err):
            raise
    try:
        responce = ec2_init.stop_instances(InstanceIds=[instances[state]], DryRun=False)
        # print(responce)
        # print('实例 %s 已经关掉', instances[state])
    except ClientError as err:
        print(err)


def ip_active_aws(instances, state):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    ip_address = ''
    first_array = response["Reservations"]
    for x in first_array:
        for y in x["Instances"]:
            if y["InstanceId"] == instances[state]:
                ip_address = y["PublicIpAddress"]
    return ip_address


def alter_aws(instances, state):
    instances_len = len(instances)
    id_close = (state + instances_len) % instances_len
    id_open = (state - 1 + instances_len) % instances_len
    id_return = (state + 1 + instances_len) % instances_len

    ip_address = ip_active_aws(instances, id_return)
    print('实例{0:s}现在可以使用,地址为{1:s}'.format(instances[id_return], ip_address))

    stop_aws(instances, id_close)
    start_aws(instances, id_open)


def to_close(instances, state):
    instances_len = len(instances)
    close = (state + instances_len) % instances_len
    return close


def to_open(instances, state):
    instances_len = len(instances)
    open = (state -1 + instances_len) % instances_len
    return open


def to_return(instances, state):
    instances_len = len(instances)
    result = (state + 1 + instances_len) % instances_len
    return result


if __name__ == "__main__":
    # instance list length should >= 2
    instance_id = ['i-039f99aa3c76a71fe',
                   'i-061ae335f33b3a04c',
                   'i-072e6130425dcac7f']


    print('选择模式 A 轮换制，不太稳定，切换慢可以一直操作')
    print('        B 全开，全关，稳定，但要手动操作')
    mode_chosen = input()
    if mode_chosen == 'A':
        state_value = 0

        for i in range(len(instance_id) - 1):
            start_aws(instance_id, i)

        process_active = True
        seconds_init = time.time()
        seconds_counter = 0
        while process_active:
            print('选择操作 A 切换ip B 关掉所有实例并退出')
            username = input()
            if username == 'A':
                if time.time() - seconds_init <= 15:
                    print('15秒只能操作一次')
                else:
                    seconds_init = time.time()
                    alter_aws(instance_id, state_value)
                    state_value += 1
            elif username == 'B':
                # for loop here
                stop_aws(instance_id, to_close(instance_id, state_value))
                stop_aws(instance_id, to_return(instance_id, state_value))
                process_active = False
                exit
            else:
                print('错误')
            seconds_counter += 1
        print('感谢使用!')
    elif mode_chosen == 'B':
        for i in range(len(instance_id)):
            start_aws(instance_id, i)
        time.sleep(20)
        for i in range(len(instance_id)):
            print('实例{0:s}现在可以使用,地址为{1:s}'.format(instance_id[i], ip_active_aws(instance_id, i)))
        print('点A关掉所有的实例 再开要重启')
        close_chose = input()
        if close_chose == 'A':
            for i in range(len(instance_id)):
                stop_aws(instance_id, i)
    else:
        print('错误')






