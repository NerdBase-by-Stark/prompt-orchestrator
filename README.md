# Prompt Orchestrator

> Automatically decompose complex prompts into orchestrated, executable workflows for Claude Code.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: v0.5.2](https://img.shields.io/badge/Status-v0.5.2-blue.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()

---

## What is this? (Plain English)

**Ever given Claude a big task and watched it forget things halfway through?** That's context fatigue.

This tool **prepares your complex tasks for better execution** - it doesn't do the work itself, it sets up the work to be done properly.

**What it does:**

1. **You give it a big, complex request** (like a detailed implementation plan)
2. **It reads through and breaks it into smaller, focused task files**
3. **It creates a coordination file** that tells a PM how to run each task in order
4. **It flags potential issues** without changing your original content

**What you get:**
- A folder of task files ready to be executed one-by-one
- Each task can run in fresh context - no fatigue, no forgotten instructions
- A manifest showing which AI agent type suits each task

**Think of it like this:** You hand over a 50-page instruction manual. This tool doesn't build the thing - it creates a project plan: "Here's Task 1 for the setup specialist, Task 2 for the database specialist..." Then you (or Claude) can execute that plan.

**Why bother?**
- Monolithic prompt execution: 4.9/10 quality
- Orchestrated task execution: 10/10 quality

---

**This project is under active development.** We're building this in the open and welcome contributions!

## The Problem

Large, complex prompts suffer from:
- **Context fatigue** after ~500 lines
- **Instruction neglect** when too many directives compete
- **Requirement omission** - the #1 failure mode (per E2EDevBench research)
- **No self-verification** in single-shot execution

**Research shows:** Decomposed workflows outperform monolithic prompts by significant margins. GPT-3.5 with agentic workflow achieves 95.1% on HumanEval vs 48.1% zero-shot.

## The Solution

A Claude Code skill that transforms complex prompts into structured, executable workflows:

```
Input:  Complex prompt (natural language)
Output: PM-ORCHESTRATION.md + CONTEXT.md + subagent-tasks/*.md
```

## Quick Start

```bash
# Install the skill (coming soon)
claude skill install prompt-orchestrator

# Use it
/orchestrate "Your complex prompt here"
```

## How It Works

1. **Analyze** - Parse prompt for tasks, dependencies, context
2. **Score** - Assess complexity (recommend decomposition or not)
3. **Decompose** - Break into logical task units
4. **Generate** - Output orchestration files

### Output Structure

```
your-project/
├── PM-ORCHESTRATION.md    # Task sequence, blockers, progress tracker
├── TASK-MANIFEST.md       # Agent allocation & capability mapping
├── CONTEXT.md             # Shared context for all subagents
├── SUGGESTIONS.md         # Advisory observations (not in tasks)
└── subagent-tasks/
    ├── 01-setup-env.md
    ├── 02-implement-api.md
    └── 03-add-tests.md
```

## Research Foundation

This project is built on proven research:

| Technique | Source | Finding |
|-----------|--------|---------|
| Prompt Chaining | ACL 2024 | Chained prompts outperform mega-prompts |
| Agentic Workflows | Andrew Ng | 4 patterns drive massive AI progress |
| Least-to-Most | Google Research | 99% vs 16% on SCAN benchmark |
| Plan-and-Solve | ACL 2023 | Explicit planning improves reasoning |
| Task Decomposition | E2EDevBench | Reduces complexity, improves success |

See [docs/research/](docs/research/) for full research compilation.

## Example

From our test case (QRC Room State Controller):

**Before (Monolithic v4):**
- Missed 4 rollback issues
- Context fatigue observed

**After (Orchestrated v4.1):**
- Caught all 4 rollback issues
- Clear task boundaries
- Verifiable progress

See [examples/](examples/) for the full orchestration files.

## Features

### Current (v0.5.2)
- [x] Prompt complexity analysis & scoring
- [x] PM-ORCHESTRATION.md generation with subagent enforcement
- [x] CONTEXT.md generation with deduplication
- [x] TASK-MANIFEST.md for agent allocation
- [x] SUGGESTIONS.md for advisory observations
- [x] Subagent task file generation with semantic bundling
- [x] Existing orchestration detection (USE AS-IS / REBUILD / BOTH)
- [x] Anti-rationalization rules (PM can't skip subagents)
- [x] Recursion guard for nested invocations
- [x] Progressive reference loading (lean core skill)

### Roadmap
- [ ] Parallel task detection & execution
- [ ] Execution feedback learning
- [ ] Custom agent type definitions
- [ ] Integration with other orchestration tools

## Contributing

We welcome contributions! This project aims to help the community build better AI workflows.

### Ways to Contribute
- Share your orchestration patterns
- Improve decomposition algorithms
- Add templates for different use cases
- Report issues and suggest features

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Documentation

- [Product Requirements (PRD)](specs/PRD.md)
- [Industry Research](docs/research/industry-findings.md)
- [Existing Tools Analysis](docs/research/existing-tools.md)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Andrew Ng's work on agentic workflows
- Allen AI's DecomP research
- AFlow team (ICLR 2025)
- The Claude Code community
