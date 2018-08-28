#!/usr/bin/python

import docker

docker_client = docker.from_env()


# CREATE DOCKER CLIENT
def login(app, credentials):
    app.log.info('Logging Into Docker')
    docker_client.login(
        username=credentials[0],
        password=credentials[1],
        registry=credentials[2],
        dockercfg_path='.docker.config')
    return


# PULL DOCKER IMAGE
def pull_image(app, ecr_image_tag, ecr_repository_name):
    app.log.info('Pulling Image')
    docker_client.images.pull(
        repository=ecr_repository_name,
        tag=ecr_image_tag
    )
    return


# TAG DOCKER IMAGE
def tag_image(ecr_image_tag):
    if 'snapshot' in ecr_image_tag:
        final_ecr_image_tag = 'snapshot__{}'.format(ecr_image_tag)
    else:
        final_ecr_image_tag = 'release__{}'.format(ecr_image_tag)
    docker_client.tag(
        tag=final_ecr_image_tag
    )
    return final_ecr_image_tag


# PUSH DOCKER IMAGE
def push_image(app, ecr_image_tag, ecr_repository_name):
    app.log.info('Pushing Image')
    docker_client.images.push(
        repository=ecr_repository_name,
        tag=ecr_image_tag
    )
    return
