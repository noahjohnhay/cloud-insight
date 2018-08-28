import cloud_insight.aws as aws
import cloud_insight.ecs as ecs
import mod_str as mod_str
import cloud_insight.output as output


def aws_caller(ecs_client, ecs_services):

    # ITERATE THROUGH ECS CLUSTERS
    for ecs_cluster in ecs.list_clusters(ecs_client)['clusterArns']:

        # PRINT CLUSTERS
        print('AWS: Found cluster {0}'.format(
            aws.parse_arn(ecs_cluster)['resource'])
        )

        # ITERATE THROUGH SERVICES IN EACH CLUSTER
        for ecs_service in \
                ecs.list_services(ecs_client,
                                  aws.parse_arn(ecs_cluster)['resource']):

            # CREATE SERVICE DICTIONARY
            service = dict()

            # ADD SERVICE ITEM TO DICTIONARY
            service['name'] = aws.parse_arn(ecs_service)['resource']

            # ADD CLUSTER ITEM TO DICTIONARY
            service['cluster'] = aws.parse_arn(ecs_cluster)['resource']

            # PRINT SERVICES
            print('AWS: Found service {0}'.format(
                aws.parse_arn(ecs_service)['resource'])
            )

            # DESCRIBE SERVICES
            ecs_service_description = ecs.describe_service(
                ecs_client,
                aws.parse_arn(ecs_service)['resource'],
                aws.parse_arn(ecs_cluster)['resource']
            )

            resource = aws.parse_arn(ecs_service)['resource']
            desired_count = \
                ecs_service_description['services'][0]['desiredCount']
            task_definition = \
                ecs_service_description['services'][0]['taskDefinition']

            print('AWS: Service {0}, Count {1}, '
                  'Active Task Definition {2}'.format(resource,
                                                      desired_count,
                                                      task_definition))

            # ADD COUNT INFORMATION TO DICTIONARY
            service['desired_count'] = \
                ecs_service_description['services'][0]['desiredCount']
            service['running_count'] = \
                ecs_service_description['services'][0]['runningCount']

            # ADD LAUNCH TYPE INFORMATION TO DICTIONARY
            service['launch_type'] = \
                ecs_service_description['services'][0]['launchType']

            # DESCRIBE TASK DEFINITIONS
            ecs_task_description = ecs.describe_task_definition(
                ecs_client,
                ecs_service_description['services'][0]['taskDefinition']
            )

            # ADD VERSION ITEM TO DICTIONARY
            service['version'] = ecs_task_description['taskDefinition']\
                ['containerDefinitions'][0]['image'].split(':', 1)[-1]

            # APPEND DICTIONARY ITEMS TO ARRAY
            ecs_services.append(service)

    return ecs_services


def execute():

    settings.init()

    # IF AWS IS ENABLED
    if settings.config['aws']['enabled']:

        logging.info('AWS: Enabled')

        ecs_services = []

        # IF AWS AUTH TYPE IS PROFILE CALL aws_auth_profile() FUNCTION
        if settings.config['aws']['auth']['type'] == 'profile':

            logging.info('AWS: Using profile authentication')

            # FOR EACH PROFILE
            for aws_profile_name in \
                    settings.config['aws']['auth']['profile names']:

                print('AWS: Trying to auth with profile {0}'
                      .format(aws_profile_name))

                # IF NO REGIONS ARE SPECIFIED FETCH ALL
                if len(settings.config['aws']['regions']) == 0:

                    # APPLY FILTERING
                    ecs_services = mod_str.filter_dictionary(app,
                                                             ecs_services)

                    # APPLY REPLACEMENTS
                    ecs_services = mod_str.replace_dictionary(app,
                                                              ecs_services)

                    ecs_client = aws.profile_client(aws_profile_name,
                                                    ecs_region,
                                                    'ecs')

                    aws_services = aws_caller(ecs_client,
                                              ecs_services)
                else:

                    # FOR EACH REGION
                    for ecs_region in settings.config['aws']['regions']:
                        ecs_client = aws.profile_client(aws_profile_name,
                                                        ecs_region,
                                                        'ecs')
                        aws_services = aws_caller(ecs_client, ecs_services)

                # IF OUTPUT IS ENABLED
                if settings.config['output']['enabled']:

                    # IF OUTPUT TYPE IS TABLE
                    if settings.config['output']['type'] == 'table':

                        table.basic_table(aws_services)

        # IF AWS AUTH TYPE IS DEFAULT
        elif settings.config['aws']['auth']['type'] == 'default':

            logging.info('AWS: Using default authentication')

            # IF NO REGIONS ARE SPECIFIED FETCH ALL
            if len(settings.config['aws']['regions']) == 0:

                logging.info('AWS: Regions is empty, fetching all regions')

                # FOR EACH REGION
                for ecs_region in aws.list_regions('ecs'):

                    ecs_client = aws.default_client(ecs_region, 'ecs')

                    aws_services = aws_caller(ecs_client, ecs_services)
            else:

                # FOR EACH REGION
                for ecs_region in settings.config['aws']['regions']:

                    ecs_client = aws.default_client(ecs_region, 'ecs')

                    aws_services = aws_caller(ecs_client, ecs_services)

            # IF OUTPUT IS ENABLED
            if settings.config['output']['enabled']:

                logging.info('OUTPUT: Output enabled')

                # IF OUTPUT TYPE IS TABLE
                if settings.config['output']['type'] == 'table':

                    logging.info('OUTPUT: Table output enabled')

                    table.basic_table(aws_services)
                else:
                    logging.error('OUTPUT: No valid output type selected')
        else:
            logging.error('AWS: Could not determine auth type')
    else:
        logging.error('MAIN: Nothing is enabled')

    # APPLY FILTERING
    source_services = mod_str.filter_dictionary(app, source_services)
    destination_services = mod_str.filter_dictionary(app, destination_services)

    # APPLY REPLACEMENTS
    source_services = mod_str.replace_dictionary(app, source_services)
    destination_services = mod_str.replace_dictionary(app,
                                                      destination_services)

    # APPLY REGEXES
    source_services = mod_str.regex_dictionary(app, source_services)
    destination_services = mod_str.regex_dictionary(app, destination_services)

    diff_services = mod_str.same_dictionary(source_services,
                                            destination_services)

    output.compare_table(diff_services, 'html_table')
