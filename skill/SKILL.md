---
name: orchestrate
description: "Decomposes complex prompts into orchestrated multi-task workflows. This skill should be used when the user provides a complex request with multiple distinct tasks, dependencies between steps, or expected output exceeding 500 lines. Triggers include: /orchestrate, 'break this down', 'decompose this', 'orchestrate this task', or prompts containing 5+ distinct action items. Not intended for simple single-step tasks."
---

# Prompt Orchestrator

**Split and organize** complex documents into structured, executable workflows using the PM-subagent pattern.

## Core Principle: EXTRACT, DON'T GENERATE

This skill is a **splitter/organizer**, NOT a generator.

| DO | DO NOT |
|----|--------|
| Identify task boundaries in source | Invent new tasks |
| Extract sections verbatim from source | Rewrite or "improve" source content |
| Preserve source code exactly | Generate new code snippets |
| Reference source line numbers/sections | Paraphrase or summarize code |
| Copy validation criteria from source | Add validation criteria not in source |
| Maintain source structure (phases, pages) | Flatten or restructure source organization |
| **Log observations in SUGGESTIONS.md** | **Inject suggestions into task files** |

## Dual Output Model

The skill produces two categories of output:

| Output Type | Purpose | Content |
|-------------|---------|---------|
| **Extraction Files** | Executable workflow | Pure verbatim content from source |
| **SUGGESTIONS.md** | Advisory observations | Skill's analysis, gaps, improvements |

This separation ensures:
- Task files remain faithful to source (subagents execute exactly what was planned)
- Analytical insights aren't lost (user can review and address before/after execution)
- No contamination of extracted content with generated suggestions

## Purpose

This skill addresses common failure modes in complex prompts:
- Context fatigue after ~500 lines
- Instruction neglect when too many directives compete
- Requirement omission (the primary failure mode per E2EDevBench)
- No self-verification in single-shot execution

**Solution**: Chop large documents into focused, manageable task files that subagents can execute with full context.

## Generated Artifacts

| File | Purpose | Content Source |
|------|---------|----------------|
| `PM-ORCHESTRATION.md` | Coordination file with task sequence | Extracted from source structure |
| `CONTEXT.md` | Shared context for all subagents | Extracted from source overview/constraints |
| `SUGGESTIONS.md` | **Advisory observations and recommendations** | **Generated analysis (NOT in task files)** |
| `subagent-tasks/*.md` | Individual task files | **VERBATIM excerpts from source** |

## Configuration Defaults

| Option | Default | Description |
|--------|---------|-------------|
| threshold | 30 | Minimum complexity score for auto-decomposition |
| output | ./ | Directory for orchestration files |
| execute | true | Execute workflow after generation |
| parallel | true | Enable parallel task detection |
| suggestions | true | Generate SUGGESTIONS.md with observations |

---

## Workflow

### Phase 1: Analyze Source Document

**1.1 Identify Document Structure**

Scan the source for structural elements:

| Element | Detection Pattern | Action |
|---------|-------------------|--------|
| Phases | `## PHASE`, `### Phase X` | Each phase becomes a task group |
| Steps | `#### Step X.Y`, numbered lists | Steps within a phase stay together |
| Code blocks | Triple backticks with content | Mark for verbatim extraction |
| Subagent prompts | `**Subagent**:`, `**Prompt**:` | Extract as task content |
| Validation | `**Success Criteria**:`, checkboxes | Extract to task validation section |
| Git commits | `git commit -m` | Mark phase boundaries |

**1.2 Map Task Boundaries**

Identify natural break points in the source:

1. **Phase boundaries** - Major sections become task groups
2. **Subagent prompts** - Each prompt in source = one task file
3. **Validation checkpoints** - Natural completion points
4. **Git commits** - Rollback points indicate task completion

**1.3 Collect Observations (for SUGGESTIONS.md)**

While analyzing, note potential issues **WITHOUT modifying extractions**:

