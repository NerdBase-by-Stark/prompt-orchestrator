# Product Requirements Document: Prompt Orchestrator

> Version: 0.4.0
> Author: NerdBase-by-Stark
> Created: 2026-01-27
> Updated: 2026-01-29
> Status: In Development

---

## 1. Overview

### 1.1 Problem Statement

Large, complex prompts suffer from:
- **Context fatigue** after ~500 lines
- **Instruction neglect** when too many directives compete
- **Requirement omission** - the primary failure mode per E2EDevBench
- **No self-verification** built into single-shot execution

Industry research shows decomposed, multi-step workflows with clear role separation **outperform monolithic prompts** by significant margins (GPT-3.5 with agentic workflow: 95.1% vs 48.1% zero-shot on HumanEval).

### 1.2 Solution

A Claude Code skill that automatically decomposes complex prompts into an orchestrated, executable workflow:

```
Input:  Complex prompt or plan document
Output: PM-ORCHESTRATION.md + TASK-MANIFEST.md + CONTEXT.md + subagent-tasks/*.md + SUGGESTIONS.md
```

### 1.3 Execution Model

**The skill ALWAYS runs as a subagent** to preserve the user's main conversation context.

| Principle | Implementation |
|-----------|----------------|
| Context Preservation | Spawn orchestrator as background/separate agent via Task tool |
| Clean Handoff | Return results summary to parent conversation |
| No Context Pollution | Decomposition work never consumes user's primary context |

This ensures the user's main conversation remains focused on their primary work while orchestration happens in an isolated context.

### 1.4 Core Design Principle

**EXTRACT, DON'T GENERATE**

The skill is a **splitter/organizer**, not a code generator.

| DO | DON'T |
|----|-------|
| Extract verbatim content from source | Generate new code |
| Preserve exact APIs and patterns | Substitute APIs (print vs Log.Message) |
| Reference source line numbers | Invent implementation details |
| Copy code blocks unchanged | "Improve" or rewrite source code |
| Capture observations in SUGGESTIONS.md | Inject suggestions into task files |

**Rationale:** When source documents already contain implementation details (code snippets, subagent prompts, validation criteria), the skill's job is to organize them into executable chunks - not to rewrite them and potentially introduce errors.

### 1.5 Target Users

**Primary:** Power users who understand AI workflows but aren't senior coders who would build orchestration files manually.

- Developers using Claude Code for complex tasks
- Teams running multi-step AI workflows
- Anyone hitting quality issues with large prompts

**Not:** Senior engineers who prefer hand-crafting orchestration (they can use templates directly)

---

## 2. Goals & Non-Goals

### 2.1 Goals

| Priority | Goal |
|----------|------|
| P0 | Analyze prompt complexity and recommend decomposition |
| P0 | Generate PM-ORCHESTRATION.md with task sequence and blockers |
| P0 | Generate CONTEXT.md with shared state |
| P0 | Generate subagent task files with clear directives |
| P1 | Detect parallelizable tasks |
| P1 | Generate validation criteria per task |
| P1 | Estimate context budget per task |
| P2 | Suggest retry/escalation logic |
| P2 | Learn from execution feedback |

### 2.2 Non-Goals (v1)

- GUI/visual workflow builder
- Integration with external frameworks (LangGraph, CrewAI)
- Real-time workflow modification during execution

**Note:** Execution IS a goal - the skill analyzes, generates, AND triggers execution.

---

## 3. PM Orchestration Detection

### 3.1 Overview

Before decomposing a document, the skill detects if existing PM orchestration structure is present. This prevents unnecessary rebuilding of well-structured documents.

### 3.2 Detection Scoring

| Signal | Points | Detection Pattern |
|--------|--------|-------------------|
| PM/Coordinator role definition | 20 | "You are the PM", "coordinator", "orchestrate", "project manager" |
| Task sequence table | 20 | Markdown table with Order/Task columns, numbered task lists |
| Dependencies stated | 15 | "blocked by", "requires", "after", "depends on" |
| Validation/completion criteria | 15 | "success criteria", "validation", checkboxes per task |
| Progress tracking | 15 | Status column, "Not Started/In Progress/Complete" |
| Error handling instructions | 15 | "if failed", "on error", "escalate" |

**Maximum Score: 100 points**

### 3.3 Threshold Actions

| Score | Interpretation | Action |
|-------|----------------|--------|
| 60-100 | Good orchestration | Present user choice |
| 40-59 | Partial orchestration | Present user choice |
| 0-39 | No orchestration | Full skill application |

### 3.4 User Choice Flow (Stargate Themed)

When existing orchestration is detected (score 40+), the skill presents a themed hold message:

