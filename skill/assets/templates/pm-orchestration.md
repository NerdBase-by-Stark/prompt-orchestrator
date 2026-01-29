# {{PROJECT_NAME}} - PM Orchestration

> Generated: {{TIMESTAMP}}
> Complexity Score: {{COMPLEXITY_SCORE}}/100
> Total Tasks: {{TASK_COUNT}}
> Source Document: `{{SOURCE_DOCUMENT_PATH}}`
> Execution Mode: `{{EXECUTION_MODE}}`

---

## TASK 0: AGENT ALLOCATION (MANDATORY FIRST)

**Before ANY other task**, spawn the Agent Allocator to match tasks to agents.

### Spawn Allocator

```
Task tool invocation:
  subagent_type: "general-purpose"
  prompt: |
    You are the Agent Allocator.

    Read: {{OUTPUT_DIR}}/TASK-MANIFEST.md
    Read: {{TEMPLATE_DIR}}/agent-allocator-task.md (your instructions)

    Discover available agents from your Task tool definition.
    Match capabilities to agents.
    Return updated manifest with allocations and confidence scores.
```

### After Allocator Returns

**Based on execution mode ({{EXECUTION_MODE}}):**

| Mode | Action |
|------|--------|
| `--trust-allocator` | Proceed with allocations immediately |
| `--confirm-agents` | Show full allocation list to user, await confirmation |
| `--ambiguous-only` (DEFAULT) | If no ambiguous tasks, proceed. If ambiguous exist, ask user ONLY about those. |

### User Confirmation (when needed)

```
+-----------------------------------------------------+
| Agent Allocation Complete                           |
+-----------------------------------------------------+
| [OK] {{AUTO_ASSIGNED_COUNT}} tasks auto-assigned (high confidence)       |
| [??] {{AMBIGUOUS_COUNT}} tasks need your input                       |
|                                                     |
| AMBIGUOUS:                                          |
{{AMBIGUOUS_TASK_LIST}}
|                                                     |
| [1] Use first suggestion for all                    |
| [2] Let me choose each ambiguous task               |
| [3] Review full allocation list                     |
| [4] Trust allocator, proceed                        |
+-----------------------------------------------------+
```

---

## SUGGESTIONS AVAILABLE

**Review `SUGGESTIONS.md` before executing tasks.**

The orchestrator identified {{SUGGESTION_COUNT}} observations:
- Critical: {{CRITICAL_COUNT}} (may cause task failure)
- Gaps: {{GAP_COUNT}} (missing implementation details)
- Improvements: {{IMPROVEMENT_COUNT}} (optional enhancements)

Suggestions are NOT included in task files - they are advisory only.
Address critical items before or during execution as appropriate.

---

## PM RULES (READ FIRST)

1. **You are the PROJECT MANAGER.** Coordinate subagents, do not execute tasks yourself.
2. **Use subagents for EVERY task.** Spawn via Task tool with task file + CONTEXT.md reference.
3. **Sequential execution.** Wait for `STATUS: COMPLETE` before proceeding to next task.
4. **Parallel groups allowed.** Tasks marked parallel can run simultaneously within their group.
5. **On failure: HALT.** Document failure, do not proceed, escalate to user.
6. **NO RATIONALIZATION.** You may NOT decide that "direct execution is more efficient." You do not have this authority. The rules exist because benchmarks prove subagent execution produces 2x better quality than direct execution.

---

## EXTRACTION-BASED WORKFLOW

Task files contain **EXTRACTED content** from the source document - not generated content.

**Subagent Instructions:**
- Each task file contains verbatim excerpts from the source document
- Execute the code/steps exactly as extracted - do NOT rewrite
- If source code uses specific APIs (e.g., `Log.Message()`), use those exact APIs
- If source content is unclear, report `STATUS: CLARIFICATION NEEDED`
- If source is missing something, report the gap - do NOT invent content

---

## TASK SEQUENCE

