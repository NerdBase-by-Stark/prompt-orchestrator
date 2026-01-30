---
name: orchestrate
version: 0.5.2
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

### Recursion Guard

If you find this content in your Task tool prompt:
> "Execute the prompt-orchestrator skill"

Then you ARE the subagent. **DO NOT spawn again.** Proceed with Phase 0.

---

## Core Principle: EXTRACT, DON'T GENERATE

This skill is a **splitter/organizer**, NOT a generator.

| DO | DO NOT |
|----|--------|
| Identify task boundaries in source | Invent new tasks |
| Extract sections verbatim from source | Rewrite or "improve" source content |
| Preserve source code exactly | Generate new code snippets |
| Reference source line numbers | Paraphrase or summarize code |
| Copy validation criteria from source | Add validation not in source |
| **Log observations in SUGGESTIONS.md** | **Inject suggestions into task files** |

---

## Generated Artifacts

| File | Purpose | Content Source |
|------|---------|----------------|
| `PM-ORCHESTRATION.md` | Coordination with task sequence | Extracted from source structure |
| `TASK-MANIFEST.md` | Task capability mapping | Generated from task analysis |
| `CONTEXT.md` | Shared context for subagents | Extracted + deduplicated content |
| `SUGGESTIONS.md` | Advisory observations | Generated analysis (NOT in task files) |
| `subagent-tasks/*.md` | Individual task files | VERBATIM excerpts from source |

---

## Workflow

### Phase 0: Detect Existing PM Orchestration

Before analyzing, check if source already contains PM orchestration structure.

**Scoring Signals:**

| Signal | Points |
|--------|--------|
| PM/Coordinator role definition | 20 |
| Task sequence table | 20 |
| Dependencies stated | 15 |
| Validation criteria | 15 |
| Progress tracking | 15 |
| Error handling instructions | 15 |

**Threshold Actions:**

| Score | Action |
|-------|--------|
| 80-100 | Present choice, recommend USE AS-IS |
| 60-79 | Present choice, recommend BOTH |
| 40-59 | Present choice, recommend REBUILD |
| 0-39 | Proceed to Phase 1 (full orchestration) |

**User Choice (Score 40+):**

```
===============================================
 UNSCHEDULED OFFWORLD ACTIVATION
===============================================

Orchestration Score: {score}/100

Options:
[USE AS-IS] "The iris is open" - Keep existing structure
[REBUILD] "Dial new coordinates" - Replace with optimized structure
[BOTH] "Establish secondary gate" - Keep original + create improved
===============================================
```

> For scoring examples, see `references/pm-detection-examples.md`

---

### Phase 1: Analyze Source Document

**1.1 Identify Document Structure**

| Element | Detection Pattern | Action |
|---------|-------------------|--------|
| Phases | `## PHASE`, `### Phase X` | Each phase becomes a task group |
| Steps | `#### Step X.Y`, numbered lists | Steps within phase stay together |
| Code blocks | Triple backticks | Mark for verbatim extraction |
| Subagent prompts | `**Subagent**:`, `**Prompt**:` | Extract as task content |
| Validation | `**Success Criteria**:`, checkboxes | Extract to task validation |
| Git commits | `git commit -m` | Mark phase boundaries |

**1.2 Map Task Boundaries**

1. Phase boundaries → task groups
2. Subagent prompts → one task file each
3. Validation checkpoints → completion points
4. Git commits → rollback points

**1.3 Collect Observations (for SUGGESTIONS.md)**

Note potential issues WITHOUT modifying extractions:
- API concerns, missing details, scope issues
- Structure gaps, error handling, dependencies
- Inconsistencies

**CRITICAL**: Observations go ONLY in SUGGESTIONS.md, NEVER in task files.

**1.4 Score Complexity**

| Factor | Points |
|--------|--------|
| Each phase/major section | +10 |
| Each subagent prompt | +5 |
| Each code block | +2 |
| Total source lines | +1 per 100 lines |
| Dependencies between sections | +3 each |

**1.5 Threshold Decision**

| Score | Action |
|-------|--------|
| 0-30 | Ask: "Complexity score [X]. Execute directly or decompose?" |
| 31+ | Proceed with orchestration |

---

### Phase 2: Extract and Organize

**2.1 Semantic Content Bundling (MANDATORY)**

Before finalizing task boundaries, perform a **full-document semantic scan** to identify ALL content related to each task, regardless of location.

**Scan Patterns:**

