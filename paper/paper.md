---

title: "CloudArchSecBench: A rule-based framework for evaluating structured AWS cloud architectures"
tags:

* Python
* AWS
* cloud security
* cloud architecture
* benchmarking
* large language models
  authors:
* name: Sanjeev Kumar Bharadwaj
  affiliation: 1
  affiliations:
* name: Independent Researcher, Guwahati, Assam, India
  index: 1
  date: 15 July 2026
  bibliography: paper.bib

---

# Summary

Cloud architecture design requires engineers to reason simultaneously about security, network exposure, availability, operational visibility, reliability, and cost. These properties are often assessed through expert review, cloud-provider guidance, deployment-specific policy tools, or analysis of Infrastructure as Code. Such approaches are valuable, but they are not always suitable for controlled experiments in which proposed architectures are generated as high-level designs rather than deployable templates.

`CloudArchSecBench` is an open-source Python framework for representing and evaluating structured Amazon Web Services (AWS) cloud architectures. It accepts a concise JSON representation of cloud resources and applies transparent rules to identify architectural concerns such as publicly exposed databases, unencrypted storage, missing backups, insufficient monitoring, and unsuitable subnet placement. It returns an overall score, category-level scores, structured findings, and remediation suggestions.

The software includes a FastAPI interface, a command-line benchmark runner, machine-readable reports, a resource-capability catalogue, and a versioned collection of ten workload scenarios. A standardized prompt template permits architectures produced by large language models or other generation methods to be compared through the same representation and evaluation process.

# Statement of need

Large language models are increasingly capable of producing cloud architecture recommendations from natural-language requirements. Researchers who study these systems need repeatable methods for determining whether generated designs express basic security and reliability controls. Manual expert evaluation is useful but can be expensive, slow, and difficult to reproduce across models or repeated experiments.

Existing Infrastructure-as-Code analysis tools operate primarily on deployable Terraform, CloudFormation, Kubernetes, or similar configuration files. Research has demonstrated the importance of static analysis for detecting defects in Infrastructure as Code [@chiari2022static], while empirical studies have found inconsistent adoption of security practices in public infrastructure repositories [@verdet2023security]. However, early-stage architecture proposals and LLM outputs may not yet be expressed as deployable code.

`CloudArchSecBench` addresses this narrower research need by defining an intermediate, architecture-level JSON representation. It enables researchers to conduct controlled evaluations before requiring a model to generate provider-specific deployment code. Its intended users include researchers studying AI-assisted cloud engineering, educators teaching secure architecture principles, and practitioners performing preliminary review of structured architecture proposals.

The framework is not intended to replace the AWS Well-Architected review process, policy-as-code tooling, threat modelling, or expert assessment. Instead, it provides a reproducible baseline that can be incorporated into larger empirical studies.

# State of the field

AWS Well-Architected provides a structured approach to evaluating workloads across operational excellence, security, reliability, performance efficiency, cost optimization, and sustainability [@awswellarchitected]. Its guidance informs many architecture-review practices, but it is designed as a comprehensive review framework rather than a lightweight executable benchmark.

Tools such as `cfn-lint` validate AWS CloudFormation templates using extensible rules [@cfnlint]. Checkov scans several Infrastructure-as-Code formats for security and configuration problems [@checkov], while Cloud Custodian applies policy rules to cloud resources and infrastructure configurations [@cloudcustodian]. These tools are appropriate when concrete templates or deployed resources exist.

`CloudArchSecBench` differs by operating on an intentionally simplified architecture representation. It does not attempt to reproduce the coverage of mature Infrastructure-as-Code scanners. Its contribution is a compact benchmark-oriented layer between natural-language architecture generation and deployable configuration. This permits the same architecture schema and scoring interface to be used for outputs from different LLMs, human baselines, or architecture-generation systems.

