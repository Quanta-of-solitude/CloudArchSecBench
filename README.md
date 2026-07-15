# CloudArchSecBench

CloudArchSecBench is an open-source Python framework for evaluating structured AWS cloud architectures using transparent, extensible, rule-based analysis.

The project accepts architecture descriptions in a machine-readable JSON format and evaluates them across security, networking, availability, and reliability dimensions. It includes a FastAPI interface, a command-line benchmark runner, example architectures, and a versioned collection of AWS workload scenarios.

CloudArchSecBench is intended for:

* researchers evaluating AI-generated cloud architectures;
* cloud engineering and DevSecOps education;
* reproducible architecture-quality experiments;
* early-stage review of structured AWS architecture proposals.

> CloudArchSecBench provides an automated baseline. It does not replace professional security review, threat modelling, compliance assessment, or AWS architecture review.

## Current status

CloudArchSecBench is an alpha-stage research software project.

Version `0.1.0` currently provides:

* AWS architecture evaluation;
* a documented JSON representation;
* ten benchmark scenarios;
* ten transparent evaluation rules;
* resource-aware rule applicability;
* category and overall scores;
* JSON and CSV report generation;
* a FastAPI interface;
* automated tests.

## Evaluation categories

The current evaluator reports scores for:

* Security
* Networking
* Availability
* Reliability
* Cost

The cost category is reserved for future cost-analysis rules and currently remains unchanged by the initial rule set.

## Installation

CloudArchSecBench requires Python 3.10 or newer.

Clone the repository:

```bash
git clone https://github.com/Quanta-of-solitude/CloudArchSecBench.git
cd CloudArchSecBench
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Install the package and development dependencies:

```bash
pip install -e ".[dev]"
```

## Verify the installation

Run the automated tests:

```bash
pytest -v
```

A successful installation should report five passing tests.

## Quick start

The following architecture places an encrypted, monitored, backed-up RDS database in an isolated subnet:

```json
{
  "provider": "AWS",
  "resources": [
    {
      "id": "database-1",
      "name": "application-database",
      "type": "RDS",
      "public": false,
      "subnet": "isolated",
      "encrypted": true,
      "backup_enabled": true,
      "availability_zones": 2,
      "has_logging": true,
      "has_monitoring": true,
      "uses_iam_role": true,
      "has_waf": false,
      "connections": []
    }
  ]
}
```

Architecture examples are available under:

```text
examples/architectures/
```

## Run a benchmark from the command line

Evaluate every JSON architecture in the example directory:

```bash
python scripts/run_benchmark.py \
  --input examples/architectures \
  --output reports/example_report \
  --model example
```

The command produces:

```text
reports/example_report.json
reports/example_report.csv
```

Example terminal output:

```text
✓ aws_001_output                 Score: 100

--------------------------------
Average Score : 100.00
JSON Report   : reports/example_report.json
CSV Report    : reports/example_report.csv
```

The `--model` value is recorded as experiment metadata. It may identify an LLM, a human-designed baseline, or another architecture-generation process.

## Run the API

Start the FastAPI service from the repository root:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive OpenAPI documentation:

```text
http://127.0.0.1:8000/docs
```

Available endpoints include:

| Endpoint    | Method | Purpose                      |
| ----------- | ------ | ---------------------------- |
| `/`         | GET    | Service status               |
| `/rules`    | GET    | List active evaluation rules |
| `/evaluate` | POST   | Evaluate an architecture     |

Example API request:

```bash
curl -X POST http://127.0.0.1:8000/evaluate \
  -H "Content-Type: application/json" \
  --data @examples/architectures/aws_001_output.json
```

## Architecture schema

An architecture contains a provider and a list of resources:

```json
{
  "provider": "AWS",
  "resources": []
}
```

Supported resource properties include:

| Property             | Type    | Description                                |
| -------------------- | ------- | ------------------------------------------ |
| `id`                 | string  | Unique resource identifier                 |
| `name`               | string  | Human-readable name                        |
| `type`               | string  | AWS resource or service type               |
| `public`             | boolean | Whether the resource is publicly reachable |
| `subnet`             | string  | `public`, `private`, `isolated`, or `none` |
| `encrypted`          | boolean | Whether encryption at rest is enabled      |
| `backup_enabled`     | boolean | Whether backups or snapshots are enabled   |
| `availability_zones` | integer | Number of Availability Zones used          |
| `has_logging`        | boolean | Whether logging is enabled                 |
| `has_monitoring`     | boolean | Whether monitoring is enabled              |
| `uses_iam_role`      | boolean | Whether IAM roles are used                 |
| `has_waf`            | boolean | Whether WAF protection is represented      |
| `connections`        | array   | Identifiers of connected resources         |

The schema intentionally represents architecture-level properties rather than complete deployable AWS configuration.

## Included evaluation rules

Version `0.1.0` includes checks for:

1. Public database exposure
2. Public object storage
3. Missing encryption
4. Missing backups on backup-capable resources
5. Single-Availability-Zone deployment
6. Missing logging
7. Missing monitoring
8. Missing IAM-role usage
9. Public compute without a load balancer
10. Database placement outside private or isolated subnets

Rules are implemented independently and can be extended under:

```text
backend/app/rules/
```

Resource-specific rule applicability is defined in:

```text
backend/app/models/resource_catalog.py
```

## Benchmark scenarios

The initial benchmark contains ten AWS scenarios:

1. Static company website
2. Small REST API
3. WordPress blog
4. E-commerce platform
5. Kubernetes SaaS application
6. Online banking platform
7. Hospital management system
8. Video-streaming platform
9. Event-driven order processing
10. Machine-learning inference API

Scenario definitions are stored under:

```text
benchmark/scenarios/v0.1/
```

The standardized generation prompt is stored in:

```text
benchmark/prompt_template.md
```

## Project structure

```text
CloudArchSecBench/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── rules/
│   │   └── services/
│   └── main.py
├── benchmark/
│   ├── scenarios/
│   ├── benchmark_manifest.json
│   └── prompt_template.md
├── examples/
│   └── architectures/
├── paper/
├── scripts/
│   └── run_benchmark.py
├── tests/
│   └── test_evaluator.py
├── CITATION.cff
├── LICENSE
├── README.md
└── pyproject.toml
```

## Limitations

The initial version:

* supports AWS only;
* evaluates declared JSON properties rather than deployed infrastructure;
* does not prove that declared controls are correctly implemented;
* includes a deliberately small rule set;
* has limited topology analysis;
* does not yet perform quantitative cost estimation;
* should not be used as a compliance-certification tool.

## Development

Run tests before submitting changes:

```bash
pytest -v
```

New rules should:

1. inherit from the base rule abstraction;
2. state their category, severity, and penalty;
3. return structured findings;
4. apply only to relevant resource types;
5. include unit tests for both compliant and non-compliant cases.

## Contributing

Issues and pull requests are welcome. Proposed rules should include a clear technical justification, expected compliant and non-compliant examples, and supporting tests.

See `CONTRIBUTING.md` for contribution guidance once available.

## License

CloudArchSecBench is distributed under the MIT License. See `LICENSE`.

## Citation

Citation metadata are provided in `CITATION.cff`.

Until an archived release DOI is available, cite the software as:

> Bharadwaj, S. K. (2026). CloudArchSecBench (Version 0.1.0) [Computer software].

## AI usage

Generative AI assisted with portions of the initial software scaffolding, benchmark drafting, documentation, and manuscript preparation. The author reviewed the resulting code, manually executed the benchmark pipeline, inspected evaluator findings, corrected identified rule errors, and verified the current implementation using automated tests.
