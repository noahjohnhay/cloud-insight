#!/usr/bin/python


# DESCRIBE ALL INSTANCES
def describe_all_instances(client):
    paginator = client.get_paginator('describe_instances')
    page_iterator = paginator.paginate()
    instances = []
    for page in page_iterator:
        instances.extend(page['Reservations'][0]['Instances'])
    return instances


# DESCRIBE INSTANCES
def describe_instances(client, instance_ids):
    paginator = client.get_paginator('describe_instances')
    page_iterator = paginator.paginate(
        InstanceIds=instance_ids
    )
    instances = []
    for page in page_iterator:
        instances.extend(page['Reservations'][0]['Instances'])
    return instances
