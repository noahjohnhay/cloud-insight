#!/usr/bin/python


# DESCRIBE LISTENERS
def describe_listeners(client, load_balancer_arn=None, listener_arns=None):
    paginator = client.get_paginator('describe_listeners')
    listener_descriptions = []
    if listener_arns is not None:
        page_iterator = paginator.paginate(
            LoadBalancerArn=load_balancer_arn,
            ListenerArns=listener_arns

        )
    elif load_balancer_arn is not None:
        page_iterator = paginator.paginate(
            LoadBalancerArn=load_balancer_arn

        )
    else:
        page_iterator = paginator.paginate()
    for page in page_iterator:
        listener_descriptions.extend(page['Listeners'])
    return listener_descriptions


# DESCRIBE LOAD BALANCERS
def describe_load_balancers(client, load_balancer_arns=None, load_balancer_names=None):
    paginator = client.get_paginator('describe_load_balancers')
    load_balancer_descriptions = []
    if load_balancer_arns is not None:
        page_iterator = paginator.paginate(
            LoadBalancerArns=load_balancer_arns

        )
    elif load_balancer_names is not None:
        page_iterator = paginator.paginate(
            Names=load_balancer_names

        )
    else:
        page_iterator = paginator.paginate()
    for page in page_iterator:
        load_balancer_descriptions.extend(page['LoadBalancers'])
    return load_balancer_descriptions


# DESCRIBE RULES
def describe_rules(client, listener_arn):
    rule_descriptions = client.describe_rules(
        ListenerArn=listener_arn
    )
    return rule_descriptions


# DESCRIBE TARGET GROUP
def describe_target_groups(client, target_group_arns=None, target_group_names=None):
    paginator = client.get_paginator('describe_target_groups')
    target_group_descriptions = []
    if target_group_arns is not None:
        page_iterator = paginator.paginate(
            TargetGroupArns=target_group_arns

        )
    elif target_group_names is not None:
        page_iterator = paginator.paginate(
            Names=target_group_names

        )
    else:
        page_iterator = paginator.paginate()
    for page in page_iterator:
        target_group_descriptions.extend(page['TargetGroups'])
    return target_group_descriptions
