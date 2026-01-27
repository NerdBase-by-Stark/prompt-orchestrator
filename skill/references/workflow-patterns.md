# Workflow Patterns Reference

Detailed patterns and examples for the Prompt Orchestrator skill.

## Task Decomposition Patterns

### Pattern 1: Sequential Pipeline

Tasks that must execute in strict order.

```
[Task 1] → [Task 2] → [Task 3] → [Task 4]
```

**Indicators:**
- "First... then... finally..."
- Numbered steps in prompt
- Output of one task feeds into next

**Example Prompt:**
> Create a new API endpoint, then write unit tests for it, then update the documentation.

**Generated Structure:**
```
01-create-endpoint.md (blocker: none)
02-write-tests.md (blocker: 01)
03-update-docs.md (blocker: 02)
```

### Pattern 2: Fan-Out/Fan-In

Parallel tasks that converge to a single point.

```
         ┌─[Task 2a]─┐
[Task 1] ├─[Task 2b]─┼─[Task 3]
         └─[Task 2c]─┘
```

**Indicators:**
- "Implement X, Y, and Z" (independent items)
- No dependencies between middle tasks
- Common validation/integration at end

**Example Prompt:**
> Set up the project structure, then implement the user module, the product module, and the order module (these can be done in parallel), finally integrate all modules together.

**Generated Structure:**
```
01-setup-structure.md (blocker: none)
02-implement-user.md (blocker: 01, parallel: yes)
03-implement-product.md (blocker: 01, parallel: yes)
04-implement-order.md (blocker: 01, parallel: yes)
05-integrate-modules.md (blocker: 02, 03, 04)
```

### Pattern 3: Generate-Review-Revise Loop

Iterative refinement pattern from AFlow.

```
[Generate] → [Review] → [Revise] → [Validate]
              ↑__________________________|
              (if issues found)
```

**Indicators:**
- Quality requirements mentioned
- "Review and refine"
- Multiple drafts expected

**Example Prompt:**
> Write a comprehensive user guide, review it for accuracy and completeness, revise based on review, then validate with stakeholders.

**Generated Structure:**
```
01-generate-guide.md (operator: Generate)
02-review-guide.md (operator: Review, blocker: 01)
03-revise-guide.md (operator: Revise, blocker: 02)
04-validate-guide.md (operator: Test, blocker: 03)
```

### Pattern 4: Build-Test Pairs

Each implementation paired with its validation.

```
[Build A] → [Test A]
[Build B] → [Test B]
[Integration Test]
```

**Indicators:**
- Testing requirements mentioned
- Multiple components
- Quality gates between phases

**Generated Structure:**
```
01-build-component-a.md
02-test-component-a.md (blocker: 01)
03-build-component-b.md (parallel with 01-02)
04-test-component-b.md (blocker: 03)
05-integration-test.md (blocker: 02, 04)
```

## Complexity Scoring Examples

### Low Complexity (0-30): Execute Directly

**Prompt:** "Add a README file to the project with installation instructions"

**Analysis:**
- Tasks: 1 (add)
- Dependencies: 0
- Files: 1
- **Score: 7** (1×5 + 1×2)

**Recommendation:** Execute directly, no orchestration needed.

### Medium Complexity (31-70): Recommend Orchestration

**Prompt:** "Refactor the authentication module: update the password hashing, add two-factor authentication support, update the user model, write tests for new features, update API documentation"

**Analysis:**
- Tasks: 5 (update, add, update, write, update)
- Dependencies: 3 (tests depend on implementation)
- Files: ~4
- Testing: yes
- **Score: 48** (5×5 + 3×3 + 4×2 + 5)

**Recommendation:** Orchestration recommended.

### High Complexity (71-100): Strongly Recommend

**Prompt:** "Build a complete e-commerce checkout system: create the cart management service, implement payment gateway integration with Stripe, add order processing with inventory checks, implement email notifications, set up webhook handlers for payment events, add comprehensive unit and integration tests, update all API documentation, configure CI/CD deployment"

**Analysis:**
- Tasks: 8
- Dependencies: 5+
- Files: 10+
- Integrations: 2 (Stripe, webhooks)
- Testing: yes
- Conditionals: yes (inventory checks)
- **Score: 95+**

**Recommendation:** Strongly recommend orchestration.

## Task File Structure Guidelines

### Minimal Task (Simple Actions)

