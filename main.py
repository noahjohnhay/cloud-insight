#!/usr/bin/python

import aws
import logging
import settings
import table


def aws_caller(ecs_client, ecs_services):

    # ITERATE THROUGH ECS CLUSTERS
    for ecs_cluster in aws.ecs_list_clusters(ecs_client)['clusterArns']:

        # PRINT CLUSTERS
        print('AWS: Found cluster {0}'.format(
            aws.parse_arn(ecs_cluster)['resource'])
        )

        # ITERATE THROUGH SERVICES IN EACH CLUSTER
        for ecs_service in aws.ecs_list_services(ecs_client, aws.parse_arn(ecs_cluster)['resource']):

            # CREATE SERVICE DICTIONARY
            service = {}

            # ADD SERVICE ITEM TO DICTIONARY
            service['name'] = aws.parse_arn(ecs_service)['resource']

            # ADD CLUSTER ITEM TO DICTIONARY
            service['cluster'] = aws.parse_arn(ecs_cluster)['resource']

            # PRINT SERVICES
            print('AWS: Found service {0}'.format(
                aws.parse_arn(ecs_service)['resource'])
            )

            # DESCRIBE SERVICES
            ecs_service_description = aws.ecs_describe_service(
                ecs_client,
                aws.parse_arn(ecs_service)['resource'],
                aws.parse_arn(ecs_cluster)['resource']
            )

            # PRINT SERVICE DESCRIPTION
            print('AWS: Service {0}, Count {1}, Active Task Definition {2}'.format(
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
            ecs_task_description = aws.ecs_describe_task_definition(
                ecs_client,
                ecs_service_description['services'][0]['taskDefinition']
            )

            # ADD VERSION ITEM TO DICTIONARY
            service['version'] = ecs_task_description['taskDefinition']['containerDefinitions'][0]['image'].split(':', 1)[-1]

            # APPEND DICTIONARY ITEMS TO ARRAY
            ecs_services.append(service)

    return ecs_services


# MAIN PROGRAM
def main():

    settings.init()

    # IF AWS IS ENABLED
    if settings.config['aws']['enabled']:

        logging.info('AWS: Enabled')

        ecs_services = []

        # IF AWS AUTH TYPE IF PROFILE CALL aws_auth_profile() FUNCTION
        if settings.config['aws']['auth']['type'] == 'profile':

            logging.info('AWS: Using profile authentication')

            # FOR EACH PROFILE
            for aws_profile_name in settings.config['aws']['auth']['profile names']:

                print('AWS: Trying to auth with profile {0}'.format(aws_profile_name))

                # IF NO REGIONS ARE SPECIFIED FETCH ALL
                if len(settings.config['aws']['regions']) == 0:

                    print('AWS: Regions is empty, fetching all regions')

                    # FOR EACH REGION
                    for ecs_region in aws.ecs_list_regions():
                        ecs_client = aws.ecs_auth_profile(aws_profile_name, ecs_region)
                        aws_services = aws_caller(ecs_client, ecs_services)
                else:

                    # FOR EACH REGION
                    for ecs_region in settings.config['aws']['regions']:
                        ecs_client = aws.ecs_auth_profile(aws_profile_name, ecs_region)
                        aws_services = aws_caller(ecs_client, ecs_services)

                # IF OUTPUT IS ENABLED
                if settings.config['output']['enabled']:
                    if settings.config['output']['type'] == 'table':
                        table.basic_table(aws_services)

        elif settings.config['aws']['auth']['type'] == 'default':
            logging.info('AWS: Using default authentication')

            # REDO ALL OF THIS
            ecs_client = aws.ecs_auth_default(settings.config['aws']['region'][0])
            aws_caller(ecs_client, ecs_services)
        else:
            logging.error('AWS: Could not determine auth type')

    else:
        logging.error('MAIN: Nothing is enabled')


main()
