---
name: orchestrate
description: "Decomposes complex prompts into orchestrated multi-task workflows. This skill should be used when the user provides a complex request with multiple distinct tasks, dependencies between steps, or expected output exceeding 500 lines. Triggers include: /orchestrate, 'break this down', 'decompose this', 'orchestrate this task', or prompts containing 5+ distinct action items. Not intended for simple single-step tasks."
---

# Prompt Orchestrator

Transform complex prompts into structured, executable workflows using the PM-subagent pattern.

## Purpose

This skill addresses common failure modes in complex prompts:
- Context fatigue after ~500 lines
- Instruction neglect when too many directives compete
- Requirement omission (the primary failure mode per E2EDevBench)
- No self-verification in single-shot execution

## Generated Artifacts

| File | Purpose |
|------|---------|
| `PM-ORCHESTRATION.md` | Project manager coordination file with task sequence |
| `CONTEXT.md` | Shared context for all subagents |
| `subagent-tasks/01-verb-noun.md` | Individual task files (auto-numbered) |

## Workflow

### Phase 1: Analyze

**1.1 Extract Elements**

Parse the input prompt for:

| Element | Detection |
|---------|-----------|
| Tasks | Action verbs: create, implement, add, update, configure, test, deploy |
| Dependencies | Sequential language: "after X", "requires Y", "once Z is complete" |
| Parallel opportunities | Independent tasks sharing no state |
| Complexity signals | Nested requirements, conditionals, multi-file changes |
| Context | Project paths, technologies, constraints |

**1.2 Score Complexity**

Run the analyzer script:

```bash
python3 scripts/analyze_prompt.py --prompt "USER_PROMPT"
```

Or manually calculate:

| Factor | Points |
|--------|--------|
| Each distinct task | +5 |
| Each dependency | +3 |
| Each file to modify | +2 |
| Nested conditionals | +10 |
| External integrations | +10 |
| Testing requirements | +5 |

**1.3 Threshold Decision**

| Score | Action |
|-------|--------|
| 0-30 | Ask: "Complexity score [X]. Execute directly or decompose anyway?" |
| 31-70 | Recommend orchestration, proceed unless user declines |
| 71-100 | Strongly recommend orchestration, proceed |

### Phase 2: Generate

**2.1 Sequence Tasks**

Apply topological sort:
1. List all extracted tasks
2. Map dependencies (task A blocks task B)
3. Sort: tasks with no blockers first
4. Tag parallel opportunities (tasks sharing no blockers)

**2.2 Name Tasks**

Use pattern: `{order:02d}-{verb}-{noun}.md`

Examples:
- `01-setup-environment.md`
- `02-implement-logging.md`
- `03-add-verification.md`

**2.3 Create Files**

Load templates from `assets/templates/`:

1. **PM-ORCHESTRATION.md** from `assets/templates/pm-orchestration.md`
   - Fill task sequence table
   - Initialize progress tracker
   - Add validation checklist

2. **CONTEXT.md** from `assets/templates/context.md`
   - Set project paths
   - Extract constraints from prompt
   - Define shared state

3. **Task files** from `assets/templates/task.md`
   - One file per task in `subagent-tasks/`
   - Include specific requirements
   - Add validation criteria

**2.4 Output Location**

Default: Create in current working directory
Override: User specifies `--output /path/to/dir`

```
{output_dir}/
├── PM-ORCHESTRATION.md
├── CONTEXT.md
└── subagent-tasks/
    ├── 01-setup-environment.md
    ├── 02-implement-feature.md
    └── 03-write-tests.md
```

### Phase 3: Execute

**3.1 Task Tool Integration**

Execute each task using Claude Code's Task tool. For each task in sequence:

```
TaskCreate:
  subject: "Execute {task_filename}"
  description: |
    Read CONTEXT.md first: {context_path}
    Then execute task: {task_path}

    Report completion with:
    STATUS: COMPLETE or FAILED
    CHANGES APPLIED: [list]
    NOTES: [any issues]
  activeForm: "Executing {task_name}"
```

**3.2 Monitor Progress**

After each task completes:
1. Check for `STATUS: COMPLETE` or `STATUS: FAILED`
2. Update PM-ORCHESTRATION.md progress tracker
3. If FAILED: halt, report failure, ask user for direction
4. If COMPLETE: proceed to next task

**3.3 Parallel Execution**

When tasks have `Parallel: Yes`:
- Create all parallel tasks simultaneously
- Wait for all to complete before next group
- Any failure halts the parallel group

**3.4 Completion Report**

```
## Orchestration Complete

STATUS: COMPLETE | PARTIAL | FAILED

### Summary
- Tasks Completed: X/Y
- Files Generated: PM-ORCHESTRATION.md, CONTEXT.md, subagent-tasks/*

### Task Results
| Task | Status | Duration |
|------|--------|----------|
| 01-setup-environment | COMPLETE | ~2min |
| 02-implement-feature | COMPLETE | ~5min |

### Files Modified
[list of files created or modified by tasks]

### Issues
[none | list of issues]
```

## Invocation

```bash
# Standard usage
/orchestrate "Your complex prompt here"

# With options
/orchestrate --threshold 20 "Your prompt"       # Lower threshold
/orchestrate --output ./my-workflow "prompt"    # Custom output dir
/orchestrate --generate-only "prompt"           # Generate without execute
/orchestrate --file requirements.md             # Read prompt from file
```

## Error Handling

| Situation | Response |
|-----------|----------|
| Task FAILED | Halt workflow, report failure, offer: retry/skip/abort |
| Task BLOCKED | Verify blocker completed, report if stuck |
| Timeout | Mark as FAILED, follow failure procedure |
| Unclear requirements | Ask for clarification before generating |

## Operator Patterns

Apply when creating tasks:

| Operator | Usage |
|----------|-------|
| Generate | Creating new content, add `-generate` suffix to task name |
| Review | Self-critique step, pair with generate tasks |
| Revise | Iterative improvement, follows review |
| Test | Validation step, add `-test` suffix |
| Ensemble | Multiple approaches, pick best result |

## Resources

For detailed patterns and examples, see `references/workflow-patterns.md`.
