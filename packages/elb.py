#!/usr/bin/python


# DESCRIBE ALL INSTANCES
def describe_all_load_balancers(client):
    paginator = client.get_paginator('describe_load_balancers')
    page_iterator = paginator.paginate()
    load_balancers = []
    for page in page_iterator:
        load_balancers.extend(page)
    return load_balancers


# DESCRIBE INSTANCES
def describe_load_balancers(client, names):
    paginator = client.get_paginator('describe_load_balancers')
    page_iterator = paginator.paginate(
        Names=names
    )
    load_balancers = []
    for page in page_iterator:
        load_balancers.extend(page)
    return load_balancers
