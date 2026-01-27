# Benchmark: Skill v1 vs v2 Comparison

> Test Date: 2026-01-27
> Source Document: QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v4.1.md (2714 lines)
> Test Location: /home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/

## Executive Summary

**v2 is definitively superior.** The v2 orchestrator skill produces output that is significantly more faithful to the source document, includes critical metadata (source line references, document traceability), properly extracts code verbatim from the source rather than generating new code, and provides a SUGGESTIONS.md file that captures potential issues.

The v1 skill **generated code that contains errors** (e.g., `print("[ERROR]")` instead of the source-specified `Log.Error()`), while v2 **extracted the exact code blocks** from the source document, preserving accuracy.

---

## Key Design Change

| v1 Approach | v2 Approach |
|-------------|-------------|
| **GENERATE** code based on understanding | **EXTRACT** code verbatim from source |
| Skill acts as code generator | Skill acts as splitter/organizer |
| Errors introduced via regeneration | Errors eliminated via extraction |

---

## Metrics Comparison

| Metric | v1 | v2 | Winner |
|--------|----|----|--------|
| Task files | 10 | 10 | Tie |
| Total lines (all markdown) | 4,904 | 5,918 | **v2** (+21%) |
| Task file lines | 1,979 | 2,685 | **v2** (+36%) |
| PM-ORCHESTRATION.md lines | 104 | 246 | **v2** (+137%) |
| CONTEXT.md lines | 110 | 157 | **v2** (+43%) |
| Source line references | 0 | 10 (every task) | **v2** |
| SUGGESTIONS.md | No | Yes (120 lines) | **v2** |
| Generated code (errors possible) | Yes | No | **v2** |
| Extracted verbatim code | No | Yes | **v2** |
| Critical issues flagged | 0 | 4 | **v2** |
| Improvement opportunities | 0 | 6 | **v2** |

---

## Code Fidelity Check (Critical Test)

### Example 1: LogManager.Error Function

**Source (line 1178)**:
```lua
Log.Error(control_name .. ": " .. message)
```

**v1 output (GENERATED)**:
```lua
print("[ERROR] " .. log_message)
```

**v2 output (EXTRACTED)**:
```lua
Log.Error(control_name .. ": " .. message)
```

**Verdict**: v1 ❌ INCORRECT (used `print()` instead of Q-SYS `Log.Error()`). v2 ✅ CORRECT.

### Example 2: EnableRoom Function (lines 760-770)

**Source**:
```lua
function EnableRoom(roomID)
  if not RoomConfig[roomID] then
    Log.Error("Room " .. roomID .. " not found")
    return false
  end
  RoomConfig[roomID].enabled = true
  UpdateRoomStatus(roomID)
  Log.Message("Room " .. roomID .. " (" .. RoomConfig[roomID].name .. ") enabled")
  return true
end
```

**v1 output**:
```lua
function EnableRoom(roomID)
  if not RoomConfig[roomID] then return false end
  RoomConfig[roomID].enabled = true
  UpdateRoomStatus(roomID)
  return true
end
```

**v2 output**: Identical to source (verbatim extraction)

**Verdict**: v1 ❌ INCOMPLETE (missing `Log.Error`, `Log.Message` calls). v2 ✅ CORRECT.

### Example 3: ProcessQRCResponse Function (lines 464-474)

**Source**:
```lua
if not success then
  Log.Error("JSON parse error: " .. tostring(response))
  return
end

if response.error then
  Log.Error("QRC Error " .. response.error.code .. ": " .. response.error.message)
```

**v1 output**:
```lua
if not success then
  Controls.Outputs["error_message"].String = "JSON parse error"
  return
end

if response.error then
  Controls.Outputs["error_message"].String = response.error.message
```

**v2 output**: Identical to source (verbatim extraction)

**Verdict**: v1 ❌ OMITTED all `Log.Error()` calls. v2 ✅ CORRECT.

---

## Confirmed Bugs in v1 Output

| Bug | Location | Impact |
|-----|----------|--------|
| `print()` instead of `Log.Error()` | Logging module | Errors go to wrong output, not Q-SYS log |
| Missing `Log.Error()` in EnableRoom | Room management | Silent failures, no debugging info |
| Missing `Log.Message()` in EnableRoom | Room management | No success confirmation |
| Omitted error logging in response handler | QRC connection | Errors not logged |

**Total: 4 bugs introduced by code generation**

---

## SUGGESTIONS.md Analysis (v2 only)

v2 generated a SUGGESTIONS.md file with 18 categorized observations:

### Critical Issues (4)
| Line | Issue |
|------|-------|
| 233 | `Status.OK()` - verify valid Q-SYS API |
| 443 | `\x00` null terminator syntax |
| 474 | Mixed `Controls.Outputs`/`Controls.Inputs` pattern |
| 1859 | Layout array indexing pattern |

### Gaps (4)
- Logon command format not provided
- `page_index` property not defined
- `os.date()` availability uncertain

### Improvement Opportunities (6)
- Request ID tracking
- Error messages could include room name
- State save/restore suggestions

**Value**: These observations help the user identify potential issues BEFORE execution, rather than discovering them during debugging.

---

## Scores

| Aspect | v1 Score (1-10) | v2 Score (1-10) |
|--------|-----------------|-----------------|
| Accuracy | 4 | 9 |
| Completeness | 5 | 8 |
| Fidelity to source | 3 | 9 |
| Usefulness | 5 | 8 |
| Execution readiness | 4 | 8 |
| Documentation | 5 | 9 |
| Error prevention | 2 | 8 |
| **TOTAL** | **28/70** | **59/70** |

---

## Conclusion

The v1 → v2 redesign validated the core principle:

> **EXTRACT, DON'T GENERATE**

v1's code generation approach introduced bugs that would have required debugging during execution. v2's extraction approach eliminates this failure mode entirely.

### Key Learnings

1. **Extraction > Generation**: When source documents contain implementation details, extract them verbatim rather than regenerating
2. **Line References Matter**: v2's source line references enable verification and debugging
3. **Separate Observations**: SUGGESTIONS.md captures analytical insights without contaminating task files
4. **Complexity Scoring**: v2's score (357) was more accurate than v1's (195) for a 2714-line document

---

## Files

- v1 output: `test-orc/`
- v2 output: `test-orc-run2/`
- Source: `QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v4.1.md`
