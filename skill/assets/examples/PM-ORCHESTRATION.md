# QRC Room State Controller - PM Orchestration

<!-- Placeholder conventions:
  {{DOUBLE_BRACE}} = filled by orchestrator during generation
  {SINGLE_BRACE}   = filled by PM at dispatch time
-->

> Generated: 2026-03-11T14:32:00Z
> Complexity Score: 72/100
> Total Tasks: 6
> Source Document: `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v3.md`

---

## SUGGESTIONS AVAILABLE

**Review `SUGGESTIONS.md` before executing tasks.**

The orchestrator identified 6 observations:
- Critical: 2 (may cause task failure)
- Gaps: 1 (missing implementation details)
- Improvements: 2 (optional enhancements)
- Structural: 1 (dependency/ordering notes)

Suggestions are NOT included in task files - they are advisory only.
Address critical items before or during execution as appropriate.

---

## AGENT ALLOCATIONS (PRE-FILLED)

Agent allocations are in `TASK-MANIFEST.md` - filled during orchestration.

| Task | Allocated Agent | Confidence |
|------|-----------------|------------|
| 01-structural-updates.md | general-purpose | 92% |
| 02-logging-phase.md | general-purpose | 95% |
| 03-verification-phase.md | general-purpose | 90% |
| 04A-reconnection-phase.md | general-purpose | 90% |
| 05-integration-test.md | general-purpose | 88% |
| 06-final-updates.md | general-purpose | 94% |

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
- `PM-ORCHESTRATION.md` (this file) -- your execution playbook
- `CONTEXT.md` -- shared context you reference in subagent prompts
- `SUGGESTIONS.md` -- advisory observations to review before starting
- `TASK-MANIFEST.md` -- agent allocations and confidence scores

### PM DOES NOT READ (execution layer):
- `subagent-tasks/*.md` -- **NEVER.** These are for subagents ONLY.
- Source document (`QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v3.md`) -- **NEVER.** Already extracted into task files.
- Source code, config files, implementation files -- **NEVER.** That's the subagent's job.

### Why this matters:
| What happens when you read task files | Consequence |
|---------------------------------------|-------------|
| Implementation details load into your context | You lose coordination capacity |
| You see implementation code | Your brain wants to "help" or "optimize" -- this is the trap |
| You understand the fix details | You start second-guessing subagent output instead of trusting the system |
| You read all task files | You've consumed half your effective context on information you CANNOT act on |