```
===============================================
 UNSCHEDULED OFFWORLD ACTIVATION
===============================================

Existing orchestration structure detected in source document.
Verifying IDC before proceeding...

Orchestration Score: {score}/100

Signals Detected:
- PM Role Definition: {points} pts
- Task Sequence Table: {points} pts
- Dependencies: {points} pts
...

===============================================
```

**User Options:**

| Option | Code | Behavior |
|--------|------|----------|
| **USE AS-IS** | "The iris is open" | Extract using source's existing PM structure |
| **REBUILD** | "Dial new coordinates" | Replace with skill's optimized orchestration |
| **BOTH** | "Establish secondary gate" | Keep original + create PM-ORCHESTRATION-SUGGESTED.md |

### 3.5 Rationale

- **Respects existing work**: If a document is already well-orchestrated, don't destroy it
- **User agency**: Let the user decide how to proceed
- **Thematic consistency**: Stargate theme adds character while being functional
- **Transparency**: Show exactly what was detected and scored

---

## 4. Agent Allocator System

### 4.1 Overview

The Agent Allocator automatically matches tasks to the best available agent/skill before execution begins. This prevents the PM from guessing agents and enables optimal agent selection based on task capabilities.

### 4.2 TASK-MANIFEST.md

Generated during orchestration, contains:

| Column | Purpose |
|--------|---------|
| Task File | Path to task file |
| Capabilities | Inferred capabilities (lua, testing, networking, etc.) |
| User-Specified Agent | Agent explicitly named in source (passthrough) |
| Allocated Agent | Assigned by Agent Allocator |
| Confidence | Confidence score (%) |

### 4.3 Agent Discovery

The Allocator discovers available agents from:
1. **Task tool definition** - `subagent_type` parameter lists available agent types
2. **System reminders** - Lists available skills

### 4.4 Capability Inference

| Content Pattern | Capability Tag |
|-----------------|----------------|
| Lua code, Q-SYS APIs | `lua`, `q-sys` |
| Test, validation | `testing` |
| UI, layout, components | `frontend`, `ui` |
| API, HTTP, networking | `networking`, `api` |
| Auth, credentials | `auth`, `security` |
| File operations | `file-ops` |

### 4.5 Confidence Scoring

| Scenario | Confidence | Action |
|----------|------------|--------|
| Single best match | 90-100% | Auto-assign |
| Good match, alternatives exist | 80-89% | Auto-assign with note |
| Multiple equal matches | 50-70% | Flag as AMBIGUOUS |
| No match, using general-purpose | 75% | Auto-assign with note |
| User-specified agent | 100% | Passthrough |

### 4.6 Execution Flags

| Flag | Behavior |
|------|----------|
| `--ambiguous-only` | (DEFAULT) Ask user only about tasks with <80% confidence |
| `--confirm-agents` | Show full allocation list, await confirmation |
| `--trust-allocator` | Accept all allocations without review |

### 4.7 PM Context Preservation

The Allocator runs as Task 0 (subagent) to:
- Keep PM context clean (coordination only)
- Delegate capability matching to specialist
- Return simple mapping table for PM to use

Allocator reads ONLY `TASK-MANIFEST.md` (~500 tokens), never individual task files.

---

## 5. User Stories

### 4.1 Primary Flow

```
As a developer,
I want to provide a complex prompt and get back orchestration files,
So that I can execute it as a high-quality, decomposed workflow.
```

**Acceptance Criteria:**
- [ ] Skill invocable via `/orchestrate` or similar
- [ ] Analyzes input prompt for complexity
- [ ] Generates complete file structure
- [ ] Files are immediately executable with Claude Code

### 4.2 Complexity Assessment

```
As a developer,
I want to know if my prompt needs decomposition,
So that I don't add overhead to simple tasks.
```

**Acceptance Criteria:**
- [ ] Provides complexity score/assessment
- [ ] Recommends: "monolithic OK" vs "decomposition recommended"
- [ ] Threshold configurable (default: 50+ changes or ~500 lines expected)

### 4.3 Customization

```
As a developer,
I want to customize the output format,
So that it fits my team's conventions.
```

**Acceptance Criteria:**
- [ ] Template system for output files
- [ ] Configurable task file structure
- [ ] Option to use different orchestration patterns

---

## 5. Functional Requirements

### 5.1 Input Analysis

The skill MUST analyze the input prompt for:

| Signal | Detection Method |
|--------|-----------------|
| Task count | Count distinct action verbs/objectives |
| Dependencies | Identify "after X", "requires Y", sequential language |
| Parallel opportunities | Independent tasks with no shared state |
| Complexity indicators | Nested requirements, conditionals, multi-file changes |
| Domain context | Extract project paths, technologies, constraints |

