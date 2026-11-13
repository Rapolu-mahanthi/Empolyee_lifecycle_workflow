# Employee Lifecycle Workflow Orchestration

A Python-based synthetic-data and business-rules project for coordinating employee pre-boarding, access provisioning, equipment delivery, offboarding, audit events and exception handling across HR, IT and Facilities.

## Quick start

Requirements: Python 3.10+ (the generator uses only the Python standard library).

```bash
python generator.py --out data --scale 1.0 --seed 20261022
python validate.py --data data
python -m unittest discover -s tests -v
```

Use `--scale 0.1` for a smaller starter dataset. The full scale creates 1,000 employees, 8,000 tasks, 1,500 access grants and 1,200 assets. The fixed seed makes runs reproducible.

## What it generates

CSV and JSON outputs for departments, roles, managers, employees, onboarding cases, tasks, task dependencies, access roles, access grants, assets, offboarding cases, audit events and a separate `ground_truth` label file. A source manifest and validation summary are also written.

## Business rules and exception scenarios

- Create master records before dependent records; use stable, zero-padded IDs.
- Generate onboarding tasks with prerequisite links.
- Baseline access requires approval and a grant date on or after the employee start date.
- Termination creates an offboarding case and access-revocation action.
- Track equipment allocation and recovery state.
- Inject and label five test anomalies: premature/unapproved access, duplicate asset assignment, terminated employee retaining access, task dependency cycle and recovered asset still assigned.
- Keep ground-truth labels separate from operational input data.

## Project structure

- `generator.py` — deterministic synthetic data generation and validation helpers.
- `validate.py` — command-line integrity checks.
- `schema.sql` — SQLite relational schema.
- `DATA_DICTIONARY.md` — fields, keys and relationship documentation.
- `tests/` — automated starter tests.

## Scope and responsible use

All generated people and email addresses are fictional. This project does not connect to real HR, identity, procurement or endpoint systems. Production use would require authentication, authorization, secure integrations, privacy review, transactional storage and stronger lifecycle controls. Ground-truth labels are for evaluation only and must not be used as model input features.
