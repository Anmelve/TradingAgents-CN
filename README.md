# TradingAgents 中文增强版

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/Version-cn--0.1.1--preview-yellow.svg)](./VERSION)
[![Documentation](https://img.shields.io/badge/docs-中文文档-green.svg)](./docs/)
[![Original](https://img.shields.io/badge/基于-TauricResearch/TradingAgents-orange.svg)](https://github.com/TauricResearch/TradingAgents)

> ⚠️ **预览版本提醒**: 当前版本为 cn-0.1.1 预览版，功能仍在完善中，建议仅在测试环境使用。
>
> 📝 **版本说明**: 为避免与源项目版本冲突，中文增强版使用 `cn-` 前缀的独立版本体系。

基于多智能体大语言模型的中文金融交易决策框架。本项目基于 [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) 开发，专为中文用户提供完整的文档体系和本地化支持。

## 🙏 致敬与感谢

### 向源项目开发者致敬

我们向 [Tauric Research](https://github.com/TauricResearch) 团队及 [TradingAgents](https://github.com/TauricResearch/TradingAgents) 项目的所有贡献者致以最诚挚的敬意和感谢！

- **🎯 创新理念**: 感谢您们创造了这个革命性的多智能体交易框架
- **💎 珍贵源码**: 感谢您们开源的每一行代码，它们凝聚着无数的智慧和心血
- **🏗️ 优秀架构**: 感谢您们设计了如此优雅和可扩展的系统架构
- **🔬 前沿技术**: 感谢您们将最新的AI技术应用到金融交易领域
- **🔄 持续贡献**: 感谢您们持续的维护、更新和改进工作
- **🌍 开源精神**: 感谢您们选择Apache 2.0协议，给予开发者最大的自由

> 💝 **特别说明**: 虽然Apache 2.0协议赋予了我们使用源码的权利，但我们深知每一行代码的珍贵价值。我们将永远铭记并感谢您们的无私贡献。

### 我们的使命

本项目的创建初衷是为了**更好地在中国推广TradingAgents**，让更多中文用户能够：

- **🇨🇳 无障碍使用**: 提供完整的中文文档和界面，降低使用门槛
- **🧠 本土化适配**: 集成国产大模型，适应国内网络环境
- **📊 市场对接**: 支持A股、港股等中国金融市场
- **🎓 学习交流**: 为中文社区提供学习和交流平台
- **🚀 技术推广**: 推动AI在中国金融科技领域的应用

我们始终尊重源项目的知识产权，遵循开源协议，并致力于将改进和创新反馈给开源社区。

## 🎯 项目目标

### 源项目介绍

[TradingAgents](https://github.com/TauricResearch/TradingAgents) 是由杰出的 [Tauric Research](https://github.com/TauricResearch) 团队开发的**革命性多智能体交易框架**。这个项目的创新之处在于：

- **🤖 智能体协作**: 模拟真实交易公司的专业分工和协作决策流程
- **🧠 AI驱动**: 通过多个专业化AI智能体协作评估市场条件
- **📈 实战导向**: 专注于实际的交易决策和风险管理
- **🔬 前沿技术**: 将最新的大语言模型技术应用到金融领域

### 中文增强的使命

为了**更好地在中国推广这个优秀的TradingAgents框架**，我们创建了这个中文增强版本，目标是：

#### 🌉 搭建技术桥梁
- **语言无障碍**: 提供完整的中文文档和用户界面
- **技术本土化**: 集成国产大模型，适应国内技术环境
- **社区建设**: 为中文开发者社区提供学习和交流平台

#### 🇨🇳 服务中国市场
- **市场对接**: 支持A股、港股、新三板等中国金融市场
- **数据源集成**: 整合Tushare、AkShare、Wind等中文金融数据
- **合规适配**: 符合国内金融监管和数据安全要求

#### 🎓 推动技术普及
- **教育资源**: 为高校和研究机构提供AI金融教学工具
- **人才培养**: 帮助培养更多AI金融复合型人才
- **创新应用**: 推动AI技术在中国金融科技领域的创新应用

我们深信，通过这些努力，能够让更多中国用户体验到TradingAgents的强大功能，并为全球开源社区贡献中国智慧。

## ✨ 核心特性

### 🤖 多智能体协作架构

- **分析师团队**: 基本面、技术面、新闻面、社交媒体四大专业分析师
- **研究员团队**: 看涨/看跌研究员进行结构化辩论
- **交易员智能体**: 基于所有输入做出最终交易决策
- **风险管理**: 多层次风险评估和管理机制
- **管理层**: 协调各团队工作，确保决策质量

### 🧠 多LLM模型支持

- **OpenAI**: GPT-4o, GPT-4o-mini, GPT-3.5-turbo
- **Anthropic**: Claude-3-Opus, Claude-3-Sonnet, Claude-3-Haiku
- **Google AI**: Gemini-Pro, Gemini-2.0-Flash
- **🇨🇳 阿里百炼**: 通义千问 Turbo/Plus/Max (已支持)
- **国产模型** (计划中): 文心一言、DeepSeek等

### 📊 全面数据集成

- **实时数据**: FinnHub、Yahoo Finance
- **新闻数据**: Google News、财经新闻
- **社交数据**: Reddit、Twitter情绪分析
- **中文数据** (计划中): Tushare、AkShare、东方财富

### 🚀 高性能特性

- **并行处理**: 多智能体并行分析，提高效率
- **智能缓存**: 多层缓存策略，减少API调用成本
- **实时分析**: 支持实时市场数据分析
- **灵活配置**: 高度可定制的智能体行为和模型选择

## 🆚 与原版的主要区别

### ✅ 已完成的增强


| 功能     | 原版     | 中文增强版             |
| -------- | -------- | ---------------------- |
| 文档语言 | 英文     | 完整中文文档体系       |
| 架构说明 | 基础说明 | 详细的架构设计文档     |
| 使用指南 | 简单示例 | 从入门到高级的完整指南 |
| 配置说明 | 基础配置 | 详细的配置优化指南     |
| 故障排除 | 无       | 完整的FAQ和故障排除    |
| 代码注释 | 英文     | 中文注释和说明         |

### 🔄 计划中的增强

- **中国市场支持**: A股、港股、新三板数据集成
- **中文数据源**: Tushare、AkShare、Wind等数据源
- **国产LLM**: 文心一言、通义千问、智谱清言等
- **中文金融术语**: 优化中文金融分析术语和表达
- **监管合规**: 符合中国金融监管要求的风险提示
- **本地化部署**: 支持私有化部署和数据安全

## 🚀 快速开始

### 🔐 重要安全提醒

> ⚠️ **API密钥安全警告**:
> - 绝对不要将包含真实API密钥的`.env`文件提交到Git仓库
> - 使用`.env.example`作为模板，创建您自己的`.env`文件
> - 详细安全指南请参考: [API密钥安全指南](docs/security/api_keys_security.md)

### 环境要求

- Python 3.10+ (推荐 3.11)
- 4GB+ RAM (推荐 8GB+)
- 稳定的网络连接

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/hsliuping/TradingAgents-CN.git
cd TradingAgents-CN

# 2. 创建虚拟环境
python -m venv tradingagents
source tradingagents/bin/activate  # Linux/macOS
# tradingagents\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt
```

### 配置API密钥

#### 🇨🇳 推荐：使用阿里百炼（国产大模型）
```bash
# 设置阿里百炼API密钥
set DASHSCOPE_API_KEY=your_dashscope_api_key
set FINNHUB_API_KEY=your_finnhub_api_key

# 或创建 .env 文件
echo "DASHSCOPE_API_KEY=your_dashscope_api_key" > .env
echo "FINNHUB_API_KEY=your_finnhub_api_key" >> .env
```

#### 使用国外模型
```bash
# OpenAI
set OPENAI_API_KEY=your_openai_api_key
set FINNHUB_API_KEY=your_finnhub_api_key

# 或其他模型...
```

### 基本使用

#### 🇨🇳 使用阿里百炼大模型（推荐）
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 配置阿里百炼
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "dashscope"
config["deep_think_llm"] = "qwen-plus"      # 深度分析
config["quick_think_llm"] = "qwen-turbo"    # 快速任务

# 创建交易智能体
ta = TradingAgentsGraph(debug=True, config=config)

# 分析股票 (以苹果公司为例)
state, decision = ta.propagate("AAPL", "2024-01-15")

# 输出分析结果
print(f"推荐动作: {decision['action']}")
print(f"置信度: {decision['confidence']:.1%}")
print(f"风险评分: {decision['risk_score']:.1%}")
print(f"推理过程: {decision['reasoning']}")
```

#### 快速启动脚本
```bash
# 阿里百炼演示（推荐中文用户）
python examples/dashscope/demo_dashscope_chinese.py

# 阿里百炼完整演示
python examples/dashscope/demo_dashscope.py

# 阿里百炼简化测试
python examples/dashscope/demo_dashscope_simple.py

# OpenAI演示（需要国外API）
python examples/openai/demo_openai.py

# 集成测试
python tests/integration/test_dashscope_integration.py
```

### 交互式分析

```bash
# 启动交互式命令行界面
python -m cli.main
```

## 🎯 **快速导航** - 找到您需要的内容

| 🎯 **我想要...** | 📖 **推荐文档** | ⏱️ **阅读时间** |
|------------------|----------------|-----------------|
| **快速上手** | [🚀 快速开始](docs/overview/quick-start.md) | 10分钟 |
| **了解架构** | [🏛️ 系统架构](docs/architecture/system-architecture.md) | 15分钟 |
| **看代码示例** | [📚 基础示例](docs/examples/basic-examples.md) | 20分钟 |
| **解决问题** | [🆘 常见问题](docs/faq/faq.md) | 5分钟 |
| **深度学习** | [📁 完整文档目录](#-详细文档目录) | 2小时+ |

> 💡 **提示**: 我们的 `docs/` 目录包含了 **50,000+字** 的详细中文文档，这是与原版最大的区别！

## 📚 完整文档体系 - 核心亮点

> **🌟 这是本项目与原版最大的区别！** 我们构建了业界最完整的中文金融AI框架文档体系，包含超过 **50,000字** 的详细技术文档，**20+** 个专业文档文件，**100+** 个代码示例。

### 🎯 为什么选择我们的文档？

| 对比维度 | 原版 TradingAgents | 🚀 **中文增强版** |
|---------|-------------------|------------------|
| **文档语言** | 英文基础说明 | **完整中文体系** |
| **文档深度** | 简单介绍 | **深度技术剖析** |
| **架构说明** | 概念性描述 | **详细设计文档 + 架构图** |
| **使用指南** | 基础示例 | **从入门到专家的完整路径** |
| **故障排除** | 无 | **详细FAQ + 解决方案** |
| **代码示例** | 少量示例 | **100+ 实用示例** |

### 📖 文档导航 - 按学习路径组织

#### 🚀 **新手入门路径** (推荐从这里开始)
1. [📋 项目概述](docs/overview/project-overview.md) - **了解项目背景和核心价值**
2. [⚙️ 详细安装](docs/overview/installation.md) - **各平台详细安装指南**
3. [🚀 快速开始](docs/overview/quick-start.md) - **10分钟上手指南**
4. [📚 基础示例](docs/examples/basic-examples.md) - **8个实用的入门示例**

#### 🏗️ **架构理解路径** (深入了解系统设计)
1. [🏛️ 系统架构](docs/architecture/system-architecture.md) - **完整的系统架构设计**
2. [🤖 智能体架构](docs/architecture/agent-architecture.md) - **多智能体协作机制**
3. [📊 数据流架构](docs/architecture/data-flow-architecture.md) - **数据处理全流程**
4. [🔄 图结构设计](docs/architecture/graph-structure.md) - **LangGraph工作流程**

#### 🤖 **智能体深度解析** (了解每个智能体的设计)
1. [📈 分析师团队](docs/agents/analysts.md) - **四类专业分析师详解**
2. [🔬 研究员团队](docs/agents/researchers.md) - **看涨/看跌辩论机制**
3. [💼 交易员智能体](docs/agents/trader.md) - **交易决策制定流程**
4. [🛡️ 风险管理](docs/agents/risk-management.md) - **多层次风险评估**
5. [👔 管理层智能体](docs/agents/managers.md) - **协调和决策管理**

#### 📊 **数据处理专题** (掌握数据处理技术)
1. [🔌 数据源集成](docs/data/data-sources.md) - **多数据源API集成**
2. [⚙️ 数据处理流程](docs/data/data-processing.md) - **数据清洗和转换**
3. [💾 缓存策略](docs/data/caching.md) - **多层缓存优化性能**

#### ⚙️ **配置和优化** (性能调优和定制)
1. [📝 配置指南](docs/configuration/config-guide.md) - **详细配置选项说明**
2. [🧠 LLM配置](docs/configuration/llm-config.md) - **大语言模型优化**

#### 💡 **高级应用** (扩展开发和实战)
1. [📚 基础示例](docs/examples/basic-examples.md) - **8个实用基础示例**
2. [🚀 高级示例](docs/examples/advanced-examples.md) - **复杂场景和扩展开发**

#### ❓ **问题解决** (遇到问题时查看)
1. [🆘 常见问题](docs/faq/faq.md) - **详细FAQ和解决方案**

### 📊 文档统计数据

- 📄 **文档文件数**: 20+ 个专业文档
- 📝 **总字数**: 50,000+ 字详细内容
- 💻 **代码示例**: 100+ 个实用示例
- 📈 **架构图表**: 10+ 个专业图表
- 🎯 **覆盖范围**: 从入门到专家的完整路径

### 🎨 文档特色

- **🇨🇳 完全中文化**: 专为中文用户优化的表达方式
- **📊 图文并茂**: 丰富的架构图和流程图
- **💻 代码丰富**: 每个概念都有对应的代码示例
- **🔍 深度剖析**: 不仅告诉你怎么做，还告诉你为什么这样做
- **🛠️ 实用导向**: 所有文档都面向实际应用场景

---

## 📚 详细文档目录

### 📁 **docs/ 目录结构** - 完整的知识体系

```
docs/
├── 📖 overview/              # 项目概览 - 新手必读
│   ├── project-overview.md   # 📋 项目详细介绍
│   ├── quick-start.md        # 🚀 10分钟快速上手
│   └── installation.md       # ⚙️ 详细安装指南
│
├── 🏗️ architecture/          # 系统架构 - 深度理解
│   ├── system-architecture.md    # 🏛️ 整体架构设计
│   ├── agent-architecture.md     # 🤖 智能体协作机制
│   ├── data-flow-architecture.md # 📊 数据流处理架构
│   └── graph-structure.md        # 🔄 LangGraph工作流
│
├── 🤖 agents/               # 智能体详解 - 核心组件
│   ├── analysts.md          # 📈 四类专业分析师
│   ├── researchers.md       # 🔬 看涨/看跌辩论机制
│   ├── trader.md           # 💼 交易决策制定
│   ├── risk-management.md  # 🛡️ 多层风险评估
│   └── managers.md         # 👔 管理层协调
│
├── 📊 data/                 # 数据处理 - 技术核心
│   ├── data-sources.md      # 🔌 多数据源集成
│   ├── data-processing.md   # ⚙️ 数据处理流程
│   └── caching.md          # 💾 缓存优化策略
│
├── ⚙️ configuration/        # 配置优化 - 性能调优
│   ├── config-guide.md      # 📝 详细配置说明
│   └── llm-config.md       # 🧠 LLM模型优化
│
├── 💡 examples/             # 示例教程 - 实战应用
│   ├── basic-examples.md    # 📚 8个基础示例
│   └── advanced-examples.md # 🚀 高级开发示例
│
└── ❓ faq/                  # 问题解决 - 疑难解答
    └── faq.md              # 🆘 常见问题FAQ
```

### 🎯 **重点推荐文档** (必读精选)

#### 🔥 **最受欢迎的文档**
1. **[📋 项目概述](docs/overview/project-overview.md)** - ⭐⭐⭐⭐⭐
   > 了解项目的核心价值和技术特色，5分钟读懂整个框架

2. **[🏛️ 系统架构](docs/architecture/system-architecture.md)** - ⭐⭐⭐⭐⭐
   > 深度解析多智能体协作机制，包含详细架构图

3. **[📚 基础示例](docs/examples/basic-examples.md)** - ⭐⭐⭐⭐⭐
   > 8个实用示例，从股票分析到投资组合优化

#### 🚀 **技术深度文档**
1. **[🤖 智能体架构](docs/architecture/agent-architecture.md)**
   > 多智能体设计模式和协作机制详解

2. **[📊 数据流架构](docs/architecture/data-flow-architecture.md)**
   > 数据获取、处理、缓存的完整流程

3. **[🔬 研究员团队](docs/agents/researchers.md)**
   > 看涨/看跌研究员辩论机制的创新设计

#### 💼 **实用工具文档**
1. **[🧠 LLM配置](docs/configuration/llm-config.md)**
   > 多LLM模型配置和成本优化策略

2. **[💾 缓存策略](docs/data/caching.md)**
   > 多层缓存设计，显著降低API调用成本

3. **[🆘 常见问题](docs/faq/faq.md)**
   > 详细的FAQ和故障排除指南

### 📖 **按模块浏览文档**

<details>
<summary><strong>📖 概览文档</strong> - 项目入门必读</summary>

- [📋 项目概述](docs/overview/project-overview.md) - 详细的项目背景和特性介绍
- [🚀 快速开始](docs/overview/quick-start.md) - 从安装到第一次运行的完整指南
- [⚙️ 详细安装](docs/overview/installation.md) - 各平台详细安装说明

</details>

<details>
<summary><strong>🏗️ 架构文档</strong> - 深度理解系统设计</summary>

- [🏛️ 系统架构](docs/architecture/system-architecture.md) - 完整的系统架构设计
- [🤖 智能体架构](docs/architecture/agent-architecture.md) - 智能体设计模式和协作机制
- [📊 数据流架构](docs/architecture/data-flow-architecture.md) - 数据获取、处理和分发流程
- [🔄 图结构设计](docs/architecture/graph-structure.md) - LangGraph工作流程设计

</details>

<details>
<summary><strong>🤖 智能体文档</strong> - 核心组件详解</summary>

- [📈 分析师团队](docs/agents/analysts.md) - 四类专业分析师详解
- [🔬 研究员团队](docs/agents/researchers.md) - 看涨/看跌研究员和辩论机制
- [💼 交易员智能体](docs/agents/trader.md) - 交易决策制定流程
- [🛡️ 风险管理](docs/agents/risk-management.md) - 多层次风险评估体系
- [👔 管理层智能体](docs/agents/managers.md) - 协调和决策管理

</details>

<details>
<summary><strong>📊 数据处理</strong> - 技术核心实现</summary>

- [🔌 数据源集成](docs/data/data-sources.md) - 支持的数据源和API集成
- [⚙️ 数据处理流程](docs/data/data-processing.md) - 数据清洗、转换和验证
- [💾 缓存策略](docs/data/caching.md) - 多层缓存优化性能

</details>

<details>
<summary><strong>⚙️ 配置与部署</strong> - 性能调优指南</summary>

- [📝 配置指南](docs/configuration/config-guide.md) - 详细的配置选项说明
- [🧠 LLM配置](docs/configuration/llm-config.md) - 大语言模型配置优化

</details>

<details>
<summary><strong>💡 示例和教程</strong> - 实战应用指南</summary>

- [📚 基础示例](docs/examples/basic-examples.md) - 8个实用的基础示例
- [🚀 高级示例](docs/examples/advanced-examples.md) - 复杂场景和扩展开发

</details>

<details>
<summary><strong>❓ 帮助文档</strong> - 问题解决方案</summary>

- [🆘 常见问题](docs/faq/faq.md) - 详细的FAQ和解决方案

</details>

## 💰 成本控制

### 典型使用成本

- **经济模式**: $0.01-0.05/次分析 (使用 gpt-4o-mini)
- **标准模式**: $0.05-0.15/次分析 (使用 gpt-4o)
- **高精度模式**: $0.10-0.30/次分析 (使用 gpt-4o + 多轮辩论)

### 成本优化建议

```python
# 低成本配置示例
cost_optimized_config = {
    "deep_think_llm": "gpt-4o-mini",
    "quick_think_llm": "gpt-4o-mini", 
    "max_debate_rounds": 1,
    "online_tools": False  # 使用缓存数据
}
```

## 🤝 贡献指南

我们欢迎各种形式的贡献：

### 贡献类型

- 🐛 **Bug修复** - 发现并修复问题
- ✨ **新功能** - 添加新的功能特性
- 📚 **文档改进** - 完善文档和教程
- 🌐 **本地化** - 翻译和本地化工作
- 🎨 **代码优化** - 性能优化和代码重构

### 贡献流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目基于 Apache 2.0 许可证开源。详见 [LICENSE](LICENSE) 文件。

### 许可证说明

- ✅ 商业使用
- ✅ 修改和分发
- ✅ 私人使用
- ✅ 专利使用
- ❗ 需要保留版权声明
- ❗ 需要包含许可证副本

## 🙏 致谢与感恩

### 🌟 向源项目开发者致敬

我们向 [Tauric Research](https://github.com/TauricResearch) 团队表达最深的敬意和感谢：

- **🎯 愿景领导者**: 感谢您们在AI金融领域的前瞻性思考和创新实践
- **💎 珍贵源码**: 感谢您们开源的每一行代码，它们凝聚着无数的智慧和心血
- **🏗️ 架构大师**: 感谢您们设计了如此优雅、可扩展的多智能体框架
- **💡 技术先驱**: 感谢您们将前沿AI技术与金融实务完美结合
- **🔄 持续贡献**: 感谢您们持续的维护、更新和改进工作
- **🌍 开源贡献**: 感谢您们选择Apache 2.0协议，给予开发者最大的自由
- **📚 知识分享**: 感谢您们提供的详细文档和最佳实践指导

**特别感谢**：[TradingAgents](https://github.com/TauricResearch/TradingAgents) 项目为我们提供了坚实的技术基础。虽然Apache 2.0协议赋予了我们使用源码的权利，但我们深知每一行代码的珍贵价值，将永远铭记并感谢您们的无私贡献。

### 🇨🇳 推广使命的初心

创建这个中文增强版本，我们怀着以下初心：

- **🌉 技术传播**: 让优秀的TradingAgents技术在中国得到更广泛的应用
- **🎓 教育普及**: 为中国的AI金融教育提供更好的工具和资源
- **🤝 文化桥梁**: 在中西方技术社区之间搭建交流合作的桥梁
- **🚀 创新推动**: 推动中国金融科技领域的AI技术创新和应用

### 🌍 开源社区

感谢所有为本项目贡献代码、文档、建议和反馈的开发者和用户。正是因为有了大家的支持，我们才能更好地服务中文用户社区。

### 🤝 合作共赢

我们承诺：
- **尊重原创**: 始终尊重源项目的知识产权和开源协议
- **反馈贡献**: 将有价值的改进和创新反馈给源项目和开源社区
- **持续改进**: 不断完善中文增强版本，提供更好的用户体验
- **开放合作**: 欢迎与源项目团队和全球开发者进行技术交流与合作

## 📞 联系方式

- **GitHub Issues**: [提交问题和建议](https://github.com/hsliuping/TradingAgents-CN/issues)
- **邮箱**: hsliup@163.com
- **原项目**: [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)

## ⚠️ 风险提示

**重要声明**: 本框架仅用于研究和教育目的，不构成投资建议。

- 📊 交易表现可能因多种因素而异
- 🤖 AI模型的预测存在不确定性
- 💰 投资有风险，决策需谨慎
- 👨‍💼 建议咨询专业财务顾问

---

<div align="center">

**🌟 如果这个项目对您有帮助，请给我们一个 Star！**

[⭐ Star this repo](https://github.com/hsliuping/TradingAgents-CN) | [🍴 Fork this repo](https://github.com/hsliuping/TradingAgents-CN/fork) | [📖 Read the docs](./docs/)

</div>
