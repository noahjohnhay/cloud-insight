#!/usr/bin/python3
import aws
import logging
import settings


def aws_caller(ecs_client):
    for ecs_cluster in aws.ecs_list_clusters(ecs_client)['clusterArns']:
        print('AWS: Found cluster {0}'.format(aws.parse_arn(ecs_cluster)['resource']))
        # FOR EACH SERVICE IN EACH CLUSTER
        for ecs_service in aws.ecs_list_services(ecs_client, aws.parse_arn(ecs_cluster)['resource']):
            # DESCRIBE THOSE SERVICES
            print('AWS: Found service {0}'.format(aws.parse_arn(ecs_service)['resource']))
            ecs_service_description = aws.ecs_describe_service(ecs_client, aws.parse_arn(ecs_service)['resource'], aws.parse_arn(ecs_cluster)['resource'])
            print('AWS: Service {0}, Count {1}, Active Task Definition {2}'.format(aws.parse_arn(ecs_service)['resource'], ecs_service_description['services'][0]['desiredCount'], ecs_service_description['services'][0]['taskDefinition']))
            aws.ecs_describe_task_definition(ecs_client, ecs_service_description['services'][0]['taskDefinition'])

# MAIN PROGRAM
def main():

    settings.init()

    if settings.config['aws']['enabled']:
        logging.info('AWS: Enabled')
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
                        aws_caller(ecs_client)
                else:
                    # FOR EACH REGION
                    for ecs_region in settings.config['aws']['regions']:
                        ecs_client = aws.ecs_auth_profile(aws_profile_name, ecs_region)
                        aws_caller(ecs_client)

        elif settings.config['aws']['auth']['type'] == 'default':
            logging.info('AWS: Using default authentication')






            ecs_client = aws.ecs_auth_default(settings.config['aws']['region'][0])
            aws_caller(ecs_client)
        else:
            logging.error('AWS: Could not determine auth type')

    else:
        logging.error('MAIN: Nothing is enabled')


main()
