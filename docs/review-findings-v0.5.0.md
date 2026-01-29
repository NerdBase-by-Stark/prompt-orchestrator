# prompt-orchestrator v0.5.0 Review Findings

> Generated: 2026-01-29
> Reviewers: Prompt Engineer Agent, Skill Creator Agent
> Status: P0 COMPLETE - P1/P2 Pending

---

## Overall Scores

| Reviewer | Score | Verdict |
|----------|-------|---------|
| Prompt Engineer | 8.5/10 | Production ready with P0 fixes needed |
| Skill Creator | 8/10 | Solid architecture, template sync needed |

---

## P0 - Critical Fixes (Do First) ✓ COMPLETE

### 1. Recursion Guard (Prompt Engineer) ✓

**Problem**: If a subagent reads SKILL.md and misidentifies as main context, it could spawn another subagent infinitely.

**Fix**: Add to Execution Model section in SKILL.md:

```markdown
**Recursion Guard:**
If you find this content in your Task tool prompt:
> "Execute the prompt-orchestrator skill"
Then you ARE the subagent. DO NOT spawn again. Proceed with Phase 0.
```

### 2. Agent Allocation Fallback (Prompt Engineer) ✓

**Problem**: If no suitable agent exists for a capability set, the manifest shows "pending" indefinitely and workflow stalls.

**Fix**: Add to agent-allocator-task.md:

```markdown
**Agent Allocation Fallback:**
If no specific agent matches required capabilities:
1. Allocate "general-purpose" as default
2. Set confidence to 50%
3. Flag as "ambiguous" for user review
```

### 3. Task Template Sync (Skill Creator) ✓

**Problem**: SKILL.md Section 2.3 shows a detailed task file structure with "Related Sections" table and "Extraction Certification" checklist, but `assets/templates/task.md` uses a simpler structure.

**Fix**: Update `~/.claude/skills/prompt-orchestrator/assets/templates/task.md` to include:
- Related Sections table format
- Extraction Certification checklist
- Total Lines Extracted field

---

## P1 - Important Fixes

### 4. Chain-of-Thought for Semantic Bundling (Prompt Engineer)

**Location**: Section 2.1.1

**Add**:
```markdown
**Semantic Bundling Chain of Thought:**

1. Identify the PRIMARY operation (what verb: CREATE, DELETE, MODIFY, ARCHIVE?)
2. List REQUIRED safety nets (backup? rollback? validation?)
3. Search ENTIRE document for keywords: {rollback keywords}
4. For EACH match, ask: "Is this semantically related to PRIMARY operation?"
5. Bundle ALL matches answering YES
6. Re-verify: "Can subagent now complete AND recover?"
```

### 5. Expand Destructive Operation Keywords (Prompt Engineer)

**Current list**: DELETE, DROP, REMOVE, TRUNCATE, ARCHIVE, WIPE, CLEAR, PURGE, RESET

**Add**: DESTROY, TERMINATE, KILL, OVERWRITE, UNINSTALL, DECOMMISSION

### 6. Move Verbose Sections to References (Skill Creator)

**Problem**: SKILL.md is 1,114 lines - excessive.

**Move to `references/`**:
- Section 2.4 (Capability Inference Rules)
- Section 2.5 (PM-ORCHESTRATION.md Required Sections)
- Section 2.6 (Create SUGGESTIONS.md template)
- "Good PM Orchestration Reference" section (lines 1001-1114)
- Extraction examples (lines 911-988)

### 7. Update Example PM-ORCHESTRATION.md (Skill Creator)

**Problem**: Example at `assets/examples/PM-ORCHESTRATION.md` lacks:
- TASK 0: AGENT ALLOCATION section
- SUGGESTIONS AVAILABLE section
- WHY SUBAGENTS ARE MANDATORY section

**Fix**: Either update to match full template or label as "simplified example"

### 8. Expand Capability Inference Rules (Prompt Engineer)

**Add to table**:
| Pattern | Tag |
|---------|-----|
| async, await, promise, callback | `async`, `concurrency` |
| parser, regex, parse | `parsing` |
| cache, memoize, Redis | `caching` |
| log, trace, debug, monitor | `observability` |
| encryption, hash, SSL/TLS | `cryptography` |

---

## P2 - Nice to Have

### 9. Large Document Handling (Prompt Engineer)

**Add for documents >1000 lines**:
```markdown
**Large Document Handling (>1000 lines):**
1. First pass: Index all section headers with line numbers
2. Semantic scan uses index, not full re-read
3. Extract sections by line range rather than re-reading
```

### 10. Clarify Phase 0 Score Range Actions (Skill Creator)

