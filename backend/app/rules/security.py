from app.rules.base import Rule
from app.models.resource_catalog import get_capability


class PublicDatabaseRule(Rule):
    name = "Public Database"
    category = "security"
    severity = "error"
    penalty = 20

    def evaluate(self, architecture):
        issues = []

        for resource in architecture.resources:
            rtype = resource.type.lower()

            if rtype in ["rds", "database", "postgres", "mysql"] and resource.public:
                issues.append({
                    "rule": self.name,
                    "severity": self.severity,
                    "category": self.category,
                    "resource": resource.name,
                    "penalty": self.penalty,
                    "message": "Public database detected",
                    "suggestion": "Move the database to a private subnet."
                })

        return issues


class PublicObjectStorageRule(Rule):
    name = "Public Object Storage"
    category = "security"
    severity = "error"
    penalty = 15

    def evaluate(self, architecture):
        issues = []

        for resource in architecture.resources:
            rtype = resource.type.lower()

            if rtype in ["s3", "bucket", "object_storage"] and resource.public:
                issues.append({
                    "rule": self.name,
                    "severity": self.severity,
                    "category": self.category,
                    "resource": resource.name,
                    "penalty": self.penalty,
                    "message": "Public object storage detected",
                    "suggestion": "Restrict bucket access and use signed URLs or CDN policies."
                })

        return issues


class MissingEncryptionRule(Rule):
    name = "Missing Encryption"
    category = "security"
    severity = "warning"
    penalty = 10

    def evaluate(self, architecture):
        issues = []

        for resource in architecture.resources:
            if not get_capability(resource.type, "supports_encryption"):
                continue

            if resource.encrypted is False:
                issues.append({
                    "rule": self.name,
                    "severity": self.severity,
                    "category": self.category,
                    "resource": resource.name,
                    "penalty": self.penalty,
                    "message": "Encryption is not enabled",
                    "suggestion": "Enable encryption at rest."
                })

        return issues