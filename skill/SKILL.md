---
name: orchestrate
description: "Decomposes complex prompts into orchestrated multi-task workflows. This skill should be used when the user provides a complex request with multiple distinct tasks, dependencies between steps, or expected output exceeding 500 lines. Triggers include: /orchestrate, 'break this down', 'decompose this', 'orchestrate this task', or prompts containing 5+ distinct action items. Not intended for simple single-step tasks."
---

# Prompt Orchestrator

**Split and organize** complex documents into structured, executable workflows using the PM-subagent pattern.

---

## Execution Model (MANDATORY SELF-CHECK)

**STOP. Before doing ANYTHING else, perform this check:**

### Am I Running in User's Main Context?

If you are executing this skill in the user's main conversation (not as a spawned subagent):

1. **DO NOT** read the source document
2. **DO NOT** analyze anything
3. **DO NOT** create any files
4. **IMMEDIATELY** spawn yourself as a subagent:

```
Task tool:
  subagent_type: "general-purpose"
  prompt: |
    Execute the prompt-orchestrator skill.
    Source: {source_file_or_prompt}
    Output: {output_directory}

    Read the skill at ~/.claude/skills/prompt-orchestrator/SKILL.md
    Follow all phases. Return results when complete.
```

5. **STOP** after spawning. Return ONLY the subagent's results.
6. **DO NOT** narrate "I will spawn a subagent" and then continue working.

### Why This Matters

| Principle | Implementation |
|-----------|----------------|
| Context Preservation | Orchestration work happens in isolated subagent context |
| Clean Handoff | User's main context receives only the results summary |
| No Context Pollution | Decomposition never consumes user's primary context |

### WRONG vs RIGHT

**WRONG** (what you did):
```
"Let me spawn this as a subagent to preserve your context..."
[Reads file]
[Analyzes]
[Creates files]
[Continues working in main context]
```

**RIGHT** (what you must do):
```
[Uses Task tool to spawn subagent]
[STOPS]
[Returns only subagent's result when complete]
```

**The skill saying "I will spawn a subagent" is NOT the same as actually spawning one.**

---

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
| `TASK-MANIFEST.md` | **Task capability mapping for Agent Allocator** | **Generated from task analysis** |
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

### Phase 0: Detect Existing PM Orchestration

Before analyzing the source document, check if it already contains PM orchestration structure.

**0.1 PM Orchestration Detection Scoring**

Scan the source document and score each signal:

| Signal | Points | Detection Pattern |
|--------|--------|-------------------|
| PM/Coordinator role definition | 20 | "You are the PM", "coordinator", "orchestrate", "project manager" in headings/instructions |
| Task sequence table | 20 | Markdown table with Order/Task columns, numbered lists with task names |
| Dependencies stated | 15 | "blocked by", "requires", "after", "depends on", dependency column |
| Validation/completion criteria | 15 | "success criteria", "validation", "verify", checkboxes per task |
| Progress tracking | 15 | Status column, "Not Started/In Progress/Complete", progress tracker section |
| Error handling instructions | 15 | "if failed", "on error", "escalate", failure handling |

**Maximum Score: 100 points**

**0.2 Threshold Interpretation**

| Score | Interpretation | Action |
|-------|----------------|--------|
| 60-100 | Good orchestration detected | Present user choice (0.3) |
| 40-59 | Orchestration present but could be improved | Present user choice (0.3) |
| 0-39 | No significant orchestration | Proceed to Phase 1 (full orchestration) |

**0.3 User Choice Flow (Score 40+)**

When existing orchestration is detected, present a hold message and user choice:

**Hold Message (Stargate themed):**
```
===============================================
 UNSCHEDULED OFFWORLD ACTIVATION
===============================================

Existing orchestration structure detected in source document.
Verifying IDC before proceeding...

Orchestration Score: {score}/100

Signals Detected:
- {signal_1}: {points} pts
- {signal_2}: {points} pts
...

===============================================
```

**Present AskUserQuestion with options:**

| Option | Code | Description |
|--------|------|-------------|
| **USE AS-IS** | "The iris is open" | Extract and split using existing PM structure from source |
| **REBUILD** | "Dial new coordinates" | Replace source orchestration with skill's optimized structure |
| **BOTH** | "Establish secondary gate" | Keep original + create PM-ORCHESTRATION-SUGGESTED.md |

**Option Behaviors:**

- **USE AS-IS**: Extract the existing PM orchestration structure, create task files based on the source's defined task sequence, preserve source validation criteria and dependencies.

- **REBUILD**: Ignore source orchestration, apply full Phase 1 analysis, generate new optimized PM-ORCHESTRATION.md and task structure.

- **BOTH**: Extract source structure into standard files, ALSO create PM-ORCHESTRATION-SUGGESTED.md with skill's recommended improvements, note differences in SUGGESTIONS.md.

