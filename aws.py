#!/usr/bin/python3
import boto3
import logging
import settings


def ecs_list_regions():
    session = boto3.Session()
    all_regions = session.get_available_regions(
        'ecs'
    )
    return all_regions


def ecs_auth_default(aws_region):
    ecs_client = boto3.client(
        'ecs',
        region_name=aws_region
    )
    return ecs_client


# AWS AUTH PROFILE FUNCTION || RETURNS A CLIENT WITH A PROFILE SESSION
def ecs_auth_profile(aws_profile_name, aws_region):
    # CREATE SESSION USING PROFILE NAME
    session = boto3.Session(
        profile_name=aws_profile_name
    )
    # USE SESSION TO INITIALIZE A CLIENT
    ecs_client = session.client(
        'ecs',
        region_name=aws_region
    )
    print('AWS: Trying to auth with profile {0} in region {1}'.format(aws_profile_name, aws_region))
    return ecs_client


# ECS LIST CLUSTERS FUNCTION || RETURNS ARRAY OF CLUSTER NAMES
def ecs_list_clusters(ecs_client):
    ecs_cluster_names = ecs_client.list_clusters()
    return ecs_cluster_names


# ECS LIST SERVICES FUNCTION || RETURNS ARRAY OF SERVICE NAMES
def ecs_list_services(ecs_client, ecs_cluster_name):
    ecs_service_names = ecs_client.list_services(
        cluster=ecs_cluster_name
    )
    print('AWS: Found {0} Services'.format(len(ecs_service_names['serviceArns'])))
    return ecs_service_names['serviceArns']


# ECS DESCRIBE SERVICES FUNCTION
def ecs_describe_service(ecs_client, ecs_service_names, ecs_cluster_name):
    ecs_service_description = ecs_client.describe_services(
        cluster=ecs_cluster_name,
        services=[ecs_service_names]
    )
    # print(ecs_service_description)
    return ecs_service_description


# ECS DESCRIBE TASK DEFINITION
def ecs_describe_task_definition(ecs_client, ecs_task_name):
    ecs_task_description = ecs_client.describe_task_definition(
        taskDefinition=ecs_task_name
    )
    print(ecs_task_description['taskDefinition']['containerDefinitions'][0]['image'])
    return ecs_task_description


# PARSE AWS ARN
def parse_arn(arn):
    elements = arn.split(':', 5)
    result = {
        'arn': elements[0],
        'partition': elements[1],
        'service': elements[2],
        'region': elements[3],
        'account': elements[4],
        'resource': elements[5],
        'resource_type': None
    }
    if '/' in result['resource']:
        result['resource_type'], result['resource'] = result['resource'].split('/',1)
    elif ':' in result['resource']:
        result['resource_type'], result['resource'] = result['resource'].split(':',1)
    return result
