#!/usr/bin/python


# LIST CLUSTERS
def list_clusters(client):
    cluster_names = client.list_clusters()
    return cluster_names


# LIST SERVICES
def list_services(app, client, cluster_name):
    paginator = client.get_paginator('list_services')
    page_iterator = paginator.paginate(
        cluster=cluster_name
    )
    service_names = []
    for page in page_iterator:
        service_names.extend(page['serviceArns'])
    app.log.info('Found {0} Services'.format(len(service_names)))
    return service_names


# DESCRIBE SERVICES
def describe_service(client, service_names, cluster_name):
    service_description = client.describe_services(
        cluster=cluster_name,
        services=[service_names]
    )
    return service_description


# DESCRIBE TASK DEFINITION
def describe_task_definition(client, task_name):
    task_description = client.describe_task_definition(
        taskDefinition=task_name
    )
    return task_description
