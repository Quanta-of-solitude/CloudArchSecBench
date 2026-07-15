from app.rules.base import Rule


class PublicComputeWithoutLoadBalancerRule(Rule):
    name = "Public Compute Without Load Balancer"
    category = "networking"
    severity = "warning"
    penalty = 10

    def evaluate(self, architecture):
        issues = []

        has_load_balancer = any(
            resource.type.lower() in ["alb", "elb", "load_balancer", "loadbalancer"]
            for resource in architecture.resources
        )

        for resource in architecture.resources:
            rtype = resource.type.lower()

            if rtype in ["ec2", "vm", "compute", "server"] and resource.public and not has_load_balancer:
                issues.append({
                    "rule": self.name,
                    "severity": self.severity,
                    "category": self.category,
                    "resource": resource.name,
                    "penalty": self.penalty,
                    "message": "Public compute resource without load balancer detected",
                    "suggestion": "Place compute resources behind a load balancer and restrict direct public access."
                })

        return issues


class DatabaseNotInPrivateSubnetRule(Rule):
    name = "Database Not In Private Subnet"
    category = "networking"
    severity = "error"
    penalty = 15
    PRIVATE_SUBNET_VALUES = {
    "private",
    "private subnet",
    "private-subnet",
    "isolated",
}
    def evaluate(self, architecture):
        issues = []

        for resource in architecture.resources:
            rtype = resource.type.lower()

            if rtype in ["rds", "database", "postgres", "mysql"] and resource.subnet not in self.PRIVATE_SUBNET_VALUES:
                issues.append({
                    "rule": self.name,
                    "severity": self.severity,
                    "category": self.category,
                    "resource": resource.name,
                    "penalty": self.penalty,
                    "message": "Database is not placed in a private subnet",
                    "suggestion": "Place database resources inside private subnets."
                })

        return issues