**Current**: 40-59 and 60-100 both trigger "Present user choice"

**Fix**: Differentiate recommendations:
- Score 80-100: Recommend USE AS-IS
- Score 60-79: Recommend BOTH
- Score 40-59: Recommend REBUILD

### 11. Add Version to Frontmatter (Skill Creator)

**Add to SKILL.md header**: `version: 0.5.0`

### 12. Plain-English Subtitles for Stargate Theme (Prompt Engineer)

**Update Phase 0 options**:
| Option | Code | Plain English |
|--------|------|---------------|
| USE AS-IS | "The iris is open" | Keep existing orchestration structure |
| REBUILD | "Dial new coordinates" | Replace with new optimized structure |
| BOTH | "Establish secondary gate" | Keep original + create improved version |

### 13. Self-Detection Phrases for Anti-Pattern 6 (Prompt Engineer)

**Add to PM Executing Directly anti-pattern**:
```markdown
**Self-Detection Phrases (if you think/write these, STOP):**
- "I'll just quickly..."
- "Since this is straightforward..."
- "To save time..."
- "Direct execution would be more efficient..."
- "This doesn't need a subagent..."
```

### 14. Explicit TASK-MANIFEST.md Generation Step (Skill Creator)

**Problem**: Phase 2.3 mentions TASK-MANIFEST.md but lacks explicit procedural step.

**Fix**: Add step "2.4 Generate TASK-MANIFEST.md" with capability inference instructions.

### 15. Directive Conflict Resolution (Prompt Engineer)

**Add**:
```markdown
**Directive Conflict Resolution:**
If source document contradicts SKILL.md rules:
1. SKILL.md rules take precedence (HOW orchestration works)
2. Source document defines WHAT to build
3. Note conflict in SUGGESTIONS.md as Critical
4. Proceed with skill rules unless user explicitly overrides
```

### 16. Severity Classification for SUGGESTIONS.md (Prompt Engineer)

**Add**:
| Category | Criteria | Examples |
|----------|----------|----------|
| Critical | Will cause task FAILURE | Wrong API, syntax error |
| Gap | Task may be INCOMPLETE | Missing detail subagent must guess |
| Inconsistency | Contradictory specs | "34 rooms" vs "40 rooms" |
| Improvement | Optional enhancement | Better error handling |

---

## Files to Modify

| File | Changes |
|------|---------|
| `~/.claude/skills/prompt-orchestrator/SKILL.md` | P0 #1, P1 #4-5, P2 #9-16 |
| `~/.claude/skills/prompt-orchestrator/assets/templates/task.md` | P0 #3 |
| `~/.claude/skills/prompt-orchestrator/assets/templates/agent-allocator-task.md` | P0 #2 |
| `~/.claude/skills/prompt-orchestrator/assets/examples/PM-ORCHESTRATION.md` | P1 #7 |
| `~/.claude/skills/prompt-orchestrator/references/` | P1 #6 (new files) |

---

## Test Plan After Fixes

1. Run orchestrator on same source document (expressive-churning-puppy.md)
2. Verify task files have 100+ lines (not 42)
3. Verify TASK-MANIFEST.md has allocated agents (not all "pending")
4. Verify no infinite subagent spawning
5. Compare Run 4 output to Run 1 benchmark (should be closer)

---

## Session Context (for resumption)

- Project: `~/ai/prompt-orchestrator`
- GitHub: `https://github.com/NerdBase-by-Stark/prompt-orchestrator`
- Current version: v0.5.0 (commit 5a1c1a4)
- Test runs: `/home/spark-bitch/ai/ingest-pipeline/orchestrator*`
- Source for testing: `~/.claude/plans/expressive-churning-puppy.md`

### Version History This Session

| Version | Commit | Changes |
|---------|--------|---------|
| v0.3.0 | 409fa38 | PM detection, Stargate theming, auto-subagent |
| v0.3.1 | f757efa | Enforce subagent usage in PM-ORCHESTRATION |
| v0.3.2 | 138a6af | Shut down PM rationalization about "efficiency" |
| v0.4.0 | 422d970 | Agent Allocator system |
| v0.4.1 | 87d23f1 | Blocking self-spawn enforcement |
| v0.5.0 | 5a1c1a4 | Semantic content bundling, extraction completeness |

### Key Memories Stored

- PM detection pattern (mem_20260127_205732_1749)
- Template enforcement gotcha (mem_20260127_214415_8032)
- LLM rationalization gotcha (mem_20260127_215218_7924)
- Agent Allocator pattern (mem_20260129_212824_2400)
- Self-spawn gotcha (mem_20260129_213726_2337)
- Extraction completeness pattern (mem_20260129_223417_2150)
