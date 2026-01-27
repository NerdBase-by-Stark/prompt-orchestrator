# Prompt Orchestrator Benchmark: v1 vs v2 vs v3

**Test Date**: 2026-01-27
**Source Document**: QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v4.1.md (2714 lines)
**Test Subject**: Q-SYS plugin implementation plan with 6 phases and v4 reliability modules

---

## Executive Summary

This benchmark compares three versions of the prompt-orchestrator skill against the same source document:

| Version | Key Focus | Result |
|---------|-----------|--------|
| **v1** | Basic extraction | Code fidelity issues (`print()` bug), no SUGGESTIONS.md |
| **v2** | Verbatim extraction | Fixed code fidelity, added source line references |
| **v3** | PM Detection + Refinements | Added PM scoring (92/100), Stargate messaging, enhanced SUGGESTIONS.md |

**Winner**: v3 provides the most comprehensive orchestration with PM detection, though v2 also achieves correct code extraction.

---

## Metrics Comparison

| Metric | v1 | v2 | v3 |
|--------|----|----|-----|
| **Task files count** | 10 | 10 | 10 |
| **Total lines (all markdown)** | 4,904 | 5,922 | 6,218 |
| **PM-ORCHESTRATION.md lines** | 103 | 245 | 156 |
| **CONTEXT.md lines** | 109 | 156 | 221 |
| **SUGGESTIONS.md lines** | N/A (not generated) | 119 | 295 |
| **Source line references** | 0 | 10 | 10 |
| **PM Detection Score** | N/A | N/A | 92/100 |

### Analysis

