# Orchestrator Suggestions

> **ADVISORY ONLY** - These observations are NOT included in task files.
> The extracted tasks contain exactly what the source specified.
> Review these suggestions and address as appropriate.

Generated: {{TIMESTAMP}}
Source: {{SOURCE_DOCUMENT}}
Lines Analyzed: {{LINE_COUNT}}

---

## Critical (May Cause Task Failure)

Issues that could prevent successful task execution:

| Line | Category | Observation | Affected Task |
|------|----------|-------------|---------------|
{{CRITICAL_OBSERVATIONS}}

---

## Gaps (Missing Implementation Details)

Items mentioned but not fully specified in source:

| Line | Topic | What's Missing | Affected Task |
|------|-------|----------------|---------------|
{{GAP_OBSERVATIONS}}

---

## Inconsistencies

Contradictions or unclear specifications in source:

| Lines | Issue |
|-------|-------|
{{INCONSISTENCY_OBSERVATIONS}}

---

## Improvement Opportunities

Optional enhancements not in source (implement only if user requests):

| Context | Suggestion |
|---------|------------|
{{IMPROVEMENT_OBSERVATIONS}}

---

## Structural Notes

Observations about task ordering and dependencies:

{{STRUCTURAL_OBSERVATIONS}}

---

## Summary

| Category | Count | Action |
|----------|-------|--------|
| Critical | {{CRITICAL_COUNT}} | Address before execution |
| Gaps | {{GAP_COUNT}} | May need clarification |
| Inconsistencies | {{INCONSISTENCY_COUNT}} | Resolve with user |
| Improvements | {{IMPROVEMENT_COUNT}} | Optional |
| Structural | {{STRUCTURAL_COUNT}} | Consider reordering |

**Recommendation**: {{RECOMMENDATION}}
