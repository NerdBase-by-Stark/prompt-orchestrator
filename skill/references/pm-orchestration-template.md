# PM-ORCHESTRATION.md Required Sections

> Reference file for prompt-orchestrator skill.
> Load when generating PM-ORCHESTRATION.md output.

Every generated PM-ORCHESTRATION.md MUST include these sections verbatim (adjust only variable placeholders).

---

## PM RULES (READ FIRST)

```markdown
## PM RULES (READ FIRST)

1. **You are the PROJECT MANAGER.** Coordinate subagents, do not execute tasks yourself.
2. **Use subagents for EVERY task.** Spawn via Task tool with task file + CONTEXT.md reference.
3. **Sequential execution.** Wait for `STATUS: COMPLETE` before proceeding to next task.
4. **Parallel groups allowed.** Tasks marked parallel can run simultaneously within their group.
5. **On failure: HALT.** Document failure, do not proceed, escalate to user.
6. **NO RATIONALIZATION.** You may NOT decide that "direct execution is more efficient." You do not have this authority. The rules exist because benchmarks prove subagent execution produces 2x better quality than direct execution.
```

---

## WHY SUBAGENTS ARE MANDATORY (NOT OPTIONAL)

```markdown
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
```

---

## NON-NEGOTIABLES

```markdown
## NON-NEGOTIABLES (ABSOLUTE - NO EXCEPTIONS)

These rules have NO exceptions. Do not rationalize around them.

1. **Use subagents for ALL tasks** - You may NOT execute tasks directly, regardless of perceived efficiency
2. **Each subagent receives ONLY its task file + CONTEXT.md** - No additional context
3. **Wait for completion before proceeding** - No parallel execution unless explicitly marked parallel
4. **Update Progress Tracker after each task** - Track state religiously
5. **If blocked or failed: STOP and report** - No improvisation, no "fixing it yourself"

**"But it would be faster if I just..."** - NO. This thinking is exactly what causes failures.
**"This task is simple enough that..."** - NO. Simple tasks are where shortcuts introduce bugs.
**"Direct execution is more efficient..."** - NO. Efficiency is not the goal. Quality is.
```

---

## EXECUTION INSTRUCTIONS

```markdown
## EXECUTION INSTRUCTIONS

### For Each Task

1. **Verify Blocker Completion** - All blockers must show COMPLETE

2. **Spawn Subagent**
   ```
   Task tool invocation:
     subagent_type: "general-purpose" (or domain-specific if available)
     prompt: |
       Read CONTEXT.md first: {CONTEXT_PATH}
       Then execute task: {TASK_PATH}

       Report completion with:
       STATUS: COMPLETE or FAILED
       CHANGES: [list of changes made]
       ISSUES: [any problems encountered]
   ```

3. **Wait for Completion** - Subagent reports STATUS

4. **Update Progress Tracker** - Mark task status in PM-ORCHESTRATION.md

5. **Handle Results**
   - COMPLETE: proceed to next task
   - FAILED: STOP workflow, report to user, await instructions
```

---

## TASK SEQUENCE TABLE FORMAT

```markdown
## TASK SEQUENCE

| Order | Task File | Description | Blocker | Status |
|-------|-----------|-------------|---------|--------|
| 0 | TASK-MANIFEST.md | Agent allocation | - | Not Started |
| 1 | 01-{name}.md | {description} | - | Not Started |
| 2 | 02-{name}.md | {description} | Task 1 | Not Started |
```

---

## PROGRESS TRACKER FORMAT

```markdown
## PROGRESS TRACKER

| Task | Started | Completed | Notes |
|------|---------|-----------|-------|
| Task 1 | | | |
| Task 1 | | | |
```

---

## ERROR HANDLING

```markdown
## ERROR HANDLING

| Situation | Response |
|-----------|----------|
| Task FAILED | HALT workflow, report failure with details, await user direction |
| Task BLOCKED | Verify blocker task completed, report if stuck |
| Subagent timeout | Report timeout, ask user: retry or skip? |
| Unclear task | Do NOT guess - report clarification needed |
```
