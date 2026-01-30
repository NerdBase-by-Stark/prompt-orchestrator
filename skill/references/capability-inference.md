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

## Agent Matching Priority

| Match Type | Confidence | Example |
|------------|------------|---------|
| Exact skill match | 100% | Task: `lua, q-sys` → Skill: `qsys-plugin-development` |
| Strong capability match | 85-95% | Task: `networking, api` → Agent: `backend-architect` |
| General match | 75-84% | Task: `file-ops, config` → Agent: `general-purpose` |
| Weak/ambiguous | <75% | Multiple agents match equally well |

---

## TASK-MANIFEST.md Format

```markdown
## Task Capabilities

| Task File | Capabilities | User-Specified Agent | Allocated Agent | Confidence |
|-----------|--------------|----------------------|-----------------|------------|
| 01-setup.md | file-ops, config | - | pending | pending |
| 02-api.md | python, api, networking | - | pending | pending |

## Execution Mode

`--ambiguous-only` (default): Only prompt user for <80% confidence allocations
```