---

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

**2.1.1 Semantic Content Bundling (MANDATORY)**

Before finalizing task boundaries, perform a **full-document semantic scan** to identify ALL content related to each task, regardless of where it appears in the source document.

**Why This Matters**

Literal section boundaries capture only the primary content. Related content (backup procedures, rollback plans, data migration, prerequisites) often appears in separate sections but is ESSENTIAL for task execution. Missing this content causes task failures.

| Extraction Type | Result | Risk |
|-----------------|--------|------|
| Literal only | 42 lines (Phase 1 only) | Task lacks rollback, backup, data handling |
| Semantic bundle | 148 lines (Phase 1 + related) | Self-contained, executable task |

**Semantic Scan Process**

For EACH task boundary, scan the ENTIRE source document for these patterns:

| Pattern | Keywords to Search | Relationship |
|---------|-------------------|--------------|
| Backup/Restore | "backup", "restore", "snapshot", "preserve" | Safety net for destructive operations |
| Rollback | "rollback", "revert", "undo", "recover", "if failed" | Recovery path |
| Data Migration | "migrate", "transfer", "export", "import", "move data" | Data dependencies |
| Prerequisites | "before you begin", "prerequisites", "requirements", "first" | Setup requirements |
| Validation | "verify", "test", "confirm", "check", "validate" | Completion criteria |
| Error Handling | "if error", "exception", "failure", "fallback" | Failure paths |

**Bundling Rules**

1. **Destructive operations MUST include rollback**: DELETE, DROP, REMOVE, ARCHIVE, WIPE, CLEAR → bundle rollback section
2. **Data operations MUST include migration plan**: Database, file, or state changes → bundle backup/migration sections
3. **Setup tasks MUST include prerequisites**: Archive/setup → bundle prerequisite checks
4. **Distance is irrelevant**: Content at line 900 is as essential as content at line 50

**Bundling Decision Heuristic**

Ask: "If a subagent executes ONLY this extracted content, can they safely complete the task AND recover from failure?"

- If NO → Find and bundle the missing pieces
- If YES → Extraction is complete

**Example: Archive/Setup Task**

**WRONG** (literal extraction):
```
Source: Phase 1 (lines 50-92) = 42 lines
Missing: Backup commands (200-215), Rollback plan (450-465), Data migration (310-340)
Result: Subagent cannot recover from failure
```

**RIGHT** (semantic bundling):
```
Primary: Phase 1 (lines 50-92)
+ Related: Backup Procedures (lines 200-215)
+ Related: Rollback Plan (lines 450-465)
+ Related: Data Migration (lines 310-340)
Total: 148 lines - complete, self-contained
```

**2.2 Name Tasks**

Use pattern: `{order:02d}-{verb}-{noun}.md`

Extract verb/noun from source section headers:
- Source: "## PHASE 2: QRC CONNECTION MODULE" → `02-implement-qrc-connection.md`
- Source: "#### Step 3.2: Add Room Management Controls" → `03-add-room-controls.md`

**2.3 Create Extraction Files**

**PM-ORCHESTRATION.md** (MUST use template structure from `assets/templates/pm-orchestration.md`):
- **REQUIRED SECTIONS** (must appear in every output):
  - PM RULES (READ FIRST) - defines PM role and subagent requirement
  - TASK SEQUENCE table with source line references
  - EXECUTION INSTRUCTIONS - includes Task tool spawn example
  - PROGRESS TRACKER
  - NON-NEGOTIABLES - enforces subagent usage
  - ERROR HANDLING
- Dependencies from source structure
- Link to source document

**TASK-MANIFEST.md** (use template: `assets/templates/task-manifest.md`):
- One row per task file generated
- Capabilities: inferred from task content using Capability Inference Rules (see below)
- User-Specified Agent: if source prompt explicitly names an agent for a task
- Allocated Agent: left as "pending" - filled by Agent Allocator (Task 0)
- Confidence: left as "pending" - filled by Agent Allocator
- Execution mode flag (default: `--ambiguous-only`)

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

**Primary Section**: {main_header}
- Lines: {start}-{end}
- Purpose: {what this section provides}

**Related Sections** (from semantic scan):

| Section | Lines | Relationship | Why Bundled |
|---------|-------|--------------|-------------|
| {header} | {A}-{B} | {type} | {reason} |

**Total Lines Extracted**: {sum}

---

## Extracted Content

### {Primary Section Header}

{VERBATIM_COPY_OF_PRIMARY_SECTION}

### {Related Section 1 Header}

{VERBATIM_COPY_OF_RELATED_SECTION}

---

## Validation Criteria (from source)

{VERBATIM_COPY_OF_SOURCE_VALIDATION}

---

