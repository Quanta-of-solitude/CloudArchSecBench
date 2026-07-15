from app.rules.security import (
    PublicDatabaseRule,
    PublicObjectStorageRule,
    MissingEncryptionRule,
)

from app.rules.operations import (
    MissingLoggingRule,
    MissingMonitoringRule,
    MissingIAMRoleRule,
)

from app.rules.reliability import (
    MissingBackupRule,
    SingleAvailabilityZoneRule,
)


from app.rules.networking import (
    PublicComputeWithoutLoadBalancerRule,
    DatabaseNotInPrivateSubnetRule,
)

RULES = [
    PublicDatabaseRule(),
    PublicObjectStorageRule(),
    MissingEncryptionRule(),
    MissingBackupRule(),
    SingleAvailabilityZoneRule(),
    MissingLoggingRule(),
    MissingMonitoringRule(),
    MissingIAMRoleRule(),
    PublicComputeWithoutLoadBalancerRule(),
    DatabaseNotInPrivateSubnetRule(),
]

def evaluate(architecture):
    score = 100
    issues = []

    for rule in RULES:
        rule_issues = rule.evaluate(architecture)
        issues.extend(rule_issues)

    total_penalty = sum(issue["penalty"] for issue in issues)
    score = max(100 - total_penalty, 0)

    category_scores = {
        "security": 100,
        "reliability": 100,
        "availability": 100,
        "networking": 100,
        "cost": 100,
    }

    for issue in issues:
        category = issue["category"]
        penalty = issue["penalty"]

        if category in category_scores:
            category_scores[category] = max(category_scores[category] - penalty, 0)

    return {
        "provider": architecture.provider,
        "score": score,
        "category_scores": category_scores,
        "issues": issues,
        "issue_count": len(issues)
    }

def list_rules():
    return [
        {
            "name": rule.name,
            "category": rule.category,
            "severity": rule.severity,
            "penalty": rule.penalty,
        }
        for rule in RULES
    ]