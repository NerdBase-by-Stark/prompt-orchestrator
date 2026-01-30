# SUGGESTIONS.md Template

> Reference file for prompt-orchestrator skill.
> Load when generating SUGGESTIONS.md output.

---

## Template

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
| {line} | {category} | {observation} | {task_file} |

---

## Gaps (Missing Implementation Details)

Items mentioned but not fully specified in source:

| Line | Topic | What's Missing | Affected Task |
|------|-------|----------------|---------------|
| {line} | {topic} | {missing} | {task_file} |

---

## Inconsistencies

Contradictions or unclear specifications in source:

| Lines | Issue |
|-------|-------|
| {line_a}, {line_b} | {contradiction} |

---

## Improvement Opportunities

Optional enhancements not in source (implement only if user requests):

| Context | Suggestion |
|---------|------------|
| Line {n} | {suggestion} |

---

## Structural Notes

Observations about task ordering and dependencies:

- {observation about dependencies}
- {observation about parallel opportunities}

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

---

## Severity Classification

| Category | Criteria | Examples |
|----------|----------|----------|
| Critical | Will cause task FAILURE | Wrong API, syntax error, missing import |
| Gap | Task may be INCOMPLETE | Missing detail subagent must guess |
| Inconsistency | Contradictory specs | "34 rooms" vs "40 rooms" |
| Improvement | Optional enhancement | Better error handling, logging |

---

## Observation Types

| Type | What to Log | Example |
|------|-------------|---------|
| API Concerns | Wrong or outdated API usage | "`print()` used - Q-SYS requires `Log.Message()`" |
| Missing Details | Mentioned but not specified | "'if auth required' - Logon implementation not provided" |
| Scope Issues | Variable/timer scoping problems | "Timer declared local - may be garbage collected" |
| Structure Gaps | Incomplete implementations | "Multi-page UI described but page transition logic missing" |
| Error Handling | Missing error scenarios | "No error handling for socket disconnect" |
| Dependencies | Unclear or missing task ordering | "Task 3 may need Task 5's output" |
| Inconsistencies | Contradictions in source | "Line 100 says 34 rooms, line 500 says 'all 40 rooms'" |
