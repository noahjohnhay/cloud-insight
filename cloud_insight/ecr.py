#!/usr/bin/python


# DESCRIBE REPOSITORIES
def describe_repositories(client):
    paginator = client.get_paginator('describe_repositories')
    page_iterator = paginator.paginate()
    repositories = []
    for page in page_iterator:
        repositories.extend(page['repositories'])
    return repositories


# LIST IMAGES
def list_images(client, repository):
    paginator = client.get_paginator('list_images')
    page_iterator = paginator.paginate(
        repositoryName=repository
    )
    images = []
    for page in page_iterator:
        images.extend(page)
    return images
