# QRC Room State Controller - PM Orchestration

## PM RULES (READ FIRST)

1. **You are the PROJECT MANAGER. You coordinate subagents.**
2. **You MUST use subagents for each CHANGE task.**
3. **You MUST NOT proceed to the next task until the current task is complete.**
4. **Each subagent receives ONLY its task file + CONTEXT.md reference.**

---

## WORKFLOW

### Step 1: Create v4.1 from v3

```bash
cp QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v3.md \
   QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v4.1.md
```

### Step 2: Execute Tasks in Sequence

Spawn subagents for each task, waiting for completion before proceeding.

---

## TASK SEQUENCE

| Order | Task File | Description | Blocker |
|-------|-----------|-------------|---------|
| 1 | `structural-updates.md` | CHANGES 1-5: Add changelog, update structure, data model, properties, controls | v4.1 file created |
| 2 | `4A-logging-phase.md` | CHANGE 6: Add Phase 4A section | Task 1 complete |
| 3 | `4B-verification-phase.md` | CHANGE 7: Add Phase 4B section | Task 2 complete |
| 4 | `4C-reconnection-phase.md` | CHANGE 8: Add Phase 4C section | Task 3 complete |
| 5 | `5A-integration-phase.md` | CHANGE 9: Add Phase 5A section | Task 4 complete |
| 6 | `final-updates.md` | CHANGES 10-13: Update success criteria, risk table, business requirements, tone | Task 5 complete |

---

## WHEN A SUBAGENT COMPLETES

1. **Read the subagent's output** - look for `STATUS: COMPLETE` or `STATUS: FAILED`
2. **If COMPLETE**: Proceed to next task
3. **If FAILED**: Do NOT proceed. Document the failure and escalate.

---

## VALIDATION AFTER ALL TASKS

1. Verify all v3 content preserved (except noted changes)
2. Verify new sections properly formatted
3. Verify phase numbers flow correctly
4. Verify subagent prompts use consistent template
5. Verify table of contents/navigation updated if present

---

## PROGRESS TRACKER

| Task | Status | Notes |
|------|--------|-------|
| Create v4.1 copy | ✅ Complete | v4.1 copied from v3 |
| Task 1: Structural Updates | ✅ Complete | CHANGES 1-5 applied (changelog, structure, data model, props, controls) |
| Task 2: Phase 4A | ✅ Complete | Logging module with flood protection added |
| Task 3: Phase 4B | ✅ Complete | State verification module added |
| Task 4: Phase 4C | ✅ Complete | Reconnection module with exponential backoff added |
| Task 5: Phase 5A | ✅ Complete | Full integration test phase added |
| Task 6: Final Updates | ✅ Complete | CHANGES 10-13 applied (success criteria, risk table, business reqs, tone) |
| Validation | ✅ Complete | v3→v4.1: 1960→2713 lines, all phases flow correctly |

Update status: ⬜ Not Started → 🔄 In Progress → ✅ Complete → ❌ Failed

---

## NON-NEGOTIABLES

1. You MUST use subagents for all tasks.
2. Each subagent gets ONLY its specific task file.
3. Wait for completion before proceeding to next task.
4. If blocked, STOP and report. Do not improvise.

---

## OUTPUT

Complete v4.1 markdown file with all changes incorporated, ready for execution.
