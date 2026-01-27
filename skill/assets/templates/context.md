# {{PROJECT_NAME}} - Shared Context

> This file is read by ALL subagents before executing their tasks.
> Content in this file is EXTRACTED from the source document.

---

## MANDATORY FIRST STEP

Before doing any work, read: `{{CLAUDE_MD_PATH}}`

---

## SOURCE DOCUMENT

**Path**: `{{SOURCE_DOCUMENT_PATH}}`
**Total Lines**: {{SOURCE_TOTAL_LINES}}

> Task files contain EXTRACTED sections from this source document.
> Implement code exactly as shown in the source - do not modify patterns or APIs.

---

## PROJECT OVERVIEW (extracted from source)

{{EXTRACTED_PROJECT_OVERVIEW}}

---

## PROJECT PATHS (extracted from source)

| Item | Path |
|------|------|
| Working Directory | `{{WORKING_DIRECTORY}}` |
| Source Document | `{{SOURCE_DOCUMENT_PATH}}` |
| Orchestration Files | `{{ORCHESTRATION_PATH}}` |
| Task Files | `{{TASK_FILES_PATH}}` |
{{EXTRACTED_ADDITIONAL_PATHS}}

---

## TECHNOLOGIES (extracted from source)

{{EXTRACTED_TECHNOLOGIES}}

---

## CONSTRAINTS (extracted from source)

{{EXTRACTED_CONSTRAINTS}}

---

## RULES FOR ALL AGENTS

1. Read this CONTEXT.md FIRST before executing your task
2. **Task files contain EXTRACTED content from source** - implement exactly as specified
3. Do NOT "improve" or rewrite code from the source
4. Do NOT substitute APIs (if source uses `Log.Message()`, use that exact API)
5. If source content is unclear, report STATUS: CLARIFICATION NEEDED
6. If source is missing something, report the gap - do NOT invent content
7. Report status when complete using the format below

---

## STATUS REPORTING

Every subagent MUST end with this format:

```
STATUS: COMPLETE or FAILED

CHANGES APPLIED:
- [change 1]
- [change 2]

FILES MODIFIED:
- [file path 1]
- [file path 2]

NOTES:
[Any issues, observations, or follow-up needed]
```

### If Blocked

If a task cannot proceed:

```
STATUS: BLOCKED

BLOCKER: [What is preventing progress]
NEEDED: [What is required to unblock]
```

### If Clarification Needed

If source content is unclear:

```
STATUS: CLARIFICATION NEEDED

SOURCE LINES: [line numbers in question]
QUESTION: [Specific question]
OPTIONS: [Possible interpretations, if applicable]
```
