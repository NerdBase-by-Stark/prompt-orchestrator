# Contributing to Prompt Orchestrator

Thank you for your interest in contributing! This project aims to help the community build better AI workflows through research-backed prompt decomposition.

## Ways to Contribute

### 1. Share Orchestration Patterns

Have you developed a successful workflow pattern? We'd love to include it!

**How to contribute:**
1. Document your pattern in the `examples/` directory
2. Include:
   - The original prompt/task
   - Your PM-ORCHESTRATION.md
   - CONTEXT.md
   - Subagent task files
   - Results/metrics if available

### 2. Improve Decomposition Logic

The core algorithm for breaking down prompts can always be improved.

**Areas of interest:**
- Better task boundary detection
- Improved dependency inference
- Parallel opportunity identification
- Context budget estimation

### 3. Add Templates

Different use cases need different templates.

**Template ideas:**
- Code refactoring workflows
- Documentation generation
- Test suite creation
- API implementation
- Bug investigation

### 4. Research & Benchmarking

Help us validate and improve with data.

**How to help:**
- Run comparative tests (monolithic vs orchestrated)
- Document quality metrics
- Share failure cases for analysis

## Development Setup

```bash
# Clone the repo
git clone https://github.com/NerdBase-by-Stark/prompt-orchestrator.git
cd prompt-orchestrator

# No dependencies yet - it's a Claude Code skill!
# Just install the skill when available
```

## Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-pattern`)
3. **Commit** your changes with clear messages
4. **Push** to your fork
5. **Open** a Pull Request

### PR Guidelines

- Keep PRs focused on a single change
- Update documentation if needed
- Add examples for new features
- Reference any related issues

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow

## Questions?

Open an issue with the `question` label, and we'll help!

## Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes for significant contributions
