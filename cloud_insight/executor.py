#!/usr/bin/python

import cloud_insight.aws as aws
import cloud_insight.ecs as ecs
import mod_str as mod_str
import cloud_insight.output as output


def list_helper(app, aws_auth_type, aws_enabled, aws_regions, namespace, list_type=None):

    services = []

    # IF AWS IS ENABLED
    if aws_enabled:

        app.log.info('AWS: Enabled')

        # SET VARIABLES TO NONE
        aws_profile_names = None
        aws_access_key = None
        aws_secret_key = None
        aws_session_token = None

        if list_type == 'default':

            if aws_auth_type == 'keys':

                aws_access_key = app.config.get_section_dict('aws')['auth']['aws_access_key']
                aws_secret_key = app.config.get_section_dict('aws')['auth']['aws_secret_key']

                if 'aws_session_token' in app.config.get_section_dict('aws')['auth']:

                    aws_session_token = app.config.get_section_dict('aws')['auth']['aws_session_token']

            elif aws_auth_type == 'profile':

                aws_profile_names = app.config.get_section_dict('aws')['auth']['profile names']

        elif list_type == 'destination':

            if aws_auth_type == 'keys':

                aws_access_key = app.config.get_section_dict('destination')['aws']['auth']['aws_access_key']
                aws_secret_key = app.config.get_section_dict('destination')['aws']['auth']['aws_secret_key']

                if 'aws_session_token' in app.config.get_section_dict('destination')['aws']['auth']:

                    aws_session_token = app.config.get_section_dict('destination')['aws']['auth']['aws_session_token']

            elif aws_auth_type == 'profile':

                aws_profile_names = app.config.get_section_dict('destination')['aws']['auth']['profile names']

        elif list_type == 'source':

            if aws_auth_type == 'keys':

                aws_access_key = app.config.get_section_dict('source')['aws']['auth']['aws_access_key']
                aws_secret_key = app.config.get_section_dict('source')['aws']['auth']['aws_secret_key']

                if 'aws_session_token' in app.config.get_section_dict('source')['aws']['auth']:

                    aws_session_token = app.config.get_section_dict('source')['aws']['auth']['aws_session_token']

            elif aws_auth_type == 'profile':

                aws_profile_names = app.config.get_section_dict('source')['aws']['auth']['profile names']

        else:
            app.log.error('list helper error occurred')
            app.close(1)

        if aws_regions is None:
            app.log.info('AWS: Regions is empty, fetching all regions')
            aws_regions = aws.list_regions('ecs')

        # ITERATE THROUGH ALL REGIONS
        for aws_region in aws_regions:

            # ITERATE THROUGH ALL CREATED SESSIONS
            for session in aws.all_sessions(
                    app=app,
                    auth_type=aws_auth_type,
                    aws_access_key=aws_access_key,
                    aws_secret_key=aws_secret_key,
                    aws_session_token=aws_session_token,
                    aws_profile_names=aws_profile_names
            ):

                # CREATE ARRAY OF SERVICE DICTIONARIES
                services = ecs.service_dictionary(
                    app=app,
                    aws_region=aws_region,
                    aws_session=session,
                    namespace=namespace
                )

    else:
        app.log.error('MAIN: Nothing is enabled')
        app.close(1)
    return services


def main(app, namespace):

    app.log.info('Running {} command'.format(namespace))
    app.config.parse_file(app.pargs.config)

    if namespace == 'compare':
        # FETCH SOURCE SERVICES INFORMATION
        source_services = list_helper(
            app=app,
            aws_auth_type=app.config.get_section_dict('source')['aws']['auth']['type'],
            aws_enabled=app.config.get_section_dict('source')['aws']['enabled'],
            aws_regions=app.config.get_section_dict('source')['aws']['regions'],
            namespace='compare',
            list_type='source'

        )

        # FETCH DESTINATION SERVICES INFORMATION
        destination_services = list_helper(
            app=app,
            aws_auth_type=app.config.get_section_dict('destination')['aws']['auth']['type'],
            aws_enabled=app.config.get_section_dict('destination')['aws']['enabled'],
            aws_regions=app.config.get_section_dict('destination')['aws']['regions'],
            namespace='compare',
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

        # FIND DIFFERENT SERVICES
        diff_services = mod_str.same_dictionary(source_services, destination_services)

        # PRINT OUTPUT
        output.main(app, diff_services, 'compare')
    else:

        # FETCH SERVICE INFORMATION
        ecs_services = list_helper(
            app=app,
            aws_auth_type=app.config.get_section_dict('aws')['auth']['type'],
            aws_enabled=app.config.get_section_dict('aws')['enabled'],
            aws_regions=app.config.get_section_dict('aws')['regions'],
            namespace=namespace,
            list_type='default'
        )

        # APPLY FILTERING
        ecs_services = mod_str.filter_dictionary(app, ecs_services)

        # APPLY REPLACEMENTS
        ecs_services = mod_str.replace_dictionary(app, ecs_services)

        # PRINT OUTPUT
        output.main(app, ecs_services, namespace)
