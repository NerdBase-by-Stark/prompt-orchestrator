# Capability Inference Rules

> Reference file for prompt-orchestrator skill.
> Load when generating TASK-MANIFEST.md.

---

## Content Pattern to Capability Tag Mapping

| Content Pattern | Capability Tags |
|-----------------|-----------------|
| Lua code, Q-SYS APIs, Controls | `lua`, `q-sys` |
| Test, validation, verify, assertion | `testing` |
| UI, layout, components, pages, UCI | `frontend`, `ui` |
| API, HTTP, sockets, networking, WebSocket | `networking`, `api` |
| Auth, login, credentials, Logon | `auth`, `security` |
| File operations, scaffolding, mkdir | `file-ops` |
| Database, storage, persistence, SQL | `database` |
| Documentation, comments, README | `documentation` |
| Refactoring, cleanup, restructuring | `refactoring` |
| Config, environment, settings | `config` |
| CI/CD, deployment, Docker, build | `devops` |
| async, await, promise, callback | `async`, `concurrency` |
| parser, regex, parse | `parsing` |
| cache, memoize, Redis | `caching` |
| log, trace, debug, monitor | `observability` |
| encryption, hash, SSL/TLS | `cryptography` |
| TypeScript, .ts, .tsx, interface, type | `typescript` |
| React, JSX, useState, useEffect, component | `react`, `frontend` |
| Next.js, getServerSideProps, App Router | `nextjs`, `frontend`, `fullstack` |
| Vue, .vue, Composition API, ref, computed | `vue`, `frontend` |
| Svelte, .svelte, SvelteKit | `svelte`, `frontend` |
| Tailwind CSS, className, utility classes | `css`, `frontend` |
| REST API, endpoint, route, middleware | `api`, `backend` |
| GraphQL, query, mutation, resolver | `graphql`, `api` |
| Prisma, Drizzle, ORM, schema | `orm`, `database` |
| WebSocket, real-time, socket.io | `websocket`, `networking` |
| Markdown, .md, documentation site | `documentation` |
| Python, pip, requirements.txt | `python` |
| JavaScript, npm, node | `javascript` |
| Bash, shell, script | `shell` |
| Git, commit, branch, merge | `git` |

---

## Inference Rules

1. **Tag ALL relevant capabilities** per task (usually 2-4 tags)
2. If task mentions specific skill (e.g., "use qsys-plugin-development"), note as **User-Specified Agent**
3. Capabilities are used during orchestration to pre-fill agent allocations in TASK-MANIFEST.md
4. When uncertain, use **broader tags** (e.g., `lua` rather than `lua-advanced`)
5. If task contains code blocks, infer language from syntax

---

## Task Action Classification (MANDATORY)

Before matching agents, classify each task's primary action. This determines which agents are eligible.

| Action Type | Description | Requires Tools | Eligible Agent Types |
|-------------|-------------|----------------|---------------------|
| `implementation` | Creates or modifies source files | Write, Edit | Write-capable agents ONLY |
| `testing` | Runs tests, writes test files | Bash, Write | Write-capable agents ONLY |
| `research` | Reads, analyzes, reports findings | Read only | ANY agent (including read-only) |
| `review` | Reviews code, provides feedback | Read only | ANY agent (including read-only) |
| `devops` | CI/CD, Docker, deployment configs | Bash, Write | Write-capable agents ONLY |
| `documentation` | Creates/updates docs | Write, Edit | Write-capable agents ONLY |

**Detection heuristic**: If the task's extracted content contains code to write, files to create/modify, or commands to run → it is `implementation`, NOT `research`.

**HARD GATE**: If a task is classified as `implementation`, `testing`, `devops`, or `documentation`, the allocated agent MUST have Write/Edit tools. Assigning a read-only agent to a write-required task is a **skill failure**. Fix before proceeding.

---

## Agent Tool Capability Matrix

**Write-capable agents** (can create/modify files):

| Agent Type | Write | Edit | Bash | Best For |
|------------|-------|------|------|----------|
| `general-purpose` | Yes | Yes | Yes | Any task (safe default) |
| `fullstack-developer` | Yes | Yes | Yes | End-to-end implementation |
| `frontend-developer` | Yes | Yes | Yes | UI/React/CSS work |
| `backend-architect` | Yes | Yes | Yes | APIs, server-side logic |
| `python-pro` | Yes | Yes | Yes | Python-specific code |
| `security-auditor` | Yes | Yes | Yes | Security fixes + reviews |
| `test-engineer` | Yes | Yes | Yes | Test writing + execution |
| `deployment-engineer` | Yes | Yes | Yes | CI/CD, Docker, infra |
| `ai-engineer` | Yes | Yes | Yes | LLM/RAG applications |
| `ml-engineer` | Yes | Yes | Yes | ML pipelines, model serving |
| `data-scientist` | Yes | Yes | Yes | Data analysis, modeling |

**Read-only agents** (CANNOT create/modify files):

| Agent Type | Write | Edit | Bash | Use ONLY For |
|------------|-------|------|------|--------------|
| `feature-dev:code-explorer` | **No** | **No** | No | Codebase research/analysis |
| `feature-dev:code-reviewer` | **No** | **No** | No | Code review feedback |
| `feature-dev:code-architect` | **No** | **No** | No | Architecture design |
| `Plan` | **No** | **No** | **No** | Planning only |
| `Explore` | **No** | **No** | **No** | Exploration/search only |

**RULE**: When in doubt, default to `general-purpose`. It has all tools and works for any task. Never allocate a read-only agent to a task that modifies files.

---

## Agent Matching Priority

| Priority | Match Type | Confidence | Example |
|----------|------------|------------|---------|
| 0 (gate) | Action-type compatibility | Pass/Fail | Task: `implementation` + Agent: `Explore` → **REJECT** |
| 1 | User-specified in source | 100% | Source says "use backend-architect" → use it |
| 2 | Exact skill match | 85-95% | Task: `lua, q-sys` → Skill: `qsys-plugin-development` |
| 3 | Strong capability match | 80-90% | Task: `networking, api` → Agent: `backend-architect` |
| 4 | General match | 75-84% | Task: `file-ops, config` → Agent: `general-purpose` |
| 5 | Fallback | 75% | No match → `general-purpose` |

Priority 0 is a **hard gate** — no agent passes to scoring if it fails the action-type check.

---

## TASK-MANIFEST.md Format

```markdown
## Task Capabilities

| Task File | Action Type | Capabilities | Allocated Agent | Can Write | Confidence |
|-----------|-------------|--------------|-----------------|-----------|------------|
| 01-setup.md | implementation | file-ops, config | general-purpose | Yes | 80% |
| 02-api.md | implementation | python, api | fullstack-developer | Yes | 85% |
| 03-review.md | review | python | feature-dev:code-reviewer | N/A | 90% |

## Execution Mode

`--ambiguous-only` (default): Only prompt user for <80% confidence allocations
```
