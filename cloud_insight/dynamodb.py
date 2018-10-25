#!/usr/bin/python

from boto3.dynamodb.conditions import Key


# CONNECT TO DYNAMODB TABLE
def connect_table(app, resource, table_name):
    app.log.info('AWS: Connecting to dynamodb table {}'.format(table_name))
    table = resource.Table(table_name)
    return table


# SEARCH FOR ALL DATA ABOUT A SERVICE
def search_service(app, resource, service_name, table_name):
    table = connect_table(app, resource, table_name)
    response = table.query(
        Select='ALL_ATTRIBUTES',
        KeyConditionExpression=Key('group').eq(
            'service:{}'.format(service_name)
        )
    )
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.query(
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression=Key('group').eq(
                'service:{}'.format(service_name)
            ),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
    data.extend(response['Items'])
    return data


# GET ALL TASK DEFINITIONS
def get_task_definitions(app, client, service_name, table_name):
    task_definitions = set()
    tasks = search_service(app, client, service_name, table_name)
    for task in tasks:
        task_definitions.add(task['taskDefinitionArn'])
    sorted_task_definitions = list(sorted(task_definitions))
    return sorted_task_definitions
