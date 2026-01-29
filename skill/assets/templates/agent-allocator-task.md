# Task 0: Agent Allocation

> **Priority**: MANDATORY FIRST
> **Purpose**: Match tasks to best available agents before execution begins

---

## YOUR ROLE

You are the **Agent Allocator**. Your job is to match tasks to the best available agents based on their capabilities.

**You are NOT executing tasks.** You are only making allocation decisions.

---

## WHAT YOU READ

**ONLY read**: `TASK-MANIFEST.md` (~500 tokens max)

**DO NOT read**:
- Individual task files (context preservation)
- Source documents
- Other orchestration files

The manifest contains all capability information you need.

---

## HOW TO DISCOVER AVAILABLE AGENTS

### 1. Agent Types (from Task Tool Definition)

Look at your Task tool definition - the `subagent_type` parameter lists all available agent types:

| Agent Type | Best For |
|------------|----------|
| `general-purpose` | Default fallback, broad capabilities |
| `code` | Code implementation, refactoring |
| `research` | Investigation, analysis, documentation |
| (others as defined in tool) | (check tool definition) |

### 2. Skills (from System Reminders)

Check your system reminders for available skills that might be relevant:

| Skill Pattern | Example Skills |
|---------------|----------------|
| Domain-specific | `qsys-plugin-development`, `cisco-codec-search` |
| Tool-based | `firecrawl`, `agent-browser` |
| Analysis | `luacheck`, `qsys-plugin-test` |

**Skills take precedence** when they match task capabilities exactly.

---

## CAPABILITY MATCHING RULES

For each task in TASK-MANIFEST.md:

1. **Read the capabilities listed** (e.g., `lua, q-sys, testing`)
2. **Match to best available agent or skill**
3. **Assign confidence score**

### Matching Priority

1. **Exact skill match** (100% confidence)
   - Task: `lua, q-sys` -> Skill: `qsys-plugin-development`

2. **Strong capability match** (85-95% confidence)
   - Task: `networking, api` -> Agent: `code`

3. **General match** (75-84% confidence)
   - Task: `file-ops, config` -> Agent: `general-purpose`

4. **Weak/ambiguous match** (<75% confidence)
   - Multiple agents could work equally well
   - Flag for user review

---

## CONFIDENCE SCORING

| Scenario | Confidence | Action |
|----------|------------|--------|
| Single agent matches all capabilities | 90-100% | Auto-assign |
| Multiple agents match, one clearly better | 80-89% | Auto-assign with note |
| Multiple agents match equally well | 50-70% | Flag as AMBIGUOUS |
| No agent matches, using general-purpose | 50% | Flag as AMBIGUOUS (see fallback rule) |
| User specified agent in source | 100% | Passthrough, no review |

### Agent Allocation Fallback

If **no specific agent** matches the required capabilities:

1. **Allocate `general-purpose`** as the default agent
2. **Set confidence to 50%**
3. **Flag as `AMBIGUOUS`** for user review
4. **Note the reason**: "No agent matched capabilities: {list}"

This ensures the workflow never stalls with "pending" allocations indefinitely.

### Confidence Thresholds

- **80%+**: Auto-assign (unless `--confirm-agents` mode)
- **<80%**: Flag as ambiguous (ask user in `--ambiguous-only` mode)

---

## OUTPUT FORMAT

Return an updated TASK-MANIFEST.md with:

1. **Allocated Agent column filled** for all tasks
2. **Confidence column filled** with percentage
3. **Ambiguous Tasks section updated** with flagged tasks

### Example Output

\`\`\`markdown
## Task Capabilities

| Task File | Capabilities | User-Specified Agent | Allocated Agent | Confidence |
|-----------|--------------|----------------------|-----------------|------------|
| 01-setup-env.md | file-ops, config | - | general-purpose | 85% |
| 02-implement-qrc.md | lua, q-sys, networking | - | qsys-plugin-development | 95% |
| 03-add-ui.md | lua, frontend, q-sys | - | AMBIGUOUS | 65% |
| 04-write-tests.md | testing, lua | test-agent | test-agent | 100% |

## Allocation Summary

**Auto-assigned**: 2 tasks (high confidence)
**Ambiguous**: 1 task (needs user input)
**User-specified**: 1 task (passthrough)

## Ambiguous Tasks

| Task | Capabilities | Options | Why Ambiguous |
|------|--------------|---------|---------------|
| 03-add-ui.md | lua, frontend, q-sys | \`qsys-plugin-development\` OR \`code\` | Both handle Lua; frontend could go either way |
\`\`\`

---

## RULES (NON-NEGOTIABLE)

1. **NEVER read individual task files** - manifest only
2. **NEVER guess capabilities** not in manifest
3. **ALWAYS provide confidence scores**
4. **ALWAYS explain ambiguous choices**
5. **User-specified agents are FINAL** - do not question them, mark as 100% confidence

---

## COMPLETION

Report when done:

\`\`\`
STATUS: COMPLETE
ALLOCATIONS: {count} tasks assigned
AMBIGUOUS: {count} tasks need user input
MANIFEST: Updated TASK-MANIFEST.md written
\`\`\`

If unable to complete:

\`\`\`
STATUS: FAILED
REASON: {specific reason}
\`\`\`
