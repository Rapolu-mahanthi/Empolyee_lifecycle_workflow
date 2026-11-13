import argparse, csv, json, random
from pathlib import Path
from datetime import date, timedelta

SEED = 20261022
DEPARTMENTS = ["Engineering", "Data", "Human Resources", "IT", "Operations", "Finance"]
ROLES = ["Python Developer", "Data Analyst", "IT Support", "HR Associate", "Operations Analyst", "QA Engineer"]
TASK_TEMPLATES = [
    ("Collect documents", "HR", []),
    ("Verify identity", "HR", ["Collect documents"]),
    ("Manager approval", "Manager", ["Verify identity"]),
    ("Create email account", "IT", ["Manager approval"]),
    ("Provision application access", "IT", ["Create email account"]),
    ("Prepare laptop", "Facilities", ["Manager approval"]),
    ("Deliver equipment", "Facilities", ["Prepare laptop"]),
    ("Employee acknowledgement", "Employee", ["Deliver equipment"]),
]

def write_csv(path, rows):
    rows = list(rows)
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def build(out: Path, scale: float = 1.0, seed: int = SEED):
    rng = random.Random(seed)
    out.mkdir(parents=True, exist_ok=True)
    n = max(10, int(1000 * scale))
    task_target, grant_target, asset_target = int(8000 * scale), int(1500 * scale), int(1200 * scale)
    departments = [{"department_id": f"DEPT-{i+1:03d}", "name": d, "cost_center": f"CC-{i+1:03d}"} for i, d in enumerate(DEPARTMENTS)]
    roles = [{"role_id": f"ROLE-{i+1:03d}", "title": r, "department_id": f"DEPT-{(i % len(DEPARTMENTS))+1:03d}", "access_template": f"ACCESS-{i+1:03d}"} for i, r in enumerate(ROLES)]
    managers = [{"manager_id": f"MGR-{i+1:04d}", "name": f"Manager {i+1}", "department_id": f"DEPT-{(i % len(DEPARTMENTS))+1:03d}", "email": f"manager{i+1}@example.test"} for i in range(30)]
    employees, onboarding, tasks, dependencies, grants, assets, offboarding, audit, truth = [], [], [], [], [], [], [], [], []
    for i in range(n):
        emp = f"EMP-{i+1:06d}"
        hire = date(2026, 1, 1) + timedelta(days=rng.randint(0, 300))
        start = hire + timedelta(days=rng.randint(1, 14) + (7 if i % 25 == 0 else 0))
        status = "terminated" if i % 40 == 0 else "active"
        contract = "contractor" if i % 12 == 0 else "employee"
        role_idx = i % len(roles)
        dept, mgr = roles[role_idx]["department_id"], f"MGR-{(i % 30)+1:04d}"
        term_date = (start + timedelta(days=rng.randint(30, 180))).isoformat() if status == "terminated" else ""
        employees.append({"employee_id": emp, "first_name": f"Employee{i+1}", "last_name": f"Sample{i+1}", "email": f"employee{i+1}@example.test", "role_id": roles[role_idx]["role_id"], "department_id": dept, "manager_id": mgr, "employment_type": contract, "hire_date": hire.isoformat(), "start_date": start.isoformat(), "termination_date": term_date, "employment_status": status})
        case = f"ONB-2026-{i+1:06d}"
        onboarding.append({"onboarding_case_id": case, "employee_id": emp, "case_status": "completed" if start <= date(2026, 11, 1) else "in_progress", "created_date": hire.isoformat(), "target_start_date": start.isoformat()})
        for j, (name, owner, prereqs) in enumerate(TASK_TEMPLATES, 1):
            tid = f"TASK-{case}-{j:03d}"
            done = status == "active" and start <= date(2026, 11, 1)
            tasks.append({"task_id": tid, "case_id": case, "employee_id": emp, "task_name": name, "owner": owner, "status": "completed" if done else "pending", "created_at": hire.isoformat(), "due_date": (start + timedelta(days=j)).isoformat(), "completed_at": (start + timedelta(days=j)).isoformat() if done else ""})
            for prereq in prereqs:
                previous = next((k for k, item in enumerate(TASK_TEMPLATES[:j-1], 1) if item[0] == prereq), None)
                if previous:
                    dependencies.append({"dependency_id": f"DEP-{len(dependencies)+1:07d}", "task_id": tid, "prerequisite_task_id": f"TASK-{case}-{previous:03d}"})
        if i % 2 == 0:
            grants.append({"grant_id": f"GRANT-{emp}-001", "employee_id": emp, "access_role_id": f"AR-{role_idx+1:03d}", "granted_at": (start + timedelta(days=2)).isoformat(), "approved": True, "revoked_at": term_date if status == "terminated" else "", "grant_status": "revoked" if status == "terminated" else "active"})
        if status == "terminated":
            offboarding.append({"offboarding_case_id": f"OFF-2026-{i+1:06d}", "employee_id": emp, "termination_date": term_date, "case_status": "completed", "reason": "End of contract" if contract == "contractor" else "Role transition"})
            audit.append({"event_id": f"AUD-{len(audit)+1:07d}", "entity_type": "Employee", "entity_id": emp, "event_type": "employment_terminated", "event_date": term_date, "actor": "HR", "details": "Termination recorded"})
    while len(tasks) < task_target:
        k = len(tasks) + 1
        e, emp = (k-1) % n + 1, f"EMP-{(k-1) % n + 1:06d}"
        tasks.append({"task_id": f"TASK-EXTRA-{k:06d}", "case_id": f"ONB-2026-{e:06d}", "employee_id": emp, "task_name": "Additional compliance check", "owner": "HR", "status": "completed" if k % 3 else "pending", "created_at": "2026-01-01", "due_date": "2026-12-31", "completed_at": "2026-01-03" if k % 3 else ""})
    tasks = tasks[:task_target]
    while len(grants) < grant_target:
        k = len(grants) + 1
        e, emp = (k-1) % n + 1, f"EMP-{(k-1) % n + 1:06d}"
        seq = 1 + sum(1 for item in grants if item["employee_id"] == emp)
        grants.append({"grant_id": f"GRANT-{emp}-{seq:03d}", "employee_id": emp, "access_role_id": f"AR-{(k % len(roles))+1:03d}", "granted_at": "2026-06-01", "approved": True, "revoked_at": "", "grant_status": "active"})
    grants = grants[:grant_target]
    for i in range(asset_target):
        assets.append({"asset_id": f"AST-{i+1:06d}", "asset_type": ["Laptop", "Monitor", "Phone"][i % 3], "serial_number": f"SN-{i+1:08d}", "asset_status": "available", "assigned_employee_id": "", "assigned_date": "", "recovered_date": ""})
    for i, employee in enumerate(employees[:min(asset_target, n)]):
        assets[i].update(asset_status="assigned", assigned_employee_id=employee["employee_id"], assigned_date=employee["start_date"])
    access_roles = [{"access_role_id": f"AR-{i+1:03d}", "role_name": f"{roles[i]['title']} Standard Access", "system_name": ["Email", "HRIS", "CRM", "Analytics"][i % 4], "risk_level": "medium"} for i in range(len(roles))]
    if grants:
        grants[0].update(granted_at="2025-12-01", approved=False)
        truth.append({"issue_id": "ISS-001", "issue_type": "access_before_start_or_approval", "entity_id": grants[0]["grant_id"], "ground_truth": "anomaly", "expected_decision": "Flag grant; require approval and valid start date"})
    if len(assets) > 1 and employees:
        assets[1].update(assigned_employee_id=assets[0]["assigned_employee_id"], asset_status="assigned", assigned_date="2026-05-01")
        truth.append({"issue_id": "ISS-002", "issue_type": "duplicate_asset_assignment", "entity_id": assets[1]["asset_id"], "ground_truth": "anomaly", "expected_decision": "Flag duplicate employee asset assignment"})
    terminated = next((e for e in employees if e["employment_status"] == "terminated"), None)
    if terminated:
        grant = next((g for g in grants if g["employee_id"] == terminated["employee_id"]), None)
        if grant:
            grant.update(grant_status="active", revoked_at="")
            truth.append({"issue_id": "ISS-003", "issue_type": "terminated_employee_retains_grant", "entity_id": grant["grant_id"], "ground_truth": "anomaly", "expected_decision": "Revoke access immediately"})
    if len(tasks) >= 2:
        dependencies.extend([{"dependency_id": f"DEP-{len(dependencies)+1:07d}", "task_id": tasks[0]["task_id"], "prerequisite_task_id": tasks[1]["task_id"]}, {"dependency_id": f"DEP-{len(dependencies)+2:07d}", "task_id": tasks[1]["task_id"], "prerequisite_task_id": tasks[0]["task_id"]}])
        truth.append({"issue_id": "ISS-004", "issue_type": "task_dependency_cycle", "entity_id": tasks[0]["task_id"], "ground_truth": "anomaly", "expected_decision": "Reject cyclic dependency graph"})
    if assets:
        assets[-1].update(asset_status="assigned", recovered_date="2026-10-01")
        truth.append({"issue_id": "ISS-005", "issue_type": "recovered_asset_still_assigned", "entity_id": assets[-1]["asset_id"], "ground_truth": "anomaly", "expected_decision": "Clear assignment and reconcile asset state"})
    tables = {"departments": departments, "roles": roles, "managers": managers, "employees": employees, "onboarding_cases": onboarding, "tasks": tasks, "dependencies": dependencies, "access_roles": access_roles, "access_grants": grants, "assets": assets, "offboarding_cases": offboarding, "audit_events": audit, "ground_truth": truth}
    for name, rows in tables.items():
        write_csv(out / f"{name}.csv", rows)
        (out / f"{name}.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    manifest = {"seed": seed, "scale": scale, "generated_at": "deterministic-seed-run", "counts": {key: len(value) for key, value in tables.items()}}
    (out / "source_manifest.json").write_text(json.dumps(manifest, indent=2))
    (out / "validation_summary.json").write_text(json.dumps(validate(tables), indent=2))
    return tables

def validate(tables):
    errors = []
    def unique(rows, key, name):
        values = [row[key] for row in rows]
        if len(values) != len(set(values)):
            errors.append(f"{name}: duplicate {key}")
    for name, key in [("employees", "employee_id"), ("tasks", "task_id"), ("access_grants", "grant_id"), ("assets", "asset_id")]:
        unique(tables[name], key, name)
    employee_ids = {row["employee_id"] for row in tables["employees"]}
    task_ids = {row["task_id"] for row in tables["tasks"]}
    for grant in tables["access_grants"]:
        if grant["employee_id"] not in employee_ids:
            errors.append("access_grants: invalid employee FK")
    for dep in tables["dependencies"]:
        if dep["task_id"] not in task_ids or dep["prerequisite_task_id"] not in task_ids:
            errors.append("dependencies: invalid task FK")
    active = sum(grant["grant_status"] == "active" for grant in tables["access_grants"])
    return {"passed": not errors, "errors": errors, "metrics": {"employees": len(tables["employees"]), "tasks": len(tables["tasks"]), "access_grants": len(tables["access_grants"]), "assets": len(tables["assets"]), "known_anomalies": len(tables["ground_truth"]), "active_grants": active}}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data")
    parser.add_argument("--scale", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    generated = build(Path(args.out), args.scale, args.seed)
    print(json.dumps(validate(generated), indent=2))
