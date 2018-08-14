#!/usr/bin/python

import plotly
import sys
from prettytable import PrettyTable


def main(app, services):
    # IF OUTPUT IS ENABLED
    if app.config.get_section_dict('output')['enabled']:

        app.log.info('OUTPUT: Output enabled')

        # IF OUTPUT TYPE IS HTML TABLE
        if app.config.get_section_dict('output')['type'] == 'html_table':

            app.log.info('OUTPUT: HTML table output enabled')

            # EXECUTE HTML TABLE FUNCTION
            html_table(services)

        # IF OUTPUT TYPE IS CLI TABLE
        elif app.config.get_section_dict('output')['type'] == 'cli_table':

            app.log.info('OUTPUT: CLI table output enabled')

            # EXECUTE CLI TABLE FUNCTION
            cli_table(services)

        else:

            app.log.error('OUTPUT: No valid output type selected')

            sys.exit(1)

    else:

        app.log.info('OUTPUT: Output disabled')

    return


def html_table(services):

    # DESCRIBE TABLE
    trace = plotly.graph_objs.Table(
        # DESCRIBE TABLE HEADERS
        columnwidth=[
            100,
            100,
            20,
            20,
            100,
            100
        ],
        header=dict(
            values=[
                'Name',
                'Version',
                'Desired Count',
                'Running Count',
                'Cluster',
                'Launch Type'
            ],
            fill=dict(
                color='#a1c3d1'
            )
        ),
        # DESCRIBE TABLE CONTENTS
        cells=dict(
            values=[
                [service['name'] for service in services],
                [service['version'] for service in services],
                [service['desired_count'] for service in services],
                [service['running_count'] for service in services],
                [service['cluster'] for service in services],
                [service['launch_type'] for service in services],
            ],
            fill=dict(
                color=[
                    '#F5F4F4',
                    '#F5F4F4',
                    [
                        '#24F015' if service['desired_count'] == service['running_count'] \
                        else '#DA100C' for service in services
                    ],
                    [
                        '#24F015' if service['desired_count'] == service['running_count'] \
                        else '#DA100C' for service in services
                    ],
                    '#F5F4F4',
                    '#F5F4F4'
                ]
            ),
            align=[
                'left',
                'center',
                'center',
                'center',
                'center',
                'center',
            ]
        )
    )

    data = [trace]

    # OUTPUT TABLE TO HTML FILE
    plotly.offline.plot(data, filename='../basic_table.html')

    return


def cli_table(services):

    # INITIALIZE TABLE
    table = PrettyTable()

    # DESCRIBE TABLE HEADERS
    table.field_names = [
        'Name',
        'Version',
        'Desired Count',
        'Running Count',
        'Cluster',
    ]

    # ALIGN COLUMNS
    table.align['Name'] = 'l'
    table.align['Version'] = 'l'

    # INSERT DATA INTO TABLE
    for service in services:
        table.add_row([
            service['name'],
            service['version'],
            service['desired_count'],
            service['running_count'],
            service['cluster'],
        ])

    # PRINT TABLE
    print(table)

    return
