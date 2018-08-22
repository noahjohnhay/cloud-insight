# CLOUD-INSIGHT
This is a project designed to simplify the tracking of docker container versions, health and other important information across various platforms.

## Running

#### CLI

[PyPI](https://pypi.org/project/cloud-insight/ "PyPI")

```
pip install cloud-inisight
```

```
cloud-insight --help
cloud-insight list --config "path/to/config.json"
```

#### DOCKER
![alt text](https://img.shields.io/docker/pulls/noahjohnhay/cloud-insight.svg "Docker Pulls")
![alt text](https://img.shields.io/docker/stars/noahjohnhay/cloud-insight.svg "Docker Stars")

[Docker Hub](https://hub.docker.com/r/noahjohnhay/cloud-insight/ "Docker Hub")

```
docker run  \
-v absolute/path/to/.aws:/root/.aws:ro \
-v .:/project \
cloud-insight:1.0.0 list \
-config "/project/relative/path/to/config"
```

### Commands

##### List
Builds an array of dictionaries consisting of various important pieces of information such as;
* Service Name
* Version
* Desired Count
* Actual Count
* Cluster Name
* Cluster Type

## Configuration

### AWS

ECS integration

##### Enabled

Whether or not to enable AWS Integration.
```
"enabled": true
```

##### Region

JSON formatted region configuration, if none is provided all clusters in all regions will be scanned.

*Ex: Will search cluster example-1 & example-2 in us-east-1 as well as all clusters in eu-west-1*

```
"regions": {
  "us-east-1": {
    "clusters": ["example-1", "example-1"]
  },
  "eu-west-1": {
  }
}
```

##### Auth

```
"auth": {
  "type": "profile",
  "profile names": [
    "profile_name_1",
    "profile_name_2"
  ]
}
```

### Consul

Consul is not currently functional

### Output

###### Enabled
Whether or not to enable an output

```
enabled: true
```

##### HTML Table
An HTML formatted table using Plotly
```
type: "html_table"
```

![Alt text](examples/html_table.png?raw=true "Basic Table")

##### CLI Table
A CLI Table using PrettyTable

```
type: "cli_table"
```
##### Example

```
"output": {
  "enabled": true,
  "type": "html_table"
}
```

##### Filters
Filtering the results

```
"filters": {
      "cluster": [
        "example"
      ]
    }
```

## Examples

```
{
  "aws": {
    "enabled": true,
    "regions": {
      "us-east-1": {
        "clusters": []
       }
    },
    "auth": {
      "type": "profile",
      "profile names": [
        "profile_name_1",
        "profile_name_2"
      ]
    }
  },
  "consul": {
    "enabled": false,
    "type": "acl",
    "token": ""
  },
  "logging": {
    "level": "INFO",
    "path": "temp.log"
  },
  "output": {
    "enabled": true,
    "type": "table"
  }
}

```