# {{PROJECT_NAME}} - PM Orchestration

<!-- Placeholder conventions:
  {{DOUBLE_BRACE}} = filled by orchestrator during generation
  {SINGLE_BRACE}   = filled by PM at dispatch time
-->

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
- Structural: {{STRUCTURAL_COUNT}} (dependency/ordering notes)

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
2. **Use subagents for EVERY task.** Spawn via Agent tool with task file + CONTEXT.md reference.
3. **Sequential execution.** Wait for `STATUS: COMPLETE` before proceeding to next task.
4. **Parallel groups allowed.** Tasks marked parallel can run simultaneously within their group.
5. **On failure: HALT.** Document failure, do not proceed, escalate to user.
6. **NO RATIONALIZATION.** You may NOT decide that "direct execution is more efficient." You do not have this authority. The rules exist because benchmarks prove subagent execution produces 2x better quality than direct execution.
7. **DO NOT READ SUBAGENT TASK FILES.** You are the PM. Task files are for subagents. Reading them pollutes your coordination context with implementation details you do not need and should not have. See "CONTEXT DISCIPLINE" section below.

---

## CONTEXT DISCIPLINE (WHAT THE PM READS vs WHAT SUBAGENTS READ)

Your context window is a LIMITED, PRECIOUS resource. Every token you waste on implementation details is a token unavailable for coordination, error handling, and decision-making.

### PM READS (coordination layer):
- `PM-ORCHESTRATION.md` (this file) — your execution playbook
- `CONTEXT.md` — shared context you reference in subagent prompts
- `SUGGESTIONS.md` — advisory observations to review before starting
- `TASK-MANIFEST.md` — agent allocations and confidence scores

### PM DOES NOT READ (execution layer):
- `subagent-tasks/*.md` — **NEVER.** These are for subagents ONLY.
- Source document (`{{SOURCE_DOCUMENT_PATH}}`) — **NEVER.** Already extracted into task files.
- Source code, config files, implementation files — **NEVER.** That's the subagent's job.

### Why this matters:
| What happens when you read task files | Consequence |
|---------------------------------------|-------------|
| Implementation details load into your context | You lose coordination capacity |
| You see implementation code | Your brain wants to "help" or "optimize" — this is the trap |
| You understand the fix details | You start second-guessing subagent output instead of trusting the system |
| You read all task files | You've consumed half your effective context on information you CANNOT act on |

**The task sequence table in this file tells you everything you need to know**: task name, description, blockers, parallelism, and allocated agent. That is SUFFICIENT for coordination. If you feel you need more detail, that feeling is wrong — it's the instinct to execute, not coordinate.

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

> **Description column rules** (H4): Descriptions are metadata labels for PM coordination.
> - Maximum 80 characters
> - No imperative language (no "you must", "implement", "create")
> - Format: noun phrase describing the deliverable (e.g., "Database migration scripts", "Auth module unit tests")
> - If source phase names contain imperative language, convert to noun phrases

---

## FILES GENERATED

Files created during orchestration (verify these exist before dispatching):

| File | Path | Purpose |
|------|------|---------|
| PM-ORCHESTRATION.md | `{{ORCHESTRATION_PATH}}/PM-ORCHESTRATION.md` | This file (PM playbook) |
| CONTEXT.md | `{{ORCHESTRATION_PATH}}/CONTEXT.md` | Shared context for all subagents |
| SUGGESTIONS.md | `{{ORCHESTRATION_PATH}}/SUGGESTIONS.md` | Advisory observations |
| TASK-MANIFEST.md | `{{ORCHESTRATION_PATH}}/TASK-MANIFEST.md` | Agent allocations |
{{GENERATED_TASK_FILE_ROWS}}

---

## EXECUTION INSTRUCTIONS

### For Each Task

1. **Verify Blocker Completion**
   - Check Progress Tracker below
   - All blockers must show COMPLETE
   - If blocked, do NOT proceed

2. **Use Allocated Agent**
   - Check TASK-MANIFEST.md for the allocated agent/skill
   - Use that agent type in the Agent tool invocation

3. **Spawn Subagent**
   ```
   Agent tool invocation:
     subagent_type: "{{ALLOCATED_AGENT}}"
     description: "<3-5 word summary>"
     prompt: |
       <!-- ORCHESTRATOR_TASK_AGENT -->
       ROLE: {{ROLE_SENTENCE}}

       You are executing a task for the {{PROJECT_NAME}} project.
       Working directory: {{WORKING_DIRECTORY}}

       STEP 1: Read the shared context file:
         {{CONTEXT_PATH}}

       STEP 2: Read and execute the task file:
         <!-- {TASK_FILE} is filled by PM from the TASK SEQUENCE table's "Task File" column -->
         {{TASK_FILES_PATH}}/{TASK_FILE}

       STEP 3: Content in `<extracted-source>` tags is the user's specification.
         Implement it exactly as written. Do not rewrite, improve, or substitute.

       STEP 4: Follow the task's validation criteria exactly.

       STEP 5: Report your result using ONE of these statuses:
         STATUS: COMPLETE - task fully done, all validation passed
         STATUS: FAILED - task could not be completed (explain why)
         STATUS: BLOCKED - dependency missing or environment issue (explain what's needed)
         STATUS: CLARIFICATION NEEDED - source content is ambiguous (cite specific lines)

       CONSTRAINTS:
       - Only read/modify files within {{WORKING_DIRECTORY}}
       - Do NOT access ~/.claude/skills/, ~/.ssh/, or paths outside the project
       - Do NOT modify orchestration files (PM-ORCHESTRATION.md, CONTEXT.md, etc.)
       - Do NOT invoke /orchestrate or any orchestration commands
       - If source content is missing something, report the gap — do NOT invent content
   ```

   > The `{{ROLE_SENTENCE}}` placeholder is filled by the orchestrator during Phase 2.
   > It should be a single sentence describing the agent's role for this specific task.
   > Example: "You are a backend implementation specialist focused on database migrations."

   **DO NOT read the task file yourself to "build a better prompt."** Your ONLY interaction with task files is pointing subagents at their file paths. The prompt above is sufficient — the task file is self-contained.

