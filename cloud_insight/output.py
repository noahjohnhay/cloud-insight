#!/usr/bin/python

from plotly.offline import plot
from prettytable import PrettyTable
import plotly.graph_objs as go
import json


def main(app, services, table_type):
    if app.config.get_section_dict('output')['enabled']:
        app.log.info('OUTPUT: Output enabled')
        if table_type == 'compare':
            compare_table(app, services, app.config.get_section_dict('output')['type'])
        elif table_type == 'connectivity':
            connectivity_table(app, services, app.config.get_section_dict('output')['type'])
        elif table_type == 'health':
            health_table(app, services, app.config.get_section_dict('output')['type'])
        elif table_type == 'history':
            history_table(app, services, app.config.get_section_dict('output')['type'])
        elif table_type == 'list':
            list_table(app, services, app.config.get_section_dict('output')['type'])
        else:
            app.log.error('OUTPUT: Could not determine table type')
            app.close(1)
    else:
        app.log.info('OUTPUT: Output disabled')
    return


def compare_table(app, services, output_type):
    if output_type == 'cli_table':

        # INITIALIZE TABLE
        table = PrettyTable()

        # DESCRIBE TABLE HEADERS
        table.field_names = [
            'Name',
            'Source Version',
            'Destination Version',
        ]

        # ALIGN COLUMNS
        table.align['Name'] = 'l'
        table.align['Source Version'] = 'l'
        table.align['Destination Version'] = 'l'

        # INSERT DATA INTO TABLE
        for service in services:
            table.add_row([
                service['service'],
                service['source_version'],
                service['destination_version'],
            ])

        # PRINT TABLE
        print(table)

    elif output_type == 'html_table':

        # DESCRIBE TABLE
        trace = go.graph_objs.Table(
            # DESCRIBE TABLE HEADERS
            columnwidth=[
                10,
                100,
                100,
                100
            ],
            header=dict(
                values=[
                    '#',
                    'Name',
                    'Source Version',
                    'Destination Version'
                ],
                fill=dict(
                    color='#a1c3d1'
                )
            ),
            # DESCRIBE TABLE CONTENTS
            cells=dict(
                values=[
                    [idx for idx, service in enumerate(services)],
                    [service['service'] for service in services],
                    [service['source_version'] for service in services],
                    [service['destination_version'] for service in services]
                ],
                fill=dict(
                    color=[
                        '#F5F4F4',
                        '#F5F4F4',
                        [
                            '#24F015' if service['source_version'] == service['destination_version'] \
                            else '#DA100C' for service in services
                        ],
                        [
                            '#24F015' if service['source_version'] == service['destination_version'] \
                            else '#DA100C' for service in services
                        ]
                    ]
                ),
                align=[
                    'center',
                    'left',
                    'left',
                    'left'
                ]
            )
        )

        data = [trace]

        # OUTPUT TABLE TO HTML FILE
        plot(
            data,
            filename=app.config.get_section_dict('output')['path']
        )

    else:
        app.log.error('OUTPUT: No valid output type selected')
        app.close(1)
    return


