RESOURCE_CAPABILITIES = {
    "rds": {
        "supports_backup": True,
        "supports_encryption": True,
        "supports_logging": True,
        "supports_monitoring": True,
        "supports_iam_role": True,
    },
    "s3": {
        "supports_backup": False,
        "supports_encryption": True,
        "supports_logging": True,
        "supports_monitoring": True,
        "supports_iam_role": True,
    },
    "ec2": {
        "supports_backup": True,
        "supports_encryption": True,
        "supports_logging": True,
        "supports_monitoring": True,
        "supports_iam_role": True,
    },
    "lambda": {
        "supports_backup": False,
        "supports_encryption": True,
        "supports_logging": True,
        "supports_monitoring": True,
        "supports_iam_role": True,
    },
    "cloudfront": {
        "supports_backup": False,
        "supports_encryption": False,
        "supports_logging": True,
        "supports_monitoring": True,
        "supports_iam_role": False,
    },
    "route53": {
        "supports_backup": False,
        "supports_encryption": False,
        "supports_logging": False,
        "supports_monitoring": True,
        "supports_iam_role": False,
    },
    "acm": {
        "supports_backup": False,
        "supports_encryption": False,
        "supports_logging": False,
        "supports_monitoring": False,
        "supports_iam_role": False,
    },
    "alb": {
        "supports_backup": False,
        "supports_encryption": False,
        "supports_logging": True,
        "supports_monitoring": True,
        "supports_iam_role": False,
    },
    "api gateway": {
        "supports_backup": False,
        "supports_encryption": False,
        "supports_logging": True,
        "supports_monitoring": True,
        "supports_iam_role": False,
    },
    "waf": {
        "supports_backup": False,
        "supports_encryption": False,
        "supports_logging": True,
        "supports_monitoring": True,
        "supports_iam_role": False,
    },
    "eks": {
        "supports_backup": True,
        "supports_encryption": True,
        "supports_logging": True,
        "supports_monitoring": True,
        "supports_iam_role": True,
    },
}


def get_capability(resource_type: str, capability: str) -> bool:
    resource_type = resource_type.lower().strip()
    return RESOURCE_CAPABILITIES.get(resource_type, {}).get(capability, False)