# Product Requirements Document: Prompt Orchestrator

> Version: 0.1.0-draft
> Author: NerdBase-by-Stark
> Created: 2026-01-27
> Status: Draft

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
Input:  Complex prompt (natural language)
Output: PM-ORCHESTRATION.md + CONTEXT.md + subagent-tasks/*.md
```

### 1.3 Target Users

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

## 3. User Stories

### 3.1 Primary Flow

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

### 3.2 Complexity Assessment

```
As a developer,
I want to know if my prompt needs decomposition,
So that I don't add overhead to simple tasks.
```

**Acceptance Criteria:**
- [ ] Provides complexity score/assessment
- [ ] Recommends: "monolithic OK" vs "decomposition recommended"
- [ ] Threshold configurable (default: 50+ changes or ~500 lines expected)

### 3.3 Customization

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

## 4. Functional Requirements

### 4.1 Input Analysis

The skill MUST analyze the input prompt for:

| Signal | Detection Method |
|--------|-----------------|
| Task count | Count distinct action verbs/objectives |
| Dependencies | Identify "after X", "requires Y", sequential language |
| Parallel opportunities | Independent tasks with no shared state |
| Complexity indicators | Nested requirements, conditionals, multi-file changes |
| Domain context | Extract project paths, technologies, constraints |

### 4.2 Output Structure

#### 4.2.1 PM-ORCHESTRATION.md

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

#### 4.2.2 CONTEXT.md

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

#### 4.2.3 subagent-tasks/{task-file}.md

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

### 4.3 Complexity Scoring

| Score | Recommendation | Criteria |
|-------|----------------|----------|
| 0-30 | Monolithic OK | <5 tasks, no dependencies, <500 lines expected |
| 31-70 | Consider decomposition | 5-15 tasks, some dependencies |
| 71-100 | Decomposition recommended | 15+ tasks, complex dependencies, >500 lines |

### 4.4 Operators (Inspired by AFlow)

The skill should recognize and apply these patterns:

| Operator | When to Apply |
|----------|---------------|
| **Generate** | Creating new content/code |
| **Review** | Self-critique needed |
| **Revise** | Iterative improvement |
| **Test** | Validation required |
| **Ensemble** | Multiple approaches, pick best |

---

## 5. Technical Design

### 5.1 Skill Structure

```
~/.claude/skills/prompt-orchestrator/
├── skill.md           # Main skill definition
├── templates/
│   ├── pm-orchestration.md
│   ├── context.md
│   └── task.md
└── examples/
    └── qsys-mute-state-controller/
```

### 5.2 Invocation

```bash
# Via slash command
/orchestrate "Your complex prompt here"

# With options
/orchestrate --threshold 30 --parallel-detect "Your prompt"

# From file
/orchestrate --file requirements.md
```

### 5.3 Algorithm (High-Level)

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

### 5.4 File Naming Convention

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

## 6. Success Metrics

### 6.1 Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Requirement coverage | >95% | Tasks cover all prompt requirements |
| Dependency accuracy | >90% | Blockers correctly identified |
| Execution success rate | >85% | Workflows complete without manual intervention |

### 6.2 Efficiency Metrics

| Metric | Target |
|--------|--------|
| Generation time | <30 seconds for typical prompt |
| Context budget accuracy | Each task <500 lines |
| Parallel detection | Identify >80% of parallel opportunities |

---

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Over-decomposition | Unnecessary overhead | Complexity threshold; user override |
| Under-decomposition | Quality issues | Conservative scoring; user feedback |
| Incorrect dependencies | Execution failures | Dependency validation step |
| Template rigidity | Doesn't fit all use cases | Customizable templates |

---

## 8. Milestones

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

### Phase 3: Learning (v0.3.0)
- [ ] Execution feedback integration
- [ ] Template refinement based on outcomes
- [ ] Pattern library

---

## 9. Decisions & Open Questions

### Resolved Decisions

| Question | Decision | Rationale |
|----------|----------|-----------|
| **Template format** | Markdown | Readable, easy to edit, works with Claude Code |
| **Execution** | Yes, analyze + generate + execute | Full workflow - don't leave user with files to run manually |
| **Naming conventions** | Auto-generate with baked-in steps | Files should be deployment-ready, numbered for sequence |

### Open Questions

1. **Feedback loop:** How to capture and learn from execution results?
   - Need to explore what data is available post-execution
   - Could track: success/failure, time taken, manual interventions needed
   - Storage: local file? agent memory? separate log?

---

## 10. References

- [Industry Research Findings](./docs/research/industry-findings.md)
- [Existing Tools Analysis](./docs/research/existing-tools.md)
- [PM-ORCHESTRATION Test Results](../examples/qsys-mute-state-controller/)