## Extraction Certification

- [ ] Self-contained: Subagent can complete with only this file
- [ ] Rollback included: Yes/No/N/A (required if destructive)
- [ ] Backup included: Yes/No/N/A (required if data operation)
- [ ] Prerequisites included: Yes
- [ ] Line count: {N} lines (flag if < 50)
- [ ] Semantic scan performed: Yes

## Output Format
[standard completion format]
```

**2.4 Capability Inference Rules**

When generating TASK-MANIFEST.md, infer capabilities from task content:

| Content Pattern | Capability Tag |
|-----------------|----------------|
| Lua code, Q-SYS APIs, Controls | `lua`, `q-sys` |
| Test, validation, verify, assertion | `testing` |
| UI, layout, components, pages, UCI | `frontend`, `ui` |
| API, HTTP, sockets, networking, WebSocket | `networking`, `api` |
| Auth, login, credentials, Logon | `auth`, `security` |
| File operations, scaffolding, mkdir | `file-ops` |
| Database, storage, persistence | `database` |
| Documentation, comments, README | `documentation` |
| Refactoring, cleanup, restructuring | `refactoring` |
| Config, environment, settings | `config` |
| CI/CD, deployment, Docker, build | `devops` |

**Rules:**
- Tag ALL relevant capabilities per task (usually 2-4 tags)
- If task mentions specific skill (e.g., "use qsys-plugin-development"), note as User-Specified Agent
- Capabilities are used by Agent Allocator (Task 0) to match tasks to best available agents
- When uncertain, use broader tags (e.g., `lua` rather than `lua-advanced`)

**2.5 PM-ORCHESTRATION.md Required Sections**

Every generated PM-ORCHESTRATION.md MUST include these sections verbatim (adjust only variable placeholders):

---

**PM RULES (READ FIRST)**

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

**WHY SUBAGENTS ARE MANDATORY (NOT OPTIONAL)**

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

**NON-NEGOTIABLES**

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

**EXECUTION INSTRUCTIONS**

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

**CRITICAL**: Without these sections, the PM may execute tasks directly instead of spawning subagents, defeating the purpose of the orchestration.

---

**2.6 Create SUGGESTIONS.md**

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

**2.7 Extraction Rules**

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

**2.7.1 Extraction Completeness Check (MANDATORY)**

Before finalizing EACH task file, verify this checklist. ALL items must pass.

**Completeness Checklist**

| Check | Question | If NO |
|-------|----------|-------|
| Self-Containment | Can subagent complete with ONLY this file + CONTEXT.md? | Bundle missing dependencies |
| Rollback Coverage | If task fails, does extraction include recovery steps? | Find and bundle rollback section |
| Backup Inclusion | If task modifies data, does extraction include backup? | Find and bundle backup section |
| Prerequisites | Does extraction include "before you begin" requirements? | Find and bundle prerequisites |
| Validation | Does extraction include completion verification? | Find and bundle validation criteria |

**Line Count Heuristic**

| Lines | Assessment | Action |
|-------|------------|--------|
| < 30 | Almost certainly incomplete | STOP - Re-scan entire source |
| 30-50 | Likely incomplete | Verify ALL checklist items |
| 50-100 | Possibly complete | Normal verification |
| 100+ | Likely complete | Check not over-bundled |

**Under 50 Lines = Automatic Re-scan Trigger**

If extraction yields < 50 lines:
1. STOP and re-read ENTIRE source document
2. Search for ALL semantic patterns (section 2.1.1)
3. Verify every checklist item passes
4. Document why extraction is genuinely small OR bundle additional content

**Destructive Operation Flag**

If task contains ANY of: `DELETE, DROP, REMOVE, TRUNCATE, ARCHIVE, WIPE, CLEAR, PURGE, RESET`

Then MANDATORY:
1. Search entire source for: rollback, restore, backup, undo, revert, recover
2. Bundle ALL matching sections
3. If no rollback exists in source → note as CRITICAL gap in SUGGESTIONS.md

**2.8 Output Location**

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

### 6. PM Executing Tasks Directly

**WRONG**: PM-ORCHESTRATION.md has task list but PM reads tasks and executes them itself.

**WRONG**: PM decides "direct execution is more efficient" and executes tasks itself.

**WRONG**: PM says "for straightforward code implementation, direct execution is more efficient."

**WRONG**: PM asks "Would you prefer I use subagents or continue directly?" (The answer is ALWAYS subagents.)

**RIGHT**: PM spawns subagents via Task tool for EVERY task, regardless of perceived complexity or efficiency.

The PM's job is COORDINATION. The moment you start executing, you've abandoned your role.

### 7. Narrow Extraction

**Definition**: Extracting only literal section boundaries while ignoring semantically related content elsewhere in the source.

**WRONG** (literal boundary only):
```markdown
## Source Reference
**Section**: Phase 1: Archive/Setup (lines 50-92)

