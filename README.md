# Architecture Decision Record: FAA Multi-Agent Deployment Strategy

**ADR-001** | Date: 2026-03-31 | Status: **Accepted**

-----

## Context

The FAA (Financial Asset Analysis) system consists of three specialized sub-agents and one orchestration workflow:

- `agents/causality` — causal factor analysis
- `agents/materiality` — materiality assessment
- `agents/market_trends` — market trend analysis
- `workflow/` — NOVA orchestrator that coordinates the three agents

The team debated three structural options for how to organize and deploy these components. A key long-term goal is that each agent should eventually be **autonomous and callable independently**, potentially via A2A (Agent-to-Agent) protocol, outside of the FAA workflow.

-----

## Options Considered

### Option 1 — 1 Repo, 1 Webapp, Multiple Routes ✅ *Chosen*

All agents and the workflow live in a single repository and are served by a single web application, each agent exposed via a dedicated API route.

```
src/
├── agents/
│   ├── causality/        → /agents/causality
│   ├── materiality/      → /agents/materiality
│   └── market_trends/    → /agents/market_trends
└── workflow/             → /workflow
```

### Option 2 — 1 Repo, 4 Webapps, 4 Routes ❌ *Rejected*

Single codebase but deployed as four separate web applications, each with its own route.

### Option 3 — 4 Repos, 4 Webapps ⏳ *Future Target*

Fully isolated — each agent has its own repository, CI/CD pipeline, and web application.

-----

## Comparison

|Dimension           |Option 1|Option 2   |Option 3|
|--------------------|--------|-----------|--------|
|Repositories        |1       |1          |4       |
|Web Applications    |1       |4          |4       |
|Dev Complexity      |Low     |Medium     |High    |
|Deploy Complexity   |Low     |**High**   |Medium  |
|Dependency Isolation|❌       |❌          |✅       |
|Independent Scaling |❌       |✅          |✅       |
|A2A Ready           |❌       |Partial    |✅       |
|QA Risk             |Low     |**High**   |Low     |
|Timeline Risk       |Low     |Medium     |High    |
|Version Control     |Simple  |Problematic|Clean   |

### Why Option 2 Was Rejected

Option 2 was identified as the worst of both worlds:

- **Not truly isolated** — all apps share the same codebase, so a dependency change in one agent forces redeployment of all four apps
- **Dependency conflicts** — shared library versions across apps in the same repo can collide
- **QA nightmare** — regression testing must account for 4 deployment targets from 1 codebase
- **Version control confusion** — a single commit can break multiple independently deployed apps
- As one team member put it: *“wants to be independent but isn’t”*

### Why Option 3 Was Deferred

Option 3 is the correct long-term architecture but introduces too much overhead at the current stage:

- 4 separate CI/CD pipelines to configure and maintain
- Cross-agent debugging is significantly harder
- Package and dependency management multiplied across repos
- Delivery timeline risk is not justified when agents are still being designed and stabilized

-----

## Decision

**We adopt Option 1** for the current development and initial production phase.

The monorepo structure with a single webapp is the pragmatic choice that minimizes operational risk and preserves delivery speed. However, the implementation must be designed with Option 3 as the future target state.

-----

## Implementation Guidelines

To ensure Option 1 remains forward-compatible with Option 3, the following constraints apply:

### 1. Hard Agent Boundaries

Each agent folder must be **self-contained**. No agent may import code from a sibling agent directory.

```
# ✅ Allowed
from agents.causality.core import run_analysis

# ❌ Forbidden
from agents.materiality.utils import shared_helper  # in causality code
```

### 2. Dedicated Routes Per Agent

Each agent must be accessible via its own dedicated route. The workflow orchestrator calls agents via their route, not via direct in-process function calls.

```
POST /agents/causality
POST /agents/materiality
POST /agents/market_trends
POST /workflow/run
```

This ensures that when we extract an agent to its own repo, the interface contract is already defined and tested.

### 3. Independent Dependency Declaration

Each agent folder must contain its own `requirements.txt` (or equivalent). The root `requirements.txt` aggregates them but agents must not rely on this.

```
src/agents/causality/requirements.txt
src/agents/materiality/requirements.txt
src/agents/market_trends/requirements.txt
```

### 4. No Cross-Agent Shared State

Agents must not share in-memory state, caches, or global variables. Any shared infrastructure (e.g. Redis, Azure AI Search) must be accessed independently by each agent through its own client instance.

### 5. Independent Testability

Each agent must have a standalone test suite that can be run in isolation without the rest of the repo:

```bash
pytest src/agents/causality/tests/
pytest src/agents/materiality/tests/
pytest src/agents/market_trends/tests/
```

-----

## Migration Path to Option 3

When the time comes to move to Option 3, the extraction process per agent should be straightforward:

1. Copy `src/agents/<agent_name>/` to a new repository
1. Promote its `requirements.txt` to root level
1. Point the CI/CD pipeline at the new repo
1. Update the workflow orchestrator to call the new endpoint URL
1. Decommission the agent from the monorepo

Because the agents are designed with hard boundaries from day one, this should be close to a copy-paste operation with minimal refactoring.

-----

## Risks & Mitigations

|Risk                                   |Likelihood|Mitigation                                           |
|---------------------------------------|----------|-----------------------------------------------------|
|Developer accidentally couples agents  |Medium    |Code review policy + linting rules                   |
|Dependency version drift between agents|Low       |Per-agent requirements files                         |
|Single webapp becomes a bottleneck     |Low       |Azure Web App scaling handles this; revisit if needed|
|Team forgets Option 3 is the target    |Medium    |This ADR to be referenced in onboarding docs         |

-----

## Stakeholders

|Name                  |Role          |Position                                                                      |
|----------------------|--------------|------------------------------------------------------------------------------|
|Kevin W.              |Author        |Proposed Option 1 as pragmatic fallback                                       |
|Julien C.             |Architect     |Advocated for agent autonomy; aligned on Option 1 with guidelines             |
|Roel F.               |Infrastructure|Flagged Option 2 complexity; aligned on Option 1                              |
|Alex / Nolan / Francis|Team          |Raised QA and version control concerns; Option 2 rejected based on their input|

-----

*This ADR supersedes informal discussion. Option 3 remains the intended long-term target and should be revisited once the agents are stable in production.*
