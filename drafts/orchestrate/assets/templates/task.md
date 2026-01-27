# TASK: {{TASK_NAME}}

**Order**: {{TASK_ORDER}}
**Operator**: {{OPERATOR_TYPE}}

---

## Context

**Read first**: `{{CONTEXT_PATH}}`

**Blocker(s)**: {{BLOCKERS}}

---

## Target

{{TARGET_DESCRIPTION}}

**Output file(s)**:
{{OUTPUT_FILES}}

---

## Objective

{{OBJECTIVE}}

---

## Requirements

{{REQUIREMENTS_LIST}}

---

## Implementation Steps

{{IMPLEMENTATION_STEPS}}

---

## Validation Criteria

Before marking COMPLETE, verify:

{{VALIDATION_CRITERIA}}

---

## Expected Output

When this task completes successfully:

{{EXPECTED_OUTPUT}}

---

## Notes

{{NOTES}}

---

## Output Format

When complete, report:

```
STATUS: COMPLETE or FAILED

CHANGES APPLIED:
- [list each change made]

FILES MODIFIED:
- [list each file created or modified]

NOTES:
[Any issues encountered, observations, or follow-up needed]
```

---

## Error Handling

If you encounter issues:

| Issue | Action |
|-------|--------|
| Missing dependencies | Report STATUS: BLOCKED with specifics |
| Unclear requirements | Report STATUS: CLARIFICATION NEEDED with question |
| Technical failures | Report STATUS: FAILED with error details |
| Partial completion | Report what completed and what failed |

**Do NOT improvise solutions that deviate from requirements.**