```markdown
# TASK: Add Configuration File

## Context
Read first: `./CONTEXT.md`

## Target
Create `config/settings.yaml`

## Requirements
1. Add database connection settings
2. Add API rate limiting defaults
3. Include environment variable overrides

## Validation
- [ ] File created at correct path
- [ ] YAML syntax valid
- [ ] All required keys present

## Output
STATUS: COMPLETE or FAILED
CHANGES APPLIED: [list]
NOTES: [any issues]
```

### Complex Task (Multi-Step Implementation)

```markdown
# TASK: Implement Authentication Service

**Order**: 03
**Operator**: Generate

## Context
Read first: `./CONTEXT.md`
**Blocker(s)**: 02-setup-database

## Target
Implement `/src/services/auth.py` and `/src/routes/auth.py`

## Objective
Create a complete authentication service with JWT tokens, password hashing, and session management.

## Requirements
1. Use bcrypt for password hashing (min 12 rounds)
2. JWT tokens with 24h expiry for access, 7d for refresh
3. Rate limiting: 5 login attempts per minute per IP
4. Session storage in Redis
5. Support for OAuth2 providers (Google, GitHub)

## Implementation Steps
1. Create auth service class with login/logout/refresh methods
2. Implement password hashing utilities
3. Add JWT token generation and validation
4. Create auth routes with rate limiting middleware
5. Add session management with Redis backend

## Validation Criteria
- [ ] All auth routes respond correctly
- [ ] Password hashing meets security requirements
- [ ] JWT tokens validated properly
- [ ] Rate limiting enforced
- [ ] Sessions persist across requests

## Expected Output
- `/src/services/auth.py` - Auth service class
- `/src/routes/auth.py` - Route handlers
- `/tests/test_auth.py` - Unit tests (if testing operator)

## Notes
- Follow existing code style in `/src/services/`
- Use dependency injection for Redis client
- Log all auth events for audit trail

## Output Format
STATUS: COMPLETE or FAILED
CHANGES APPLIED: [files created/modified]
FILES MODIFIED: [list]
NOTES: [any issues]
```

## Operator Application Guidelines

### Generate Operator
**Use for:** Creating new content, code, or documentation

**Task naming:** `XX-create-*.md`, `XX-implement-*.md`, `XX-write-*.md`

**Include in requirements:**
- Specific output format
- Quality standards
- Style guidelines

### Review Operator
**Use for:** Self-critique, code review, document review

**Task naming:** `XX-review-*.md`, `XX-check-*.md`

**Include in requirements:**
- Review criteria checklist
- What to look for (bugs, style, completeness)
- How to report findings

### Revise Operator
**Use for:** Iterative improvement based on review

**Task naming:** `XX-revise-*.md`, `XX-fix-*.md`, `XX-improve-*.md`

**Include in requirements:**
- Reference to review findings
- Specific changes required
- When to stop iterating

### Test Operator
**Use for:** Validation, verification, testing

**Task naming:** `XX-test-*.md`, `XX-validate-*.md`, `XX-verify-*.md`

**Include in requirements:**
- Test cases to execute
- Expected outcomes
- Pass/fail criteria

### Ensemble Operator
**Use for:** Multiple approaches, pick best result

**Task naming:** `XX-ensemble-*.md`, `XX-compare-*.md`

**Include in requirements:**
- Multiple approaches to try
- Evaluation criteria
- Selection method

## Error Recovery Patterns

### Task Failure Recovery

```
WORKFLOW PAUSED
Failed Task: 03-implement-auth
Reason: Missing dependency - Redis not configured
Completed Tasks: 2/5

Options:
1. [RETRY] Retry task 03 after fixing Redis config
2. [SKIP] Skip task 03, continue with tasks that don't depend on it
3. [ABORT] Stop workflow, preserve progress
```

### Blocked Task Detection

When a task reports BLOCKED:
1. Identify the blocker (missing file, unclear requirement, external dependency)
2. Check if blocker can be resolved automatically
3. If not, escalate to user with specific question
4. Resume workflow when blocker resolved

### Partial Completion

When a task partially completes:
1. Document what completed vs what failed
2. Create follow-up task for incomplete portion
3. Update dependencies to reflect partial state
4. Continue if downstream tasks can proceed

## Best Practices

### Task Granularity
- Aim for tasks completable in 2-10 minutes
- Each task should have clear, verifiable output
- Avoid tasks that require user input mid-execution

### Dependency Mapping
- Be explicit about blockers
- Prefer many small dependencies over few large ones
- Allow parallel execution where possible

### Validation Criteria
- Make criteria binary (pass/fail)
- Include automated checks where possible
- Reference specific files/outputs

### Status Reporting
- Always end with STATUS line
- List all changes made
- Note anything unusual for PM awareness
