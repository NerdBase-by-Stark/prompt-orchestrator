# SUGGESTIONS.md Generation Guide

> Reference file for prompt-orchestrator skill.
> Load when generating SUGGESTIONS.md output.
>
> **Template location**: `assets/templates/suggestions.md` (single source of truth)

---

## Purpose

SUGGESTIONS.md captures orchestrator observations that are ADVISORY ONLY. Suggestions NEVER appear in task files. If a suggestion is accepted, the source document must be amended first -- task files are not modified directly (H5).

## Severity Classification

| Category | Criteria | Examples |
|----------|----------|----------|
| Critical | Will cause task FAILURE | Wrong API, syntax error, missing import |
| Gap | Task may be INCOMPLETE | Missing detail subagent must guess |
| Inconsistency | Contradictory specs | "34 rooms" vs "40 rooms" |
| Improvement | Optional enhancement | Better error handling, logging |

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

## Ambiguous Content Detection (NEW - v0.7, C1)

During Phase 1.3, if extracted content contains language that could be confused with instructions to the executing agent (e.g., "you should", "make sure to", "always do X"), flag it:

| Line | Category | Observation | Affected Task |
|------|----------|-------------|---------------|
| {line} | Ambiguous Content | Extracted text at lines X-Y contains directive language that subagents may confuse with orchestrator instructions. Wrapped in `<extracted-source>` for clarity. | {task} |

This is NOT a security flag -- it's a clarity improvement for self-authored plans.

## Status Tracking (NEW - v0.7, I10)

The suggestions table in the asset template now includes a Status column (promoted from biltong-buddy real-world output):

| Status | Meaning |
|--------|---------|
| OPEN | Not yet reviewed |
| ACKNOWLEDGED | PM has read it |
| DEFERRED | Will address post-orchestration |
| N/A | Not applicable to this project |
