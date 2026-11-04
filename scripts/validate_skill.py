from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skill/kernel-optimization-orchestrator'
required=[SKILL/'SKILL.md',SKILL/'agents/openai.yaml',SKILL/'references/reviewer-csbmv-lessons.md',SKILL/'references/roles/kernel.md',SKILL/'references/roles/performance.md',SKILL/'references/roles/benchmark.md',SKILL/'references/roles/reviewer.md']
for p in required:
    if not p.exists(): raise SystemExit(f"missing {p}")
for p in (ROOT/'schemas').glob('*.json'): json.loads(p.read_text())
metadata=(SKILL/'agents/openai.yaml').read_text()
if '$kernel-optimization-orchestrator' not in metadata: raise SystemExit('openai.yaml default_prompt must name the skill')
print('project skill validation: PASS')
