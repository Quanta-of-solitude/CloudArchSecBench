from app.rules.base import Rule
from app.models.resource_catalog import get_capability


class MissingBackupRule(Rule):
    name = "Missing Backups"
    category = "reliability"
    severity = "warning"
    penalty = 10

    def evaluate(self, architecture):
        issues = []

        for resource in architecture.resources:
            if not get_capability(resource.type, "supports_backup"):
                continue

            if resource.backup_enabled is False:
                issues.append({
                    "rule": self.name,
                    "severity": self.severity,
                    "category": self.category,
                    "resource": resource.name,
                    "penalty": self.penalty,
                    "message": "Backups are not enabled",
                    "suggestion": "Enable automated backups or snapshots."
                })

        return issues


class SingleAvailabilityZoneRule(Rule):
    name = "Single Availability Zone"
    category = "availability"
    severity = "warning"
    penalty = 10

    def evaluate(self, architecture):
        issues = []

        for resource in architecture.resources:
            if resource.availability_zones == 1:
                issues.append({
                    "rule": self.name,
                    "severity": self.severity,
                    "category": self.category,
                    "resource": resource.name,
                    "penalty": self.penalty,
                    "message": "Single Availability Zone deployment",
                    "suggestion": "Use at least two Availability Zones for production workloads."
                })

        return issues