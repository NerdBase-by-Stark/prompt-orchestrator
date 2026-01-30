# TASK-MANIFEST

> Generated: {{TIMESTAMP}}
> Source: {{SOURCE_FILE}}
> Total Tasks: {{TASK_COUNT}}

---

## Execution Flags

**Mode**: `{{EXECUTION_MODE}}`

| Flag | Behavior |
|------|----------|
| `--ambiguous-only` | (DEFAULT) Ask user only about tasks with confidence <80% |
| `--confirm-agents` | Show full allocation list, await user confirmation |
| `--trust-allocator` | Accept all allocations without user review |

---

## Task Capabilities

| Task File | Capabilities | User-Specified Agent | Allocated Agent | Confidence |
|-----------|--------------|----------------------|-----------------|------------|
{{TASK_CAPABILITY_ROWS}}

---

## Capability Legend

| Tag | Description |
|-----|-------------|
| `lua` | Lua scripting, Q-SYS plugin code |
| `q-sys` | Q-SYS Designer APIs, controls, components |
| `testing` | Test writing, validation, verification |
| `frontend` | UI layout, components, user interface |
| `networking` | API calls, HTTP, sockets, protocols |
| `auth` | Authentication, credentials, security |
| `file-ops` | File operations, scaffolding, directory setup |
| `database` | Database operations, storage, persistence |
| `documentation` | Comments, docs, README files |
| `refactoring` | Code cleanup, restructuring |
| `config` | Configuration files, environment setup |
| `devops` | CI/CD, deployment, infrastructure |

---

## Allocation Summary

**Auto-assigned**: {{AUTO_ASSIGNED_COUNT}} tasks (high confidence)
**Ambiguous**: {{AMBIGUOUS_COUNT}} tasks (needs user input)
**User-specified**: {{USER_SPECIFIED_COUNT}} tasks (passthrough)

---

## Ambiguous Tasks

Tasks requiring user decision (confidence <80% or multiple good matches):

| Task | Capabilities | Options | Why Ambiguous |
|------|--------------|---------|---------------|
{{AMBIGUOUS_TASK_ROWS}}

---

## Notes

- Capabilities are inferred from task content during orchestration
- User-specified agents (from source prompt) are passed through without review (confidence: 100%)
- Allocated Agent and Confidence columns are pre-filled during orchestration
- Tasks with confidence 80%+ are auto-assigned unless `--confirm-agents` flag is set
