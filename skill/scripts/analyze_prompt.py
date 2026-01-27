#!/usr/bin/env python3
"""
Prompt Complexity Analyzer

Analyzes a prompt for complexity signals and outputs a structured report
with task extraction, dependency mapping, and complexity scoring.

Usage:
    python3 analyze_prompt.py --prompt "Your complex prompt here"
    python3 analyze_prompt.py --file requirements.md
    python3 analyze_prompt.py --prompt "..." --json  # JSON output for programmatic use
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Tuple


# Action verbs that indicate distinct tasks
ACTION_VERBS = [
    # Creation
    "create", "build", "implement", "add", "write", "generate", "design",
    # Modification
    "update", "modify", "change", "edit", "refactor", "rename", "move",
    # Configuration
    "configure", "setup", "install", "deploy", "enable", "disable",
    # Testing/Validation
    "test", "validate", "verify", "check", "ensure", "confirm",
    # Data operations
    "migrate", "import", "export", "sync", "backup", "restore",
    # Integration
    "integrate", "connect", "link", "wire", "hook",
    # Removal
    "remove", "delete", "clean", "clear", "drop",
]

# Patterns indicating dependencies
DEPENDENCY_PATTERNS = [
    r"after (?:completing|finishing|doing) (.+)",
    r"once (.+) is (?:complete|done|finished|ready)",
    r"requires (.+) (?:to be|first)",
    r"depends on (.+)",
    r"following (.+)",
    r"when (.+) is (?:complete|done|ready)",
    r"then (.+)",  # Sequential language
    r"next,? (.+)",
    r"finally,? (.+)",
]

# Complexity multipliers
COMPLEXITY_WEIGHTS = {
    "task": 5,
    "dependency": 3,
    "file": 2,
    "conditional": 10,
    "integration": 10,
    "testing": 5,
}


@dataclass
class Task:
    """Represents an extracted task."""
    id: int
    verb: str
    description: str
    blockers: List[int] = field(default_factory=list)
    parallel_group: Optional[int] = None


@dataclass
class AnalysisResult:
    """Complete analysis result."""
    raw_prompt: str
    tasks: List[Task]
    dependencies: List[Tuple[int, int]]  # (blocker_id, blocked_id)
    parallel_groups: List[List[int]]
    complexity_score: int
    complexity_breakdown: dict
    recommendation: str
    file_references: List[str]
    technologies: List[str]


def extract_tasks(prompt: str) -> List[Task]:
    """Extract distinct tasks from prompt based on action verbs."""
    tasks = []

    # Split on sentence boundaries and sequential markers
    # This handles "First... Then... After that... Finally..."
    split_patterns = [
        r'[.;]',  # Sentence boundaries
        r'\n-',  # Bullet points
        r'\n\d+\.',  # Numbered lists
        r'(?:^|\s)(?:first|then|after that|next|finally|lastly|subsequently),?\s',  # Sequential markers
    ]
    combined_pattern = '|'.join(f'({p})' for p in split_patterns)
    sentences = re.split(combined_pattern, prompt, flags=re.IGNORECASE)

    task_id = 1
    for sentence in sentences:
        if not sentence:
            continue
        sentence_clean = sentence.strip().lower()
        if not sentence_clean or len(sentence_clean) < 5:
            continue

        for verb in ACTION_VERBS:
            # Match verb at start of sentence or after common prefixes
            patterns = [
                rf"^{verb}\s+(.+)",
                rf"(?:should|must|need to|will|to)\s+{verb}\s+(.+)",
                rf"(?:i want to|please)\s+{verb}\s+(.+)",
                rf",\s*{verb}\s+(.+)",  # After comma
                rf":\s*{verb}\s+(.+)",  # After colon
            ]

            for pattern in patterns:
                match = re.search(pattern, sentence_clean)
                if match:
                    description = match.group(1)[:100]  # Truncate long descriptions
                    # Clean up description
                    description = re.sub(r'\s+', ' ', description).strip()
                    if description:
                        tasks.append(Task(
                            id=task_id,
                            verb=verb,
                            description=description
                        ))
                        task_id += 1
                        break
            else:
                continue
            break  # Found a task in this sentence, move on

    return tasks


def extract_dependencies(prompt: str, tasks: List[Task]) -> List[Tuple[int, int]]:
    """Extract task dependencies from sequential language."""
    dependencies = []
    prompt_lower = prompt.lower()

    # Look for explicit dependency patterns
    for pattern in DEPENDENCY_PATTERNS:
        matches = re.finditer(pattern, prompt_lower)
        for match in matches:
            referenced = match.group(1)
            # Try to match referenced text to a task
            for i, task in enumerate(tasks):
                if task.description.lower() in referenced or referenced in task.description.lower():
                    # This task depends on task i
                    # Mark the next task as blocked by this one
                    if i + 1 < len(tasks):
                        dependencies.append((task.id, tasks[i + 1].id))

    # Detect sequential language patterns
    sequential_markers = [
        r'first\b.*?then\b',
        r'then\b.*?(?:after that|next|finally)\b',
        r'after that\b.*?(?:next|finally)\b',
        r'\d+\.\s+\w+.*\d+\.\s+\w+',  # Numbered lists
    ]

    has_sequential = any(re.search(p, prompt_lower, re.DOTALL) for p in sequential_markers)

    # If sequential language found and we have tasks, assume sequential order
    if has_sequential and len(tasks) > 1:
        for i in range(len(tasks) - 1):
            dep = (tasks[i].id, tasks[i + 1].id)
            if dep not in dependencies:
                dependencies.append(dep)

    return dependencies


def identify_parallel_opportunities(tasks: List[Task], dependencies: List[Tuple[int, int]]) -> List[List[int]]:
    """Identify tasks that can run in parallel (no shared dependencies)."""
    # Build dependency graph
    blocked_by = {task.id: set() for task in tasks}
    for blocker, blocked in dependencies:
        blocked_by[blocked].add(blocker)

    # Group tasks by their dependency depth
    groups = []
    assigned = set()

    while len(assigned) < len(tasks):
        current_group = []
        for task in tasks:
            if task.id in assigned:
                continue
            # Can run if all blockers are already assigned (completed)
            if blocked_by[task.id].issubset(assigned):
                current_group.append(task.id)

        if current_group:
            groups.append(current_group)
            assigned.update(current_group)
        else:
            # Circular dependency or error - assign remaining
            remaining = [t.id for t in tasks if t.id not in assigned]
            groups.append(remaining)
            break

    return groups


def extract_file_references(prompt: str) -> List[str]:
    """Extract file path references from prompt."""
    patterns = [
        r'[`"\']([^`"\']*\.[a-z]{1,5})[`"\']',  # Quoted file extensions
        r'(/[a-zA-Z0-9_/-]+\.[a-z]{1,5})',  # Absolute paths
        r'(\./[a-zA-Z0-9_/-]+\.[a-z]{1,5})',  # Relative paths
    ]

    files = []
    for pattern in patterns:
        files.extend(re.findall(pattern, prompt))

    return list(set(files))


def extract_technologies(prompt: str) -> List[str]:
    """Extract technology references from prompt."""
    tech_keywords = [
        "python", "javascript", "typescript", "react", "vue", "angular",
        "node", "express", "django", "flask", "fastapi",
        "postgres", "mysql", "mongodb", "redis", "sqlite",
        "docker", "kubernetes", "aws", "gcp", "azure",
        "git", "github", "gitlab", "ci/cd",
        "api", "rest", "graphql", "grpc",
        "lua", "q-sys", "qrc",  # Domain-specific
    ]

    found = []
    prompt_lower = prompt.lower()
    for tech in tech_keywords:
        if tech in prompt_lower:
            found.append(tech)

    return found


def calculate_complexity(
    tasks: List[Task],
    dependencies: List[Tuple[int, int]],
    files: List[str],
    prompt: str
) -> Tuple[int, dict]:
    """Calculate complexity score with breakdown."""
    breakdown = {
        "tasks": len(tasks) * COMPLEXITY_WEIGHTS["task"],
        "dependencies": len(dependencies) * COMPLEXITY_WEIGHTS["dependency"],
        "files": len(files) * COMPLEXITY_WEIGHTS["file"],
        "conditionals": 0,
        "integrations": 0,
        "testing": 0,
    }

    # Check for conditionals
    conditional_patterns = [r"if .+", r"when .+", r"unless .+", r"depending on"]
    for pattern in conditional_patterns:
        breakdown["conditionals"] += len(re.findall(pattern, prompt.lower())) * COMPLEXITY_WEIGHTS["conditional"]

    # Check for integration requirements
    integration_patterns = [r"integrate", r"connect to", r"api", r"external"]
    for pattern in integration_patterns:
        if re.search(pattern, prompt.lower()):
            breakdown["integrations"] += COMPLEXITY_WEIGHTS["integration"]

    # Check for testing requirements
    testing_patterns = [r"test", r"validate", r"verify", r"ensure"]
    for pattern in testing_patterns:
        if re.search(pattern, prompt.lower()):
            breakdown["testing"] += COMPLEXITY_WEIGHTS["testing"]

    total = sum(breakdown.values())
    # Cap at 100
    return min(total, 100), breakdown


def get_recommendation(score: int) -> str:
    """Get recommendation based on complexity score."""
    if score <= 30:
        return "MONOLITHIC_OK: Simple task, orchestration optional"
    elif score <= 70:
        return "RECOMMEND_DECOMPOSITION: Moderate complexity, orchestration recommended"
    else:
        return "STRONGLY_RECOMMEND: High complexity, orchestration strongly recommended"


def analyze_prompt(prompt: str) -> AnalysisResult:
    """Main analysis function."""
    tasks = extract_tasks(prompt)
    dependencies = extract_dependencies(prompt, tasks)
    parallel_groups = identify_parallel_opportunities(tasks, dependencies)
    files = extract_file_references(prompt)
    technologies = extract_technologies(prompt)
    score, breakdown = calculate_complexity(tasks, dependencies, files, prompt)
    recommendation = get_recommendation(score)

    # Update tasks with blocker info
    for blocker, blocked in dependencies:
        for task in tasks:
            if task.id == blocked:
                task.blockers.append(blocker)

    # Assign parallel groups to tasks
    for group_idx, group in enumerate(parallel_groups):
        for task_id in group:
            for task in tasks:
                if task.id == task_id:
                    task.parallel_group = group_idx

    return AnalysisResult(
        raw_prompt=prompt,
        tasks=tasks,
        dependencies=dependencies,
        parallel_groups=parallel_groups,
        complexity_score=score,
        complexity_breakdown=breakdown,
        recommendation=recommendation,
        file_references=files,
        technologies=technologies,
    )


def format_human_readable(result: AnalysisResult) -> str:
    """Format analysis result for human reading."""
    lines = [
        "=" * 60,
        "PROMPT COMPLEXITY ANALYSIS",
        "=" * 60,
        "",
        f"Complexity Score: {result.complexity_score}/100",
        f"Recommendation: {result.recommendation}",
        "",
        "BREAKDOWN:",
    ]

    for key, value in result.complexity_breakdown.items():
        lines.append(f"  {key}: {value}")

    lines.extend([
        "",
        f"TASKS IDENTIFIED: {len(result.tasks)}",
        "-" * 40,
    ])

    for task in result.tasks:
        blockers = f" [blocked by: {task.blockers}]" if task.blockers else ""
        parallel = f" [parallel group: {task.parallel_group}]" if task.parallel_group is not None else ""
        lines.append(f"  {task.id}. {task.verb.upper()}: {task.description}{blockers}{parallel}")

    if result.parallel_groups:
        lines.extend([
            "",
            "PARALLEL EXECUTION GROUPS:",
            "-" * 40,
        ])
        for i, group in enumerate(result.parallel_groups):
            lines.append(f"  Group {i + 1}: Tasks {group}")

    if result.file_references:
        lines.extend([
            "",
            "FILE REFERENCES:",
            "-" * 40,
        ])
        for f in result.file_references:
            lines.append(f"  - {f}")

    if result.technologies:
        lines.extend([
            "",
            "TECHNOLOGIES DETECTED:",
            "-" * 40,
            f"  {', '.join(result.technologies)}",
        ])

    lines.extend(["", "=" * 60])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze prompt complexity")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prompt", "-p", help="The prompt text to analyze")
    group.add_argument("--file", "-f", help="File containing the prompt")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, 'r') as f:
                prompt = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    else:
        prompt = args.prompt

    result = analyze_prompt(prompt)

    if args.json:
        # Convert to JSON-serializable format
        output = {
            "complexity_score": result.complexity_score,
            "complexity_breakdown": result.complexity_breakdown,
            "recommendation": result.recommendation,
            "task_count": len(result.tasks),
            "tasks": [
                {
                    "id": t.id,
                    "verb": t.verb,
                    "description": t.description,
                    "blockers": t.blockers,
                    "parallel_group": t.parallel_group,
                }
                for t in result.tasks
            ],
            "dependencies": result.dependencies,
            "parallel_groups": result.parallel_groups,
            "file_references": result.file_references,
            "technologies": result.technologies,
        }
        print(json.dumps(output, indent=2))
    else:
        print(format_human_readable(result))


if __name__ == "__main__":
    main()
