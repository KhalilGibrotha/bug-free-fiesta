# Epic: Windows Server In-Place Upgrade Automation

**Epic ID:** SEO-AUTO-WSUPGRADE  
**Summary:** Automate Windows Server 2016/2019 upgrades to 2022 or 2025 using Ansible Automation Platform  
**Owner:** Principal Engineer & Architect  
**Primary Drivers:** AAP Engineer, Server Operations Admin  
**Priority:** High  
**Target Start:** Current Sprint (Feasibility)  
**Support Ends:** January 2027  

## Epic Description
Server Engineering & Operations must automate Windows Server upgrades from 2016 and 2019 to supported releases (2022 or 2025). The current manual upgrade process requires RDP access and takes ~135 minutes per pair of servers. Approximately 824 servers are in scope. 

This effort will develop and implement automation via the Ansible Automation Platform (AAP) to streamline pre-checks, ISO-based upgrades, and post-validation, while maintaining compliance and observability standards. 

The project will proceed through structured phases: Feasibility, Design/PoC, Full Automation Build, Pilot, and Rollout Enablement.

---

## Story 1: Feasibility & Discovery
**Story ID:** SEO-AUTO-WSUPGRADE-001  
**Sprint:** Current (Ends Oct 29)  
**Owner:** AAP Engineer / Server Ops Admin  
**Goal:** Validate automation feasibility and dependencies for Windows in-place upgrades.  
**Due Date:** Oct 27  

### Description
Evaluate existing PowerShell-based process and determine what components can be automated using Ansible (preferably via WinRM). Identify dependencies, blockers, and required configuration standards for remote execution. Establish inventory model and test environment to support automation development.

### Acceptance Criteria
- [ ] Review current manual documentation and scripts for 2016 → 2022 and 2019 → 2022/2025 upgrade paths.  
- [ ] Validate pre-check, upgrade, and post-check scripts under WinRM execution.  
- [ ] Confirm SentinelOne does not interfere with upgrade or automation process.  
- [ ] Establish 4-lab test systems (2×2016, 2×2019) joined to domain with snapshot capability.  
- [ ] Mount and validate both 2022 and 2025 ISOs.  
- [ ] Confirm AAP → Windows connectivity using WinRM from current EE.  
- [ ] Document any EE adjustments required for Windows automation.  
- [ ] Define CSV inventory schema (hostname, app group, environment, upgrade target).  
- [ ] Document dependency list (MECM, SentinelOne, ISO shares, permissions).  
- [ ] Deliver Feasibility Summary and recommendations by Oct 27.  

### Deliverables
- Feasibility Summary (recommended automation method, risks, dependencies)
- Connectivity test results and findings
- Draft inventory structure (CSV schema)
- Risk/mitigation log

---

## Story 2: Design & Proof of Concept
**Story ID:** SEO-AUTO-WSUPGRADE-002  
**Sprint:** Next Sprint (Nov)  
**Owner:** AAP Engineer  
**Goal:** Develop a functional prototype automating one full upgrade path (likely 2019 → 2025) under AAP control.  

### Description
Develop an Ansible playbook using WinRM to execute pre-checks, mount ISO, run setup.exe /auto upgrade, handle reboot tracking, and validate post-upgrade conditions. Validate rollback through snapshot revert and document results.

### Acceptance Criteria
- [ ] Pre-check role modularized and validated remotely.  
- [ ] Upgrade role executes unattended setup and tracks reboots.  
- [ ] Post-check validates version, domain membership, MECM agent health.  
- [ ] Snapshot/revert procedure documented and validated.  
- [ ] Execution confirmed via AAP job template and job logs.  
- [ ] Results reviewed with Architecture and Server Ops.  

### Deliverables
- Prototype playbook and supporting roles
- AAP job template prototype
- Design document (workflow diagram + description)
- Rollback and recovery validation results

---