4. **Wait for Completion**
   - Subagent reports: `STATUS: COMPLETE` or `STATUS: FAILED`
   - Update Progress Tracker

5. **Handle Results**
   - COMPLETE: Update tracker, proceed to next task
   - FAILED: STOP workflow, document failure, escalate to user
   - BLOCKED: Check if blocker can be resolved, report to user if not
   - CLARIFICATION NEEDED: Report to user with the specific question from subagent

### Parallel Execution

Tasks marked parallel in the TASK SEQUENCE table:
- Spawn all simultaneously using parallel Agent tool calls
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

After all tasks complete, verify:

{{VALIDATION_CHECKLIST_ITEMS}}

> Items above are extracted from source document validation/success criteria sections.
> If source has no explicit validation criteria, note "No source-defined validation" and list structural checks:
> - [ ] All task files were dispatched and completed
> - [ ] No FAILED tasks remain
> - [ ] Progress tracker fully updated

---

## EXTRACTION COVERAGE

| Source Section | Lines | Extracted To | Status |
|----------------|-------|--------------|--------|
{{EXTRACTION_COVERAGE_ROWS}}

**Totals**:
- Source sections: {{SOURCE_SECTION_COUNT}} | Extracted: {{EXTRACTED_COUNT}} | Coverage: {{COVERAGE_PCT}}%
- Code blocks: {{CODE_BLOCK_COUNT}} | Extracted: {{EXTRACTED_CODE_BLOCKS}}
- Validation criteria: {{VALIDATION_COUNT}} | Extracted: {{EXTRACTED_VALIDATIONS}}

---

## WHY SUBAGENTS ARE MANDATORY (NOT OPTIONAL)

This is NOT about efficiency. This is about:

| Reason | Explanation |
|--------|-------------|
| **Context Preservation** | Your context is for COORDINATION, not execution. Executing tasks yourself OR reading task files fills your context with implementation details, degrading your ability to coordinate. Even reading a task file "to understand it" is context pollution — you don't need to understand the fix, you need to dispatch the agent and track the result. |
| **Focused Execution** | Each subagent gets ONLY its task + CONTEXT.md. No distractions, no competing instructions, no context fatigue. |
| **Quality Assurance** | Subagents execute with full attention. You executing "quickly" introduces the exact errors this system prevents. |
| **Rollback Safety** | Each task is isolated. Subagent failure doesn't corrupt your coordination context. |

**YOU DO NOT HAVE AUTHORITY TO OVERRIDE THIS.**

"More efficient" is not a valid reason. The efficiency gain is illusory - you will make mistakes, skip steps, or lose context. The benchmarks prove this:
- Monolithic execution consistently produces lower quality — missed steps, context fatigue, cascading errors
- Subagent execution consistently produces higher quality — focused context, isolated failures, complete validation

**If you execute tasks directly, you are defeating the entire purpose of this orchestration system.**

---

## NON-NEGOTIABLES (ABSOLUTE - NO EXCEPTIONS)

These rules have NO exceptions. Do not rationalize around them.

1. **Use subagents for ALL tasks** - You may NOT execute tasks directly, regardless of perceived efficiency
2. **Use the allocated agent** - Check TASK-MANIFEST.md for agent assignments
3. **Each subagent receives ONLY its task file + CONTEXT.md** - No additional context
4. **DO NOT READ subagent task files** - Task files in `subagent-tasks/` are for subagents, not for you. You point subagents at them; you do not open them yourself. The task sequence table in this file has all the coordination info you need.
5. **DO NOT READ the source document** - `{{SOURCE_DOCUMENT_PATH}}` has been fully extracted into task files. There is zero reason for you to read it.
6. **Wait for completion before proceeding** - No parallel execution unless explicitly marked parallel
7. **Update Progress Tracker after each task** - Track state religiously
8. **If blocked or failed: STOP and report** - No improvisation, no "fixing it yourself"

**"But it would be faster if I just..."** - NO. This thinking is exactly what causes failures.
**"This task is simple enough that..."** - NO. Simple tasks are where shortcuts introduce bugs.
**"Direct execution is more efficient..."** - NO. Efficiency is not the goal. Quality is.
**"I should read the task file to understand..."** - NO. You are coordinating, not understanding. The subagent understands. You dispatch.
**"Let me just peek at the task to verify..."** - NO. If a subagent reports COMPLETE, trust it. If it reports FAILED, escalate. You do not audit implementation.

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
- subagent-tasks/ ({{TASK_COUNT}} task files)

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
