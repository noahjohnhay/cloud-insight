#!/usr/bin/python

import cloud_insight.aws as aws
import cloud_insight.ecs as ecs
import mod_str as mod_str
import cloud_insight.output as output


def list_helper(app, aws_auth_type, aws_enabled, aws_regions, list_type=None):

    # CREATE EMPTY ARRAY
    ecs_services = []

    # IF AWS IS ENABLED
    if aws_enabled:

        app.log.info('AWS: Enabled')

        # IF AWS AUTH TYPE IS DEFAULT
        if aws_auth_type == 'default':

            # SET AWS PROFILE NAMES TO NONE
            aws_profile_names = None

        elif list_type == 'default':

            aws_profile_names = app.config.get_section_dict('aws')['auth']['profile names']

        elif list_type == 'source':

            aws_profile_names = app.config.get_section_dict('source')['aws']['auth']['profile names']

        elif list_type == 'destination':

            aws_profile_names = app.config.get_section_dict('destination')['aws']['auth']['profile names']

        else:
            aws_profile_names = None
            app.log.error('list helper error occurred')
            app.close(1)

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
        aws_regions=app.config.get_section_dict('aws')['regions'],
        list_type='default'
    )

    # APPLY FILTERING
    ecs_services = mod_str.filter_dictionary(app, ecs_services)

    # APPLY REPLACEMENTS
    ecs_services = mod_str.replace_dictionary(app, ecs_services)

    # PRINT OUTPUTS
    output.main(app, ecs_services)


def compare_command(app):
    app.log.info('Running compare command')
    app.config.parse_file(app.pargs.config)

    source_services = list_helper(
        app=app,
        aws_auth_type=app.config.get_section_dict('source')['aws']['auth']['type'],
        aws_enabled=app.config.get_section_dict('source')['aws']['enabled'],
        aws_regions=app.config.get_section_dict('source')['aws']['regions'],
        list_type='source'
    )

    destination_services = list_helper(
        app=app,
        aws_auth_type=app.config.get_section_dict('destination')['aws']['auth']['type'],
        aws_enabled=app.config.get_section_dict('destination')['aws']['enabled'],
        aws_regions=app.config.get_section_dict('destination')['aws']['regions'],
        list_type='destination'
    )

    # APPLY FILTERING
    source_services = mod_str.filter_dictionary(app, source_services)
    destination_services = mod_str.filter_dictionary(app, destination_services)

    # APPLY REPLACEMENTS
    source_services = mod_str.replace_dictionary(app, source_services)
    destination_services = mod_str.replace_dictionary(app, destination_services)

    # APPLY REGEXES
    source_services = mod_str.regex_dictionary(app, source_services)
    destination_services = mod_str.regex_dictionary(app, destination_services)

    diff_services = mod_str.same_dictionary(source_services, destination_services)

    output.compare_table(diff_services, 'html_table')
