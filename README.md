# NEEDS A NEW NAME

## Installation

```
pip install python-consul boto3
```

## Links

https://python-consul.readthedocs.io/en/latest/#id1

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