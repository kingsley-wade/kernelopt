# KernelOpt GitHub 交接文档

## 1. 交付内容

本目录是一个可以发布到 GitHub 并安装到 Codex 的 skill workflow。

主 skill 目录：

```text
skill/kernel-optimization-orchestrator/
```

该目录必须保留在 GitHub 仓库中，因为 Codex GitHub installer 需要从这里读取 `SKILL.md`。

## 2. 从 Docker 容器拷贝到本地机器

在宿主机执行。当前容器名为 `ops-blas-torch`：

```bash
docker cp ops-blas-torch:/workspace/ops-blas/kernel-optimization-system/dist/kernelopt-v0.1.0.zip .
```

如果容器名不同，先执行：

```bash
docker ps --format '{{.Names}}'
```

## 3. 在本地解压

```bash
mkdir -p kernelopt-upload
unzip kernelopt-v0.1.0.zip -d kernelopt-upload
cd kernelopt-upload
test -f skill/kernel-optimization-orchestrator/SKILL.md && echo OK
```

## 4. 上传到 GitHub

先在 <https://github.com/new> 创建空仓库 `kernelopt`，不要预先添加 README、`.gitignore` 或 License。

在解压目录执行：

```bash
git init -b main
git add .
git commit -m "feat: add multi-role kernel optimization skill workflow"
git remote add origin https://github.com/kingsley-wade/kernelopt.git
git push -u origin main
```

HTTPS 推送时，Username 使用 `kingsley-wade`，Password 使用 GitHub Personal Access Token（PAT），不是 GitHub 登录密码。PAT 需要对 `kernelopt` 有 `Contents: Read and write` 权限。

如果本地已经有同名 remote：

```bash
git remote set-url origin https://github.com/kingsley-wade/kernelopt.git
git push -u origin main
```

## 5. 其他人安装 skill

仓库发布后，其他 Codex 用户执行：

```bash
python "$HOME/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo kingsley-wade/kernelopt \
  --path skill/kernel-optimization-orchestrator
```

或者：

```bash
python "$HOME/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --url https://github.com/kingsley-wade/kernelopt/tree/main/skill/kernel-optimization-orchestrator
```

安装后重新开始一个 Codex turn，让 Codex 重新发现 skill。

## 6. 发布前验证

解压目录中执行：

```bash
PYTHONPATH=src python scripts/validate_skill.py
PYTHONPATH=src python scripts/smoke_test.py
PYTHONPATH=src python -m unittest discover -s tests -v
```

预期结果：project skill validation `PASS`、dry-run mock `PASS`、23 个单元测试通过。没有可验证的 CUDA/Ascend 设备时，硬件测试记录为 `NOT_AVAILABLE` 或 `NOT_CONFIGURED`，不能填写虚构 latency、吞吐或 profiler 数据。

## 7. 运行限制

工作流包含 Orchestrator、Kernel、Performance、Benchmark 和 Reviewer 五个角色。每个新算子任务必须先确认 Orchestrator/default 模型和四个 subagent 模型，再确认硬件架构。当前 Runtime 不提供原生按角色 subagent 路由时，使用顺序 fallback，并记录 `native_subagents=false`。

## 8. 更新版本

修改 workflow 后更新 `VERSION`，再运行验证和打包：

```bash
printf '0.1.1\n' > VERSION
PYTHONPATH=src python scripts/validate_skill.py
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python scripts/package_skill.py --output dist/kernelopt-v0.1.1.zip
```

不要把 Docker 中的 `build/`、临时 profiler 文件、私有配置或 `__pycache__` 上传到 GitHub。