def connectivity_table(app, services, output_type):
    if output_type == 'cli_table':

        # INITIALIZE TABLE
        table = PrettyTable()

        # DESCRIBE TABLE HEADERS
        table.field_names = [
            'Name',
            'LB Name',
            'LB Scheme',
            'LB Paths',
        ]

        # ALIGN COLUMNS
        table.align['Name'] = 'l'
        table.align['LB Name'] = 'c'
        table.align['LB Scheme'] = 'c'
        table.align['LB Paths'] = 'c'

        # INSERT DATA INTO TABLE
        for service in services:
            table.add_row(
                [
                    service['service'],
                    service['alb_name'],
                    service['alb_scheme'],
                    service['paths'],
                ]
            )

        # PRINT TABLE
        print(table)

    elif output_type == 'html_table':

        # DESCRIBE TABLE
        trace = go.graph_objs.Table(

            # DESCRIBE TABLE HEADERS
            columnwidth=[
                10,
                100,
                100,
                40,
                100
            ],
            header=dict(
                values=[
                    '#',
                    'Name',
                    'LB Name',
                    'LB Scheme',
                    'LB Paths',
                ],
                fill=dict(
                    color='#a1c3d1'
                )
            ),
            cells=dict(
                values=[
                    [idx for idx, service in enumerate(services)],
                    [service['service'] for service in services],
                    [service['alb_name'] for service in services],
                    [service['alb_scheme'] for service in services],
                    [service['paths'] for service in services]
                ],
                fill=dict(
                    color=[
                        '#F5F4F4',
                        '#F5F4F4',
                        '#F5F4F4',
                        '#F5F4F4',
                        '#F5F4F4',
                    ]
                ),
                align=[
                    'center',
                    'left',
                    'left',
                    'left',
                    'left'
                ]
            )
        )

        data = [trace]

        # OUTPUT TABLE TO HTML FILE
        plot(
            data,
            filename=app.config.get_section_dict('output')['path']
        )

    else:
        app.log.error('OUTPUT: No valid output type selected')
        app.close(1)
    return


