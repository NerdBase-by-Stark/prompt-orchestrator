<!-- Orchestrator: Only include the MANDATORY FIRST STEP section if a CLAUDE.md file
     exists at the project root or a known location. Check for existence before including.
     If no CLAUDE.md found, omit the entire MANDATORY FIRST STEP section. -->

# QRC Room State Controller - Shared Context

> This file is read by ALL subagents before executing their tasks.
> Content in this file is EXTRACTED from the source document.

---

{{#IF_CLAUDE_MD_EXISTS}}
## MANDATORY FIRST STEP

Before doing any work, read: `/home/spark-bitch/CLAUDE.md`
{{/IF_CLAUDE_MD_EXISTS}}

---

## SOURCE DOCUMENT

**Path**: `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v3.md`
**Total Lines**: 1960

> Task files contain EXTRACTED sections from this source document.
> Implement code exactly as shown in the source - do not modify patterns or APIs.

---

## PROJECT OVERVIEW (extracted from source)

The QRC Room State Controller is a Q-SYS plugin (.qplug) that manages mute state across multiple rooms via the QRC (Q-SYS Remote Control) protocol. It connects to a remote Q-SYS Core over TCP, sends Control.Set commands to enforce mute states on a polling interval, and monitors state drift via Control.Get verification.

Version 4.1 adds three new runtime modules: LogManager (flood-protected logging), VerificationManager (periodic Control.Get state checks), and ReconnectManager (exponential backoff reconnection). These modules are developed by isolated subagents to prevent context bloat.

---

## PROJECT PATHS (extracted from source)

| Item | Path |
|------|------|
| Working Directory | `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller` |
| Source Document | `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v3.md` |
| Target Document | `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/QRC-ROOM-STATE-CONTROLLER-IMPLEMENTATION-PLAN-v4.1.md` |
| Orchestration Files | `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/orchestration` |
| Task Files | `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/orchestration/subagent-tasks` |
| Plugin Output (future) | `/home/spark-bitch/ai/qsys-plugins/qsys-mute-state-controller/plugin/room-state-controller.qplug` |

---

## TECHNOLOGIES (extracted from source)

- **Q-SYS Designer**: Audio/video/control DSP platform by QSC
- **Lua 5.3**: Plugin scripting language used by Q-SYS
- **QRC Protocol**: Q-SYS Remote Control -- JSON-RPC 2.0 over raw TCP (port 1710)
- **QPDK**: Q-SYS Plugin Development Kit -- validation tool for .qplug files
- **Mock Server**: `qpdk qrc --port 1710` provides a simulated QRC endpoint for testing

---

## CONSTRAINTS (extracted from source)

1. **Timer scoping (QPDK005)**: All `Timer.New()` calls MUST be at module level, not inside functions. Timers created inside functions are garbage collected immediately.
2. **Module-level variables**: Manager tables (`LogManager`, `VerificationManager`, `ReconnectManager`) must be declared at module level to persist across timer callbacks.
3. **API fidelity**: Use exact Q-SYS APIs as specified -- `Log.Error()`, `Log.Message()`, `Timer.New()`, `Controls.*`. Do NOT substitute with `print()` or other alternatives.
4. **JSON-RPC format**: All QRC commands must use JSON-RPC 2.0 format with `jsonrpc`, `method`, `params`, and `id` fields.
5. **Control naming**: Controls follow the pattern `<room_id>.<control_number>.mic.mute` (e.g., `09.01.mic.mute`).
6. **Preserve v3 content**: All existing v3 content must be preserved except where explicitly modified by a task.

---

## SHARED REFERENCE DATA (extracted from source)

### QRC Port Configuration

| Parameter | Value |
|-----------|-------|
| Default Port | 1710 |
| Protocol | TCP (raw socket) |
| Message Format | JSON-RPC 2.0 |
| Logon Required | Yes (if Core has credentials) |
| Logon Command | `{"jsonrpc":"2.0","method":"Logon","params":{"User":"<user>","Password":"<pass>"},"id":1}` |

### Room Configuration

| Property | Details |
|----------|---------|
| Room Count | User-configurable (1-40), default 34 |
| Controls Per Room | User-configurable (1-20), default 3 |
| Refresh Interval | 5 seconds (polling timer) |
| Verify Interval | 60 seconds (state verification timer) |

---

## RULES FOR ALL AGENTS

1. Read this CONTEXT.md FIRST before executing your task
2. **Task files contain EXTRACTED content from source** - implement exactly as specified
3. Do NOT "improve" or rewrite code from the source
4. Do NOT substitute APIs (if source uses `Log.Message()`, use that exact API)
5. If source content is unclear, report STATUS: CLARIFICATION NEEDED
6. If source is missing something, report the gap - do NOT invent content
7. Report status when complete using the format below

---

## STATUS REPORTING

Every subagent MUST end with this format:

```
STATUS: COMPLETE or FAILED

CHANGES APPLIED:
- [change 1]
- [change 2]

FILES MODIFIED:
- [file path 1]
- [file path 2]

NOTES:
[Any issues, observations, or follow-up needed]
```

### If Blocked

If a task cannot proceed:

```
STATUS: BLOCKED

BLOCKER: [What is preventing progress]
NEEDED: [What is required to unblock]
```

### If Clarification Needed

If source content is unclear:

```
STATUS: CLARIFICATION NEEDED

SOURCE LINES: [line numbers in question]
QUESTION: [Specific question]
OPTIONS: [Possible interpretations, if applicable]
```
