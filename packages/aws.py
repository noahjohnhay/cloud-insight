#!/usr/bin/python

import boto3


# LIST REGIONS
def list_regions(service):
    session = boto3.Session()
    all_regions = session.get_available_regions(
        service
    )
    return all_regions


# DEFAULT CLIENT
def default_client(region, service):
    client = boto3.client(
        service,
        region_name=region
    )
    return client


# PROFILE CLIENT
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
