#!/usr/bin/python

import boto3


# CREATE ALL CLIENTS
def all_clients(
        app,
        auth_type,
        aws_service,
        aws_profile_names=None,
        aws_regions=None,
        aws_access_key=None,
        aws_secret_key=None,
        aws_session_token=None):

    clients = []
    if aws_regions is None:
        app.log.info('AWS: Regions is empty, fetching all regions')
        aws_regions = list_regions(aws_service)
    if auth_type == 'profile':
        app.log.info('AWS: Using profile authentication')
        for aws_profile_name in aws_profile_names:
            for aws_region in aws_regions:
                clients.append(
                    profile_client(
                        app=app,
                        profile_name=aws_profile_name,
                        region=aws_region,
                        service=aws_service
                    )
                )
    elif auth_type == 'default':
        app.log.info('AWS: Using default authentication')
        for aws_region in aws_regions:
            clients.append(
                default_client(
                    region=aws_region,
                    service=aws_service
                )
            )
    elif auth_type == 'keys':
        app.log.info('AWS: Using keys authentication')
        for aws_region in aws_regions:
            clients.append(
                key_client(
                    region=aws_region,
                    service=aws_service,
                    access_key=aws_access_key,
                    secret_key=aws_secret_key,
                    session_token=aws_session_token
                )
            )

    else:
        app.log.error('AWS: Could not determine authentication type')
        app.close(1)
    return clients


# CREATE DEFAULT CLIENT
def default_client(region, service):
    client = boto3.client(
        service,
        region_name=region
    )
    return client


# CREATE KEY CLIENT
def key_client(region, service, access_key, secret_key, session_token):
    client = boto3.client(
        service,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token,
        region_name=region
    )
    return client


# LIST ALL REGIONS BY SERVICE
def list_regions(service):
    session = boto3.Session()
    all_regions = session.get_available_regions(
        service
    )
    return all_regions


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
        result['resource_type'], result['resource'] = result['resource'].split('/', 1)
    elif ':' in result['resource']:
        result['resource_type'], result['resource'] = result['resource'].split(':', 1)
    return result


# CREATE PROFILE CLIENT
def profile_client(app, profile_name, region, service):
    session = boto3.Session(
        profile_name=profile_name
    )
    client = session.client(
        service,
        region_name=region
    )
    app.log.info('AWS: Trying to auth with profile {0} in region {1}'.format(profile_name, region))
    return client
