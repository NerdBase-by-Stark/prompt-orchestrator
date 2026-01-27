# TASK: Structural Updates (CHANGES 1-5)

## Context

Read first: `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/CONTEXT.md`

---

## Target File

`/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v4.1.md`

---

## CHANGE 1: ADD "CHANGES FROM v3" SECTION

Insert immediately after the existing "CHANGES FROM v2" section:

```markdown
---

## CHANGES FROM v3

### v4 Enhancements

**Problems Addressed in v4**:
- No feedback on command success/failure - commands sent blindly
- No protection against log flooding from persistent errors
- No verification that Core B controls actually hold correct values
- Basic reconnection without backoff could hammer failed connection
- Testing was integrated into build phases, risking context bloat

**Solutions in v4**:
1. **Logging Module with Flood Protection**: Errors logged once per control, then suppressed for 5 minutes with summary count
2. **State Verification Module**: Periodic Control.Get confirms Core B values match expected state
3. **Reconnection with Exponential Backoff**: 5s→10s→20s→40s→60s delays, max 10 attempts before manual intervention required
4. **Subagent Isolation**: Each module built and tested by dedicated subagent to keep context slim
5. **Dedicated Test Phases**: Unit tests per module plus full integration test

**Changes Made**:
1. New Runtime Module: LogManager (flood protection)
2. New Runtime Module: VerificationManager (Control.Get round-robin)
3. New Runtime Module: ReconnectManager (exponential backoff)
4. New Property: "Verify Interval" (integer, default 60 seconds)
5. New Control: "verification_mismatches" (indicator, read-only)
6. New Control: "reconnect_attempts" (indicator, read-only)
7. Updated Data Model: Added error tracking fields per room
8. New Subagent Prompts: 3 implementation + 3 unit test + 1 integration test
9. Updated Phase Success Criteria: Include new module validations
```

---

## CHANGE 2: UPDATE PLUGIN STRUCTURE SECTION

Replace the Runtime Code tree within the Plugin Structure section:

```markdown
└── Runtime Code
    ├── QRC Connection Module     # TCP socket, JSON-RPC, response handling
    ├── Room Management Module    # Dynamic room definitions, user-defined names, enable/disable
    ├── Command Generation Module # Control.Set JSON-RPC messages
    ├── Timer Module              # 5-second polling (module-level)
    ├── Persistence Module        # State storage (table)
    ├── Logging Module            # Flood-protected logging (v4)
    ├── Verification Module       # Control.Get state verification (v4)
    └── Reconnection Module       # Exponential backoff reconnection (v4)
```

---

## CHANGE 3: UPDATE DATA MODEL SECTION

Replace the Room Definition code block:

```markdown
**Room Definition** (v4 - With Error Tracking):
```lua
{
  id = "09",                        -- Floor/zone ID (used for control name generation)
  name = "Executive Boardroom",     -- USER-DEFINED via room_name control
  enabled = false,
  controls = {
    "09.01.mic.mute",
    "09.02.mic.mute",
    "09.03.mic.mute"
  },
  -- v4 additions for logging flood protection
  last_error = nil,                 -- Last error message for this room
  error_count = 0,                  -- Count of suppressed errors
  last_error_log_time = 0           -- Timestamp of last logged error
}
```
```

---

## CHANGE 4: UPDATE GetProperties()

Add to the GetProperties requirements list in Phase 1, Step 1.2:

```markdown
   - "Verify Interval" (integer, min 10, max 300, default 60) # seconds between state verification checks
```

---

## CHANGE 5: UPDATE GetControls()

Add to the controls list in the phase where controls are defined:

```markdown
   - "verification_mismatches" (Indicator, Integer, read-only, default 0) -- count of detected value drifts
   - "reconnect_attempts" (Indicator, Integer, read-only, default 0) -- current consecutive reconnect attempts
```

---

## Output

When complete, report:

```
STATUS: COMPLETE or FAILED
CHANGES APPLIED: 1, 2, 3, 4, 5
NOTES: Any issues encountered
```
