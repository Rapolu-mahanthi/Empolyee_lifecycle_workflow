<!-- ✨ Employee Lifecycle Workflow | Project README -->

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:141E30,50:243B55,100:36BCF7&height=190&section=header&text=Employee%20Lifecycle%20Workflow&fontSize=32&fontColor=ffffff&animation=fadeIn&fontAlignY=38" width="100%" alt="Animated project banner" />

  <h2>👋 Welcome to the Employee Lifecycle Workflow Project!</h2>
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=19&duration=2800&pause=900&color=36BCF7&center=true&vCenter=true&width=760&lines=Automating+Employee+Lifecycle+Workflows;Pre-boarding+%7C+Access+%7C+Assets+%7C+Offboarding;Python+%7C+Synthetic+Data+%7C+Audit+%26+Validation" alt="Animated project description" />
  <br/>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/Tests-4%20passing-success?style=for-the-badge&logo=pytest&logoColor=white" alt="Four passing tests in the uploaded project build report" />
  <img src="https://img.shields.io/badge/Data-Synthetic-7B2CBF?style=for-the-badge" alt="Synthetic data only" />
</div>

---

## 🌟 Project Overview

A Python-based workflow and audit system that models the employee journey across **HR, IT, managers, and Facilities** — from pre-boarding to access provisioning, equipment delivery, and employee offboarding.

The project uses reproducible synthetic data, business rules, audit events, and validation checks to make workflow decisions and exceptions traceable. 🧩

## ✨ Key Features

- 🧑‍💼 **Pre-boarding:** Create employee and onboarding records.
- 🔐 **Access provisioning:** Track access requests, approvals, grants, and revocation.
- 💻 **Equipment management:** Model asset assignment, acknowledgement, and recovery.
- 🚪 **Offboarding:** Coordinate exit cases and urgent revoke/recovery tasks.
- 🧾 **Audit trail:** Record lifecycle events for traceability.
- 🚨 **Exception handling:** Include labelled edge cases for validation and analysis.
- 🔁 **Reproducible data:** Generate consistent synthetic datasets using a fixed seed.
- 🗃️ **Multiple formats:** Export CSV, JSON, and SQLite data.

## 📦 Download the Complete Project

The uploaded project archive includes the Python package, documentation, tests, build report, and synthetic sample datasets.

👉 **[Download / view the project ZIP](./employee_lifecycle_workflow.zip)**

## 🧪 Project Dataset

The full-scale build report records these expected entity counts:

| Entity | Records |
|---|---:|
| Employees | 1,000 |
| Onboarding cases | 1,000 |
| Tasks | 8,000 |
| Task dependencies | 7,002 |
| Access grants | 1,500 |
| Assets | 1,200 |
| Audit events | 6,051 |

Five labelled scenarios are included for evaluation: access before start, duplicate asset assignment, active access after termination, a task dependency cycle, and a recovered asset that remains assigned.

## ⚙️ Run the Project

**Requirements:** Python 3.10+

After downloading and extracting the ZIP, open a terminal inside the `employee_lifecycle_workflow` folder:

```bash
python -m venv .venv
```

**Windows**
```bash
.venv\Scripts\activate
```

**Install and run**
```bash
pip install -e ".[dev]"
python -m lifecycle.generator --scale starter --output data
python -m lifecycle.validate --data data
pytest -q
```

To generate the full dataset:

```bash
python -m lifecycle.generator --scale full --output data --seed 20261022
```

## 🧪 Testing & Validation

The uploaded build report records **4 passing automated tests**. The validator checks structural integrity, dependency cycles, active grants for terminated employees, duplicate asset assignments, and recovered assets that remain assigned.

## 🗂️ Repository Contents

- `generator.py`, `validate.py`, and `schema.sql` — original repository implementation.
- `tests/` — repository tests.
- `DATA_DICTIONARY.md` — data model reference.
- `employee_lifecycle_workflow.zip` — complete expanded Python project and sample data.

## 🔒 Responsible Use

All generated employee records are synthetic and fictional. This project does not connect to real HR, identity, procurement, or endpoint systems. Ground-truth labels are for evaluation only and should not be used as model input features.

## 🙌 About

Built as a practical Python project to explore workflow automation, data generation, validation, auditability, and exception handling.

<div align="center">
  <h3>🚀 Automate • Validate • Audit • Improve ✨</h3>
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:141E30,50:243B55,100:36BCF7&height=110&section=footer" width="100%" alt="Animated footer" />
</div>
