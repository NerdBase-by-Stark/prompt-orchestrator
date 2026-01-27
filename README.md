# Prompt Orchestrator

> Automatically decompose complex prompts into orchestrated, executable workflows for Claude Code.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
├── CONTEXT.md             # Shared context for all subagents
└── subagent-tasks/
    ├── task-1-setup.md
    ├── task-2-implement.md
    └── task-3-validate.md
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

### Current (Planned for v0.1)
- [ ] Prompt complexity analysis
- [ ] PM-ORCHESTRATION.md generation
- [ ] CONTEXT.md generation
- [ ] Subagent task file generation

### Roadmap
- [ ] Complexity scoring with threshold
- [ ] Parallel task detection
- [ ] Dependency inference
- [ ] Validation criteria generation
- [ ] Execution feedback learning

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
