#!/usr/bin/python

import boto3


# CREATE AN ARRAY OF ALL POSSIBLE SESSIONS
def all_sessions(
        app,
        auth_type,
        aws_profile_names=None,
        aws_access_key=None,
        aws_secret_key=None,
        aws_session_token=None):
    sessions = []
    if auth_type == 'profile':
        app.log.info(
            'AWS: Using profile authentication'
        )
        for aws_profile_name in aws_profile_names:
            sessions.append(
                profile_session(
                    app=app,
                    profile_name=aws_profile_name
                )
            )
    elif auth_type == 'default':
        app.log.info(
            'AWS: Using default authentication'
        )
        sessions.append(
            default_session(
                app=app
            )
        )
    elif auth_type == 'keys':
        app.log.info(
            'AWS: Using keys authentication'
        )
        sessions.append(
            key_session(
                app=app,
                access_key=aws_access_key,
                secret_key=aws_secret_key,
                session_token=aws_session_token
            )
        )
    else:
        app.log.error(
            'AWS: Could not determine authentication type'
        )
        app.close(1)
    return sessions


# CREATE A SESSION USING DEFAULT CREDENTIALS
def default_session(app):
    app.log.info(
        'AWS: Trying to auth with default credentials'
    )
    session = boto3.Session()
    return session


# CREATE A SESSION USING ACCESS KEY AND SECRET KEY
def key_session(app, access_key, secret_key, session_token=None):
    app.log.info(
        'AWS: Trying to auth with provided keys ACCESS_KEY_ID:{}'.format(
            access_key
        )
    )
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token
    )
    return session


# LIST ALL REGIONS AVAILABLE FOR A SPECIFIC SERVICE
def list_regions(aws_service):
    session = boto3.Session()
    all_service_regions = session.get_available_regions(
        aws_service
    )
    return all_service_regions


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


# CREATE A SESSION USING PROFILE
def profile_session(app, profile_name):
    app.log.info(
        'AWS: Trying to auth with profile {}'.format(
            profile_name
        )
    )
    session = boto3.Session(
        profile_name=profile_name
    )
    return session


# CREATE A CLIENT USING A SESSION
def session_client(app, aws_region, aws_service, session):
    app.log.info(
        'AWS: Creating a {} client in {}'.format(
            aws_service,
            aws_region
        )
    )
    client = session.client(
        aws_service,
        region_name=aws_region
    )
    return client


# CREATE A RESOURCE USING A SESSION
def session_resource(app, aws_region, aws_service, session):
    app.log.info(
        'AWS: Creating a {} resource in {}'.format(
            aws_service,
            aws_region
        )
    )
    resource = session.resource(
        aws_service,
        region_name=aws_region
    )
    return resource
