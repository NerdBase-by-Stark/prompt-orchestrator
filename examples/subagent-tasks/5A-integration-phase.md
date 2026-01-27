# TASK: Add Phase 5A - Integration Test (CHANGE 9)

## Context

Read first: `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/CONTEXT.md`

---

## Target File

`/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v4.1.md`

---

## CHANGE 9: ADD PHASE 5A - INTEGRATION TEST

Insert before the final packaging/deployment phase:

```markdown
---

## PHASE 5A: FULL INTEGRATION TEST

**Goal**: Verify all v4 modules work together correctly

**Duration**: 1-2 hours

**Deliverables**:
- Full integration test executed
- All modules verified working together
- Test report documented
- Git commit: "Phase 5A: Integration test passed"

### PHASE 5A EXECUTION STEPS

#### Step 5A.1: Run Integration Test

**Subagent**: `integration-test`

**Prompt**:
~~~
MANDATORY CONTEXT: Read /home/spark-bitch/CLAUDE.md before proceeding.

PROJECT: QRC Room State Controller - Integration Test

TASK: Execute comprehensive integration test

TEST SETUP:
1. Start mock with partial controls (one missing):
   qpdk qrc --port 1710 \
     -c "09.01.mic.mute=0" -c "09.02.mic.mute=0" \
     -c "10.01.mic.mute=0" -c "10.02.mic.mute=0" -c "10.03.mic.mute=0"

   NOTE: 09.03.mic.mute MISSING

2. Configure plugin:
   - Target Core IP: 127.0.0.1
   - Port: 1710
   - Refresh Interval: 5
   - Verify Interval: 30
   - Room Count: 2
   - Controls Per Room: 3

---

TEST A: Initial Connection (0:00)
- [ ] Connect, verify status green
- [ ] reconnect_attempts = 0
- [ ] commands_sent = 0
- [ ] verification_mismatches = 0

TEST B: Single Room (0:01)
- [ ] Name Room 09 "Test Alpha"
- [ ] Enable Room 09
- [ ] Wait 10s, verify commands_sent > 0
- [ ] active_rooms = 1
- [ ] Mock receiving Control.Set

TEST C: Error Handling (0:02)
- [ ] Check ONE error for 09.03
- [ ] Wait 30s, NO duplicate errors
- [ ] Commands still sending

TEST D: Multi-Room (0:03)
- [ ] Name Room 10 "Test Beta"
- [ ] Enable Room 10
- [ ] active_rooms = 2
- [ ] Mock receiving both rooms

TEST E: Verification Normal (0:04)
- [ ] Wait for verify interval
- [ ] Mock receives Control.Get
- [ ] verification_mismatches = 0

TEST F: Drift Detection (0:05)
- [ ] Restart mock with drift:
   -c "09.01.mic.mute=1" ...
- [ ] Wait for reconnect + verify
- [ ] verification_mismatches >= 1
- [ ] Log shows drift warning

TEST G: Reconnection Under Load (0:08)
- [ ] Restore correct mock
- [ ] Kill mock suddenly
- [ ] Status = "Reconnecting..."
- [ ] NO socket errors
- [ ] Wait 15s, restart mock
- [ ] Verify full recovery

TEST H: Room Disable (0:12)
- [ ] Disable Room 09
- [ ] active_rooms = 1
- [ ] Only Room 10 commands

TEST I: All Disabled (0:13)
- [ ] Disable Room 10
- [ ] active_rooms = 0
- [ ] Connection maintained
- [ ] Verification skipped

VALIDATION:
- All checkboxes pass
- No unexpected errors
- QPDK still passes

OUTPUT: Full test report
~~~

**Success Criteria**:
- All test sequences pass
- All modules work together
- No regressions

---

#### Step 5A.2: Git Commit Phase 5A

**Command**:
```bash
cd /home/spark-bitch/ai/qsys-plugins && \
git add . && \
git commit -m "Phase 5A: Integration test passed

- All v4 modules verified working together
- Logging flood protection: VERIFIED
- State verification: VERIFIED
- Reconnection backoff: VERIFIED
- Multi-room operation: VERIFIED
- Error handling: VERIFIED
- Full integration test: PASSED"
```

### PHASE 5A SUCCESS CRITERIA

- All test sequences passed
- All modules working together
- No regressions identified
- Git commit created
```

---

## Output

When complete, report:

```
STATUS: COMPLETE or FAILED
SECTION ADDED: Phase 5A
NOTES: Any issues encountered
```
