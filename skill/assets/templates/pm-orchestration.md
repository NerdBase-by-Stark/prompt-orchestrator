# {{PROJECT_NAME}} - PM Orchestration

> Generated: {{TIMESTAMP}}
> Complexity Score: {{COMPLEXITY_SCORE}}/100
> Total Tasks: {{TASK_COUNT}}
> Source Document: `{{SOURCE_DOCUMENT_PATH}}`

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

## AGENT ALLOCATIONS (PRE-FILLED)

Agent allocations are in `TASK-MANIFEST.md` - filled during orchestration.

| Task | Allocated Agent | Confidence |
|------|-----------------|------------|
{{ALLOCATION_SUMMARY}}

All allocations above 80% confidence. Review TASK-MANIFEST.md if you need to override.

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
{{TASK_SEQUENCE_ROWS}}

---

## EXECUTION INSTRUCTIONS

### For Each Task

1. **Verify Blocker Completion**
   - Check Progress Tracker below
   - All blockers must show COMPLETE
   - If blocked, do NOT proceed

2. **Use Allocated Agent**
   - Check TASK-MANIFEST.md for the allocated agent/skill
   - Use that agent type in the Task tool invocation

3. **Spawn Subagent**
   ```
   Task tool invocation:
     subagent_type: "{{ALLOCATED_AGENT}}"
     prompt: |
       Read CONTEXT.md: {{CONTEXT_PATH}}
       Execute task: {{TASK_PATH}}
       Report: STATUS: COMPLETE or FAILED
   ```

4. **Wait for Completion**
   - Subagent reports: `STATUS: COMPLETE` or `STATUS: FAILED`
   - Update Progress Tracker

5. **Handle Results**
   - COMPLETE: Update tracker, proceed to next task
   - FAILED: STOP workflow, document failure, escalate

### Parallel Execution

Tasks marked `Yes` in Parallel column:
- Spawn all simultaneously using parallel Task tool calls
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

1. **Use subagents for ALL tasks** - You may NOT execute tasks directly, regardless of perceived efficiency
2. **Use the allocated agent** - Check TASK-MANIFEST.md for agent assignments
3. **Each subagent receives ONLY its task file + CONTEXT.md** - No additional context
4. **Wait for completion before proceeding** - No parallel execution unless explicitly marked parallel
5. **Update Progress Tracker after each task** - Track state religiously
6. **If blocked or failed: STOP and report** - No improvisation, no "fixing it yourself"

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
