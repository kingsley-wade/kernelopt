# Kernel Optimization System

这是一个可以发布到 GitHub、再安装到其他 Codex 环境的多角色 Kernel Optimization skill workflow。

仓库包含两层：

- `skill/kernel-optimization-orchestrator/`：真正安装到 Codex 的主 skill，包含 `SKILL.md`、四个角色说明、Contract、状态机、Backend 和性能诊断参考。
- `src/`、`scripts/`、`tests/`、`schemas/`：可复现的 Orchestrator fallback、Contract 校验、Backend 探测、dry run、测试和打包工具。

Docker 容器到本地机器、GitHub 上传和其他人安装的完整步骤见 [docs/GITHUB_HANDOFF.md](docs/GITHUB_HANDOFF.md)。

## 从 GitHub 安装主 skill

将 `<owner>/<repo>` 替换成发布后的 GitHub 仓库：

```bash
python "$HOME/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo <owner>/<repo> \
  --path skill/kernel-optimization-orchestrator
```

如果设置了 `CODEX_HOME`，将 `$HOME/.codex` 替换为 `$CODEX_HOME`。也可以使用完整 URL：

```bash
python "$HOME/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --url https://github.com/<owner>/<repo>/tree/main/skill/kernel-optimization-orchestrator
```

安装器会复制包含 `SKILL.md` 的 skill 目录到 `CODEX_HOME/skills/kernel-optimization-orchestrator`。目标目录已存在时，先备份或删除旧版本，再重新安装。安装后重新开始一个 Codex turn，确认 skill 出现在可发现列表中。

## 从 clone 的仓库本地安装

```bash
python scripts/register_skill.py --install
```

默认安装到 `${CODEX_HOME:-$HOME/.codex}/skills/kernel-optimization-orchestrator`。只检查安装状态：

```bash
python scripts/register_skill.py --check
```

## 验证仓库和打包

```bash
PYTHONPATH=src python scripts/validate_skill.py
PYTHONPATH=src python scripts/smoke_test.py
PYTHONPATH=src python -m unittest discover -s tests -v
python scripts/package_skill.py --output dist/skill.zip
```

`smoke_test.py` 是无硬件 dry run。没有实际 CUDA/Ascend 设备、SDK 或 profiler 时，adapter 返回 `NOT_CONFIGURED`，不会写入虚构的 latency 或吞吐。

## 运行模型协议

每个算子任务开始时，Orchestrator 先向用户确认 default/Orchestrator 模型，再确认 Kernel、Performance、Benchmark、Reviewer 的 subagent 模型，之后才询问目标硬件和 backend。Runtime 不支持原生按角色路由时，workflow 使用显式顺序 fallback，并记录 `native_subagents=false`。

## 发布前检查

1. 提交 `skill/`、`src/`、`schemas/`、`scripts/`、`tests/`、`configs/`、`subagents/` 和文档。
2. 不提交本地 `build/`、设备日志、私有配置、临时 profiler 数据和 `__pycache__`。
3. 执行上面的验证命令，并把 `test_report.json` 的硬件限制如实保留。
4. GitHub 仓库公开后，用官方 installer 命令从仓库路径安装一次，并在新 Codex turn 中确认发现结果。

当前工程没有声称拥有原生 subagent 路由，也没有声称完成真实硬件编译或性能测量；这些能力由安装者的 Runtime、SDK 和设备决定。
