#!/usr/bin/python


# DESCRIBE ALL AUTO SCALING GROUPS
def describe_auto_scaling_groups(app, client):
    app.log.info('AWS: Listing Auto Scaling Groups')
    paginator = client.get_paginator('describe_auto_scaling_groups')
    page_iterator = paginator.paginate()
    auto_scaling_groups = []
    for page in page_iterator:
        auto_scaling_groups.extend(page['AutoScalingGroups'])
    return auto_scaling_groups


# GET INSTANCES FROM AUTO SCALING GROUPS
def auto_scaling_groups_instances(auto_scaling_groups):
    instances = []
    for auto_scaling_group in auto_scaling_groups:
        instances.extend(auto_scaling_group['Instances'])
    return instances


# GET INSTANCE IDS FROM AUTO SCALING GROUP
def auto_scaling_group_instance_ids(instances):
    instance_ids = []
    for instance in instances:
        instance_ids.append(instance["InstanceId"])
    return instance_ids


# GET INSTANCE IDS FROM AUTO SCALING GROUPS
def auto_scaling_groups_instance_ids(auto_scaling_groups):
    instances = auto_scaling_groups_instances(auto_scaling_groups)
    instance_ids = auto_scaling_group_instance_ids(instances)
    return instance_ids