1. **Total Output Growth**: v3 produces 27% more output than v1, primarily due to:
   - Enhanced SUGGESTIONS.md (295 lines vs v2's 119 lines)
   - More comprehensive CONTEXT.md (221 vs 109)

2. **PM-ORCHESTRATION Efficiency**: v3's PM-ORCHESTRATION.md is actually more concise (156 lines) than v2's (245 lines) while containing the PM detection results. This is because v3 uses a cleaner task sequence table format.

3. **Source Line References**: Both v2 and v3 correctly include source line references in all 10 task files. v1 had zero source line references.

---

## Code Fidelity Spot Check

### Test 1: Logging API (source line 1179)

**Source Document** (line 1179):
```
- Log via Log.Error(control_name .. ": " .. message)
```

| Version | Extracted Code | Fidelity |
|---------|----------------|----------|
| **v1** | `print("[ERROR] " .. log_message)` | INCORRECT - Uses `print()` instead of `Log.Error()` |
| **v2** | `Log.Error(control_name .. ": " .. message)` | CORRECT - Verbatim from source |
| **v3** | `Log.Error(control_name .. ": " .. message)` | CORRECT - Verbatim from source |

**v1 Bug Location**: `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/test-orc/subagent-tasks/05-implement-logging-module.md` line 41

### Test 2: Timer Scoping Pattern (source lines 971-972)

**Source Document**:
```lua
-- Module-level timer (CRITICAL: not local)
RefreshTimer = Timer.New()
```

| Version | Preserved Comment | Module-Level | Fidelity |
|---------|------------------|--------------|----------|
| **v1** | Partial | Yes | ADEQUATE |
| **v2** | Yes | Yes | CORRECT |
| **v3** | Yes | Yes | CORRECT |

### Test 3: QRC Command Format (source lines 137-146)

**Source Document**:
```json
{
  "jsonrpc": "2.0",
  "method": "Control.Set",
  "params": {
    "Name": "09.01.mic.mute",
    "Value": 0
  },
  "id": 1
}
```

| Version | Format Preserved | Fidelity |
|---------|-----------------|----------|
| **v1** | Yes | CORRECT |
| **v2** | Yes | CORRECT |
| **v3** | Yes | CORRECT |

---

## PM Detection Results (v3 Feature)

v3 introduced Phase 0: PM Orchestration Detection. For this source document:

### Score Breakdown

| Signal | Points Available | Points Awarded | Detection Notes |
|--------|------------------|----------------|-----------------|
| PM/Coordinator role definition | 20 | 18 | "SUBAGENT PROMPT TEMPLATE", phase coordination language |
| Task sequence table | 20 | 20 | 6 phases with sub-phases 4A/4B/4C/5A clearly defined |
| Dependencies stated | 15 | 13 | Phase rollbacks reference prior phases, implicit dependencies |
| Validation/completion criteria | 15 | 15 | Multiple "Success Criteria:" sections with checkboxes |
| Progress tracking | 15 | 12 | Git commits per phase, v1.0.0 tag mentioned |
| Error handling instructions | 15 | 14 | "ROLLBACK PROCEDURE" sections for each phase |
| **TOTAL** | **100** | **92** | Good orchestration detected |

### User Choice Flow

With score 92/100, v3 would have presented:
```
===============================================
 UNSCHEDULED OFFWORLD ACTIVATION
===============================================

Existing orchestration structure detected in source document.
Verifying IDC before proceeding...

Orchestration Score: 92/100
```

Options:
- **USE AS-IS**: Extract existing PM structure verbatim
- **REBUILD**: Generate skill's optimized structure (selected for this test)
- **BOTH**: Keep original + create PM-ORCHESTRATION-SUGGESTED.md

For this benchmark, **REBUILD** was selected to enable apples-to-apples comparison.

---

## SUGGESTIONS.md Quality Comparison

### v2 SUGGESTIONS.md (119 lines)

Categories covered:
- Critical issues (3 items, 1 fixed)
- Gaps (4 items)
- Inconsistencies (4 items)
- Improvements (6 items)
- Q-SYS API verification needed
- QPDK error codes to watch

### v3 SUGGESTIONS.md (295 lines)

Enhanced categories:
- API Concerns with detailed code examples (3 items)
- Implementation Gaps with suggested fixes (6 items)
- Inconsistencies with line references (4 items)
- Improvement Opportunities with code examples (6 items)
- Structural Observations on dependencies (4 items)
- Risk Observations with mitigations (3 items)
- Summary table with priority ratings

**Key v3 Enhancements**:
1. More detailed API concern explanations with example code
2. Suggested code fixes for gaps (not in task files, advisory only)
3. Risk observations section (new)
4. Priority ratings (HIGH/MEDIUM/LOW)
5. PM detection score context

---

## Scores

Based on the benchmark criteria:

| Criterion | Weight | v1 | v2 | v3 |
|-----------|--------|----|----|-----|
| Code Extraction Fidelity | 30% | 7/10 | 10/10 | 10/10 |
| Source Line References | 15% | 0/10 | 10/10 | 10/10 |
| SUGGESTIONS.md Quality | 20% | 0/10 | 7/10 | 10/10 |
| PM-ORCHESTRATION Structure | 15% | 7/10 | 9/10 | 10/10 |
| CONTEXT.md Completeness | 10% | 7/10 | 9/10 | 10/10 |
| PM Detection (v3 feature) | 10% | N/A | N/A | 10/10 |
| **Weighted Score** | 100% | **4.9/10** | **8.6/10** | **10/10** |

### Score Calculations

**v1**: (0.3 * 7) + (0.15 * 0) + (0.2 * 0) + (0.15 * 7) + (0.1 * 7) = 4.9
**v2**: (0.3 * 10) + (0.15 * 10) + (0.2 * 7) + (0.15 * 9) + (0.1 * 9) = 8.6
**v3**: (0.3 * 10) + (0.15 * 10) + (0.2 * 10) + (0.15 * 10) + (0.1 * 10) + (0.1 * 10) = 10.0

---

## Stargate Messaging (v3 Feature)

v3 introduced thematic messaging for the PM detection flow:

| Scenario | Message Theme |
|----------|---------------|
| Orchestration detected | "UNSCHEDULED OFFWORLD ACTIVATION" |
| USE AS-IS selected | "The iris is open" |
| REBUILD selected | "Dial new coordinates" |
| BOTH selected | "Establish secondary gate" |

This messaging was not triggered in v1/v2 as they lack the PM detection feature.

---

## Conclusion

### v1 Issues
1. Critical code fidelity bug (`print()` vs `Log.Error()`)
2. No source line references
3. No SUGGESTIONS.md
4. No PM detection

### v2 Improvements over v1
1. Fixed code extraction fidelity
2. Added source line references
3. Added SUGGESTIONS.md
4. Improved PM-ORCHESTRATION structure

### v3 Improvements over v2
1. PM Detection scoring (92/100 for this document)
2. User choice flow for detected orchestration
3. Enhanced SUGGESTIONS.md (2.5x more content)
4. Stargate-themed messaging
5. More concise PM-ORCHESTRATION.md

### Recommendation

**v3 is recommended** for production use. The PM detection feature correctly identified that the source document already had strong orchestration (92/100), which would have given the user the choice to:
- Use the existing structure (saving orchestration time)
- Rebuild with skill's optimized structure
- Generate both for comparison

This adaptive behavior makes v3 significantly more useful for varied source documents.

---

## Files Reference

| Version | Location |
|---------|----------|
| v1 Output | `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/test-orc/` |
| v2 Output | `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/test-orc-run2/` |
| v3 Output | `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/test-orc-run3/` |
| Source Document | `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v4.1.md` |
| Benchmark Document | `/home/spark-bitch/ai/prompt-orchestrator/docs/benchmarks/v1-v2-v3-comparison.md` |
