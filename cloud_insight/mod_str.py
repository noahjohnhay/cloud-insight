#!/usr/bin/python

import re


def filter_dictionary(app, services):

    # IF FILTER IS ENABLED
    if 'filter' in app.config.get_section_dict('output'):

        app.log.info('OUTPUT: Filtering enabled')

        # FOR EACH FILTER KEY
        for filter_key in app.config.get_section_dict('output')['filter']:

            # ASSIGN THE VALUES FROM THE FILTER KEY TO VARIABLE
            filter_list = app.config.get_section_dict('output')['filter'][filter_key]

            # FILTER DICTIONARY BASED ON FILTER KEY & FILTER LIST
            services = [
                d for d in services if d[filter_key] in filter_list
            ]

    return services


def regex_dictionary(app, services):

    # IF REGEX IS ENABLED
    if 'regex' in app.config.get_section_dict('output'):

        app.log.info('OUTPUT: Regex enabled')

        # ITERATE THROUGH EACH SERVICE DICTIONARY
        for service in services:

            # FOR EACH REGEX KEY (ex: 'service', 'cluster')
            for regex_key in app.config.get_section_dict('output')['regex']:

                # FETCH DICTIONARY OF REGEXES
                regex_dict = app.config.get_section_dict('output')['regex'][regex_key]

                # ITERATE THROUGH REGEXES
                for item in regex_dict.keys():

                    # ATTEMPT TO RUN REGEX AGAINST STRING
                    service[regex_key] = re.sub(item, regex_dict[item], service[regex_key])

    return services


def replace_dictionary(app, services):

    # IF REPLACE ENABLED
    if 'replace' in app.config.get_section_dict('output'):

        app.log.info('OUTPUT: Replacing enabled')

        # ITERATE THROUGH EACH SERVICE DICTIONARY
        for service in services:

            # FOR EACH REPLACE KEY (ex: 'service', 'cluster')
            for replace_key in app.config.get_section_dict('output')['replace']:

                # FETCH DICTIONARY OF REPLACEMENTS
                replace_dict = app.config.get_section_dict('output')['replace'][replace_key]

                # ITERATE THROUGH REPLACEMENTS
                for item in replace_dict.keys():

                    # ATTEMPT TO REPLACE ITEM IN STRING
                    service[replace_key] = service[replace_key].replace(item, replace_dict[item])

    return services


def same_dictionary(source_services, destination_services):

    # CREATE NEW ARRAY FOR COMPARE DICTIONARIES
    all_compare = []

    # ITERATE THROUGH SOURCE DICTIONARIES
    for source_dict in source_services:

        # ITERATE THROUGH DESTINATION DICTIONARIES
        for dest_dict in destination_services:

            # IF THE SOURCE SERVICE IS THE SAME AS THE DESTINATION SERVICE
            if source_dict['service'] == dest_dict['service']:

                # CREATE A NEW DICTIONARY
                compare = dict()

                # ADD THE SERVICE NAME
                compare['service'] = source_dict['service']

                # ADD THE SOURCE VERSION
                compare['source_version'] = source_dict['version']

                # ADD THE DESTINATION VERSION
                compare['destination_version'] = dest_dict['version']

                # APPEND DICTIONARY TO ARRAY
                all_compare.append(compare)

                break

    return all_compare
