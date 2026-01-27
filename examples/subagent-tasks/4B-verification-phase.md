# TASK: Add Phase 4B - Verification Module (CHANGE 7)

## Context

Read first: `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/CONTEXT.md`

---

## Target File

`/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v4.1.md`

---

## CHANGE 7: ADD PHASE 4B - VERIFICATION MODULE

Insert after Phase 4A:

```markdown
---

## PHASE 4B: STATE VERIFICATION MODULE

**Goal**: Implement periodic Control.Get to verify Core B values match expected state

**Duration**: 1-2 hours

**Deliverables**:
- VerificationManager module integrated
- Control.Get commands working
- Mismatch detection and logging
- verification_mismatches control updating
- QPDK validation passes
- Git commit: "Phase 4B: State verification module"

### PHASE 4B EXECUTION STEPS

#### Step 4B.1: Implement Verification Module

**Subagent**: `verification-module-implementation`

**Prompt**:
~~~
MANDATORY CONTEXT: Read /home/spark-bitch/CLAUDE.md before proceeding.

PROJECT: QRC Room State Controller - State Verification Module

TASK: Implement state verification module in room-state-controller.qplug

REQUIREMENTS:
1. Create VerificationManager table at module level with:
   - current_room_index = 1
   - EXPECTED_VALUE = 0

2. Create module-level timer:
   - verify_timer = Timer.New()

3. Function: VerificationManager.Initialize(interval)
   - Set timer interval from "Verify Interval" property
   - Set timer EventHandler to VerificationManager.VerifyNextRoom
   - Start timer

4. Function: VerificationManager.GetEnabledRooms()
   - Return table of rooms where enabled == true

5. Function: VerificationManager.VerifyNextRoom()
   - Get enabled_rooms
   - If none, return
   - Wrap current_room_index if needed
   - Get room, pick first control
   - Send QRC Control.Get command
   - Increment current_room_index

6. QRC Control.Get format:
   {
     "jsonrpc": "2.0",
     "method": "Control.Get",
     "params": ["<control_name>"],
     "id": <unique_id>
   }

7. Function: VerificationManager.HandleResponse(control_name, value)
   - Compare value to EXPECTED_VALUE
   - If mismatch:
     - Increment Controls.verification_mismatches.Value
     - LogManager.Error(control_name, "Value drift: expected 0, got " .. value)

8. Function: VerificationManager.Stop()
   - Stop verify_timer

9. Function: VerificationManager.Start()
   - Start verify_timer

VALIDATION:
- luacheck (no errors)
- qpdk validate (passes)
- verify_timer at module level (QPDK005)

OUTPUT: Updated runtime code with VerificationManager
~~~

**Success Criteria**:
- VerificationManager at module level
- Timer at module level
- Control.Get format correct
- QPDK validation passes

---

#### Step 4B.2: Test State Verification

**Subagent**: `verification-module-test`

**Prompt**:
~~~
MANDATORY CONTEXT: Read /home/spark-bitch/CLAUDE.md before proceeding.

PROJECT: QRC Room State Controller - Verification Test

TASK: Verify state verification detects drift

TEST SETUP:
1. Start mock server with correct values:
   qpdk qrc --port 1710 \
     -c "09.01.mic.mute=0" -c "09.02.mic.mute=0" -c "09.03.mic.mute=0" \
     -c "10.01.mic.mute=0" -c "10.02.mic.mute=0" -c "10.03.mic.mute=0"

2. Configure plugin:
   - Verify Interval: 15 (shorter for testing)
   - Room Count: 2

TEST PROCEDURE PART 1 - Normal:
1. Enable Room 09 and 10
2. Wait 30 seconds
3. Check verification_mismatches = 0
4. Check logs for success messages

TEST PROCEDURE PART 2 - Drift:
1. Restart mock with wrong value:
   qpdk qrc --port 1710 -c "09.01.mic.mute=1" ...
2. Wait for verification
3. Check verification_mismatches >= 1
4. Check logs for drift warning

TEST PROCEDURE PART 3 - Round Robin:
1. Observe 4+ verification cycles
2. Verify both rooms checked alternately

VALIDATION CRITERIA:
- [ ] Control.Get sent at correct interval
- [ ] Correct values = no mismatch
- [ ] Wrong values = detected and logged
- [ ] Counter increments on drift
- [ ] Round-robin works

OUTPUT: Test report (PASS/FAIL)
~~~

**Success Criteria**:
- All criteria pass
- Drift detection verified

---

#### Step 4B.3: Git Commit Phase 4B

**Command**:
```bash
cd /home/spark-bitch/ai/qsys-plugins && \
git add room-state-controller.qplug && \
git commit -m "Phase 4B: State verification module

- VerificationManager at module level
- Control.Get every Verify Interval seconds
- Round-robin through enabled rooms
- Drift detection with mismatch counter
- QPDK validation: PASSED
- Verification test: PASSED"
```

### PHASE 4B SUCCESS CRITERIA

- VerificationManager implemented
- Control.Get working
- Drift detection verified
- Round-robin verified
- QPDK validation: PASSED
- Unit test: PASSED
- Git commit created
```

---

## Output

When complete, report:

```
STATUS: COMPLETE or FAILED
SECTION ADDED: Phase 4B
NOTES: Any issues encountered
```
