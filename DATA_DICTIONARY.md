# Data dictionary

All IDs are immutable strings and primary keys unless identified as foreign keys. Dates use ISO-8601 `YYYY-MM-DD`. Names and `example.test` email addresses are fictional.

| Entity | Primary key | Important fields / validation |
|---|---|---|
| Department | department_id | name required; cost_center unique |
| Role | role_id | title required; department_id FK |
| Manager | manager_id | name, department_id FK, email unique |
| Employee | employee_id | role_id, department_id, manager_id FKs; employment_type employee/contractor; status active/terminated; start_date >= hire_date |
| OnboardingCase | onboarding_case_id | employee_id FK; case_status pending/in_progress/completed |
| Task | task_id | case_id and employee_id FKs; owner HR/IT/Facilities/Manager/Employee; status pending/completed |
| Dependency | dependency_id | task_id and prerequisite_task_id both Task FKs; self-dependency prohibited; graph should be acyclic in clean baseline |
| AccessRole | access_role_id | role_name, system_name, risk_level low/medium/high |
| AccessGrant | grant_id | employee_id and access_role_id FKs; approved boolean; grant_status active/revoked |
| Asset | asset_id | asset_type, unique serial_number; asset_status available/assigned/recovered |
| OffboardingCase | offboarding_case_id | employee_id FK; termination_date; case_status |
| AuditEvent | event_id | entity_type, entity_id, event_type, event_date, actor, details |
| GroundTruth | issue_id | issue_type, entity_id, ground_truth, expected_decision; evaluation-only labels |

## Relationships
- Department 1:N Role, Employee, Manager.
- Role 1:N Employee; Manager 1:N Employee.
- Employee 1:N OnboardingCase and AccessGrant.
- OnboardingCase 1:N Task.
- Task N:M Task through the directed Dependency prerequisite bridge.
- AccessRole 1:N AccessGrant.
- Employee 1:N asset assignments in a production history model; this starter stores current assignment on Asset.
- Employee 0:1 OffboardingCase in the common lifecycle; AuditEvent uses polymorphic entity references.

## Known limitations
This is a runnable synthetic-data starter, not a production HR platform. Extend with EmployeeRoleHistory, AssetAssignmentHistory, AccessGrantEvent and TaskStatusEvent tables. Add graph-cycle detection, comprehensive enum/date/FK checks and stronger SQL constraints before production use.
