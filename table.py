#!/usr/bin/python

import plotly


def basic_table(services):

    # DESCRIBE TABLE
    trace = plotly.graph_objs.Table(
        # DESCRIBE TABLE HEADERS
        header=dict(
            values=[
                'Name',
                'Version',
                'Desired Count',
                'Running Count',
                'Cluster',
                'Launch Type'
            ]
        ),
        # DESCRIBE TABLE CONTENTS
        cells=dict(
            values=[
                [service['name'] for service in services],
                [service['version'] for service in services],
                [service['desired_count'] for service in services],
                [service['running_count'] for service in services],
                [service['cluster'] for service in services],
                [service['launch_type'] for service in services]
            ]
        )
    )

    data = [trace]
    plotly.offline.plot(data, filename='basic_table.html')
    return
