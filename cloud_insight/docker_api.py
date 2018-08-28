#!/usr/bin/python

import docker


# DEFAULT CLIENT
def default_client(base_url):
    client = docker.DockerClient(
        base_url=base_url,
        version='auto',
        timeoutdoc=4,
        tls=False
    )
    return client


# LIST CONTAINERS
def list_containers(client):
    all_containers = client.containers()
    return all_containers


# PARSE DOCKER IMAGE
def parse_image(image):
    try:
        split_name = image.split('/')[1].split(':')
        result = {
            'dockerName': image,
            'parsedName': split_name[0],
            'parsedVersion': split_name[1],
        }
    except:
        result = {
            'dockerName': image,
            'parsedName': image,
            'parsedVersion': 'N/A',
        }
    return result