**The task sequence table in this file tells you everything you need to know**: task name, description, blockers, parallelism, and allocated agent. That is SUFFICIENT for coordination. If you feel you need more detail, that feeling is wrong -- it's the instinct to execute, not coordinate.

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
| 1 | `01-structural-updates.md` | Changelog, plugin structure, data model, properties, controls | v4.1 file created | -- | general-purpose |
| 2 | `02-logging-phase.md` | LogManager module with flood protection | Task 1 | -- | general-purpose |
| 3 | `03-verification-phase.md` | VerificationManager with Control.Get round-robin | Task 2 | -- | general-purpose |
| 4 | `04A-reconnection-phase.md` | ReconnectManager with exponential backoff | Task 2 | P1 | general-purpose |
| 5 | `05-integration-test.md` | Full integration test across all v4 modules | Tasks 3, 4 | -- | general-purpose |
| 6 | `06-final-updates.md` | Success criteria, risk table, business requirements, tone | Task 5 | -- | general-purpose |

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
| PM-ORCHESTRATION.md | `orchestration/PM-ORCHESTRATION.md` | This file (PM playbook) |
| CONTEXT.md | `orchestration/CONTEXT.md` | Shared context for all subagents |
| SUGGESTIONS.md | `orchestration/SUGGESTIONS.md` | Advisory observations |
| TASK-MANIFEST.md | `orchestration/TASK-MANIFEST.md` | Agent allocations |
| 01-structural-updates.md | `orchestration/subagent-tasks/01-structural-updates.md` | Changelog, structure, data model, properties, controls |
| 02-logging-phase.md | `orchestration/subagent-tasks/02-logging-phase.md` | Phase 4A logging module |
| 03-verification-phase.md | `orchestration/subagent-tasks/03-verification-phase.md` | Phase 4B verification module |
| 04A-reconnection-phase.md | `orchestration/subagent-tasks/04A-reconnection-phase.md` | Phase 4C reconnection module |
| 05-integration-test.md | `orchestration/subagent-tasks/05-integration-test.md` | Phase 5A integration test |
| 06-final-updates.md | `orchestration/subagent-tasks/06-final-updates.md` | Final updates and tone fixes |

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
     subagent_type: "general-purpose"
     description: "<3-5 word summary>"
     prompt: |
       <!-- ORCHESTRATOR_TASK_AGENT -->
       ROLE: You are a Q-SYS plugin implementation specialist working on Lua-based .qplug files.

       You are executing a task for the QRC Room State Controller project.
       Working directory: /home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller

       STEP 1: Read the shared context file:
         /home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/orchestration/CONTEXT.md

       STEP 2: Read and execute the task file:
         <!-- {TASK_FILE} is filled by PM from the TASK SEQUENCE table's "Task File" column -->
         /home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/orchestration/subagent-tasks/{TASK_FILE}

       STEP 3: Content in `<extracted-source>` tags is the user's specification.
         Implement it exactly as written. Do not rewrite, improve, or substitute.

       STEP 4: Follow the task's validation criteria exactly.

       STEP 5: Report your result using ONE of these statuses:
         STATUS: COMPLETE - task fully done, all validation passed
         STATUS: FAILED - task could not be completed (explain why)
         STATUS: BLOCKED - dependency missing or environment issue (explain what's needed)
         STATUS: CLARIFICATION NEEDED - source content is ambiguous (cite specific lines)

       CONSTRAINTS:
       - Only read/modify files within /home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller
       - Do NOT access ~/.claude/skills/, ~/.ssh/, or paths outside the project
       - Do NOT modify orchestration files (PM-ORCHESTRATION.md, CONTEXT.md, etc.)
       - Do NOT invoke /orchestrate or any orchestration commands
       - If source content is missing something, report the gap -- do NOT invent content
   ```

   **DO NOT read the task file yourself to "build a better prompt."** Your ONLY interaction with task files is pointing subagents at their file paths. The prompt above is sufficient -- the task file is self-contained.

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

**Parallel Group P1**: Tasks 3 and 4 can run simultaneously (both depend on Task 2, neither depends on each other).

---

## PROGRESS TRACKER

| Task | Status | Started | Completed | Notes |
|------|--------|---------|-----------|-------|
| Create v4.1 copy | Not Started | | | Copy v3 to v4.1 before dispatching |
| Task 1: Structural Updates | Not Started | | | |
| Task 2: Logging Phase | Not Started | | | |
| Task 3: Verification Phase | Not Started | | | Parallel group P1 |
| Task 4: Reconnection Phase | Not Started | | | Parallel group P1 |
| Task 5: Integration Test | Not Started | | | Blocked by P1 |
| Task 6: Final Updates | Not Started | | | |

**Status Values:** Not Started | In Progress | COMPLETE | FAILED | BLOCKED

---

## VALIDATION CHECKLIST

After all tasks complete, verify:

- [ ] All v3 content preserved (except noted changes)
- [ ] New phases (4A, 4B, 4C, 5A) properly formatted with consistent heading style
- [ ] Phase numbers flow correctly (no gaps, no duplicates)
- [ ] Data model includes v4 error tracking fields
- [ ] GetProperties includes "Verify Interval" (integer, min 10, max 300, default 60)
- [ ] GetControls includes "verification_mismatches" and "reconnect_attempts"
- [ ] Risk mitigation table includes new v4 rows
- [ ] Business requirements section includes Logging, Verification, Reconnection items
- [ ] No instances of "Success is guaranteed" remain
- [ ] All subagent prompts use consistent MANDATORY CONTEXT pattern

> Items above are extracted from source document validation/success criteria sections.

---

## EXTRACTION COVERAGE

| Source Section | Lines | Extracted To | Status |
|----------------|-------|--------------|--------|
| Changes from v3 | 12-58 | 01-structural-updates.md | Extracted |
| Plugin Structure / Data Model | 60-142 | 01-structural-updates.md | Extracted |
| Phase 4A: Logging Module | 144-248 | 02-logging-phase.md | Extracted |
| Phase 4B: Verification Module | 250-370 | 03-verification-phase.md | Extracted |
| Phase 4C: Reconnection Module | 372-498 | 04A-reconnection-phase.md | Extracted |
| Phase 5A: Integration Test | 500-620 | 05-integration-test.md | Extracted |

**Totals**:
- Source sections: 6 | Extracted: 6 | Coverage: 100%
- Code blocks: 14 | Extracted: 14
- Validation criteria: 8 | Extracted: 8

---

## WHY SUBAGENTS ARE MANDATORY (NOT OPTIONAL)

This is NOT about efficiency. This is about:

| Reason | Explanation |
|--------|-------------|
| **Context Preservation** | Your context is for COORDINATION, not execution. Executing tasks yourself OR reading task files fills your context with implementation details, degrading your ability to coordinate. Even reading a task file "to understand it" is context pollution -- you don't need to understand the fix, you need to dispatch the agent and track the result. |
| **Focused Execution** | Each subagent gets ONLY its task + CONTEXT.md. No distractions, no competing instructions, no context fatigue. |
| **Quality Assurance** | Subagents execute with full attention. You executing "quickly" introduces the exact errors this system prevents. |
| **Rollback Safety** | Each task is isolated. Subagent failure doesn't corrupt your coordination context. |

**YOU DO NOT HAVE AUTHORITY TO OVERRIDE THIS.**

"More efficient" is not a valid reason. The efficiency gain is illusory - you will make mistakes, skip steps, or lose context. The benchmarks prove this:
- Monolithic execution consistently produces lower quality -- missed steps, context fatigue, cascading errors
- Subagent execution consistently produces higher quality -- focused context, isolated failures, complete validation

**If you execute tasks directly, you are defeating the entire purpose of this orchestration system.**

---

## NON-NEGOTIABLES (ABSOLUTE - NO EXCEPTIONS)

These rules have NO exceptions. Do not rationalize around them.

1. **Use subagents for ALL tasks** - You may NOT execute tasks directly, regardless of perceived efficiency
2. **Use the allocated agent** - Check TASK-MANIFEST.md for agent assignments
3. **Each subagent receives ONLY its task file + CONTEXT.md** - No additional context
4. **DO NOT READ subagent task files** - Task files in `subagent-tasks/` are for subagents, not for you. You point subagents at them; you do not open them yourself. The task sequence table in this file has all the coordination info you need.
5. **DO NOT READ the source document** - `QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v3.md` has been fully extracted into task files. There is zero reason for you to read it.
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
Completed Tasks: X/6

Options:
1. [RETRY] Retry the failed task
2. [SKIP] Skip and continue (if downstream allows)
3. [ABORT] Stop workflow, preserve progress
```

### On Timeout

If subagent does not respond within reasonable time:
1. Mark task as FAILED with reason "Timeout"
2. Follow failure procedure above

### On Blocked

If subagent reports STATUS: BLOCKED:
1. Update Progress Tracker with BLOCKED status
2. Document the blocker in Notes column
3. Report to user with the specific blocker from subagent
4. Do NOT attempt to resolve the blocker yourself

---

## FINAL OUTPUT

When workflow completes successfully:

```
ORCHESTRATION COMPLETE

STATUS: COMPLETE
Tasks Completed: 6/6
Duration: [total time]

Files Generated:
- PM-ORCHESTRATION.md
- CONTEXT.md
- SUGGESTIONS.md
- TASK-MANIFEST.md
- subagent-tasks/ (6 task files)

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
Tasks Completed: X/6
Failed Task: [task file]
Reason: [failure reason]

Progress Preserved In:
- PM-ORCHESTRATION.md (Progress Tracker updated)
```