Building a separate framework rather than extending an Infrastructure-as-Code scanner was necessary because the evaluated input lacks the complete provider properties expected by those scanners. The simplified representation also makes assumptions explicit and allows researchers to inspect exactly which declared properties produced each finding.

# Software design

The software separates data representation, resource applicability, evaluation rules, orchestration, and interfaces.

Pydantic models validate the top-level architecture and resource fields. Individual rules implement independent checks and return structured findings containing a rule name, category, severity, penalty, affected resource, explanatory message, and remediation suggestion. The evaluator executes the registered rules, aggregates penalties, calculates category scores, and enforces a lower bound of zero.

An explicit resource-capability catalogue determines whether properties such as backup, encryption, logging, monitoring, or IAM-role use are meaningful for a given AWS service. This design followed pilot evaluation, during which a universal backup rule incorrectly penalized resources such as ACM certificates and CloudFront distributions. Resource-aware applicability prevents such properties from being treated as universally meaningful.

The same pilot also identified that an isolated database subnet should not be penalized for failing to use a private subnet. The finalized networking rule therefore recognizes both private and isolated database placement as acceptable. These refinements illustrate the benefit of transparent rules: assumptions can be inspected, tested, revised, and versioned.

The JSON schema trades deployment-level completeness for experimental consistency. It records architecture properties relevant to the initial benchmark without attempting to represent every AWS configuration option. This makes model outputs easier to constrain and compare but means that positive declarations, such as `"encrypted": true`, are not independently verified against deployed infrastructure.

The FastAPI interface supports interactive and programmatic evaluation. The command-line runner evaluates directories of architecture files without requiring an HTTP server and exports both detailed JSON and tabular CSV reports. Invalid JSON files are skipped with a warning so that a malformed experiment output does not terminate an entire benchmark run.

# Research impact statement

The initial release provides a complete reproducible workflow comprising ten AWS scenarios, a standardized generation prompt, a structured architecture schema, ten evaluation rules, automated tests, a command-line runner, and JSON and CSV reporting. The software has been exercised end to end on ten generated architecture outputs, demonstrating that the benchmark scenarios can be converted into structured model outputs and processed automatically.

Its near-term scholarly use is as an experimental instrument for comparing cloud architecture generation methods. A researcher can retain the scenarios and prompt, vary the source model, record version and generation settings, evaluate all outputs with one command, and compare category-level findings. Because the rules and resource catalogue are public, studies can report the exact evaluator version used and audit the basis for each score.

The framework also creates reusable materials for teaching and controlled experimentation. Future releases can add topology-aware checks, scenario-specific requirements, broader test coverage, and additional cloud providers without changing the core evaluation interface.

# Limitations

`CloudArchSecBench` currently supports AWS-oriented resources and a small benchmark. It evaluates declared architecture properties and does not confirm that a deployment implements those properties correctly. The scoring weights are explicit engineering choices rather than empirically calibrated risk estimates. The initial cost category is included in the report structure but is not yet populated by cost-analysis rules.

The framework should therefore be interpreted as a transparent baseline, not as a security certification, compliance decision, or substitute for expert architectural review.

# AI usage disclosure

Generative AI was used substantially during the initial development of `CloudArchSecBench`. It assisted with software scaffolding, rule and schema drafts, benchmark-scenario drafting, documentation, and preparation of this manuscript. The author directed the development process, executed the software locally, inspected generated outputs and evaluator findings, identified and corrected rule-applicability errors, and reviewed the final text.

Correctness was assessed through manual end-to-end execution and automated tests covering secure architecture scoring, public database detection, missing encryption, missing database backups, and acceptance of isolated database subnets. AI-generated suggestions were not treated as authoritative cloud guidance; they were reviewed and modified when pilot results exposed incorrect assumptions.

# Acknowledgements

The author acknowledges the maintainers of the open-source Python, FastAPI, Pydantic, pytest, and broader cloud-security ecosystems on which this project depends.

# References
