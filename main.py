#!/usr/bin/python3
import aws
import logging
import settings


def aws_caller(ecs_client):
    for ecs_cluster in aws.ecs_list_clusters(ecs_client):
        # FOR EACH SERVICE IN EACH CLUSTER
        for ecs_service in aws.ecs_list_services(ecs_client, ecs_cluster):
            # DESCRIBE THOSE SERVICES
            aws.ecs_describe_services(ecs_client, ecs_service, ecs_cluster)


# MAIN PROGRAM
def main():

    settings.init()

    if settings.config['aws']['enabled']:
        logging.info('AWS is enabled')
        # IF AWS AUTH TYPE IF PROFILE CALL aws_auth_profile() FUNCTION
        if settings.config['aws']['auth']['type'] == 'profile':
            logging.info('AWS: Using profile authentication')
            # FOR EACH PROFILE
            for aws_profile_name in settings.config['aws']['auth']['profile names']:
                if settings.config['aws']['regions'] is None:
                    for ecs_region in aws.ecs_list_regions("profile", aws_profile_name):
                        ecs_client = aws.ecs_auth_profile(aws_profile_name, ecs_region)
                        aws_caller(ecs_client)
                else:
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
        print('nothing is enabled')



main()