### 5.2 Output Structure

#### 5.2.1 PM-ORCHESTRATION.md

```markdown
# {Project Name} - PM Orchestration

## PM RULES (READ FIRST)
1. You are the PROJECT MANAGER. You coordinate subagents.
2. You MUST use subagents for each task.
3. You MUST NOT proceed to the next task until current is complete.
4. Each subagent receives ONLY its task file + CONTEXT.md reference.

## TASK SEQUENCE

| Order | Task File | Description | Blocker | Parallel |
|-------|-----------|-------------|---------|----------|
| 1 | task-1-{name}.md | {description} | - | No |
| 2 | task-2-{name}.md | {description} | Task 1 | No |
...

## PROGRESS TRACKER

| Task | Status | Notes |
|------|--------|-------|
| Task 1 | ⬜ Not Started | |
...

## VALIDATION CHECKLIST
- [ ] All tasks completed
- [ ] All blockers resolved
- [ ] Output verified against requirements

## NON-NEGOTIABLES
1. Use subagents for all tasks
2. Wait for completion before proceeding
3. If blocked, STOP and report
```

#### 5.2.2 CONTEXT.md

```markdown
# {Project Name} - Shared Context

## MANDATORY FIRST STEP
Before doing any work, read: {claude.md path if exists}

## PROJECT PATHS
| Item | Path |
|------|------|
| Source | {path} |
| Output | {path} |
| Task Files | {path}/subagent-tasks/ |

## RULES FOR ALL AGENTS
1. {extracted constraints}
2. Report status: STATUS: COMPLETE or STATUS: FAILED
3. {additional rules from prompt}

## SHARED STATE
{any state that needs to persist across tasks}
```

#### 5.2.3 subagent-tasks/{task-file}.md

```markdown
# TASK: {Task Name}

## Context
Read first: {path}/CONTEXT.md

## Target
{file/output this task produces}

## Requirements
1. {requirement 1}
2. {requirement 2}
...

## Validation Criteria
- [ ] {criterion 1}
- [ ] {criterion 2}

## Output
When complete, report:
```
STATUS: COMPLETE or FAILED
CHANGES APPLIED: {list}
NOTES: {any issues}
```
```

### 5.3 Complexity Scoring

| Score | Recommendation | Criteria |
|-------|----------------|----------|
| 0-30 | Monolithic OK | <5 tasks, no dependencies, <500 lines expected |
| 31-70 | Consider decomposition | 5-15 tasks, some dependencies |
| 71-100 | Decomposition recommended | 15+ tasks, complex dependencies, >500 lines |

### 5.4 Operators (Inspired by AFlow)

The skill should recognize and apply these patterns:

| Operator | When to Apply |
|----------|---------------|
| **Generate** | Creating new content/code |
| **Review** | Self-critique needed |
| **Revise** | Iterative improvement |
| **Test** | Validation required |
| **Ensemble** | Multiple approaches, pick best |

---

## 6. Technical Design

### 6.1 Skill Structure

```
~/.claude/skills/prompt-orchestrator/
├── SKILL.md                    # Main skill definition
├── assets/
│   ├── templates/
│   │   ├── pm-orchestration.md
│   │   ├── context.md
│   │   ├── task.md
│   │   └── suggestions.md      # NEW: Advisory output template
│   └── examples/
│       └── qsys-mute-state-controller/
├── references/
│   └── workflow-patterns.md    # Pattern library
└── scripts/
    └── analyze_prompt.py       # Optional complexity analyzer
```

### 6.1.1 Dual Output Model

| Output | Purpose | Content |
|--------|---------|---------|
| **Task files** | Execution | Extracted verbatim from source |
| **SUGGESTIONS.md** | Advisory | Analytical observations, gaps, improvements |

This separation ensures task files remain pure extractions while the skill's analytical capability is captured separately for user review.

### 6.2 Invocation

```bash
# Via slash command
/orchestrate "Your complex prompt here"

# With options
/orchestrate --threshold 30 --parallel-detect "Your prompt"

# From file
/orchestrate --file requirements.md
```

### 6.3 Algorithm (High-Level)