| Observation Type | What to Log | Example |
|------------------|-------------|---------|
| **API Concerns** | Wrong or outdated API usage | "Line 42: `print()` used - Q-SYS requires `Log.Message()`" |
| **Missing Details** | Mentioned but not specified | "Line 156: 'if auth required' - Logon implementation not provided" |
| **Scope Issues** | Variable/timer scoping problems | "Line 230: Timer declared local - may be garbage collected" |
| **Structure Gaps** | Incomplete implementations | "Multi-page UI described but page transition logic missing" |
| **Error Handling** | Missing error scenarios | "No error handling for socket disconnect" |
| **Dependencies** | Unclear or missing task ordering | "Task 3 may need Task 5's output" |
| **Inconsistencies** | Contradictions in source | "Line 100 says 34 rooms, line 500 says 'all 40 rooms'" |

**CRITICAL**: These observations go ONLY in SUGGESTIONS.md, NEVER in task files.

**1.4 Score Complexity**

| Factor | Points |
|--------|--------|
| Each phase/major section | +10 |
| Each subagent prompt in source | +5 |
| Each code block to extract | +2 |
| Total source lines | +1 per 100 lines |
| Dependencies between sections | +3 each |

**1.5 Threshold Decision**

| Score | Action |
|-------|--------|
| 0-30 | Ask: "Complexity score [X]. Execute directly or decompose anyway?" |
| 31-70 | Recommend orchestration, proceed |
| 71+ | Strongly recommend orchestration, proceed |

---

### Phase 2: Extract and Organize

**2.1 Create Task Boundaries**

For each identified task boundary:
1. Note the source line range (e.g., lines 150-280)
2. Identify the section header
3. List code blocks within that range
4. Note dependencies (what must complete first)

**2.2 Name Tasks**

Use pattern: `{order:02d}-{verb}-{noun}.md`

Extract verb/noun from source section headers:
- Source: "## PHASE 2: QRC CONNECTION MODULE" → `02-implement-qrc-connection.md`
- Source: "#### Step 3.2: Add Room Management Controls" → `03-add-room-controls.md`

**2.3 Create Extraction Files**

**PM-ORCHESTRATION.md**:
- Task sequence table with source line references
- Dependencies from source structure
- Progress tracker
- Link to source document

**CONTEXT.md**:
- Project paths from source
- Technologies mentioned in source
- Constraints from source
- **Copy source's "Executive Summary" or "Overview" section verbatim**

**Task Files** (CRITICAL - extraction only):
```markdown
# Task: {name}

## Source Reference
**Document**: {source_path}
**Section**: {section_header}
**Lines**: {start_line}-{end_line}

## Extracted Content

{VERBATIM_COPY_OF_SOURCE_SECTION}

## Validation Criteria (from source)

{VERBATIM_COPY_OF_SOURCE_VALIDATION}

## Output Format
[standard completion format]
```

**2.4 Create SUGGESTIONS.md**

Compile all observations from Phase 1.3:

```markdown
# Orchestrator Suggestions

> **ADVISORY ONLY** - These observations are NOT included in task files.
> The extracted tasks contain exactly what the source specified.
> Review these suggestions and address as appropriate.

Generated: {timestamp}
Source: {source_document}
Lines Analyzed: {line_count}

---

## Critical (May Cause Task Failure)

Issues that could prevent successful task execution:

| Line | Category | Observation | Affected Task |
|------|----------|-------------|---------------|
| 42 | API | `print()` used - Q-SYS requires `Log.Message()` | 05-implement-logging |
| 230 | Scope | Timer declared local - will be garbage collected | 04-command-timer |

---

## Gaps (Missing Implementation Details)

Items mentioned but not fully specified in source:

| Line | Topic | What's Missing | Affected Task |
|------|-------|----------------|---------------|
| 156 | Auth | "if auth required" - no Logon command format provided | 02-qrc-connection |
| 890 | UI | Multi-page layout - page switching logic not specified | 08-ui-layout |

---

## Inconsistencies

Contradictions or unclear specifications in source:

| Lines | Issue |
|-------|-------|
| 100, 500 | Room count: "34 rooms" vs "all 40 rooms" |
| 200, 450 | Control naming: "room_enabled" vs "room_enable" |

---

## Improvement Opportunities

Optional enhancements not in source (implement only if user requests):

| Context | Suggestion |
|---------|------------|
| Line 450 | Consider retry logic for failed QRC commands |
| Line 720 | Error messages could include control name for debugging |
| General | No persistence strategy - consider Snapshots |

---

## Structural Notes

Observations about task ordering and dependencies:

- Phase 4 uses output from Phase 2 but no explicit dependency stated
- Consider: Task 08 (UI) could run parallel with Task 07 (reconnection)
- Validation in Phase 3 references controls defined in Phase 5

---

## Summary

| Category | Count | Action |
|----------|-------|--------|
| Critical | {n} | Address before execution |
| Gaps | {n} | May need clarification |
| Inconsistencies | {n} | Resolve with user |
| Improvements | {n} | Optional |
| Structural | {n} | Consider reordering |

**Recommendation**: Review Critical items before executing tasks.
```

