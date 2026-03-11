---
name: orchestrate
version: 0.7.0
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
Agent tool:
  subagent_type: "general-purpose"
  description: "Orchestrate complex task plan"
  prompt: |
    <!-- ORCHESTRATOR_SUBAGENT_ACTIVE_v0.7 -->
    Execute the prompt-orchestrator skill.
    Source: {source_file_or_prompt}
    Output: {output_directory}

    Read the skill at ~/.claude/skills/prompt-orchestrator/SKILL.md
    Follow all phases. Return results when complete.

    IMPORTANT: You must NOT invoke the prompt-orchestrator skill or /orchestrate command.
    You ARE the orchestrator. Proceed directly with the Pre-Analysis Gate.
```

5. **STOP** after spawning. Return ONLY the subagent's results.

### Recursion Guard

If your prompt contains ANY of these indicators, you ARE the subagent:
- The HTML comment `<!-- ORCHESTRATOR_SUBAGENT_ACTIVE_v0.7 -->`
- The phrase "Execute the prompt-orchestrator skill"
- You were spawned via the Agent tool

**DO NOT spawn again.** Proceed with the Pre-Analysis Gate.

**Hard limit**: This skill must NEVER spawn more than one level deep. If you are a subagent and the skill tells you to spawn, STOP and proceed directly.

### Anti-Re-entry Guard

Subagent spawn prompts (Phase 3.2) MUST include:
"You must NOT invoke the prompt-orchestrator skill, /orchestrate, or any orchestration commands."

This prevents task subagents from accidentally triggering re-entry.

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

## Instruction Priority (RFC 2119)

| Keyword | Meaning | Enforcement |
|---------|---------|-------------|
| MUST / MANDATORY | Required. Violation = skill failure. | Hard gate — cannot proceed without compliance |
| SHOULD | Strongly recommended. Skip only with documented justification. | Soft gate — note in SUGGESTIONS.md if skipped |
| MAY / OPTIONAL | Permitted but not required. | No enforcement |

When instructions conflict, higher-priority keywords win. MUST > SHOULD > MAY.

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

### Pre-Analysis Gate: Detection Confidence

> This gate measures whether the source ALREADY contains PM orchestration structure.
> It produces a "Detection Confidence" score (0-100), which is SEPARATE from the
> Phase 1.4 "Complexity Score" that measures how complex the source content is.

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
| 60-79 | Present choice: USE AS-IS (recommended) or REBUILD |
| 40-59 | Present choice, recommend REBUILD |
| 0-39 | Proceed to Phase 1 (full orchestration) |

**User Choice (Score 40+):**

```
===============================================
 UNSCHEDULED OFFWORLD ACTIVATION
===============================================

Detection Confidence: {score}/100

