# Existing Tools & Frameworks Analysis

> Research compiled: 2026-01-27

## Purpose

Evaluate existing tools that could fulfill prompt decomposition needs before building custom solution.

---

## Tier 1: Native to Claude Code

### Task Tool (Built-in)
- **What:** Spawn subagents with isolated context
- **Strengths:** Native, no setup, good isolation
- **Gap:** No auto-decomposition; manual orchestration required
- **Verdict:** Core building block, not a complete solution

### Custom Subagents (.claude/agents/)
- **What:** Define specialized agent types
- **Strengths:** Can formalize PM/worker pattern
- **Gap:** Still requires manual task file creation
- **Verdict:** Could be part of solution

### Plan Mode
- **What:** Research before implementation
- **Strengths:** Built-in context gathering
- **Gap:** Doesn't auto-decompose into executable tasks
- **Verdict:** Complementary, not sufficient

---

## Tier 2: Python Frameworks

### CrewAI
- **Architecture:** Role-based teams ("crews")
- **Alignment:** HIGH - Maps directly to PM + worker pattern
- **Setup:** `pip install crewai`
- **Pros:**
  - Easiest entry point
  - Role/backstory abstraction
  - Task routing by capability
- **Cons:**
  - Python dependency
  - Not native to Claude Code
- **Repo:** https://github.com/crewAIInc/crewAI

### LangGraph
- **Architecture:** Stateful graph workflows
- **Alignment:** MEDIUM - Different paradigm (graphs vs files)
- **Setup:** `pip install langgraph`
- **Pros:**
  - Best for complex state machines
  - Strong output formatting
  - Long-term flexibility
- **Cons:**
  - Steep learning curve
  - Overkill for document generation
- **Repo:** https://github.com/langchain-ai/langgraph

### DSPy
- **Architecture:** Declarative prompt programming
- **Alignment:** MEDIUM - Optimizes prompts, doesn't decompose them
- **Setup:** `pip install dspy-ai`
- **Pros:**
  - Auto-optimizes with metrics
  - Modular signatures
  - Research-backed (Stanford)
- **Cons:**
  - Requires training examples
  - Different mental model
- **Repo:** https://github.com/stanfordnlp/dspy

### DecomP (Allen AI)
- **Architecture:** Modular task decomposition
- **Alignment:** HIGH - Core purpose matches
- **Setup:** Clone repo, Python
- **Pros:**
  - Proven research
  - Sub-task handlers concept
  - Extensible
- **Cons:**
  - Research code, not production tool
  - Requires adaptation
- **Repo:** https://github.com/allenai/DecomP

### AFlow
- **Architecture:** MCTS-based workflow optimization
- **Alignment:** HIGH - Auto-discovers optimal structure
- **Setup:** Clone repo, Python
- **Pros:**
  - ICLR 2025 Oral (validated research)
  - Discovers non-obvious workflows
  - Outperforms manual design
- **Cons:**
  - Outputs code workflows, not markdown
  - Requires Claude adapter
- **Repo:** https://github.com/FoundationAgents/AFlow

---

## Tier 3: Claude Code Community Projects

### claude-flow
- **What:** Multi-agent swarm orchestration
- **Stars:** 1.5k+
- **Alignment:** MEDIUM - Different approach (swarms vs PM)
- **Repo:** https://github.com/ruvnet/claude-flow

### wshobson/agents
- **What:** 108 specialized agents + 15 workflow orchestrators
- **Alignment:** LOW - Pre-built agents, not decomposition
- **Repo:** https://github.com/wshobson/agents

---

## Gap Analysis

### What Exists
- Frameworks for running multi-agent workflows (CrewAI, LangGraph)
- Prompt optimization (DSPy)
- Workflow discovery (AFlow)
- Subagent execution (Claude Code Task tool)

### What Doesn't Exist
**No tool currently does this:**
> "Take complex prompt → analyze → generate PM-ORCHESTRATION.md + CONTEXT.md + subagent-tasks/*.md"

The decomposition-to-files pipeline is missing.

---

## Recommendation

**Build a Claude Code skill** that:
1. Uses native Task tool for execution
2. Borrows concepts from DecomP (modular handlers)
3. Incorporates AFlow operators (Review, Revise, Test)
4. Outputs our proven file structure

This fills the gap while leveraging existing research.