**2.5 Extraction Rules**

| Source Element | Extraction Method |
|----------------|-------------------|
| Section text | Copy verbatim, preserve formatting |
| Code blocks | Copy exactly, including comments |
| Subagent prompts | Copy the entire prompt block |
| Validation criteria | Copy checkboxes and criteria |
| Commands | Copy bash/shell commands exactly |
| Tables | Copy complete tables |

**NEVER in task files**:
- Summarize code blocks
- "Clean up" or reformat source content
- Add explanations not in source
- Change variable names or patterns
- Substitute APIs
- Include suggestions or observations (those go in SUGGESTIONS.md)

**2.6 Output Location**

```
{output_dir}/
├── PM-ORCHESTRATION.md      # Coordination (extracted)
├── CONTEXT.md               # Shared context (extracted)
├── SUGGESTIONS.md           # Advisory observations (generated)
├── {source_document}.md     # Copy of source (optional)
└── subagent-tasks/
    ├── 01-phase-one-task.md   # Extracted
    ├── 02-phase-two-task.md   # Extracted
    └── ...
```

---

### Phase 3: Execute

**3.1 Pre-Execution Review**

Before executing, present summary to user:

```
## Orchestration Generated

Source: {source_path}
Tasks: {n} task files extracted
Suggestions: {m} observations logged

### Critical Observations ({count})
{list top 3 critical items from SUGGESTIONS.md}

### Options
[REVIEW] View full SUGGESTIONS.md before proceeding
[PROCEED] Execute tasks as extracted from source
[ABORT] Cancel execution
```

**3.2 Task Tool Integration**

Execute each task using Claude Code's Task tool:

```
TaskCreate:
  subject: "Execute {task_filename}"
  description: |
    Read CONTEXT.md first: {context_path}
    Then execute task: {task_path}

    The task file contains EXTRACTED content from the source plan.
    Implement exactly as specified - do not modify patterns or APIs.

    Report completion with:
    STATUS: COMPLETE or FAILED
    CHANGES APPLIED: [list]
    NOTES: [any issues]
  activeForm: "Executing {task_name}"
```

**3.3 Monitor Progress**

After each task completes:
1. Check for `STATUS: COMPLETE` or `STATUS: FAILED`
2. Update PM-ORCHESTRATION.md progress tracker
3. If FAILED: halt, report failure, ask user for direction
4. If COMPLETE: proceed to next task

**3.4 Parallel Execution**

When source structure allows parallel tasks:
- Create all parallel tasks simultaneously
- Wait for all to complete before next group
- Any failure halts the parallel group

**3.5 Completion Report**

```
## Orchestration Complete

STATUS: COMPLETE | PARTIAL | FAILED

### Summary
- Tasks Completed: X/Y
- Source Document: {path}
- Files Generated: PM-ORCHESTRATION.md, CONTEXT.md, SUGGESTIONS.md, subagent-tasks/*

### Task Results
| Task | Source Section | Status |
|------|----------------|--------|
| 01-setup | Phase 1 (lines 155-300) | COMPLETE |
| 02-connect | Phase 2 (lines 301-590) | COMPLETE |

### Suggestions Status
SUGGESTIONS.md contains {N} observations.
- Critical: {n} (review recommended)
- Gaps: {n}
- Improvements: {n}

### Files Modified
[list of files created or modified by tasks]

### Issues
[none | list of issues encountered during execution]
```