def health_table(app, services, output_type):

    # IF OUTPUT TYPE IS CLI
    if output_type == 'cli_table':
        table = PrettyTable()

        table.field_names = [
            'Name',
            'Desired Count',
            'Running Count',
            'Min Uptime',
            'Max Uptime',
            'Avg Uptime',
            'Last Updated',
        ]

        table.align['Name'] = 'l'
        table.align['Desired Count'] = 'c'
        table.align['Running Count'] = 'c'
        table.align['Min Uptime'] = 'c'
        table.align['Max Uptime'] = 'c'
        table.align['Avg Uptime'] = 'c'
        table.align['Last Updated'] = 'c'

        for service in services:
            table.add_row(
                [
                    service['service'],
                    service['min_uptime'],
                    service['max_uptime'],
                    service['avg_uptime'],
                    service['desired_count'],
                    service['running_count'],
                    service['updated_at'],
                ]
            )

        print(table)

    # IF OUTPUT TYPE IS HTML
    elif output_type == 'html_table':

        trace = go.graph_objs.Table(
            columnwidth=[
                10,
                100,
                20,
                20,
                60,
                60,
                80,
                100,
            ],
            header=dict(
                values=[
                    '#',
                    'Name',
                    'Desired Count',
                    'Running Count',
                    'Min Uptime',
                    'Max Uptime',
                    'Avg Uptime',
                    'Last Updated',
                ],
                fill=dict(
                    color='#a1c3d1'
                )
            ),
            cells=dict(
                values=[
                    [idx for idx, service in enumerate(services)],
                    [service['service'] for service in services],
                    [service['desired_count'] for service in services],
                    [service['running_count'] for service in services],
                    [service['min_uptime'] for service in services],
                    [service['max_uptime'] for service in services],
                    [service['avg_uptime'] for service in services],
                    [service['updated_at'] for service in services],
                ],
                fill=dict(
                    color=[
                        '#F5F4F4',
                        '#F5F4F4',
                        [
                            '#FFFF00' if service['desired_count'] == 0
                            else '#24F015' for service in services
                        ],
                        [
                            '#24F015' if service['desired_count'] == service['running_count']
                            else '#DA100C' for service in services
                        ],
                        '#F5F4F4',
                        '#F5F4F4',
                        '#F5F4F4',
                        '#F5F4F4',
                    ]
                ),
                align=[
                    'center',
                    'left',
                    'center',
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
        plot(
            data,
            filename=app.config.get_section_dict('output')['path']
        )

    else:
        app.log.error('OUTPUT: No valid output type selected')
        app.close(1)
    return


def history_table(app, services, output_type):

    # IF OUTPUT TYPE IS CLI
    if output_type == 'cli_table':
        table = PrettyTable()

        table.field_names = [
            'Name',
            'Created',
            'Last Updated',
            'History',
        ]

        table.align['Name'] = 'l'
        table.align['Created'] = 'c'
        table.align['Last Updated'] = 'c'
        table.align['History'] = 'c'

        for service in services:
            table.add_row(
                [
                    service['service'],
                    service['created_at'],
                    service['updated_at'],
                    service['history'],
                ]
            )

        print(table)

    # IF OUTPUT TYPE IS HTML
    elif output_type == 'html_table':

        trace = go.graph_objs.Table(
            columnwidth=[
                10,
                100,
                40,
                40,
                100,
            ],
            header=dict(
                values=[
                    '#',
                    'Name',
                    'Created',
                    'Last Updated',
                    'History',
                ],
                fill=dict(
                    color='#a1c3d1'
                )
            ),
            cells=dict(
                values=[
                    [idx for idx, service in enumerate(services)],
                    [service['service'] for service in services],
                    [service['created_at'] for service in services],
                    [service['updated_at'] for service in services],
                    [service['history'] for service in services],
                ],
                fill=dict(
                    color=[
                        '#F5F4F4',
                        '#F5F4F4',
                        '#F5F4F4',
                        '#F5F4F4',
                        '#F5F4F4',
                    ]
                ),
                align=[
                    'center',
                    'left',
                    'center',
                    'center',
                    'center',
                ]
            )
        )

        data = [trace]

        # OUTPUT TABLE TO HTML FILE
        plot(
            data,
            filename=app.config.get_section_dict('output')['path']
        )

    else:
        app.log.error('OUTPUT: No valid output type selected')
        app.close(1)
    return


def list_table(app, services, output_type):
    if output_type == 'cli_table':

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
                service['service'],
                service['version'],
                service['desired_count'],
                service['running_count'],
                service['cluster'],
            ])

        # PRINT TABLE
        print(table)

    elif output_type == 'html_table':

        # DESCRIBE TABLE
        trace = go.graph_objs.Table(

            # DESCRIBE TABLE HEADERS
            columnwidth=[
                10,
                100,
                100,
                20,
                20,
                60,
                60,
                80,
                80,
                30,
                30
            ],
            header=dict(
                values=[
                    '#',
                    'Name',
                    'Version',
                    'Desired Count',
                    'Running Count',
                    'Min Uptime',
                    'Max Uptime',
                    'Avg Uptime',
                    'Cluster',
                    'Region',
                    'Launch Type'
                ],
                fill=dict(
                    color='#a1c3d1'
                )
            ),
            # DESCRIBE TABLE CONTENTS
            cells=dict(
                values=[
                    [idx for idx, service in enumerate(services)],
                    [service['service'] for service in services],
                    [service['version'] for service in services],
                    [service['desired_count'] for service in services],
                    [service['running_count'] for service in services],
                    [service['min_uptime'] for service in services],
                    [service['max_uptime'] for service in services],
                    [service['avg_uptime'] for service in services],
                    [service['cluster'] for service in services],
                    [service['region'] for service in services],
                    [service['launch_type'] for service in services]
                ],
                fill=dict(
                    color=[
                        '#F5F4F4',
                        '#F5F4F4',
                        '#F5F4F4',
                        [
                            '#FFFF00' if service['desired_count'] == 0 \
                            else '#24F015' for service in services
                        ],
                        [
                            '#24F015' if service['desired_count'] == service['running_count'] \
                            else '#DA100C' for service in services
                        ],
                        '#F5F4F4',
                        '#F5F4F4',
                        '#F5F4F4',
                        '#F5F4F4',
                        '#F5F4F4',
                        '#F5F4F4'
                    ]
                ),
                align=[
                    'center',
                    'left',
                    'center',
                    'center',
                    'center',
                    'center',
                    'center',
                    'center',
                    'center',
                    'center',
                    'center'
                ]
            )
        )

        data = [trace]

        # OUTPUT TABLE TO HTML FILE
        plot(
            data,
            filename=app.config.get_section_dict('output')['path']
        )

    elif output_type == 'json':
        print(json.dumps(services))

    else:
        app.log.error('OUTPUT: No valid output type selected')
        app.close(1)
    return