| Order | Task File | Description | Blocker | Parallel | Allocated Agent |
|-------|-----------|-------------|---------|----------|-----------------|
| 0 | (Agent Allocator) | Match tasks to agents | - | No | general-purpose |
{{TASK_SEQUENCE_ROWS}}

---

## EXECUTION INSTRUCTIONS

### Task 0: Agent Allocation (ALWAYS FIRST)

See "TASK 0: AGENT ALLOCATION" section above. This must complete before any other task.

### For Each Subsequent Task

1. **Verify Blocker Completion**
   - Check Progress Tracker below
   - All blockers must show COMPLETE
   - If blocked, do NOT proceed

2. **Use Allocated Agent**
   - Check TASK-MANIFEST.md for the allocated agent/skill
   - Use that agent type in the Task tool invocation

3. **Spawn Subagent**
   ```
   TaskCreate:
     subject: "Execute {{TASK_FILE}}"
     subagent_type: "{{ALLOCATED_AGENT}}"
     description: |
       Read CONTEXT.md: {{CONTEXT_PATH}}
       Execute task: {{TASK_PATH}}
       Report: STATUS: COMPLETE or FAILED
     activeForm: "Executing {{TASK_NAME}}"
   ```

4. **Wait for Completion**
   - Subagent reports: `STATUS: COMPLETE` or `STATUS: FAILED`
   - Update Progress Tracker

5. **Handle Results**
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
| Task 0 (Allocator) | Not Started | | | |
{{PROGRESS_TRACKER_ROWS}}

**Status Values:** Not Started | In Progress | COMPLETE | FAILED | BLOCKED

---

## VALIDATION CHECKLIST

After all tasks complete:

{{VALIDATION_CHECKLIST}}

---

## WHY SUBAGENTS ARE MANDATORY (NOT OPTIONAL)

This is NOT about efficiency. This is about:

| Reason | Explanation |
|--------|-------------|
| **Context Preservation** | Your context is for COORDINATION, not execution. Executing tasks yourself fills your context with implementation details, degrading your ability to coordinate. |
| **Focused Execution** | Each subagent gets ONLY its task + CONTEXT.md. No distractions, no competing instructions, no context fatigue. |
| **Quality Assurance** | Subagents execute with full attention. You executing "quickly" introduces the exact errors this system prevents. |
| **Rollback Safety** | Each task is isolated. Subagent failure doesn't corrupt your coordination context. |

**YOU DO NOT HAVE AUTHORITY TO OVERRIDE THIS.**

"More efficient" is not a valid reason. The efficiency gain is illusory - you will make mistakes, skip steps, or lose context. The benchmarks prove this:
- Monolithic execution: 4.9/10 quality score
- Subagent execution: 10/10 quality score

**If you execute tasks directly, you are defeating the entire purpose of this orchestration system.**

---

## NON-NEGOTIABLES (ABSOLUTE - NO EXCEPTIONS)

These rules have NO exceptions. Do not rationalize around them.

1. **Run Task 0 (Agent Allocator) FIRST** - Before any other task
2. **Use subagents for ALL tasks** - You may NOT execute tasks directly, regardless of perceived efficiency
3. **Use the allocated agent** - Check TASK-MANIFEST.md for agent assignments
4. **Each subagent receives ONLY its task file + CONTEXT.md** - No additional context
5. **Wait for completion before proceeding** - No parallel execution unless explicitly marked parallel
6. **Update Progress Tracker after each task** - Track state religiously
7. **If blocked or failed: STOP and report** - No improvisation, no "fixing it yourself"

**"But it would be faster if I just..."** - NO. This thinking is exactly what causes failures.
**"This task is simple enough that..."** - NO. Simple tasks are where shortcuts introduce bugs.
**"Direct execution is more efficient..."** - NO. Efficiency is not the goal. Quality is.

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
- SUGGESTIONS.md
- TASK-MANIFEST.md
- subagent-tasks/

Files Modified By Tasks:
[list from task reports]

Suggestions Status:
- Reviewed: [yes/no]
- Critical addressed: [count]
- Remaining: [count]
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