## Story 3: Full Automation Build
**Story ID:** SEO-AUTO-WSUPGRADE-003  
**Sprint:** December (Target)  
**Owner:** AAP Engineer / Principal Architect  
**Goal:** Build complete automation framework supporting all four upgrade paths.  

### Description
Expand PoC automation to handle:
- 2016 → 2022  
- 2016 → 2025  
- 2019 → 2022  
- 2019 → 2025  

Integrate standardized pre-checks, rollback, logging, and post-validation steps. Create job templates with inventory grouping by application/environment/availability.

### Acceptance Criteria
- [ ] Four upgrade playbooks validated end-to-end.  
- [ ] Centralized logging to AAP/Splunk verified.  
- [ ] Parameterized playbook variables (source OS, target OS, ISO path).  
- [ ] Role-based modular design aligned with AAP standards.  
- [ ] Documentation reviewed and approved by Architecture.  
- [ ] Runbook for operator execution drafted.  

### Deliverables
- Final playbooks and EE configuration
- Documentation and operator runbook
- Change management artifacts for production readiness

---

## Story 4: Pilot Rollout
**Story ID:** SEO-AUTO-WSUPGRADE-004  
**Sprint:** January  
**Owner:** Server Operations Admin  
**Goal:** Validate automation in production-like environment using controlled batch upgrades.  

### Description
Run the automation against a small pilot group (10–20 servers) across diverse applications and environments. Measure upgrade time, failure rate, and overall efficiency compared to manual baseline.

### Acceptance Criteria
- [ ] 10–20 servers successfully upgraded using automation.  
- [ ] Rollback/retry procedures validated.  
- [ ] Pilot metrics captured (duration, success %, issues logged).  
- [ ] Adjustments documented and finalized.  

### Deliverables
- Pilot report with success metrics and recommendations
- Finalized procedures for full rollout

---

## Story 5: Full Rollout Enablement
**Story ID:** SEO-AUTO-WSUPGRADE-005  
**Sprint:** TBD (Post-Pilot)  
**Owner:** Server Operations Admin  
**Goal:** Transition automation to operations and enable broad rollout planning.  

### Description
Finalize operator documentation, define scheduling guidelines, and prepare Server Operations to manage rollout. Deliver updated runbook, inventory grouping standards, and coordination process for cross-team upgrades.

### Acceptance Criteria
- [ ] Operator runbook completed and validated.  
- [ ] Inventory grouping and scheduling structure finalized.  
- [ ] Training or knowledge transfer session completed.  
- [ ] Server Operations ready for scale-out execution.  

### Deliverables
- Final Runbook (AAP job templates, inventory instructions, troubleshooting)
- Deployment planning guide
- Knowledge transfer completion record

---

## Risks & Mitigations (Epic-Level)
| Risk | Mitigation |
|------|-------------|
| MECM 2025 support delay | Allow alternate path for patch trigger or manual validation post-upgrade. |
| SentinelOne blocking automation | Work with Security to whitelist upgrade binaries and WinRM actions. |
| Low disk space on C: drives | Enforce pre-checks to verify ≥15GB free; cleanup MECM cache. |
| WinRM instability | Validate connectivity at scale; tune EE WinRM timeout and concurrency. |
| Application compatibility | Support fallback upgrade to 2022 if 2025 fails or is unsupported. |

---

## Metrics for Leadership
| Metric | Baseline | Target |
|---------|-----------|--------|
| Avg. upgrade time per pair | 135 min | ≤ 60 min automated |
| Automation coverage (servers in scope) | 0% | ≥ 95% by Jan 2026 |
| Manual effort reduction | — | ≥ 60% |
| Pilot success rate | — | ≥ 95% |

---

**References:**  
- AAP Policy & Governance Document (Server Engineering & Operations)  
- Existing Windows Upgrade Procedure – Server Ops Documentation  
- Satellite Inventory / CSV Source – Server Ops  
- MECM Post-Upgrade Process  
- SentinelOne Policy Controls  

