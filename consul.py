#!/usr/bin/python3

import consul
import logging

# INITIATE CONSUL CONNECTION
consul = consul.Consul(
            host='127.0.0.1',
            port=8500,
            token=None,
            scheme='http',
            consistency='default',
            dc=None,
            verify=True,
            cert=None
)


# FETCH A CONSUL SERVICE
def consul_get_service():
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
