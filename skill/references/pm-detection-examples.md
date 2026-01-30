# PM Detection Examples

> Reference file for prompt-orchestrator skill.
> Load when evaluating Phase 0 orchestration detection scoring.

---

## Essential Elements for Good Orchestration

| Element | Purpose | Required For Good Score |
|---------|---------|------------------------|
| Clear role definition | Distinguish PM from worker agents | "You are the PM", "coordinate subagents" |
| Task sequence with ordering | Explicit execution order | Numbered list or Order column |
| Dependencies between tasks | Prevent out-of-order execution | "blocked by", "requires", dependency column |
| Validation criteria per task | Verify completion | Checkboxes, "success criteria" section |
| Progress tracking mechanism | Monitor workflow state | Status column with states |
| Failure handling instructions | Graceful degradation | "if FAILED", "on error", escalation |

---

## Good Examples (High Scores)

### Task Sequence Table (20 pts)

```markdown
| Order | Task File | Description | Blocker |
|-------|-----------|-------------|---------|
| 1 | 01-setup-env.md | Configure environment | - |
| 2 | 02-implement-core.md | Build core module | Task 1 |
| 3 | 03-add-tests.md | Write test suite | Task 2 |
```

### Progress Tracker with Status (15 pts)

```markdown
| Task | Status | Notes |
|------|--------|-------|
| Task 1 | Complete | Env configured |
| Task 2 | In Progress | 60% done |
| Task 3 | Not Started | Blocked by Task 2 |
```

### Explicit Failure Handling (15 pts)

```markdown
## Error Protocol
- If FAILED: halt workflow, report to user, do not proceed
- Escalation: provide failure context and affected tasks
- Recovery: user must approve retry or skip
```

### Validation Criteria (15 pts)

```markdown
## Validation
- [ ] All unit tests pass
- [ ] No linting errors
- [ ] Documentation updated
- [ ] Commit message follows convention
```

### PM Role Definition (20 pts)

```markdown
## PM RULES (READ FIRST)
1. You are the PROJECT MANAGER. You coordinate subagents.
2. You MUST use subagents for each task.
3. You MUST NOT proceed to the next task until current is complete.
```

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
| Medium | 60-79 | Good structure - recommend BOTH |
| Low | 40-59 | Partial structure - recommend REBUILD |
| None | 0-39 | No orchestration - full skill application |
