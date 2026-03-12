# TASK-MANIFEST

> Generated: 2026-03-11T14:32:00Z
> Source: QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v3.md
> Total Tasks: 6

---

## Execution Flags

**Mode**: `--ambiguous-only`

| Flag | Behavior |
|------|----------|
| `--ambiguous-only` | (DEFAULT) Ask user only about tasks with confidence <80% |
| `--confirm-agents` | Show full allocation list, await user confirmation |
| `--trust-allocator` | Accept all allocations without user review |

---

## Available Agents (Runtime Discovery)

Agents/skills discovered at orchestration time:

| Agent Type | Can Write/Edit | Description | Best For |
|------------|----------------|-------------|----------|
| `general-purpose` | Yes | Default Claude agent with full tool access | General code editing, file operations, broad tasks |
| `fullstack-developer` | Yes | Specialized agent for full-stack web development | Frontend/backend combined work, API + UI tasks |
| `feature-dev:code-reviewer` | **No** | Read-only code review agent | Code review feedback only |

> This list was populated by scanning the Agent tool's available `subagent_type` values
> and cross-referencing with the Agent Tool Capability Matrix in `references/capability-inference.md`.
> Only assign agents from this list. **Implementation tasks MUST use write-capable agents.**

---

## Context Rot Risk Assessment

| Task File | Extracted Lines | Files Touched | Risk Level | Action |
|-----------|----------------|---------------|-----------|--------|
| 01-structural-updates.md | 165 | 1 | Medium | Monitor -- multiple sections modified in single file |
| 02-logging-phase.md | 168 | 1 | Medium | Monitor -- implementation + test + commit in one task |
| 03-verification-phase.md | 185 | 1 | Medium | Monitor -- implementation + test + commit in one task |
| 04A-reconnection-phase.md | 210 | 1 | High | Split considered but kept unified -- modules are tightly coupled |
| 05-integration-test.md | 140 | 1 | Low | Read-only verification, no code changes |
| 06-final-updates.md | 92 | 1 | Low | Small scattered edits across existing sections |

**Risk Levels:** Low (<100 lines) | Medium (100-300) | High (300-500) | Critical (500+)
Tasks marked High/Critical have been split into sub-tasks to prevent context degradation.

---

## Task Capabilities

| Task File | Action Type | Capabilities | Allocated Agent | Can Write | Confidence |
|-----------|-------------|--------------|-----------------|-----------|------------|
| 01-structural-updates.md | implementation | `lua`, `q-sys`, `documentation` | general-purpose | Yes | 92% |
| 02-logging-phase.md | implementation | `lua`, `q-sys`, `networking` | general-purpose | Yes | 95% |
| 03-verification-phase.md | implementation | `lua`, `q-sys`, `networking` | general-purpose | Yes | 90% |
| 04A-reconnection-phase.md | implementation | `lua`, `q-sys`, `networking` | general-purpose | Yes | 90% |
| 05-integration-test.md | testing | `lua`, `q-sys`, `testing` | general-purpose | Yes | 88% |
| 06-final-updates.md | implementation | `lua`, `q-sys`, `documentation` | general-purpose | Yes | 94% |

---

## Capability Legend

| Tag | Description |
|-----|-------------|
| `lua` | Lua scripting, Q-SYS plugin code |
| `q-sys` | Q-SYS Designer APIs, controls, components |
| `testing` | Test writing, validation, verification |
| `networking` | API calls, HTTP, sockets, protocols |
| `documentation` | Comments, docs, README files |
| `file-ops` | File operations, scaffolding, directory setup |
| `refactoring` | Code cleanup, restructuring |
| `config` | Configuration files, environment setup |

---

## Allocation Summary

**Auto-assigned**: 5 tasks (high confidence)
**Ambiguous**: 1 task (needs user input)
**User-specified**: 0 tasks (passthrough)

---

## Ambiguous Tasks

Tasks requiring user decision (confidence <80% or multiple good matches):

| Task | Capabilities | Options | Why Ambiguous |
|------|--------------|---------|---------------|
| 05-integration-test.md | `lua`, `q-sys`, `testing` | general-purpose (88%), fullstack-developer (72%) | Integration test spans all modules and requires understanding of QRC protocol, socket handling, and timer interactions. general-purpose recommended but fullstack-developer could handle the cross-cutting nature. Confidence at 88% is above threshold but closest to ambiguous boundary. |

---

## Notes

- Capabilities are inferred from task content during orchestration
- User-specified agents (from source prompt) are passed through without review (confidence: 100%)
- Allocated Agent and Confidence columns are pre-filled during orchestration
- Tasks with confidence 80%+ are auto-assigned unless `--confirm-agents` flag is set