Options:
[USE AS-IS] "The iris is open" - Keep existing structure, execute as-is
[REBUILD] "Dial new coordinates" - Discard existing, create optimized structure
===============================================
```

> If the user wants BOTH the original preserved AND a new orchestration, they should choose
> USE AS-IS first, then re-run the orchestrator with `--rebuild` flag on the same source.

> For scoring examples, see `references/pm-detection-examples.md` (Detection Confidence examples)

---

### Phase 1: Analyze Source Document

**1.1 Identify Document Structure**

**1.1.1 Inline Prompt Handling**

If the source is an inline prompt (not a file with structure/headers/line numbers):

1. Treat the entire prompt as a single "source document"
2. Use sentence/paragraph boundaries instead of header-based structure
3. Line numbers are optional — use paragraph references instead
4. Task files should quote the relevant prompt excerpt rather than referencing lines
5. Source Reference in task files uses `**Source**: inline prompt` with the quoted excerpt

All other phases apply normally. The orchestrator still extracts, does not generate.

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

> This produces the "Complexity Score" — measuring how complex the SOURCE CONTENT is.
> This is DIFFERENT from the Detection Confidence score in the Pre-Analysis Gate.
> The Complexity Score determines whether orchestration is warranted for new content.

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

> **Optional**: For automated analysis, run `python3 ~/.claude/skills/prompt-orchestrator/scripts/analyze_prompt.py --file {source}`

**1.6 Runtime Agent/Skill Discovery (MANDATORY)**

Before assigning agents to tasks, you MUST inventory what's actually available. Do NOT guess or hallucinate agent names.

**Where to find available agents and skills:**

The information is in YOUR system prompt (the context you received when this conversation started). Specifically:

1. **Agent tool `subagent_type` parameter** — Your system prompt describes the Agent tool. The `subagent_type` parameter has an enum or description listing valid agent types. Extract that list. Common types include `general-purpose`, but the exact list depends on your environment.

2. **Available skills** — Your system prompt contains `<available-skills>` or skill listings in system reminders. Extract skill names from these. Each skill can be invoked by a subagent.

3. **If you cannot find either list** — Use ONLY `general-purpose` as the agent type and note in TASK-MANIFEST.md: "Agent discovery found no specialized types; all tasks assigned to general-purpose."

**Discovery procedure:**

```
Step 1: Search your system prompt for "subagent_type" — extract valid values
Step 2: Search your system prompt for skill names (e.g., lines starting with skill names, <available-skills> tags)
Step 3: Record findings in TASK-MANIFEST.md "Available Agents" section
Step 4: If Step 1 and Step 2 yield nothing, default to general-purpose for all tasks
```

**Matching Rules:**

| Priority | Match Type | Example |
|----------|-----------|---------|
| 1 | User-specified in source | Source says "use backend-architect" -> use it |
| 2 | Exact skill match from discovery | Task needs Q-SYS -> discovered `qsys-plugin-development` skill |
| 3 | General domain match | Task needs backend work -> `general-purpose` with descriptive prompt |
| 4 | Fallback | No match -> `general-purpose` |

**NEVER assign an agent type that you did not find in Steps 1-2.** If uncertain, default to `general-purpose`.

**1.7 Context Rot Risk Assessment (MANDATORY)**

For each identified task, estimate **context consumption risk** — will the agent run out of effective context before completing?

**Risk Signals:**

| Signal | Risk Level | Action |
|--------|-----------|--------|
| Extracted content < 100 lines | Low | Single agent run |
| Extracted content 100-300 lines | Medium | Single agent run, monitor |
| Extracted content 300-500 lines | High | Consider splitting into sub-tasks |
| Extracted content 500+ lines | Critical | MUST split into sub-tasks |
| Task touches 10+ files | High | Split by file group |
| Task has 5+ distinct operations | High | Split by operation |
| Task includes research + implementation | High | Split: research first, then implement |

**Splitting Rules:**

When a task exceeds risk thresholds:
1. Split into 2-3 sequential sub-tasks (e.g., `01a-`, `01b-`, `01c-`)
2. Each sub-task must be self-contained with its own validation
3. Later sub-tasks depend on earlier ones
4. Mark in TASK SEQUENCE table with sub-task ordering

**Heuristic**: "Can an agent with ~100K context comfortably read CONTEXT.md + this task file + the relevant source files + produce all changes, without context quality degrading?"

If the answer is "probably not" → split the task.

**1.8 Agent Teams vs PM-Subagent Decision**

For high-complexity orchestrations, consider whether **Agent Teams** (experimental) would be more effective than the PM-subagent pattern.

**When PM-Subagent is better** (default):
- Sequential tasks with dependencies
- Tasks that share files (need coordination)
- Strict ordering requirements
- Need centralized progress tracking

**When Agent Teams may be better:**
- Many truly independent tasks (5+ parallel)
- Tasks that benefit from inter-agent communication
- Long-running workflows where PM context may itself degrade
- Tasks that need iterative collaboration between specialists

**If recommending Agent Teams**, note in SUGGESTIONS.md:
```
| - | Structural | Agent Teams may improve parallelism for Tasks X, Y, Z (all independent, zero file overlap) | - |
```

Agent Teams requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` — always note this prerequisite.

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

> **Example**: If the source document has a "Port Configuration" table referenced by 3 different
> phases, extract it ONCE to CONTEXT.md under `## Port Configuration`. In each task file that
> needs it, write: `See CONTEXT.md Section: Port Configuration`. Do NOT copy the table 3 times.

**2.3 Name Tasks**

Pattern: `{order:02d}-{verb}-{noun}.md`

Examples:
- "## PHASE 2: QRC CONNECTION" → `02-implement-qrc-connection.md`
- "#### Step 3.2: Add Controls" → `03-add-room-controls.md`

**2.4 Create Extraction Files**

**PM-ORCHESTRATION.md** - Use template: `references/pm-orchestration-template.md`

