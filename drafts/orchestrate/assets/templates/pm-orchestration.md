# {{PROJECT_NAME}} - PM Orchestration

> Generated: {{TIMESTAMP}}
> Complexity Score: {{COMPLEXITY_SCORE}}/100
> Total Tasks: {{TASK_COUNT}}

---

## PM RULES (READ FIRST)

1. **You are the PROJECT MANAGER.** Coordinate subagents, do not execute tasks yourself.
2. **Use subagents for EVERY task.** Spawn via Task tool with task file + CONTEXT.md reference.
3. **Sequential execution.** Wait for `STATUS: COMPLETE` before proceeding to next task.
4. **Parallel groups allowed.** Tasks marked parallel can run simultaneously within their group.
5. **On failure: HALT.** Document failure, do not proceed, escalate to user.

---

## TASK SEQUENCE

| Order | Task File | Description | Blocker | Parallel |
|-------|-----------|-------------|---------|----------|
{{TASK_SEQUENCE_ROWS}}

---

## EXECUTION INSTRUCTIONS

### For Each Task

1. **Verify Blocker Completion**
   - Check Progress Tracker below
   - All blockers must show COMPLETE
   - If blocked, do NOT proceed

2. **Spawn Subagent**
   ```
   TaskCreate:
     subject: "Execute {{TASK_FILE}}"
     description: |
       Read CONTEXT.md: {{CONTEXT_PATH}}
       Execute task: {{TASK_PATH}}
       Report: STATUS: COMPLETE or FAILED
     activeForm: "Executing {{TASK_NAME}}"
   ```

3. **Wait for Completion**
   - Subagent reports: `STATUS: COMPLETE` or `STATUS: FAILED`
   - Update Progress Tracker

4. **Handle Results**
   - COMPLETE: Update tracker, proceed to next task
   - FAILED: STOP workflow, document failure, escalate

### Parallel Execution

Tasks marked `Yes` in Parallel column:
- Spawn all simultaneously using parallel TaskCreate calls
- Wait for ALL to complete before next group
- Any failure halts the parallel group

---

## PROGRESS TRACKER

| Task | Status | Started | Completed | Notes |
|------|--------|---------|-----------|-------|
{{PROGRESS_TRACKER_ROWS}}

**Status Values:** Not Started | In Progress | COMPLETE | FAILED | BLOCKED

---

## VALIDATION CHECKLIST

After all tasks complete:

{{VALIDATION_CHECKLIST}}

---

## NON-NEGOTIABLES

1. Use subagents for ALL tasks - never execute directly
2. Each subagent receives ONLY its task file + CONTEXT.md
3. Wait for completion before proceeding
4. Update Progress Tracker after each task
5. If blocked or failed: STOP and report - no improvisation

---

## ERROR HANDLING

### On Task Failure

1. Update Progress Tracker with FAILED status
2. Document failure reason in Notes column
3. STOP the workflow immediately
4. Report to user:

```
WORKFLOW PAUSED

Failed Task: [task file]
Reason: [failure reason from subagent]
Completed Tasks: X/Y

Options:
1. [RETRY] Retry the failed task
2. [SKIP] Skip and continue (if downstream allows)
3. [ABORT] Stop workflow, preserve progress
```

### On Timeout

If subagent does not respond within reasonable time:
1. Mark task as FAILED with reason "Timeout"
2. Follow failure procedure above

---

## FINAL OUTPUT

When workflow completes successfully:

```
ORCHESTRATION COMPLETE

STATUS: COMPLETE
Tasks Completed: {{TASK_COUNT}}/{{TASK_COUNT}}
Duration: [total time]

Files Generated:
- PM-ORCHESTRATION.md
- CONTEXT.md
- subagent-tasks/

Files Modified By Tasks:
[list from task reports]
```

When workflow fails or partially completes:

```
ORCHESTRATION INCOMPLETE

STATUS: PARTIAL | FAILED
Tasks Completed: X/{{TASK_COUNT}}
Failed Task: [task file]
Reason: [failure reason]

Progress Preserved In:
- PM-ORCHESTRATION.md (Progress Tracker updated)
```