| Pattern | Keywords | Relationship |
|---------|----------|--------------|
| Backup/Restore | backup, restore, snapshot | Safety net |
| Rollback | rollback, revert, undo, recover | Recovery path |
| Data Migration | migrate, transfer, export, import | Data dependencies |
| Prerequisites | before you begin, requirements | Setup requirements |
| Validation | verify, test, confirm, check | Completion criteria |
| Error Handling | if error, exception, fallback | Failure paths |

**Bundling Rules:**

1. Destructive operations (DELETE, DROP, REMOVE, ARCHIVE, WIPE, CLEAR, PURGE, RESET, DESTROY, TERMINATE, OVERWRITE) → bundle rollback section
2. Data operations → bundle backup/migration sections
3. Setup tasks → bundle prerequisite checks
4. Distance is irrelevant: content at line 900 is as essential as line 50

**Heuristic**: "If a subagent executes ONLY this extracted content, can they safely complete AND recover from failure?"

**Line Count Check:**

| Lines | Action |
|-------|--------|
| < 30 | STOP - Re-scan entire source |
| 30-50 | Verify ALL checklist items |
| 50-100 | Normal verification |
| 100+ | Check not over-bundled |

**2.2 Context Deduplication (MANDATORY)**

Before creating task files, identify **shared context**:

| Content Type | Detection | Action |
|--------------|-----------|--------|
| Reference tables | Same table in 2+ phases | Extract to CONTEXT.md |
| Background analysis | Pro/con, comparison, rationale | Extract to CONTEXT.md |
| Architectural diagrams | System overview, flow diagrams | Extract to CONTEXT.md |
| Shared dependencies | Same prereqs for multiple tasks | Extract to CONTEXT.md |

**Deduplication Rule:**

If content is referenced by 2+ tasks:
1. Extract ONCE to CONTEXT.md under appropriate heading
2. In task files, add: `See CONTEXT.md Section: {heading}`
3. Do NOT duplicate verbatim content

**2.3 Name Tasks**

Pattern: `{order:02d}-{verb}-{noun}.md`

Examples:
- "## PHASE 2: QRC CONNECTION" → `02-implement-qrc-connection.md`
- "#### Step 3.2: Add Controls" → `03-add-room-controls.md`

**2.4 Create Extraction Files**

**PM-ORCHESTRATION.md** - Use template: `references/pm-orchestration-template.md`

Required sections:
- PM RULES (READ FIRST)
- WHY SUBAGENTS ARE MANDATORY
- TASK SEQUENCE table
- EXECUTION INSTRUCTIONS
- PROGRESS TRACKER
- NON-NEGOTIABLES
- ERROR HANDLING

**TASK-MANIFEST.md** - Use template: `assets/templates/task-manifest.md`

For capability inference rules, see `references/capability-inference.md`

**CONTEXT.md**:
- Project paths from source
- Technologies mentioned
- Constraints from source
- Deduplicated shared content (tables, rationale, diagrams)
- Copy source's "Executive Summary" or "Overview" verbatim

**Task Files** - Use template: `assets/templates/task.md`

Structure:
```markdown
# Task: {name}

## Source Reference
**Document**: {path}
**Primary Section**: {header} (lines X-Y)

**Related Sections** (from semantic scan):
| Section | Lines | Relationship | Why Bundled |
|---------|-------|--------------|-------------|

**Total Lines Extracted**: {N}

## Extracted Content
{VERBATIM_COPY}

## Validation Criteria (from source)
{VERBATIM_COPY}

## Extraction Certification
- [ ] Self-contained
- [ ] Rollback included (if destructive)
- [ ] Backup included (if data operation)
- [ ] Prerequisites included
- [ ] Line count: {N} (flag if < 50)
- [ ] Semantic scan performed
```

**SUGGESTIONS.md** - Use template: `references/suggestions-template.md`

**2.5 Extraction Rules**

| Source Element | Method |
|----------------|--------|
| Section text | Copy verbatim, preserve formatting |
| Code blocks | Copy exactly, including comments |
| Subagent prompts | Copy entire prompt block |
| Validation criteria | Copy checkboxes and criteria |
| Commands | Copy bash/shell exactly |
| Tables | Copy complete tables |

**NEVER in task files:**
- Summarize code blocks
- "Clean up" or reformat
- Add explanations not in source
- Change variable names
- Substitute APIs
- Include suggestions (those go in SUGGESTIONS.md)

**2.6 Output Location**

