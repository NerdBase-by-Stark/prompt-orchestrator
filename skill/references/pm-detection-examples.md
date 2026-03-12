# Detection Confidence Examples

> Reference file for prompt-orchestrator skill.
> Load when evaluating Pre-Analysis Gate detection confidence scoring.
>
> This measures whether the source ALREADY contains PM orchestration structure.
> It is NOT the same as the Complexity Score (Phase 1.4).

---

## CRITICAL: Plan vs PM Orchestration

A well-structured implementation plan is NOT a PM orchestration document. The scorer must
distinguish between general organization quality and PM-specific coordination structure.

| Feature | Implementation Plan | PM Orchestration Doc |
|---------|--------------------|-----------------------|
| Has numbered phases | Yes | Yes |
| Has validation criteria | Yes | Yes |
| Has dependencies | Yes | Yes |
| Defines PM role | **No** | **Yes** — "You are the PM" |
| Has subagent spawn prompts | **No** | **Yes** — Agent tool syntax |
| Has task sequence TABLE with agent column | **No** | **Yes** — Order/Task/Agent/Blocker |
| Has STATUS protocol | **No** | **Yes** — COMPLETE/FAILED/BLOCKED |
| Has context isolation rules | **No** | **Yes** — "PM does not read task files" |

**Rule of thumb**: If the document tells humans what code to change but doesn't tell a PM
how to dispatch subagents, it's a plan (score 0-20), not an orchestration doc (score 60+).

---

## Essential Elements for Good Orchestration

| Element | Purpose | Required For Good Score | What Does NOT Count |
|---------|---------|------------------------|---------------------|
| Clear PM role definition | Distinguish PM from worker agents | "You are the PM", "coordinate subagents" | Having phases, numbered steps |
| Task sequence TABLE with agent assignments | Explicit execution order with delegation | Table with Order/Task/Blocker/Agent columns | Numbered phase list, TODO list |
| Subagent spawn instructions | How to dispatch agents | Agent tool syntax, `subagent_type` refs | "Implement step X", "do this" |
| Status protocol | Monitor workflow state | STATUS: COMPLETE/FAILED/BLOCKED | Checkboxes, validation criteria |
| Context isolation rules | Prevent PM context pollution | "PM reads only coordination files" | General scope constraints |
| PM escalation procedures | Graceful degradation | PM-specific halt/report/escalate | Generic error handling |

---

## Good Examples (High Scores)

### Task sequence TABLE with agent assignments (20 pts)

```markdown
| Order | Task File | Description | Blocker | Agent |
|-------|-----------|-------------|---------|-------|
| 1 | 01-setup-env.md | Configure environment | - | general-purpose |
| 2 | 02-implement-core.md | Build core module | Task 1 | fullstack-developer |
| 3 | 03-add-tests.md | Write test suite | Task 2 | test-engineer |
```

### Status protocol (15 pts)

```markdown
| Task | Status | Notes |
|------|--------|-------|
| Task 1 | COMPLETE | Env configured |
| Task 2 | In Progress | 60% done |
| Task 3 | Not Started | Blocked by Task 2 |

STATUS: COMPLETE | FAILED | BLOCKED | CLARIFICATION NEEDED
```

### Error handling with PM escalation (15 pts)

```markdown
## Error Protocol
- If FAILED: halt workflow, report to user, do not proceed
- Escalation: provide failure context and affected tasks
- Recovery: user must approve retry or skip
```

### Context isolation rules (15 pts)

```markdown
## CONTEXT DISCIPLINE
- PM reads ONLY: PM-ORCHESTRATION.md, CONTEXT.md, TASK-MANIFEST.md
- PM does NOT read: subagent-tasks/*.md, source document, source code
- Task files are for subagents ONLY
```

### Subagent spawn instructions (15 pts)

```markdown
Agent tool:
  subagent_type: "fullstack-developer"
  description: "Implement auth module"
  prompt: |
    Read CONTEXT.md, then execute task file 02-implement-auth.md
    Report STATUS: COMPLETE or FAILED
```

### PM/Coordinator role definition (20 pts)

```markdown
## PM RULES (READ FIRST)
1. You are the PROJECT MANAGER. You coordinate subagents.
2. You MUST use subagents for each task.
3. You MUST NOT proceed to the next task until current is complete.
```

---

## FALSE POSITIVE: Well-Structured Plan (Score 0-20, NOT 60+)

This is the most common scoring mistake. A well-organized implementation plan looks like orchestration but is NOT.

```markdown
# Implementation Plan v1.6.0

## Phase 0: Prerequisite Validation
- Verify 150 tests pass
- Confirm git clean state

## Phase 1: Error Handling Consolidation
### Fix 1.1: Standardize error responses (server/routes/deploy.ts:45)
Current: `res.status(500).send("error")`
Replace: `res.status(500).json({ error: "Deploy failed", code: "DEPLOY_ERR" })`

### Fix 1.2: Add timeout wrapper (server/services/network.ts:120)
...

## Phase 2: Network Discovery Refactor
...

## Phase 3: UI State Management
...

git commit -m "Phase 1: error handling consolidation"
```

**Why this scores LOW (10-15 pts max):**
- Has phases ≠ has task sequence TABLE with agent assignments (0 pts for "task sequence")
- Has validation criteria ≠ has STATUS protocol (0 pts for "status protocol")
- Has dependencies between phases ≠ has PM escalation procedures (0 pts for "error handling")
- Has NO PM role definition, NO spawn prompts, NO context isolation rules
- This tells a developer what code to change — it does NOT tell a PM how to dispatch subagents

**Correct action**: Score ~15, proceed to Phase 1 (full orchestration), use plan as SOURCE for extraction.

---

## Weak Examples (Low Scores)

### Numbered list without dependencies (5 pts max)

```markdown
1. Setup environment
2. Implement core
3. Add tests
```

*Missing: blockers, validation, failure handling, status tracking*

### Vague instructions (0-10 pts)

```markdown
Do these tasks in order:
- Build the thing
- Test it
- Deploy
```

*Missing: everything essential*

### No validation criteria (loses 15 pts)

```markdown
| Task | Description |
|------|-------------|
| Setup | Configure environment |
| Build | Implement feature |
```

*Missing: how to know when complete*

### No failure handling (loses 15 pts)

```markdown
Execute tasks 1-5 in sequence.
```

*What happens if task 3 fails? Undefined behavior.*

---

## Scoring Heuristics

When evaluating source documents:

1. **Role definition** - Look in first 50 lines for PM/coordinator language
2. **Task sequence** - Search for markdown tables with "Task", "Order", numbered headers
3. **Dependencies** - Scan for "block", "require", "after", "depend" keywords
4. **Validation** - Look for checkboxes `[ ]`, "criteria", "verify", "validate"
5. **Progress** - Search for "Status", "Progress", state words (Complete/Started/Failed)
6. **Error handling** - Find "if fail", "on error", "escalate", exception language

---

## Detection Confidence

| Confidence | Score Range | Recommendation |
|------------|-------------|----------------|
| High | 80-100 | Strong orchestration - recommend USE AS-IS |
| Medium | 60-79 | Good structure - present choice: USE AS-IS (recommended) or REBUILD |
| Low | 40-59 | Partial structure - recommend REBUILD |
| None | 0-39 | No orchestration - full skill application |
