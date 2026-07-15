# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List, Optional, Any

# app = FastAPI(title="CloudArchSecBench Evaluator")


# class Resource(BaseModel):
#     name: str
#     type: str
#     public: Optional[bool] = False
#     encrypted: Optional[bool] = None
#     backup_enabled: Optional[bool] = None
#     availability_zones: Optional[int] = None


# class Architecture(BaseModel):
#     provider: str
#     resources: List[Resource]


# @app.get("/")
# def root():
#     return {"message": "CloudArchSecBench Evaluator is running"}


# @app.post("/evaluate")
# def evaluate_architecture(architecture: Architecture):
#     score = 100
#     issues = []

#     for resource in architecture.resources:
#         rtype = resource.type.lower()

#         if rtype in ["rds", "database", "postgres", "mysql"] and resource.public:
#             score -= 20
#             issues.append({
#                 "severity": "error",
#                 "category": "security",
#                 "resource": resource.name,
#                 "message": "Public database detected",
#                 "suggestion": "Move the database to a private subnet."
#             })

#         if rtype in ["s3", "bucket", "object_storage"] and resource.public:
#             score -= 15
#             issues.append({
#                 "severity": "error",
#                 "category": "security",
#                 "resource": resource.name,
#                 "message": "Public object storage detected",
#                 "suggestion": "Restrict bucket access and use signed URLs or CDN policies."
#             })

#         if resource.encrypted is False:
#             score -= 10
#             issues.append({
#                 "severity": "warning",
#                 "category": "security",
#                 "resource": resource.name,
#                 "message": "Encryption is not enabled",
#                 "suggestion": "Enable encryption at rest."
#             })

#         if resource.backup_enabled is False:
#             score -= 10
#             issues.append({
#                 "severity": "warning",
#                 "category": "reliability",
#                 "resource": resource.name,
#                 "message": "Backups are not enabled",
#                 "suggestion": "Enable automated backups."
#             })

#         if resource.availability_zones == 1:
#             score -= 10
#             issues.append({
#                 "severity": "warning",
#                 "category": "availability",
#                 "resource": resource.name,
#                 "message": "Single Availability Zone deployment",
#                 "suggestion": "Use at least two Availability Zones for production workloads."
#             })

#     score = max(score, 0)

#     return {
#         "provider": architecture.provider,
#         "score": score,
#         "issues": issues,
#         "issue_count": len(issues)
#     }

from fastapi import FastAPI
from app.models.schema import Architecture
from app.services.evaluator import evaluate
from app.services.evaluator import evaluate, list_rules

app = FastAPI(title="CloudArchSecBench Evaluator")


@app.get("/")
def root():
    return {"message": "CloudArchSecBench Evaluator is running"}


@app.post("/evaluate")
def evaluate_architecture(architecture: Architecture):
    return evaluate(architecture)

@app.get("/rules")
def get_rules():
    return list_rules()