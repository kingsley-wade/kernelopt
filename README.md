# Kernel Optimization Orchestrator

一个面向 CUDA 和 Ascend C 算子优化的 Codex skill。它把算子优化过程组织成可审查的阶段，并要求记录模型、硬件、正确性和性能证据。

> **项目定位：** 这是优化工作流与配套工具，不是现成的 CUDA/Ascend kernel 库。它不会自动提供设备、SDK、编译器或原生 subagent 路由；没有可用硬件时会标记 `NOT_CONFIGURED`，不会生成虚构的性能数据。

## 能做什么

- 引导一次算子优化任务经过架构资料核对、算子规格、基线、正确性、基准测试、诊断、单因素实验和审查。
- 以 Kernel、Performance、Benchmark、Reviewer 四种角色组织工作；当前运行环境不支持原生角色路由时，按顺序执行并记录 `native_subagents=false`。
- 提供 CUDA 与 Ascend C backend 的配置示例、JSON contracts、mock dry run 和单元测试。
- 区分实测、推导、估算和模拟数据，并保留实验与源码 provenance。

## 安装到 Codex

### 从 GitHub 安装 skill（推荐）

先确认本机已有 Codex 的 `skill-installer`。以下命令只安装主 skill 目录：

**macOS / Linux**

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo kingsley-wade/kernelopt \
  --path skill/kernel-optimization-orchestrator
```

**Windows PowerShell**

```powershell
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
$installer = Join-Path $codexHome 'skills/.system/skill-installer/scripts/install-skill-from-github.py'
python $installer --repo kingsley-wade/kernelopt --path skill/kernel-optimization-orchestrator
```

如果已安装过同名 skill，先备份或移走 `skills/kernel-optimization-orchestrator`，再重新运行安装命令。安装完成后开启一个新的 Codex 对话，让 Codex 重新发现 skill。

### 从源码安装

需要使用仓库中的 Python orchestrator、mock、校验脚本或测试时，克隆完整仓库：

```bash
git clone https://github.com/kingsley-wade/kernelopt.git
cd kernelopt
python scripts/register_skill.py --install
```

安装器会将主 skill 复制到 `${CODEX_HOME:-$HOME/.codex}/skills/kernel-optimization-orchestrator`。目标目录已存在时，脚本会停止，不会覆盖旧安装。也可以只检查默认安装位置：

```bash
python scripts/register_skill.py --check
```

本地脚本要求 Python 3.10 或更新版本。硬件工作还需要与目标设备匹配的驱动、SDK、编译器和 profiler。

## 开始一次优化任务

安装后，在新的 Codex 对话中调用：

```text
使用 $kernel-optimization-orchestrator 帮我优化 <算子名称>，目标设备是 <设备型号>。
```

按 workflow 提示提供或确认：

1. Orchestrator/default 模型，以及 Kernel、Performance、Benchmark、Reviewer 各角色的模型。
2. 厂商、backend、设备 SKU、架构标识、SDK、driver 和运行时设备 ID。
3. 算子语义与输入约束、独立 correctness reference、现有实现和可比较的 benchmark 基线。
4. 官方架构资料和可复现的实验环境。

流程会先检查架构依据和正确性条件，再进入性能测量与实验。缺少架构资料、reference、硬件或工具链时，workflow 会暂停或报告相应状态；不要把 mock、估算值或缺失数据当成真实硬件结果。

## 本地验证

在仓库根目录运行。下面的命令只验证项目代码与 mock，不需要 GPU/NPU：

**macOS / Linux**

```bash
PYTHONPATH=src python scripts/validate_skill.py
PYTHONPATH=src python scripts/smoke_test.py
PYTHONPATH=src python -m unittest discover -s tests -v
```

**Windows PowerShell**

```powershell
$env:PYTHONPATH = 'src'
python scripts/validate_skill.py
python scripts/smoke_test.py
python -m unittest discover -s tests -v
```

`smoke_test.py` 是无硬件 dry run。它验证流程行为，不编译 kernel，也不产出真实 latency、吞吐或 profiler 指标。完整硬件验证必须在配置了对应 SDK、设备和工具链的机器上单独进行。

## 仓库结构

```text
skill/kernel-optimization-orchestrator/  Codex 安装的主 skill 与参考资料
src/kernel_opt/                          Python workflow、contracts 和 backend 适配器
backends/                                CUDA / Ascend C backend 描述与指标映射
configs/                                 默认配置及设备配置示例
schemas/                                 请求、候选和报告的 JSON schema
scripts/                                 注册、校验、dry run 和打包脚本
tests/                                   无硬件单元测试
examples/                                mock 请求与 backend 扩展示例
docs/GITHUB_HANDOFF.md                   仓库发布与交接记录
```

如果只通过 GitHub skill installer 安装，Codex 会获得 `skill/` 下的 skill 与参考文档；Python 源码、测试和仓库工具需要另行 clone 完整仓库。

## 当前限制

- 角色说明不代表运行时已经创建了四个原生 subagent。没有原生路由时使用顺序 fallback，并在记录中明确标记。
- CUDA/Ascend C adapter 的设备与工具探测依赖安装者环境；本仓库本身不附带厂商 SDK 或设备二进制文件。
- 项目测试和 mock 通过不代表特定设备上的 kernel 正确或更快。硬件 correctness、benchmark 和 profiler 结果必须在目标环境中实测。
- 尚未在仓库中附加 `LICENSE` 文件；在明确许可证之前，访客可以查看和下载仓库，但公开仓库本身不等于授予再分发或改编许可。

## 贡献与问题反馈

提交问题时，请附上 Python 版本、操作系统、backend、设备与 SDK 版本、相关命令和脱敏后的日志。不要上传私有配置、访问令牌、用户数据或未经清理的设备日志。
