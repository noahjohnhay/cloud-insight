#!/usr/bin/python

import re


def main(app, services):
    if 'filter' in app.config.get_section_dict('output'):
        services = filter_dictionary(app, services)
    if 'replace' in app.config.get_section_dict('output'):
        services = replace_dictionary(app, services)
    if 'regex' in app.config.get_section_dict('output'):
        services = regex_dictionary(app, services)
    return services


def filter_dictionary(app, services):
    app.log.info('OUTPUT: Filtering enabled')
    for filter_key in app.config.get_section_dict('output')['filter']:
        filter_list = app.config.get_section_dict('output')['filter'][filter_key]
        # TODO: figure out how to iterate through the list of filter keys again
        services = [
            service for service in services if re.match(filter_list[0], service[filter_key])
        ]
    return services


def regex_dictionary(app, services):
    app.log.info('OUTPUT: Regex enabled')
    for service in services:
        for regex_key in app.config.get_section_dict('output')['regex']:
            regex_dict = app.config.get_section_dict('output')['regex'][regex_key]
            for item in regex_dict.keys():
                service[regex_key] = re.sub(item, regex_dict[item], service[regex_key])
    return services


def replace_dictionary(app, services):
    app.log.info('OUTPUT: Replacing enabled')
    for service in services:
        for replace_key in app.config.get_section_dict('output')['replace']:
            replace_dict = app.config.get_section_dict('output')['replace'][replace_key]
            for item in replace_dict.keys():
                service[replace_key] = service[replace_key].replace(item, replace_dict[item])
    return services


def same_dictionary(source_services, destination_services):
    all_compare = []
    for source_dict in source_services:
        for dest_dict in destination_services:
            if source_dict['service'] == dest_dict['service']:
                compare = dict()
                compare['service'] = source_dict['service']
                compare['source_version'] = source_dict['version']
                compare['destination_version'] = dest_dict['version']
                all_compare.append(compare)
                break
    return all_compare
