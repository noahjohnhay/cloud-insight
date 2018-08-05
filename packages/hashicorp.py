#!/usr/bin/python

import consul


# INITIATE CONSUL CONNECTION
def default_client():
    client = consul.Consul(
        host='127.0.0.1',
        port=8500,
        token=None,
        scheme='http',
        consistency='default',
        dc=None,
        verify=True,
        cert=None
    )
    return client


# FETCH A CONSUL SERVICE
def consul_get_service(service):
    consul_service = consul.service(
                        service,
                        index=None,
                        wait=None,
                        tag=None,
                        consistency=None,
                        dc=None,
                        near=None,
                        token=None
    )
    return consul_service