[Only 42 lines extracted]

Problems:
- No backup commands (exist at lines 200-215)
- No restore procedures (exist at lines 450-465)
- Subagent cannot recover from failure
```

**RIGHT** (semantic bundling):
```markdown
## Source Reference
**Primary Section**: Phase 1: Archive/Setup (lines 50-92)
**Related Sections**:
| Section | Lines | Relationship |
|---------|-------|--------------|
| Backup Procedures | 200-215 | Pre-execution safety |
| Rollback Plan | 450-465 | Failure recovery |

**Total Lines Extracted**: 148

[All 148 lines from primary + related sections]

Result: Self-contained, subagent can backup and recover
```

**Detection**: This anti-pattern is likely when:
- Extracted task < 50 lines for a substantive phase
- Task involves destructive operations but no rollback in extraction
- Source has "Backup", "Rollback", or "Recovery" sections that weren't bundled

**Mantra**: "Extract the TASK, not the SECTION. A task includes everything needed to complete it safely."

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

---

## Good PM Orchestration Reference

This section defines what constitutes well-structured PM orchestration for detection scoring.

### Essential Elements

| Element | Purpose | Required For Good Score |
|---------|---------|------------------------|
| Clear role definition | Distinguish PM from worker agents | "You are the PM", "coordinate subagents" |
| Task sequence with ordering | Explicit execution order | Numbered list or Order column |
| Dependencies between tasks | Prevent out-of-order execution | "blocked by", "requires", dependency column |
| Validation criteria per task | Verify completion | Checkboxes, "success criteria" section |
| Progress tracking mechanism | Monitor workflow state | Status column with states |
| Failure handling instructions | Graceful degradation | "if FAILED", "on error", escalation |

### Good Examples

**Task Sequence Table (20 pts)**
```markdown
| Order | Task File | Description | Blocker |
|-------|-----------|-------------|---------|
| 1 | 01-setup-env.md | Configure environment | - |
| 2 | 02-implement-core.md | Build core module | Task 1 |
| 3 | 03-add-tests.md | Write test suite | Task 2 |
```

**Progress Tracker with Status (15 pts)**
```markdown
| Task | Status | Notes |
|------|--------|-------|
| Task 1 | Complete | Env configured |
| Task 2 | In Progress | 60% done |
| Task 3 | Not Started | Blocked by Task 2 |
```

**Explicit Failure Handling (15 pts)**
```markdown
## Error Protocol
- If FAILED: halt workflow, report to user, do not proceed
- Escalation: provide failure context and affected tasks
- Recovery: user must approve retry or skip
```

**Validation Criteria (15 pts)**
```markdown
## Validation
- [ ] All unit tests pass
- [ ] No linting errors
- [ ] Documentation updated
- [ ] Commit message follows convention
```

**PM Role Definition (20 pts)**
```markdown
## PM RULES (READ FIRST)
1. You are the PROJECT MANAGER. You coordinate subagents.
2. You MUST use subagents for each task.
3. You MUST NOT proceed to the next task until current is complete.
```

### Weak Examples (Low Scores)

**Numbered list without dependencies (5 pts max)**
```markdown
1. Setup environment
2. Implement core
3. Add tests
```
*Missing: blockers, validation, failure handling, status tracking*

**Vague instructions (0-10 pts)**
```markdown
Do these tasks in order:
- Build the thing
- Test it
- Deploy
```
*Missing: everything essential*

**No validation criteria (loses 15 pts)**
```markdown
| Task | Description |
|------|-------------|
| Setup | Configure environment |
| Build | Implement feature |
```
*Missing: how to know when complete*

**No failure handling (loses 15 pts)**
```markdown
Execute tasks 1-5 in sequence.
```
*What happens if task 3 fails? Undefined behavior.*

### Scoring Heuristics

When evaluating source documents:

1. **Role definition** - Look in first 50 lines for PM/coordinator language
2. **Task sequence** - Search for markdown tables with "Task", "Order", numbered headers
3. **Dependencies** - Scan for "block", "require", "after", "depend" keywords
4. **Validation** - Look for checkboxes `[ ]`, "criteria", "verify", "validate"
5. **Progress** - Search for "Status", "Progress", state words (Complete/Started/Failed)
6. **Error handling** - Find "if fail", "on error", "escalate", exception language

### Detection Confidence

| Confidence | Score Range | Recommendation |
|------------|-------------|----------------|
| High | 80-100 | Strong orchestration - USE AS-IS likely best |
| Medium | 60-79 | Good structure - User choice appropriate |
| Low | 40-59 | Partial structure - REBUILD may improve |
| None | 0-39 | No orchestration - Full skill application |