**Role Sentence Generation (MANDATORY for each task)**:

During Phase 2, for each task, write a single `{{ROLE_SENTENCE}}` that will be inserted into
the spawn prompt. This sentence primes the subagent's identity for the specific task.

Format: "You are a {domain} specialist focused on {specific task objective}."

Examples:
- "You are a database migration specialist focused on schema evolution."
- "You are a Lua plugin developer focused on Q-SYS control integration."
- "You are a documentation writer focused on API reference completeness."

Store role sentences in the TASK SEQUENCE table as an additional column, or in TASK-MANIFEST.md.

Required sections:
- PM RULES (READ FIRST) — includes Rule 7: Your only task-file interaction is pointing subagents at file paths
- CONTEXT DISCIPLINE (WHAT THE PM READS vs WHAT SUBAGENTS READ)
- WHY SUBAGENTS ARE MANDATORY
- TASK SEQUENCE table
- EXECUTION INSTRUCTIONS — uses Agent tool (NOT Task tool)
- PROGRESS TRACKER
- NON-NEGOTIABLES — 8 items including anti-read rules
- ERROR HANDLING
- EXTRACTION COVERAGE

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

**SUGGESTIONS.md** - Use template: `assets/templates/suggestions.md` (guide: `references/suggestions-template.md`)

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

**2.5.1 Parallel Group File-Overlap Verification (MANDATORY for parallel tasks)**

Before marking tasks as parallel, verify zero file overlap:

1. For each candidate parallel task, list ALL files it will read or modify
2. Compare file lists between all tasks in the proposed parallel group
3. If ANY file appears in 2+ task file lists → tasks CANNOT be parallel

Document the verification in PM-ORCHESTRATION.md:

```markdown
### Parallel Group {N} File-Overlap Analysis

| Task | Files Read | Files Modified |
|------|-----------|---------------|
| {task_a} | {list} | {list} |
| {task_b} | {list} | {list} |

**Overlap**: None confirmed → safe for parallel execution
```

If overlap is found, convert to sequential execution with appropriate blockers.

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

**2.6.1 Output Directory Conflict Resolution**

If the output directory already contains orchestration files:

| Existing Files Found | Action |
|---------------------|--------|
| PM-ORCHESTRATION.md with all tasks NOT STARTED | Ask: OVERWRITE or choose new directory |
| PM-ORCHESTRATION.md with some tasks COMPLETE | Ask: RESUME (continue from last complete) or OVERWRITE |
| PM-ORCHESTRATION.md with all tasks COMPLETE | Ask: RE-RUN (fresh) or ABORT |
| subagent-tasks/ exists but no PM-ORCHESTRATION.md | OVERWRITE (orphaned files) |

**Resume Behavior**: Read existing PROGRESS TRACKER, skip COMPLETE tasks, begin from first non-COMPLETE task. Regenerate only task files that need re-extraction.

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

**HARD GATE**: You MUST NOT proceed to Phase 3 if coverage is below 95%.
If coverage < 95%, identify the missing sections and re-extract before continuing.
The only exception is sections explicitly marked "out of scope" by the user.

**This is your proof of work.** The coverage table proves you did your job correctly.

---

### Phase 3: Execute

**If `--generate-only` flag is set**: Skip Phase 3 entirely. Return the generated artifacts
(PM-ORCHESTRATION.md, TASK-MANIFEST.md, CONTEXT.md, SUGGESTIONS.md, task files) without
executing. Report: "Orchestration generated. {N} task files ready for execution."

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

**WAIT FOR USER RESPONSE.** Do NOT proceed to Phase 3.2 until the user selects an option.
If no response is received, do NOT default to [PROCEED]. The user MUST explicitly confirm.

**3.1.1 Suggestion Triage**

After the user responds to the pre-execution review, if they choose [REVIEW]:
1. Present the full SUGGESTIONS.md
2. For each Critical item, ask: ACKNOWLEDGE / DEFER / N/A
3. Update the Status column in SUGGESTIONS.md accordingly
4. Return to the options prompt

The PM SHOULD review SUGGESTIONS.md before dispatching the first task and note any
ACKNOWLEDGED items that may affect execution.

**3.2 Task Execution**