---

## Invocation

```bash
# Standard usage - from file (recommended)
/orchestrate --file implementation-plan.md

# From inline prompt (for shorter content)
/orchestrate "Your complex prompt here"

# With options
/orchestrate --threshold 20 --file plan.md       # Lower threshold
/orchestrate --output ./workflow --file plan.md  # Custom output dir
/orchestrate --generate-only --file plan.md      # Generate without execute
/orchestrate --no-suggestions --file plan.md     # Skip SUGGESTIONS.md
```

---

## Error Handling

| Situation | Response |
|-----------|----------|
| Task FAILED | Halt workflow, report failure, offer: retry/skip/abort |
| Task BLOCKED | Verify blocker completed, report if stuck |
| Source section unclear | Include full section, note in SUGGESTIONS.md |
| Missing source content | Note gap in SUGGESTIONS.md, extract what exists |

---

## Anti-Patterns (MUST AVOID)

### 1. Injecting Suggestions into Task Files

**WRONG**: Task file contains "Note: Consider using Log.Message() instead of print()"

**RIGHT**: Task file has source code exactly. SUGGESTIONS.md notes the print() concern.

### 2. Summarizing Sections

**WRONG**: Source has 50-line subagent prompt. Task file says "Implement the logging module".

**RIGHT**: Task file contains the complete 50-line prompt from source.

### 3. Adding Requirements

**WRONG**: Source doesn't mention error handling. Task file adds "implement comprehensive error handling".

**RIGHT**: Task file only contains what source specifies. SUGGESTIONS.md notes "No error handling specified".

### 4. Restructuring

**WRONG**: Source has 3-page UI layout. Task file creates "simplified single-page layout".

**RIGHT**: Task file extracts each page's layout exactly as specified in source.

### 5. Pattern Substitution

**WRONG**: Source uses `print()`. Task file "fixes" it to `Log.Message()`.

**RIGHT**: Task file preserves `print()` exactly. SUGGESTIONS.md notes "print() should be Log.Message()".

---

## Extraction Examples

### Example 1: Code Block with Issue

**Source (lines 450-470)**:
```lua
function LogError(message)
  print("[ERROR] " .. message)  -- Wrong API for Q-SYS
end
```

**Task File** (pure extraction):
```markdown
## Implementation (source lines 450-470)

```lua
function LogError(message)
  print("[ERROR] " .. message)  -- Wrong API for Q-SYS
end
```
```

**SUGGESTIONS.md** (observation):
```markdown
| 451 | API | `print()` used for error logging - Q-SYS requires `Log.Error()` | 05-implement-logging |
```

### Example 2: Missing Implementation

**Source (line 156)**:
```
Connected: Log, set status=0 (OK), connected=true, send Logon if auth required
```

**Task File** (extract what exists):
```markdown
## Socket Connected Handler (source line 156)

Connected: Log, set status=0 (OK), connected=true, send Logon if auth required
```

**SUGGESTIONS.md** (note the gap):
```markdown
| 156 | Gap | "send Logon if auth required" - Logon command format/sequence not specified | 02-qrc-connection |
```

### Example 3: Subagent Prompt Extraction

**Source (lines 200-240)**:
```
**Subagent**: `qsys-plugin-development` skill

**Prompt**:
MANDATORY CONTEXT: Read /home/spark-bitch/CLAUDE.md before proceeding.

PROJECT: QRC Room State Controller

TASK: Create plugin skeleton file...
[40 more lines of detailed requirements]
```

**Task File** (complete extraction):
```markdown
## Subagent Instructions (source lines 200-240)

**Skill**: `qsys-plugin-development`

**Prompt**:

MANDATORY CONTEXT: Read /home/spark-bitch/CLAUDE.md before proceeding.

PROJECT: QRC Room State Controller

TASK: Create plugin skeleton file...
[ALL 40 lines copied verbatim - no summarization]
```

---

## Resources

For detailed patterns and examples, see:
- `references/workflow-patterns.md` - Workflow patterns and best practices
- `assets/templates/` - Templates for generated files
- `assets/examples/` - Working examples from real projects
