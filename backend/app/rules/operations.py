from app.rules.base import Rule
from app.models.resource_catalog import get_capability


class MissingLoggingRule(Rule):
    name = "Missing Logging"
    category = "reliability"
    severity = "warning"
    penalty = 8

    def evaluate(self, architecture):
        issues = []

        for resource in architecture.resources:
            if not get_capability(resource.type, "supports_logging"):
                continue

            if resource.has_logging is False:
                issues.append({
                    "rule": self.name,
                    "severity": self.severity,
                    "category": self.category,
                    "resource": resource.name,
                    "penalty": self.penalty,
                    "message": "Logging is not enabled",
                    "suggestion": "Enable service-level logging for auditability and troubleshooting."
                })

        return issues


class MissingMonitoringRule(Rule):
    name = "Missing Monitoring"
    category = "reliability"
    severity = "warning"
    penalty = 8

    def evaluate(self, architecture):
        issues = []

        for resource in architecture.resources:
            if not get_capability(resource.type, "supports_monitoring"):
                continue

            if resource.has_monitoring is False:
                issues.append({
                    "rule": self.name,
                    "severity": self.severity,
                    "category": self.category,
                    "resource": resource.name,
                    "penalty": self.penalty,
                    "message": "Monitoring is not enabled",
                    "suggestion": "Enable metrics, alerts, and health checks."
                })

        return issues


class MissingIAMRoleRule(Rule):
    name = "Missing IAM Role"
    category = "security"
    severity = "warning"
    penalty = 10

    def evaluate(self, architecture):
        issues = []

        for resource in architecture.resources:
            if not get_capability(resource.type, "supports_iam_role"):
                continue

            if resource.uses_iam_role is False:
                issues.append({
                    "rule": self.name,
                    "severity": self.severity,
                    "category": self.category,
                    "resource": resource.name,
                    "penalty": self.penalty,
                    "message": "IAM role is not used",
                    "suggestion": "Use IAM roles or managed identities instead of static credentials."
                })

        return issues