For each task, spawn subagent via Agent tool:
```
Agent tool:
  subagent_type: {from TASK-MANIFEST.md}
  description: "{3-5 word task summary}"
  prompt: |
    You are executing a task for the {PROJECT_NAME} project.
    Working directory: {WORKING_DIRECTORY}

    STEP 1: Read the shared context file:
      {CONTEXT_PATH}

    STEP 2: Read and execute the task file:
      {TASK_PATH}

    STEP 3: Follow the task's validation criteria exactly.

    STEP 4: Report STATUS: COMPLETE or FAILED with the output format specified in the task file.
```

**DO NOT read the task file yourself to "build a better prompt."** The prompt above is sufficient. The task file is self-contained. Adding your own context from reading it defeats the isolation model.

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

| # | Anti-Pattern | Positive Reframe | Fix |
|---|--------------|-----------------|-----|
| 1 | Injecting suggestions into task files | Suggestions live in SUGGESTIONS.md | Move to SUGGESTIONS.md |
| 2 | Summarizing sections | Source content is copied verbatim | Copy verbatim |
| 3 | Adding requirements not in source | Gaps are noted in SUGGESTIONS.md | Note gap in SUGGESTIONS.md |
| 4 | Restructuring source organization | Source structure is preserved | Preserve source structure |
| 5 | Pattern substitution (changing APIs) | Source APIs are preserved exactly | Preserve source exactly |
| 6 | PM executing tasks directly | PM dispatches agents and tracks results | Always spawn subagents |
| 7 | Narrow extraction (missing rollback) | Full semantic bundling captures all related content | Semantic bundling |
| 8 | PM reading subagent task files | PM coordinates using TASK SEQUENCE table only | PM reads ONLY coordination files |
| 9 | PM reading source document | Source is fully extracted — TASK SEQUENCE has everything | Source is fully extracted |
| 10 | Assigning nonexistent agents | Agents come from runtime discovery only | Use runtime discovery (Phase 1.6) |
| 11 | Over-sized tasks causing context rot | Tasks are sized for agent context comfort | Use context rot assessment (Phase 1.7) |

> For detailed examples, see `references/extraction-examples.md`

**PM Direct Execution Detection:**

If you think/write these phrases, STOP:
- "I'll just quickly..."
- "Since this is straightforward..."
- "To save time..."
- "Direct execution would be more efficient..."

**PM Context Pollution Detection:**

If you think/write these phrases, STOP:
- "Let me read the task file to understand..."
- "I should check what the task contains..."
- "Let me peek at the source to verify..."
- "I need more context about this task..."

**Instead, remind yourself:**
- "The TASK SEQUENCE table has every coordination detail I need."
- "I dispatch agents and track results — that's my entire job."
- "Reading task files would pollute my coordination context."

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

| Reference | When to Load | Content Type |
|-----------|-------------|-------------|
| `references/pm-orchestration-template.md` | Generating PM-ORCHESTRATION.md | Generation guide (template is in `assets/templates/`) |
| `references/suggestions-template.md` | Generating SUGGESTIONS.md | Generation guide (template is in `assets/templates/`) |
| `references/capability-inference.md` | Generating TASK-MANIFEST.md | Inference rules and tag mapping |
| `references/pm-detection-examples.md` | Scoring Detection Confidence | Examples for Pre-Analysis Gate |
| `references/extraction-examples.md` | Reviewing extraction patterns | Good/bad extraction examples |
| `references/workflow-patterns.md` | Identifying task decomposition | Pattern library (Sequential, Fan-Out, Build-Test) |

---

## Error Handling

| Situation | Response |
|-----------|----------|
| Task FAILED | Halt, report failure, offer: retry/skip/abort |
| Task BLOCKED | Verify blocker completed, report if stuck |
| Source unclear | Include full section, note in SUGGESTIONS.md |
| Missing content | Note gap in SUGGESTIONS.md, extract what exists |

---

## Operational Limits

| Limit | Value | Rationale |
|-------|-------|-----------|
| Max tasks per orchestration | 20 | Beyond 20, PM context rot becomes likely |
| Max retries per failed task | 2 | After 2 retries, escalate to user |
| Max parallel group size | 5 | File-overlap analysis becomes unreliable above 5 |
| Checkpoint interval | Every 3 tasks | PM should summarize progress every 3 completions |
| Single-task threshold | 1 task identified | If only 1 task, ask user: "Only 1 task detected. Execute directly or use full orchestration?" |

If any limit is exceeded, pause and report to the user before continuing.
