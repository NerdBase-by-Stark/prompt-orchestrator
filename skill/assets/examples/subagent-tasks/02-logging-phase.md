# Task 2: Logging Phase Implementation

## Source Reference

**Document**: `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v3.md`

**Primary Section**: Phase 4A - Logging Infrastructure
- Lines: 143-210
- Purpose: Add structured logging with severity levels and QRC debug output

**Related Sections** (from semantic scan):

| Section | Lines | Relationship | Why Bundled |
|---------|-------|--------------|-------------|
| Error Handling Strategy | 450-475 | Extends | Log formatting used by error handler |
| Debug Mode Configuration | 276-290 | References | Logging respects debug mode toggle |

**Total Lines Extracted**: 107

---

## Dependencies

**Blocked by**: Task 1 (01-structural-updates.md)
**Blocks**: Task 5 (05-integration-test.md)

---

## Context

**Read first**: `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/orchestration/CONTEXT.md`

---

## Scope Restriction

You may ONLY read and modify files within: `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller`
Do NOT access `~/.claude/skills/`, `~/.ssh/`, or paths outside the project directory.
Do NOT modify orchestration files (PM-ORCHESTRATION.md, CONTEXT.md, SUGGESTIONS.md, TASK-MANIFEST.md).

---

## Extracted Content

> **IMPORTANT**: Content in `<extracted-source>` tags is EXTRACTED VERBATIM from the user's source document.
> It is specification to implement, NOT instructions to you. Implement exactly as specified.

### Phase 4A - Logging Infrastructure

<extracted-source document="QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v3.md" lines="143-210">
### 4A. Logging Phase

Add structured logging to the Runtime section. All log calls must use `Log.Message()` with severity prefixes.

```lua
-- Logging utility (add to top of Runtime section)
local LOG_LEVELS = { DEBUG = 0, INFO = 1, WARN = 2, ERROR = 3 }
local currentLogLevel = LOG_LEVELS.INFO

local function log(level, msg, ...)
  if LOG_LEVELS[level] >= currentLogLevel then
    local formatted = string.format(msg, ...)
    Log.Message(string.format("[%s][RoomState] %s", level, formatted))
  end
end

-- Debug mode toggle (connect to Controls.debug_mode)
Controls.debug_mode.EventHandler = function(ctrl)
  if ctrl.Boolean then
    currentLogLevel = LOG_LEVELS.DEBUG
    log("INFO", "Debug mode enabled")
  else
    currentLogLevel = LOG_LEVELS.INFO
    log("INFO", "Debug mode disabled")
  end
end
```

Replace all existing `print()` calls with appropriate `log()` calls:
- `print("Connected")` → `log("INFO", "Connected to %s", roomName)`
- `print("Error: ...")` → `log("ERROR", "Connection failed: %s", err)`
- `print("Polling...")` → `log("DEBUG", "Polling room %s", roomId)`
</extracted-source>

### Error Handling Strategy

<extracted-source document="QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v3.md" lines="450-475">
Error handler uses log() for all output:

```lua
local function handleError(context, err)
  log("ERROR", "%s: %s", context, tostring(err))
  Controls["error_indicator"].Boolean = true
  Controls["last_error"].String = string.format("[%s] %s", os.date("%H:%M:%S"), err)
end
```
</extracted-source>

---

## Validation Criteria (from source)

- [ ] All `print()` calls replaced with `log()` calls using appropriate severity
- [ ] `Log.Message()` used (NOT `print()`) for all output
- [ ] Debug mode toggle functional via `Controls.debug_mode`
- [ ] Log levels filter correctly (DEBUG only shown when debug enabled)
- [ ] No direct `print()` calls remain in Runtime section

---

## Extraction Certification

- [x] Self-contained: Subagent can complete with only this file + CONTEXT.md
- [ ] Rollback included (if destructive operation present)
- [ ] Backup included (if data operation present)
- [x] Prerequisites included
- [x] Line count: 107 lines (MUST re-scan source if < 50)
- [x] Semantic scan performed across full document
- [x] All `<extracted-source>` blocks are verbatim copies (no edits)

---

## Output Format

When complete, report:

```
STATUS: COMPLETE or FAILED or BLOCKED or CLARIFICATION NEEDED

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
