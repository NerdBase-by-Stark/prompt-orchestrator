# {{PROJECT_NAME}} - Shared Context

> This file is read by ALL subagents before executing their tasks.

---

## MANDATORY FIRST STEP

Before doing any work, read: `{{CLAUDE_MD_PATH}}`

---

## PROJECT OVERVIEW

{{PROJECT_DESCRIPTION}}

---

## PROJECT PATHS

| Item | Path |
|------|------|
| Working Directory | `{{WORKING_DIRECTORY}}` |
| Orchestration Files | `{{ORCHESTRATION_PATH}}` |
| Task Files | `{{TASK_FILES_PATH}}` |
{{ADDITIONAL_PATHS}}

---

## TECHNOLOGIES

{{TECHNOLOGIES}}

---

## RULES FOR ALL AGENTS

1. Read this CONTEXT.md FIRST before executing your task
2. Preserve existing content unless explicitly instructed to modify
3. Maintain consistent formatting and style with existing code/documents
4. Follow any coding standards in CLAUDE.md
5. Report status when complete using the format below

{{ADDITIONAL_RULES}}

---

## SHARED STATE

Variables and state tracked across tasks:

{{SHARED_STATE}}

---

## CONSTRAINTS

{{CONSTRAINTS}}

---

## NAMING CONVENTIONS

| Element | Convention |
|---------|------------|
| Task Files | `{order:02d}-{verb}-{noun}.md` |
{{NAMING_CONVENTIONS}}

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

If requirements are unclear:

```
STATUS: CLARIFICATION NEEDED

QUESTION: [Specific question]
OPTIONS: [Possible interpretations, if applicable]
```

---

## REFERENCE DOCUMENTS

{{REFERENCE_DOCUMENTS}}

---

## VALIDATION REQUIREMENTS

All changes must:

{{VALIDATION_REQUIREMENTS}}
