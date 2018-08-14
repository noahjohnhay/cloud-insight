#!/usr/bin/python

import packages.aws as aws
import packages.ecs as ecs
import packages.settings as settings
import packages.output as output
import sys


def aws_caller(app, ecs_client, ecs_services):

    # ITERATE THROUGH ECS CLUSTERS
    for ecs_cluster in ecs.list_clusters(ecs_client)['clusterArns']:

        # PRINT CLUSTERS
        app.log.info('AWS: Found cluster {0}'.format(
            aws.parse_arn(ecs_cluster)['resource'])
        )

        # ITERATE THROUGH SERVICES IN EACH CLUSTER
        for ecs_service in ecs.list_services(app, ecs_client, aws.parse_arn(ecs_cluster)['resource']):

            # CREATE SERVICE DICTIONARY
            service = dict()

            # ADD SERVICE ITEM TO DICTIONARY
            service['name'] = aws.parse_arn(ecs_service)['resource']

            # ADD CLUSTER ITEM TO DICTIONARY
            service['cluster'] = aws.parse_arn(ecs_cluster)['resource']

            # PRINT SERVICES
            app.log.info('AWS: Found service {0}'.format(
                aws.parse_arn(ecs_service)['resource'])
            )

            # DESCRIBE SERVICES
            ecs_service_description = ecs.describe_service(
                ecs_client,
                aws.parse_arn(ecs_service)['resource'],
                aws.parse_arn(ecs_cluster)['resource']
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
            ecs_task_description = ecs.describe_task_definition(
                ecs_client,
                ecs_service_description['services'][0]['taskDefinition']
            )

            # ADD VERSION ITEM TO DICTIONARY
            service['version'] = \
                ecs_task_description['taskDefinition']['containerDefinitions'][0]['image'].split(':', 1)[-1]

            # APPEND DICTIONARY ITEMS TO ARRAY
            ecs_services.append(service)

    sorted_ecs_services = sorted(ecs_services, key=lambda k: k['name'])

    return sorted_ecs_services


def default_command(app):
    app.log.error('A namespace must be specified use "--help" to see all options')
    sys.exit(1)


def list_command(app):
    app.log.info('Running list command')
    app.config.parse_file('../config.json')

    settings.init()

    # IF AWS IS ENABLED
    if app.config.get_section_dict('aws')['enabled']:

        app.log.info('AWS: Enabled')

        ecs_services = []

        # IF AWS AUTH TYPE IS PROFILE CALL aws_auth_profile() FUNCTION
        if app.config.get_section_dict('aws')['auth']['type'] == 'profile':

            app.log.info('AWS: Using profile authentication')

            # FOR EACH PROFILE
            for aws_profile_name in app.config.get_section_dict('aws')['auth']['profile names']:

                app.log.info('AWS: Trying to auth with profile {0}'.format(aws_profile_name))

                # IF NO REGIONS ARE SPECIFIED FETCH ALL
                if len(app.config.get_section_dict('aws')['regions']) == 0:

                    app.log.info('AWS: Regions is empty, fetching all regions')

                    # FOR EACH REGION
                    for ecs_region in aws.list_regions('ecs'):

                        ecs_client = aws.profile_client(app, aws_profile_name, ecs_region, 'ecs')

                        aws_services = aws_caller(app, ecs_client, ecs_services)
                else:

                    # FOR EACH REGION
                    for ecs_region in app.config.get_section_dict('aws')['regions']:

                        ecs_client = aws.profile_client(app, aws_profile_name, ecs_region, 'ecs')

                        aws_services = aws_caller(app, ecs_client, ecs_services)

                output.main(app, aws_services)

        # IF AWS AUTH TYPE IS DEFAULT
        elif app.config.get_section_dict('aws')['auth']['type'] == 'default':

            app.log.info('AWS: Using default authentication')

            # IF NO REGIONS ARE SPECIFIED FETCH ALL
            if len(app.config.get_section_dict('aws')['regions']) == 0:

                app.log.info('AWS: Regions is empty, fetching all regions')

                # FOR EACH REGION
                for ecs_region in aws.list_regions('ecs'):

                    ecs_client = aws.default_client(ecs_region, 'ecs')

                    aws_services = aws_caller(app, ecs_client, ecs_services)
            else:

                # FOR EACH REGION
                for ecs_region in app.config.get_section_dict('aws')['regions']:

                    ecs_client = aws.default_client(ecs_region, 'ecs')

                    aws_services = aws_caller(app, ecs_client, ecs_services)

            output.main(app, aws_services)

            app.log.info('AWS: Could not determine auth type')
    else:
        app.log.error('MAIN: Nothing is enabled')


def compare_command(app):
    app.log.info('Running compare command')
