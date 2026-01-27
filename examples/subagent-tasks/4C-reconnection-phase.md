# TASK: Add Phase 4C - Reconnection Module (CHANGE 8)

## Context

Read first: `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/CONTEXT.md`

---

## Target File

`/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v4.1.md`

---

## CHANGE 8: ADD PHASE 4C - RECONNECTION MODULE

Insert after Phase 4B:

```markdown
---

## PHASE 4C: RECONNECTION MODULE WITH EXPONENTIAL BACKOFF

**Goal**: Implement robust reconnection with exponential backoff

**Duration**: 1-2 hours

**Deliverables**:
- ReconnectManager module integrated
- Exponential backoff working (5s→60s cap)
- Max 10 attempts before manual intervention
- reconnect_attempts control updating
- QPDK validation passes
- Git commit: "Phase 4C: Reconnection module"

### PHASE 4C EXECUTION STEPS

#### Step 4C.1: Implement Reconnection Module

**Subagent**: `reconnection-module-implementation`

**Prompt**:
~~~
MANDATORY CONTEXT: Read /home/spark-bitch/CLAUDE.md before proceeding.

PROJECT: QRC Room State Controller - Reconnection Module

TASK: Implement reconnection with exponential backoff

REQUIREMENTS:
1. Create ReconnectManager table at module level:
   - attempt_count = 0
   - current_delay = 5
   - BASE_DELAY = 5
   - MAX_DELAY = 60
   - MAX_ATTEMPTS = 10

2. Create module-level timer:
   - reconnect_timer = Timer.New()

3. Function: ReconnectManager.OnDisconnect()
   - Stop command timer
   - Stop verification timer
   - Update status to "Disconnected - Reconnecting..."
   - Call ScheduleReconnect()

4. Function: ReconnectManager.ScheduleReconnect()
   - If attempt_count >= MAX_ATTEMPTS:
     - Status = "Reconnect Failed - Manual Intervention Required"
     - Log error, return
   - Increment attempt_count
   - Update reconnect_attempts control
   - Log attempt info
   - Set reconnect_timer to current_delay
   - Start timer (single shot)

5. Function: ReconnectManager.AttemptReconnect()
   - Stop reconnect_timer
   - Log "Attempting reconnection..."
   - Call Socket:Connect()
   - current_delay = math.min(current_delay * 2, MAX_DELAY)

6. Function: ReconnectManager.OnConnect()
   - Stop reconnect_timer
   - Reset attempt_count = 0
   - Reset current_delay = BASE_DELAY
   - Update reconnect_attempts to 0
   - Status = "Connected"
   - Log success
   - Restart command timer
   - Restart verification timer

7. Function: ReconnectManager.Reset()
   - Reset all state
   - Stop reconnect_timer

8. Wire into socket EventHandler:
   - Connected → OnConnect()
   - Closed/Error → OnDisconnect()

VALIDATION:
- luacheck (no errors)
- qpdk validate (passes)
- reconnect_timer at module level (QPDK005)

OUTPUT: Updated runtime with ReconnectManager
~~~

**Success Criteria**:
- ReconnectManager at module level
- Backoff logic correct
- Max attempts enforced
- QPDK validation passes

---

#### Step 4C.2: Test Reconnection Logic

**Subagent**: `reconnection-module-test`

**Prompt**:
~~~
MANDATORY CONTEXT: Read /home/spark-bitch/CLAUDE.md before proceeding.

PROJECT: QRC Room State Controller - Reconnection Test

TASK: Verify exponential backoff works

TEST SETUP:
1. Start mock server:
   qpdk qrc --port 1710 -c "09.01.mic.mute=0" -c "09.02.mic.mute=0" -c "09.03.mic.mute=0"
2. Connect plugin, enable Room 09

TEST PART 1 - Disconnect Detection:
1. Kill mock server
2. Check:
   - [ ] Status = "Disconnected - Reconnecting..."
   - [ ] Timers stopped (no socket errors)
   - [ ] Log shows "Connection closed"

TEST PART 2 - Backoff Timing:
1. Keep mock stopped
2. Timestamp attempts:
   - Attempt 1: ~5s after disconnect
   - Attempt 2: ~10s after attempt 1
   - Attempt 3: ~20s after attempt 2
   - Attempt 4: ~40s
   - Attempt 5+: ~60s (capped)
3. Verify reconnect_attempts incrementing

TEST PART 3 - Successful Reconnect:
1. At attempt 3-4, restart mock
2. Check:
   - [ ] Status = "Connected"
   - [ ] reconnect_attempts = 0
   - [ ] Timers resumed

TEST PART 4 - Max Attempts:
1. Let it fail 10 times (~7 min, or reduce MAX_ATTEMPTS for testing)
2. Check:
   - [ ] Status = "Manual Intervention Required"
   - [ ] No more attempts
3. Manually click Connect
4. Verify connection works

VALIDATION CRITERIA:
- [ ] Disconnect detected
- [ ] Timers stopped during disconnect
- [ ] Backoff correct (5→10→20→40→60→60...)
- [ ] Successful reconnect resets state
- [ ] Max attempts stops trying
- [ ] Manual connect works after max

OUTPUT: Test report with timestamps
~~~

**Success Criteria**:
- All criteria pass
- Backoff timing verified

---

#### Step 4C.3: Git Commit Phase 4C

**Command**:
```bash
cd /home/spark-bitch/ai/qsys-plugins && \
git add room-state-controller.qplug && \
git commit -m "Phase 4C: Reconnection with exponential backoff

- ReconnectManager at module level
- Backoff: 5s -> 10s -> 20s -> 40s -> 60s (cap)
- Max 10 attempts before manual intervention
- reconnect_attempts control
- All timers stopped during disconnect
- QPDK validation: PASSED
- Reconnection test: PASSED"
```

### PHASE 4C SUCCESS CRITERIA

- ReconnectManager implemented
- Exponential backoff verified
- Max attempts enforced
- Timer management correct
- QPDK validation: PASSED
- Unit test: PASSED
- Git commit created
```

---

## Output

When complete, report:

```
STATUS: COMPLETE or FAILED
SECTION ADDED: Phase 4C
NOTES: Any issues encountered
```
