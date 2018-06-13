# NEEDS A NEW NAME

## Installation

```
pip install python-consul boto3 plotly
```

## Links

https://python-consul.readthedocs.io/en/latest/#id1


## Configuration

### AWS

**Enabled** *required*

Enable AWS integration
```
"enabled": true
```

**Regions** *optional*

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

**Auth** *optional*

```
"auth": {
  "type": "profile",
  "profile names": [
    "profile_name_1",
    "profile_name_2"
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
  }
}

```