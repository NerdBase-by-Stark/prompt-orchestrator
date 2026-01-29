# Task {{TASK_ORDER}}: {{TASK_NAME}}

## Source Reference

**Document**: `{{SOURCE_DOCUMENT_PATH}}`

**Primary Section**: {{PRIMARY_SECTION_HEADER}}
- Lines: {{PRIMARY_LINE_START}}-{{PRIMARY_LINE_END}}
- Purpose: {{PRIMARY_PURPOSE}}

**Related Sections** (from semantic scan):

| Section | Lines | Relationship | Why Bundled |
|---------|-------|--------------|-------------|
| {{RELATED_SECTION_1}} | {{LINES_1}} | {{RELATIONSHIP_1}} | {{REASON_1}} |

**Total Lines Extracted**: {{TOTAL_LINES}}

---

## Context

**Read first**: `{{CONTEXT_PATH}}`

---

## Extracted Content

> **IMPORTANT**: The content below is EXTRACTED VERBATIM from the source document.
> Implement exactly as specified - do not modify patterns, APIs, or structure.

### {{PRIMARY_SECTION_HEADER}}

{{EXTRACTED_PRIMARY_CONTENT}}

### {{RELATED_SECTION_HEADER}}

{{EXTRACTED_RELATED_CONTENT}}

---

## Validation Criteria (from source)

{{EXTRACTED_VALIDATION}}

---

## Extraction Certification

- [ ] Self-contained: Subagent can complete with only this file
- [ ] Rollback included: {{YES_NO_NA}} (required if destructive operation)
- [ ] Backup included: {{YES_NO_NA}} (required if data operation)
- [ ] Prerequisites included: {{YES_NO_NA}}
- [ ] Line count: {{TOTAL_LINES}} lines (flag if < 50)
- [ ] Semantic scan performed: Yes

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
| Source content unclear | Report STATUS: CLARIFICATION NEEDED - reference specific source lines |
| Technical failures | Report STATUS: FAILED with error details |
| Partial completion | Report what completed and what failed |

**CRITICAL**: Do NOT improvise solutions that deviate from the extracted source content.
If the source is missing something, report the gap - do NOT invent content.
