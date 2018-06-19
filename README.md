# NEEDS A NEW NAME
This is a project designed to simplify the tracking of docker container versions, health and other important information across various platforms.

## Installation

```
pip install python-consul boto3 plotly
```

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

```
"output": {
  "enabled": true,
  "type": "table"
}
```

![Alt text](examples/basic_table.png?raw=true "Basic Table")

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