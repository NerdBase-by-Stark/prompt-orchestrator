# Orchestrator Suggestions

> **ADVISORY ONLY** - These observations are NOT included in task files.
> The extracted tasks contain exactly what the source specified.
> Review these suggestions and address as appropriate.
>
> **CRITICAL RULE**: Suggestions are ADVISORY ONLY. They MUST NOT be implemented in task files.
> If a suggestion is accepted by the user, the SOURCE DOCUMENT must be amended first.
> Task files are then re-extracted from the amended source. NEVER modify task files to
> implement a suggestion -- that violates EXTRACT DON'T GENERATE.
>
> Status values: OPEN | ACKNOWLEDGED | DEFERRED | N/A

Generated: 2026-03-11T14:32:00Z
Source: QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v3.md
Lines Analyzed: 1960

---

## Critical (May Cause Task Failure)

Issues that could prevent successful task execution:

| Line | Category | Observation | Affected Task | Status |
|------|----------|-------------|---------------|--------|
| 162 | API mismatch | Source uses `print("Error: " .. msg)` in LogManager.Error example but Q-SYS requires `Log.Error()`. Using `print()` will not appear in Q-SYS diagnostic logs and may cause silent failures during testing. | 02-logging-phase.md | OPEN |
| 385 | Missing API | Source references `Socket:Connect(ip, port)` in ReconnectManager but does not specify whether this is `TcpSocket:Connect()` or `TcpSocketClient:Connect()`. Wrong class will cause runtime error. | 04A-reconnection-phase.md | ACKNOWLEDGED |

---

## Gaps (Missing Implementation Details)

Items mentioned but not fully specified in source:

| Line | Topic | What's Missing | Affected Task | Status |
|------|-------|----------------|---------------|--------|
| 78 | QRC Logon | Source mentions "Logon Required: Yes (if Core has credentials)" but never specifies the exact JSON-RPC Logon command format or when to send it in the connection sequence. Subagent may need to infer or look up the Logon message structure. | 02-logging-phase.md, 04A-reconnection-phase.md | OPEN |

---

## Inconsistencies

Contradictions or unclear specifications in source:

| Lines | Issue | Status |
|-------|-------|--------|
| 24, 310 | Room count discrepancy: Line 24 states "supports up to 34 rooms" in project overview, but line 310 defines Room Count property as "integer, min 1, max 40, default 34". The max and the stated limit disagree -- 34 vs 40. Tasks use the property definition (max 40) but documentation may confuse users. | OPEN |

---

## Improvement Opportunities

Optional enhancements not in source (implement only if user requests):

| Context | Suggestion | Status |
|---------|------------|--------|
| Phase 4C reconnection uses exponential backoff but has no jitter. Under network partition, multiple plugins reconnecting simultaneously could create a thundering herd. Adding random jitter (e.g., delay * (0.8 + math.random() * 0.4)) would spread reconnection attempts. | Add jitter to exponential backoff delay calculation | DEFERRED |
| LogManager.Error suppresses per control_name but has no way to clear the cache when connection is re-established. Stale entries persist indefinitely. | Add LogManager.ClearCache() called from ReconnectManager.OnConnect() | OPEN |

---

## Structural Notes

Observations about task ordering and dependencies:

Phase 4B (verification module) depends on Phase 4A's LogManager being available because `VerificationManager.HandleResponse()` calls `LogManager.Error()` for drift detection logging. The task sequence correctly enforces this ordering (Task 3 blocked by Task 2). If Task 2 fails, Tasks 3 and 4 cannot proceed.

---

## Ambiguous Content (Clarity Flags)

Content where extracted source text may be confused with agent instructions:

| Line | Extracted Text (preview) | Affected Task | Status |
|------|--------------------------|---------------|--------|
| 158 | "MANDATORY CONTEXT: Read /home/spark-bitch/CLAUDE.md before proceeding." -- This text appears inside a nested subagent prompt within the extracted source. A subagent executing the task file may interpret this as a direct instruction rather than content to insert into the v4.1 document. | 02-logging-phase.md | ACKNOWLEDGED |

---

## Deferred Items

Items identified during orchestration that should be addressed after workflow completion:

| Item | Context | Suggested Timing |
|------|---------|-----------------|
| Performance benchmarking | With 40 rooms x 20 controls = 800 Control.Set commands per 5-second cycle, the timer callback may exceed its interval. Source does not address command batching or throttling. | Post-v4.1, before production deployment |

---

## Summary

| Category | Count | Action |
|----------|-------|--------|
| Critical | 2 | Address before execution |
| Gaps | 1 | May need clarification |
| Inconsistencies | 1 | Resolve with user |
| Improvements | 2 | Optional |
| Structural | 1 | Consider reordering |
| Ambiguous Content | 1 | Review for clarity |
| Deferred | 1 | Address post-workflow |

**Recommendation**: Address the 2 critical items (print() vs Log.Error() API mismatch, Socket class ambiguity) before dispatching Tasks 2 and 4. The gap regarding Logon command format may be resolvable by the subagent via CONTEXT.md shared reference data. All other items are non-blocking.