```
{output_dir}/
├── PM-ORCHESTRATION.md
├── TASK-MANIFEST.md
├── CONTEXT.md
├── SUGGESTIONS.md
└── subagent-tasks/
    ├── 01-phase-one.md
    ├── 02-phase-two.md
    └── ...
```

**2.7 Extraction Validation (MANDATORY)**

Before completing Phase 2, verify extraction completeness:

1. **Re-scan source** - List all major sections/headers
2. **Map to output** - Where did each land?
3. **Count verification**:
   - Code blocks: Source X → Extracted Y
   - Phases/sections: Source X → Tasks Y
   - Validation criteria: Source X → Extracted Y

**Generate coverage proof** in PM-ORCHESTRATION.md:

```markdown
## Extraction Coverage

| Source Section | Lines | Extracted To | Status |
|----------------|-------|--------------|--------|
| Phase 1: Setup | 50-92 | Task 01 | ✓ |
| Phase 2: API | 100-300 | Task 02 | ✓ |
| Rollback Plan | 450-480 | Task 01, 06 | ✓ bundled |
| Port Config | 500-520 | CONTEXT.md | ✓ deduped |

**Totals**:
- Source sections: X | Extracted: Y | Coverage: Z%
- Code blocks: X | Extracted: Y
- Validation criteria: X | Extracted: Y
```

**If any section shows NOT EXTRACTED** → Stop, re-scan, bundle before proceeding.

**This is your proof of work.** The coverage table proves you did your job correctly.

---

### Phase 3: Execute

**3.1 Pre-Execution Review**

```
## Orchestration Generated

Source: {path}
Tasks: {n} task files
Suggestions: {m} observations

### Critical Observations ({count})
{top 3 from SUGGESTIONS.md}

### Options
[REVIEW] View full SUGGESTIONS.md
[PROCEED] Execute tasks
[ABORT] Cancel
```

**3.2 Task Execution**

For each task, spawn subagent via Task tool:
```
subagent_type: {from TASK-MANIFEST.md}
prompt: |
  Read CONTEXT.md first: {path}
  Then execute task: {path}
  Report: STATUS: COMPLETE or FAILED
```

**3.3 Monitor Progress**

1. Check for STATUS: COMPLETE or FAILED
2. Update PM-ORCHESTRATION.md progress tracker
3. If FAILED: halt, report, ask user
4. If COMPLETE: proceed to next

**3.4 Completion Report**

```
## Orchestration Complete

STATUS: COMPLETE | PARTIAL | FAILED
Tasks Completed: X/Y

| Task | Status |
|------|--------|
| 01-setup | COMPLETE |

SUGGESTIONS.md: {N} observations ({critical} critical)
```

---

## Anti-Patterns (MUST AVOID)

| # | Anti-Pattern | Fix |
|---|--------------|-----|
| 1 | Injecting suggestions into task files | Move to SUGGESTIONS.md |
| 2 | Summarizing sections | Copy verbatim |
| 3 | Adding requirements not in source | Note gap in SUGGESTIONS.md |
| 4 | Restructuring source organization | Preserve source structure |
| 5 | Pattern substitution (changing APIs) | Preserve source exactly |
| 6 | PM executing tasks directly | Always spawn subagents |
| 7 | Narrow extraction (missing rollback) | Semantic bundling |

> For detailed examples, see `references/extraction-examples.md`

**PM Direct Execution Detection:**

If you think/write these phrases, STOP:
- "I'll just quickly..."
- "Since this is straightforward..."
- "To save time..."
- "Direct execution would be more efficient..."

---

## Invocation

```bash
/orchestrate --file plan.md              # Standard usage
/orchestrate "Complex prompt here"       # Inline prompt
/orchestrate --threshold 20 --file x.md  # Lower threshold
/orchestrate --generate-only --file x.md # Generate without execute
```

---

## References (load as needed)

| Reference | When to Load |
|-----------|--------------|
| `references/pm-orchestration-template.md` | Generating PM-ORCHESTRATION.md |
| `references/suggestions-template.md` | Generating SUGGESTIONS.md |
| `references/capability-inference.md` | Generating TASK-MANIFEST.md |
| `references/pm-detection-examples.md` | Scoring Phase 0 detection |
| `references/extraction-examples.md` | Reviewing extraction patterns |

---

## Error Handling

| Situation | Response |
|-----------|----------|
| Task FAILED | Halt, report failure, offer: retry/skip/abort |
| Task BLOCKED | Verify blocker completed, report if stuck |
| Source unclear | Include full section, note in SUGGESTIONS.md |
| Missing content | Note gap in SUGGESTIONS.md, extract what exists |
