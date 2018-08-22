#!/usr/bin/python

import packages.aws as aws
import packages.ecs as ecs
import packages.output as output


def list_helper(app, aws_auth_type, aws_enabled, aws_profile_names, aws_regions):

    # CREATE EMPTY ARRAY
    ecs_services = []

    # IF AWS IS ENABLED
    if aws_enabled:

        app.log.info('AWS: Enabled')

        # IF AWS AUTH TYPE IS DEFAULT
        if aws_auth_type == 'default':

            # SET AWS PROFILE NAMES TO NONE
            aws_profile_names = None

        # ITERATE THROUGH ALL CREATED CLIENTS
        for ecs_client in aws.all_clients(
                app=app,
                auth_type=aws_auth_type,
                aws_service='ecs',
                aws_profile_names=aws_profile_names,
                aws_regions=aws_regions):

            # CREATE ARRAY OF SERVICE DICTIONARIES
            ecs_services = ecs.service_dictionary(
                app=app,
                ecs_client=ecs_client,
                ecs_services=ecs_services
            )

    else:

        app.log.error('MAIN: Nothing is enabled')

        app.close(1)

    return ecs_services


def default_command(app):
    app.log.error('A namespace must be specified use "--help" to see all options')
    app.close(1)


def list_command(app):
    app.log.info('Running list command')
    app.config.parse_file(app.pargs.config)

    ecs_services = list_helper(
        app=app,
        aws_auth_type=app.config.get_section_dict('aws')['auth']['type'],
        aws_enabled=app.config.get_section_dict('aws')['enabled'],
        aws_profile_names=app.config.get_section_dict('aws')['auth']['profile names'],
        aws_regions=app.config.get_section_dict('aws')['regions']
    )

    # APPLY FILTERING
    ecs_services = output.filter_dict(app, ecs_services)

    # APPLY REPLACEMENTS
    ecs_services = output.replace_dictionary(app, ecs_services)

    # PRINT OUTPUTS
    output.main(app, ecs_services)


def compare_command(app):
    app.log.info('Running compare command')
    app.config.parse_file(app.pargs.config)

    source_services = list_helper(
        app=app,
        aws_auth_type=app.config.get_section_dict('source')['aws']['auth']['type'],
        aws_enabled=app.config.get_section_dict('source')['aws']['enabled'],
        aws_profile_names=app.config.get_section_dict('source')['aws']['auth']['profile names'],
        aws_regions=app.config.get_section_dict('source')['aws']['regions']
    )

    destination_services = list_helper(
        app=app,
        aws_auth_type=app.config.get_section_dict('destination')['aws']['auth']['type'],
        aws_enabled=app.config.get_section_dict('destination')['aws']['enabled'],
        aws_profile_names=app.config.get_section_dict('destination')['aws']['auth']['profile names'],
        aws_regions=app.config.get_section_dict('destination')['aws']['regions']
    )

    # APPLY FILTERING
    source_services = output.filter_dict(app, source_services)
    destination_services = output.filter_dict(app, destination_services)

    # APPLY REPLACEMENTS
    source_services = output.replace_dictionary(app, source_services)
    destination_services = output.replace_dictionary(app, destination_services)

    print (source_services)
    print (destination_services)
