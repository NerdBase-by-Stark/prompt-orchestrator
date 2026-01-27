# TASK: Add Phase 4A - Logging Module (CHANGE 6)

## Context

Read first: `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/CONTEXT.md`

---

## Target File

`/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v4.1.md`

---

## CHANGE 6: ADD PHASE 4A - LOGGING MODULE

Insert as a new phase after the basic connection/timer phase:

```markdown
---

## PHASE 4A: LOGGING MODULE WITH FLOOD PROTECTION

**Goal**: Implement intelligent logging that prevents log flooding from persistent errors

**Duration**: 1 hour

**Deliverables**:
- LogManager module integrated into runtime
- Flood protection working (5-minute suppression)
- Success logging per timer cycle
- QPDK validation passes
- Git commit: "Phase 4A: Logging module with flood protection"

### PHASE 4A EXECUTION STEPS

#### Step 4A.1: Implement Logging Module

**Subagent**: `logging-module-implementation`

**Prompt**:
~~~
MANDATORY CONTEXT: Read /home/spark-bitch/CLAUDE.md before proceeding.

PROJECT: QRC Room State Controller - Logging Module

TASK: Implement logging module with flood protection in room-state-controller.qplug

REQUIREMENTS:
1. Create LogManager table at module level with:
   - error_cache = {} -- keyed by control name
   - SUPPRESS_DURATION = 300 -- 5 minutes in seconds

2. Function: LogManager.Error(control_name, message)
   - Check if control_name exists in error_cache
   - If not exists OR (current_time - last_log_time) > SUPPRESS_DURATION:
     - If error_count > 0, append to message: " (suppressed " .. error_count .. " times)"
     - Log via Log.Error(control_name .. ": " .. message)
     - Reset error_count to 0
     - Update last_log_time to current_time
     - Store in error_cache[control_name]
   - Else:
     - Increment error_count only (no log output)

3. Function: LogManager.Success(room_count, control_count)
   - Log.Message("Sent commands to " .. room_count .. " rooms, " .. control_count .. " controls")
   - Called once per timer cycle after all commands sent

4. Function: LogManager.Info(message)
   - Simple wrapper: Log.Message(message)
   - Use for non-error status messages

5. Integrate with command sending:
   - On QRC response error: Call LogManager.Error(control_name, error_message)
   - On control not found: Call LogManager.Error(control_name, "Control not found on remote core")
   - End of timer cycle: Call LogManager.Success(enabled_room_count, total_control_count)

VALIDATION:
- luacheck room-state-controller.qplug (no errors)
- qpdk validate room-state-controller.qplug (passes)

OUTPUT: Updated runtime code section with LogManager integrated
~~~

**Success Criteria**:
- LogManager table exists at module level
- Error and Success functions implemented
- Integration points wired
- QPDK validation passes

---

#### Step 4A.2: Test Logging Flood Protection

**Subagent**: `logging-module-test`

**Prompt**:
~~~
MANDATORY CONTEXT: Read /home/spark-bitch/CLAUDE.md before proceeding.

PROJECT: QRC Room State Controller - Logging Module Test

TASK: Verify logging flood protection works correctly

TEST SETUP:
1. Start QRC mock server with MISSING control to trigger errors:
   cd /home/spark-bitch/ai/qsys-plugins
   qpdk qrc --port 1710 -c "09.01.mic.mute=0" -c "09.02.mic.mute=0"

   NOTE: 09.03.mic.mute intentionally NOT defined

2. Load plugin in test environment
3. Configure Target Core IP to 127.0.0.1, Port 1710
4. Connect to mock server

TEST PROCEDURE:
1. Enable Room 09 (expects 3 controls: 09.01, 09.02, 09.03)

2. Observe logs for first 30 seconds:
   - EXPECTED: ONE error log for 09.03.mic.mute
   - EXPECTED: Success logs each cycle
   - NOT EXPECTED: Repeated errors every 5 seconds

3. Continue observing for 5+ minutes

4. After 5 minutes:
   - EXPECTED: Summary log with suppression count

VALIDATION CRITERIA:
- [ ] First error logged immediately
- [ ] No duplicate errors within 5-minute window
- [ ] Suppression count accurate in summary
- [ ] Success messages logged each cycle

OUTPUT: Test report (PASS/FAIL with observations)
~~~

**Success Criteria**:
- All validation criteria pass
- Log flooding confirmed prevented

---

#### Step 4A.3: Git Commit Phase 4A

**Command**:
```bash
cd /home/spark-bitch/ai/qsys-plugins && \
git add room-state-controller.qplug && \
git commit -m "Phase 4A: Logging module with flood protection

- LogManager table at module level
- Error logging with 5-minute suppression
- Suppression count in summary logs
- Success logging per timer cycle
- QPDK validation: PASSED
- Flood protection test: PASSED"
```

### PHASE 4A SUCCESS CRITERIA

- LogManager module implemented
- Flood protection verified
- QPDK validation: PASSED
- Unit test: PASSED
- Git commit created
```

---

## Output

When complete, report:

```
STATUS: COMPLETE or FAILED
SECTION ADDED: Phase 4A
NOTES: Any issues encountered
```
