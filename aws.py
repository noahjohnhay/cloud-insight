#!/usr/bin/python3
import boto3
import logging
import settings


def ecs_list_regions(aws_auth_type, *aws_profile_name):
    if aws_auth_type == 'profile':
        session = boto3.Session(
            profile_name=aws_profile_name
        )
        client = session.client('ecs')
        all_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    else:
        client = boto3.client('ecs')
        all_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    return all_regions


def ecs_auth_default(aws_region):
    ecs_client = boto3.client('ecs', region_name=aws_region)
    return ecs_client


# AWS AUTH PROFILE FUNCTION || RETURNS A CLIENT WITH A PROFILE SESSION
def ecs_auth_profile(aws_profile_name, aws_region):
    # CREATE SESSION USING PROFILE NAME
    session = boto3.Session(
        profile_name=aws_profile_name
    )
    # USE SESSION TO INITIALIZE A CLIENT
    ecs_client = session.client('ecs', region_name=aws_region)
    return ecs_client


# ECS LIST CLUSTERS FUNCTION || RETURNS ARRAY OF CLUSTER NAMES
def ecs_list_clusters(ecs_client):
    # CHECK IF USER PROVIDED ANY CLUSTER NAMES
    if len(settings.config['aws']['cluster names']) < 1:
        # IF NOT GRAB ALL CLUSTER NAMES FROM AWS AND ASSIGN TO VARIABLE
        ecs_cluster_names = ecs_client.list_clusters()
    else:
        # IF YES ASSIGN THEM TO VARIABLE
        ecs_cluster_names = settings.config['aws']['cluster_names']

    # CHECK IF MORE THAN ONE CLUSTER ...we will need to figure out how to handle this...
    if len(ecs_cluster_names['clusterArns']) > 1:
        print('Multiple ECS clusters detected', ecs_cluster_names['clusterArns'])
    else:
        print('One ECS cluster detected', ecs_cluster_names['clusterArns'])
    return ecs_cluster_names


# ECS LIST SERVICES FUNCTION || RETURNS ARRAY OF SERVICE NAMES
def ecs_list_services(ecs_client, ecs_cluster_name):
    ecs_service_names = ecs_client.list_services(
        cluster=ecs_cluster_name
    )
    print('Found ', len(ecs_service_names['serviceArns']), ' Services')
    return ecs_service_names


# ECS DESCRIBE SERVICES FUNCTION
def ecs_describe_services(ecs_client, ecs_service_names, ecs_cluster_name):
    ecs_service_descriptions = ecs_client.describe_services(
        cluster=ecs_cluster_name,
        services=[ecs_service_names]
    )
    print(ecs_service_descriptions)
    return


# ECS DESCRIBE TASK DEFINITION
def ecs_describe_task_definition(ecs_client, ecs_task_name):
    ecs_task_description = ecs_client.describe_task_definition(
        taskDefinition=ecs_task_name
    )
    print(ecs_task_description['containerDefinitions'])
    return


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