# Orchestrator Suggestions

> **ADVISORY ONLY** - These observations are NOT included in task files.
> The extracted tasks contain exactly what the source specified.
> Review these suggestions and address as appropriate.
>
> **CRITICAL RULE**: Suggestions are ADVISORY ONLY. They MUST NOT be implemented in task files.
> If a suggestion is accepted by the user, the SOURCE DOCUMENT must be amended first.
> Task files are then re-extracted from the amended source. NEVER modify task files to
> implement a suggestion — that violates EXTRACT DON'T GENERATE.
>
> Status values: OPEN | ACKNOWLEDGED | DEFERRED | N/A

Generated: {{TIMESTAMP}}
Source: {{SOURCE_DOCUMENT}}
Lines Analyzed: {{LINE_COUNT}}

---

## Critical (May Cause Task Failure)

Issues that could prevent successful task execution:

| Line | Category | Observation | Affected Task | Status |
|------|----------|-------------|---------------|--------|
{{CRITICAL_OBSERVATIONS}}

---

## Gaps (Missing Implementation Details)

Items mentioned but not fully specified in source:

| Line | Topic | What's Missing | Affected Task | Status |
|------|-------|----------------|---------------|--------|
{{GAP_OBSERVATIONS}}

---

## Inconsistencies

Contradictions or unclear specifications in source:

| Lines | Issue | Status |
|-------|-------|--------|
{{INCONSISTENCY_OBSERVATIONS}}

---

## Improvement Opportunities

Optional enhancements not in source (implement only if user requests):

| Context | Suggestion | Status |
|---------|------------|--------|
{{IMPROVEMENT_OBSERVATIONS}}

---

## Structural Notes

Observations about task ordering and dependencies:

{{STRUCTURAL_OBSERVATIONS}}

---

## Ambiguous Content (Clarity Flags)

Content where extracted source text may be confused with agent instructions:

| Line | Extracted Text (preview) | Affected Task | Status |
|------|--------------------------|---------------|--------|
{{AMBIGUOUS_CONTENT_ROWS}}

---

## Deferred Items

Items identified during orchestration that should be addressed after workflow completion:

| Item | Context | Suggested Timing |
|------|---------|-----------------|
{{DEFERRED_ITEMS_ROWS}}

---

## Summary

| Category | Count | Action |
|----------|-------|--------|
| Critical | {{CRITICAL_COUNT}} | Address before execution |
| Gaps | {{GAP_COUNT}} | May need clarification |
| Inconsistencies | {{INCONSISTENCY_COUNT}} | Resolve with user |
| Improvements | {{IMPROVEMENT_COUNT}} | Optional |
| Structural | {{STRUCTURAL_COUNT}} | Consider reordering |
| Ambiguous Content | {{AMBIGUOUS_COUNT}} | Review for clarity |
| Deferred | {{DEFERRED_COUNT}} | Address post-workflow |

**Recommendation**: {{RECOMMENDATION}}
