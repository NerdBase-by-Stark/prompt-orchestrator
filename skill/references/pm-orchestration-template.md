# PM-ORCHESTRATION.md Generation Guide

> Reference file for prompt-orchestrator skill.
> Load when generating PM-ORCHESTRATION.md output.
>
> **Template location**: `assets/templates/pm-orchestration.md` (single source of truth)

---

## Purpose

PM-ORCHESTRATION.md is the PM's execution playbook. It must contain everything the PM needs to coordinate subagents WITHOUT reading task files or source documents.

## Required Sections Checklist

Every generated PM-ORCHESTRATION.md MUST include these sections (template provides structure):

1. Header with project name, timestamp, complexity score, task count, source path
2. SUGGESTIONS AVAILABLE - counts by severity
3. AGENT ALLOCATIONS - summary from TASK-MANIFEST.md
4. PM RULES (READ FIRST) - 7 rules
5. CONTEXT DISCIPLINE - PM reads vs PM does not read, consequence table
6. EXTRACTION-BASED WORKFLOW - subagent instructions for verbatim execution
7. TASK SEQUENCE - order/file/description/blocker/parallel/agent table
8. FILES GENERATED - every file path created during orchestration [NEW in v0.7]
9. EXECUTION INSTRUCTIONS - per-task steps, parallel execution rules
10. PROGRESS TRACKER - status table
11. VALIDATION CHECKLIST - post-completion checks
12. EXTRACTION COVERAGE - source section mapping with totals
13. WHY SUBAGENTS ARE MANDATORY - reasoning table
14. NON-NEGOTIABLES - 8 absolute rules with anti-rationalization phrases
15. ERROR HANDLING - failure/timeout/blocked procedures
16. FINAL OUTPUT - complete/incomplete report formats

## Generation Rules

- Populate ALL `{{DOUBLE_BRACE}}` placeholders during orchestration
- The `{SINGLE_BRACE}` placeholders (only `{TASK_FILE}`) are filled by the PM at dispatch time
- Task descriptions in TASK SEQUENCE must be < 80 chars, no imperative language (H4)
- VALIDATION CHECKLIST must list concrete checks extracted from source (I7)
- FILES GENERATED section must list every file path the orchestrator created (C7)

## Positive Framing Guide (H3)

When writing PM instructions, prefer positive framing:

| Instead of | Write |
|------------|-------|
| "DO NOT READ task files" | "Your ONLY interaction with task files is pointing subagents at their file paths" |
| "DO NOT read the source" | "The source has been fully extracted -- the TASK SEQUENCE table has every detail you need" |
| "DO NOT execute tasks" | "Your role is dispatching agents and tracking results" |

Keep the negative reinforcement in NON-NEGOTIABLES (it works there as a backstop), but lead with positive framing in the main instruction sections.
