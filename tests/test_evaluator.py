from app.models.schema import Architecture
from app.services.evaluator import evaluate


def test_secure_architecture_scores_100():
    architecture = Architecture(
        provider="AWS",
        resources=[
            {
                "id": "db-1",
                "name": "secure-database",
                "type": "RDS",
                "public": False,
                "subnet": "isolated",
                "encrypted": True,
                "backup_enabled": True,
                "availability_zones": 2,
                "has_logging": True,
                "has_monitoring": True,
                "uses_iam_role": True,
                "connections": [],
            }
        ],
    )

    result = evaluate(architecture)

    assert result["score"] == 100
    assert result["issue_count"] == 0


def test_public_database_is_detected():
    architecture = Architecture(
        provider="AWS",
        resources=[
            {
                "id": "db-1",
                "name": "public-database",
                "type": "RDS",
                "public": True,
                "subnet": "public",
                "encrypted": True,
                "backup_enabled": True,
                "availability_zones": 2,
                "has_logging": True,
                "has_monitoring": True,
                "uses_iam_role": True,
                "connections": [],
            }
        ],
    )

    result = evaluate(architecture)

    rules = [issue["rule"] for issue in result["issues"]]

    assert "Public Database" in rules


def test_missing_encryption_is_detected():
    architecture = Architecture(
        provider="AWS",
        resources=[
            {
                "id": "bucket-1",
                "name": "unencrypted-bucket",
                "type": "S3",
                "public": False,
                "encrypted": False,
                "has_logging": True,
                "has_monitoring": True,
                "uses_iam_role": True,
                "connections": [],
            }
        ],
    )

    result = evaluate(architecture)

    rules = [issue["rule"] for issue in result["issues"]]

    assert "Missing Encryption" in rules


def test_missing_backup_is_detected_for_rds():
    architecture = Architecture(
        provider="AWS",
        resources=[
            {
                "id": "db-1",
                "name": "database",
                "type": "RDS",
                "public": False,
                "subnet": "private",
                "encrypted": True,
                "backup_enabled": False,
                "availability_zones": 2,
                "has_logging": True,
                "has_monitoring": True,
                "uses_iam_role": True,
                "connections": [],
            }
        ],
    )

    result = evaluate(architecture)

    rules = [issue["rule"] for issue in result["issues"]]

    assert "Missing Backups" in rules


def test_isolated_database_is_valid():
    architecture = Architecture(
        provider="AWS",
        resources=[
            {
                "id": "db-1",
                "name": "isolated-database",
                "type": "RDS",
                "public": False,
                "subnet": "isolated",
                "encrypted": True,
                "backup_enabled": True,
                "availability_zones": 2,
                "has_logging": True,
                "has_monitoring": True,
                "uses_iam_role": True,
                "connections": [],
            }
        ],
    )

    result = evaluate(architecture)

    rules = [issue["rule"] for issue in result["issues"]]

    assert "Database Not In Private Subnet" not in rules