```
1. PARSE input prompt
2. EXTRACT:
   - Tasks (action items)
   - Dependencies (blockers)
   - Context (paths, constraints)
   - Shared state
3. SCORE complexity
4. IF score < threshold:
   - INFORM user "Monolithic execution recommended"
   - ASK: proceed anyway or execute directly?
5. ELSE:
   - SEQUENCE tasks (topological sort by dependencies)
   - DETECT parallel opportunities
   - GENERATE PM-ORCHESTRATION.md
   - GENERATE CONTEXT.md
   - FOR EACH task:
     - GENERATE subagent-tasks/{task}.md with numbered prefix (01-, 02-, etc.)
6. EXECUTE workflow:
   - Load PM-ORCHESTRATION.md
   - FOR EACH task in sequence:
     - Spawn subagent with task file
     - Wait for STATUS: COMPLETE/FAILED
     - Update progress tracker
     - IF FAILED: halt and report
7. REPORT final status
```

### 6.4 File Naming Convention

Task files auto-named with pattern: `{order}-{verb}-{noun}.md`

Examples:
- `01-setup-environment.md`
- `02-implement-logging.md`
- `03-add-verification.md`
- `04-write-tests.md`
- `05-validate-output.md`

This ensures:
- Clear execution order at a glance
- Alphabetical sorting matches execution order
- Descriptive names for debugging

---

## 7. Success Metrics

### 7.1 Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Requirement coverage | >95% | Tasks cover all prompt requirements |
| Dependency accuracy | >90% | Blockers correctly identified |
| Execution success rate | >85% | Workflows complete without manual intervention |

### 7.2 Efficiency Metrics

| Metric | Target |
|--------|--------|
| Generation time | <30 seconds for typical prompt |
| Context budget accuracy | Each task <500 lines |
| Parallel detection | Identify >80% of parallel opportunities |

---

## 8. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Over-decomposition | Unnecessary overhead | Complexity threshold; user override |
| Under-decomposition | Quality issues | Conservative scoring; user feedback |
| Incorrect dependencies | Execution failures | Dependency validation step |
| Template rigidity | Doesn't fit all use cases | Customizable templates |

---

## 9. Milestones

### Phase 1: MVP (v0.1.0)
- [ ] Basic prompt analysis
- [ ] Generate 3-file structure
- [ ] Sequential task ordering
- [ ] Manual invocation

### Phase 2: Smart Detection (v0.2.0)
- [ ] Complexity scoring
- [ ] Parallel task detection
- [ ] Dependency inference
- [ ] Validation criteria generation

### Phase 3: PM Detection & User Agency (v0.3.0)
- [x] PM orchestration detection scoring
- [x] User choice flow (USE AS-IS / REBUILD / BOTH)
- [x] Stargate-themed hold message
- [x] Auto-subagent execution model
- [x] Good PM orchestration reference documentation

### Phase 4: Agent Allocator (v0.4.0)
- [x] TASK-MANIFEST.md generation with capability inference
- [x] Agent Allocator subagent (Task 0)
- [x] Agent discovery from Task tool definition and system reminders
- [x] Confidence scoring (80%+ auto-assign, <80% ambiguous)
- [x] Execution flags (--ambiguous-only default, --confirm-agents, --trust-allocator)
- [x] User choice for ambiguous tasks only
- [x] PM context preservation (allocator reads manifest only)

### Phase 5: Learning (v0.5.0)
- [ ] Execution feedback integration
- [ ] Template refinement based on outcomes
- [ ] Pattern library

---

## 10. Decisions & Open Questions

### Resolved Decisions

| Question | Decision | Rationale |
|----------|----------|-----------|
| **Template format** | Markdown | Readable, easy to edit, works with Claude Code |
| **Execution** | Yes, analyze + generate + execute | Full workflow - don't leave user with files to run manually |
| **Naming conventions** | Auto-generate with baked-in steps | Files should be deployment-ready, numbered for sequence |
| **PM detection theme** | Stargate SG-1 | User preference; adds character while remaining functional |
| **Subagent execution** | Always run as subagent | Preserve user's main context; isolate decomposition work |
| **User choice on existing orchestration** | Present options (USE AS-IS/REBUILD/BOTH) | Respect existing work; give user agency |
| **Agent allocation** | Task 0 Allocator subagent | PM stays lean; delegate matching to specialist |
| **Agent discovery** | Allocator reads Task tool definition | Subagent has same visibility as PM; no hardcoded lists |
| **Allocation confirmation** | Ambiguous-only by default | Balance user control with minimal friction |

### Open Questions

1. **Feedback loop:** How to capture and learn from execution results?
   - Need to explore what data is available post-execution
   - Could track: success/failure, time taken, manual interventions needed
   - Storage: local file? agent memory? separate log?

---

## 11. References

- [Industry Research Findings](./docs/research/industry-findings.md)
- [Existing Tools Analysis](./docs/research/existing-tools.md)
- [PM-ORCHESTRATION Test Results](../examples/qsys-mute-state-controller/)
