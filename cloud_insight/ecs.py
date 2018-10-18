#!/usr/bin/python

import cloud_insight.aws as aws
import datetime


# DESCRIBE SERVICES
def describe_service(client, service_names, cluster_name):
    service_description = client.describe_services(
        cluster=cluster_name,
        services=[service_names]
    )
    return service_description


# DESCRIBE TASK
def describe_task(client, cluster_name, task_id):
    task_description = client.describe_tasks(
        cluster=cluster_name,
        tasks=[task_id]
    )
    return task_description


# DESCRIBE TASK DEFINITION
def describe_task_definition(client, task_definition_name):
    task_definition_description = client.describe_task_definition(
        taskDefinition=task_definition_name
    )
    return task_definition_description


# LIST CLUSTERS
def list_clusters(client):
    cluster_names = client.list_clusters()
    return cluster_names


# LIST ALL SERVICES IN A CLUSTER
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


# LIST ALL TASKS IN A CLUSTER
def list_tasks(client, cluster_name, service_name):
    paginator = client.get_paginator('list_tasks')
    page_iterator = paginator.paginate(
        cluster=cluster_name,
        serviceName=service_name
    )
    tasks = []
    for page in page_iterator:
        tasks.extend(page['taskArns'])
    return tasks


def get_uptime(client, cluster_name, service_name):

    uptime_list = []

    for task in list_tasks(client, cluster_name, service_name):

        start_time = describe_task(client, cluster_name, task)['tasks'][0]['startedAt']

        current_time = datetime.datetime.now(start_time.tzinfo)

        uptime = ' {}'.format(current_time.replace(microsecond=0) - start_time.replace(microsecond=0))

        uptime_list.append(uptime.replace(",", ""))

    return uptime_list


def service_dictionary(app, ecs_client, ecs_services):

    # ITERATE THROUGH ECS CLUSTERS
    for ecs_cluster in list_clusters(ecs_client)['clusterArns']:

        # PRINT CLUSTERS
        app.log.info('AWS: Found cluster {0}'.format(
            aws.parse_arn(ecs_cluster)['resource'])
        )

        # ITERATE THROUGH SERVICES IN EACH CLUSTER
        for ecs_service in list_services(app, ecs_client, aws.parse_arn(ecs_cluster)['resource']):

            # CREATE SERVICE DICTIONARY
            service = dict()

            # ADD SERVICE ITEM TO DICTIONARY
            service['service'] = aws.parse_arn(ecs_service)['resource']

            # ADD CLUSTER ITEM TO DICTIONARY
            service['cluster'] = aws.parse_arn(ecs_cluster)['resource']

            # PRINT SERVICES
            app.log.info('AWS: Found service {0}'.format(
                aws.parse_arn(ecs_service)['resource'])
            )

            # DESCRIBE SERVICES
            ecs_service_description = describe_service(
                ecs_client,
                aws.parse_arn(ecs_service)['resource'],
                aws.parse_arn(ecs_cluster)['resource']
            )

            # GET ALL TASKS UPTIME
            service['uptime'] = get_uptime(
                ecs_client,
                aws.parse_arn(ecs_cluster)['resource'],
                aws.parse_arn(ecs_service)['resource']
            )

            # PRINT SERVICE DESCRIPTION
            app.log.info('AWS: Service {0}, Count {1}, Active Task Definition {2}'.format(
                aws.parse_arn(ecs_service)['resource'],
                ecs_service_description['services'][0]['desiredCount'],
                ecs_service_description['services'][0]['taskDefinition'])
            )

            # ADD COUNT INFORMATION TO DICTIONARY
            service['desired_count'] = ecs_service_description['services'][0]['desiredCount']
            service['running_count'] = ecs_service_description['services'][0]['runningCount']

            # ADD LAUNCH TYPE INFORMATION TO DICTIONARY
            service['launch_type'] = ecs_service_description['services'][0]['launchType']

            # DESCRIBE TASK DEFINITIONS
            ecs_task_description = describe_task_definition(
                ecs_client,
                ecs_service_description['services'][0]['taskDefinition']
            )

            # ADD VERSION ITEM TO DICTIONARY
            service['version'] = \
                ecs_task_description['taskDefinition']['containerDefinitions'][0]['image'].split(':', 1)[-1]

            # APPEND DICTIONARY ITEMS TO ARRAY
            ecs_services.append(service)

    sorted_ecs_services = sorted(ecs_services, key=lambda k: k['service'])

    return sorted_ecs_services
