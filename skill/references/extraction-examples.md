# Extraction Examples

> Reference file for prompt-orchestrator skill.
> Load when reviewing extraction patterns and anti-patterns.

---

## Example 1: Code Block with Issue

**Source (lines 450-470)**:
```lua
function LogError(message)
  print("[ERROR] " .. message)  -- Wrong API for Q-SYS
end
```

**Task File** (pure extraction):
```markdown
## Implementation (source lines 450-470)

```lua
function LogError(message)
  print("[ERROR] " .. message)  -- Wrong API for Q-SYS
end
```
```

**SUGGESTIONS.md** (observation):
```markdown
| 451 | API | `print()` used for error logging - Q-SYS requires `Log.Error()` | 05-implement-logging |
```

---

## Example 2: Missing Implementation

**Source (line 156)**:
```
Connected: Log, set status=0 (OK), connected=true, send Logon if auth required
```

**Task File** (extract what exists):
```markdown
## Socket Connected Handler (source line 156)

Connected: Log, set status=0 (OK), connected=true, send Logon if auth required
```

**SUGGESTIONS.md** (note the gap):
```markdown
| 156 | Gap | "send Logon if auth required" - Logon command format/sequence not specified | 02-qrc-connection |
```

---

## Example 3: Subagent Prompt Extraction

**Source (lines 200-240)**:
```
**Subagent**: `qsys-plugin-development` skill

**Prompt**:
MANDATORY CONTEXT: Read /home/spark-bitch/CLAUDE.md before proceeding.

PROJECT: QRC Room State Controller

TASK: Create plugin skeleton file...
[40 more lines of detailed requirements]
```

**Task File** (complete extraction):
```markdown
## Subagent Instructions (source lines 200-240)

**Skill**: `qsys-plugin-development`

**Prompt**:

MANDATORY CONTEXT: Read /home/spark-bitch/CLAUDE.md before proceeding.

PROJECT: QRC Room State Controller

TASK: Create plugin skeleton file...
[ALL 40 lines copied verbatim - no summarization]
```

---

## Example 4: Semantic Bundling

**Source Structure**:
- Phase 1: Archive/Setup (lines 50-92)
- Backup Procedures (lines 200-215)
- Rollback Plan (lines 450-465)
- Data Migration (lines 310-340)

**WRONG** (literal extraction):
```markdown
## Source Reference
**Section**: Phase 1: Archive/Setup (lines 50-92)

[Only 42 lines extracted]

Problems:
- No backup commands (exist at lines 200-215)
- No restore procedures (exist at lines 450-465)
- Subagent cannot recover from failure
```

**RIGHT** (semantic bundling):
```markdown
## Source Reference

**Primary Section**: Phase 1: Archive/Setup (lines 50-92)

**Related Sections**:

| Section | Lines | Relationship | Why Bundled |
|---------|-------|--------------|-------------|
| Backup Procedures | 200-215 | Pre-execution safety | Destructive archive operation |
| Rollback Plan | 450-465 | Failure recovery | Must be able to undo |
| Data Migration | 310-340 | Data dependencies | Archive affects this data |

**Total Lines Extracted**: 148

[All 148 lines from primary + related sections]

Result: Self-contained, subagent can backup and recover
```

---

## Anti-Pattern Detection

| Anti-Pattern | Detection Signal | Fix |
|--------------|------------------|-----|
| Narrow extraction | < 50 lines for substantive phase | Re-scan for related sections |
| Missing rollback | Destructive op without recovery | Search for rollback/restore keywords |
| Summarization | Task says "implement X" instead of showing X | Copy source verbatim |
| Pattern substitution | Changed APIs/variable names | Preserve source exactly |
| Injected suggestions | Task contains "Note:" or "Consider:" | Move to SUGGESTIONS.md |
