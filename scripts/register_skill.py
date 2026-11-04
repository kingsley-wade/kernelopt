"""Install or inspect this repository's Codex skill directory."""
import argparse
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "kernel-optimization-orchestrator"
SOURCE = ROOT / "skill" / SKILL_NAME

def codex_home():
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))

def make_report(destination, installed, mode):
    return {
        "runtime_name": "Codex local skill directory",
        "runtime_version": "unknown",
        "skill_source": str(SOURCE),
        "destination": str(destination),
        "registered": installed,
        "discovery_verified": installed and (destination / "SKILL.md").is_file(),
        "native_subagents": False,
        "role_registration": {
            "orchestrator": "skill_entrypoint",
            "kernel": "sequential_fallback",
            "performance": "sequential_fallback",
            "benchmark": "sequential_fallback",
            "reviewer": "sequential_fallback",
        },
        "mode": mode,
        "registration_status": "verified_with_fallback" if installed else "ready_to_install",
        "install_command": "python scripts/register_skill.py --install",
        "github_install_command": "python $CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo <owner>/<repo> --path skill/kernel-optimization-orchestrator",
        "limitations": [
            "Native per-role subagent routing depends on the installing Runtime.",
            "Hardware compile, correctness, benchmark and profiler execution depends on the installer's SDK and devices.",
        ],
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--install", action="store_true", help="copy the skill into CODEX_HOME/skills")
    p.add_argument("--check", action="store_true", help="only inspect the default destination")
    p.add_argument("--dest", type=Path, help="override the destination skill directory")
    args = p.parse_args()
    if args.install and args.check:
        p.error("choose --install or --check")
    destination = args.dest or (codex_home() / "skills" / SKILL_NAME)
    if args.install:
        if destination.exists():
            raise SystemExit(f"destination already exists: {destination}; remove or choose --dest")
        shutil.copytree(SOURCE, destination)
        installed = True
        mode = "local_copy"
    else:
        installed = (destination / "SKILL.md").is_file()
        mode = "check" if args.check else "dry_run"
    report = make_report(destination, installed, mode)
    (ROOT / "registration_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
