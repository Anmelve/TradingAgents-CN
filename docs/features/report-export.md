# Report Export Feature Guide

## Feature Overview

TradingAgents-CN 提供了强大的报告导出功能，支持将股票分析结果导出为多种专业格式，方便用户保存、分享和进一步分析。

## Supported Export Formats

### 1. **Markdown Format**

- **用途**: 在线查看、版本控制、技术文档
- **特点**: 轻量级、可编辑、支持版本控制
- **适用场景**: 开发者文档、在线分享、技术博客

### 2. **Word Document (.docx)**

- **用途**: 商业报告、正式文档、打印输出
- **特点**: 专业格式、易于编辑、广泛兼容
- **适用场景**: 投资报告、客户演示、存档备份

### 3. **PDF Document (.pdf)**

- **用途**: 正式发布、打印、长期保存
- **特点**: 格式固定、跨平台兼容、专业外观
- **适用场景**: 正式报告、监管提交、客户交付

## Usage Guide

### Web Interface Export

1. **完成股票分析**

   - 在Web界面输入股票代码
   - 选择分析深度和配置
   - 等待分析完成
2. **选择导出格式**

   - 在分析结果页面找到导出按钮
   - 点击对应格式的导出按钮：
     - 📝 **导出 Markdown**
     - 📄 **导出 Word**
     - 📊 **导出 PDF**
3. **下载文件**

   - 系统自动生成文件
   - 浏览器自动下载到本地
   - 文件名格式：`{股票代码}_analysis_{时间戳}.{格式}`

### 命令行导出

```bash
# 使用CLI进行分析并导出
python main.py --symbol 000001 --export-format word,pdf
```

## 📊 报告内容结构

### 标准报告包含以下章节：

1. **📈 股票基本信息**

   - 股票代码和名称
   - 当前价格和涨跌幅
   - 市场板块信息
   - 分析时间戳
2. **🎯 投资决策摘要**

   - 投资建议（买入/卖出/持有）
   - 置信度评分
   - 风险评分
   - 目标价位
3. **📊 详细分析报告**

   - 市场技术分析
   - 基本面分析
   - 情绪分析（如启用）
   - 新闻分析（如启用）
4. **🔬 专家辩论记录**

   - 看涨分析师观点
   - 看跌分析师观点
   - 辩论过程记录
5. **⚠️ 风险提示**

   - 市场风险警告
   - 投资建议免责声明
   - 数据来源说明
6. **📝 技术信息**

   - 使用的LLM模型
   - 分析师配置
   - 数据源信息
   - 生成时间

## ⚙️ 技术实现

### 导出引擎

- **核心引擎**: Pandoc
- **Word转换**: pypandoc + python-docx
- **PDF生成**: wkhtmltopdf / weasyprint
- **格式处理**: 自动清理YAML冲突

### Docker环境优化

```yaml
# Docker环境已预装所有依赖
- pandoc: 文档转换核心
- wkhtmltopdf: PDF生成引擎
- python-docx: Word文档处理
- 中文字体支持: 完整中文显示
```

### 错误处理机制

1. **YAML解析保护**

   ```python
   # 自动禁用YAML元数据解析
   extra_args = ['--from=markdown-yaml_metadata_block']
   ```
2. **内容清理**

   ```python
   # 清理可能导致冲突的字符
   content = content.replace('---', '—')  # 表格分隔符保护
   content = content.replace('...', '…')  # 省略号处理
   ```
3. **降级策略**

   ```python
   # PDF引擎降级顺序
   engines = ['wkhtmltopdf', 'weasyprint', 'default']
   ```

## 🔧 配置选项

### 环境变量配置

```bash
# .env 文件配置
EXPORT_ENABLED=true                    # 启用导出功能
EXPORT_DEFAULT_FORMAT=word,pdf         # 默认导出格式
EXPORT_INCLUDE_DEBUG=false             # 是否包含调试信息
EXPORT_WATERMARK=false                 # 是否添加水印
```

### Web界面配置

- **导出格式选择**: 用户可选择单个或多个格式
- **文件命名**: 自动生成带时间戳的文件名
- **下载管理**: 自动触发浏览器下载

## 📁 文件管理

### 文件命名规则

```
格式: {股票代码}_analysis_{YYYYMMDD_HHMMSS}.{扩展名}
示例: 
- 000001_analysis_20250113_143022.docx
- AAPL_analysis_20250113_143022.pdf
- 600519_analysis_20250113_143022.md
```

### 存储位置

- **Web导出**: 临时文件，自动下载后清理
- **CLI导出**: 保存到 `./exports/` 目录
- **Docker环境**: 映射到主机目录（如配置）

## Pandoc Installation Guide

### What is Pandoc?

Pandoc is a universal document converter that enables the export functionality in TradingAgents-CN. It converts Markdown content to Word (.docx) and PDF formats.

### Installation Methods

#### Method 1: Package Managers (Recommended)

**Windows (Chocolatey):**
```bash
choco install pandoc
```

**macOS (Homebrew):**
```bash
brew install pandoc
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install pandoc
```

**CentOS/RHEL/Fedora:**
```bash
sudo yum install pandoc
# or for newer versions
sudo dnf install pandoc
```

#### Method 2: Direct Download

1. Visit the official Pandoc website: https://pandoc.org/installing.html
2. Download the appropriate installer for your operating system
3. Run the installer and follow the setup wizard
4. Add Pandoc to your system PATH if not done automatically

#### Method 3: Python Auto-Download

The system can automatically download Pandoc if it's not found:

```python
import pypandoc
pypandoc.download_pandoc()
```

### Verification

After installation, verify Pandoc is working:

```bash
pandoc --version
```

You should see output similar to:
```
pandoc 3.1.9
Compiled with pandoc-types 1.23, citeproc 0.8.0.1, skylighting 0.14.1.3,
Default user data directory: /home/user/.local/share/pandoc
Copyright (C) 2006-2023 John MacFarlane. Web:  https://pandoc.org
This is free software; see the source for copying conditions. There is no
warranty, not even for merchantability or fitness for a particular purpose.
```

### Additional Dependencies

#### For PDF Export

**wkhtmltopdf (Recommended):**
- Windows: Download from https://wkhtmltopdf.org/downloads.html
- macOS: `brew install wkhtmltopdf`
- Linux: `sudo apt install wkhtmltopdf`

**WeasyPrint (Alternative):**
```bash
pip install weasyprint
```

#### For Word Export

No additional dependencies required - Pandoc handles Word conversion natively.

### Docker Environment

If you're using Docker, all dependencies are pre-installed in the container:

```bash
# Check if running in Docker
docker exec TradingAgents-web pandoc --version
docker exec TradingAgents-web wkhtmltopdf --version
```

## Troubleshooting

### Common Issues

1. **Word导出失败**

   ```
   错误: YAML parse exception
   解决: 系统已自动修复，重试即可
   ```
2. **PDF生成失败**

   ```
   错误: wkhtmltopdf not found
   解决: Docker环境已预装，本地环境需安装
   ```
3. **中文显示问题**

   ```
   错误: 中文字符显示为方块
   解决: Docker环境已配置中文字体
   ```

### 调试方法

1. **查看详细日志**

   ```bash
   docker logs TradingAgents-web --follow
   ```
2. **测试转换功能**

   ```bash
   docker exec TradingAgents-web python test_conversion.py
   ```
3. **检查依赖**

   ```bash
   docker exec TradingAgents-web pandoc --version
   docker exec TradingAgents-web wkhtmltopdf --version
   ```

## 🎯 最佳实践

### 使用建议

1. **格式选择**

   - **日常使用**: Markdown（轻量、可编辑）
   - **商业报告**: Word（专业、可编辑）
   - **正式发布**: PDF（固定格式、专业外观）
2. **性能优化**

   - 大批量导出时使用CLI模式
   - 避免同时导出多种格式（按需选择）
   - 定期清理导出文件
3. **质量保证**

   - 导出前检查分析结果完整性
   - 验证关键数据（价格、建议等）
   - 确认时间戳和股票代码正确

## 🔮 未来规划

### 计划增强功能

1. **📊 图表集成**
   - 技术指标图表
   - 价格走势图
   - 风险评估图表

2. **🎨 模板定制**
   - 多种报告模板
   - 企业品牌定制
   - 个性化样式

3. **📧 自动分发**
   - 邮件自动发送
   - 定时报告生成
   - 多人协作分享

4. **📱 移动优化**
   - 移动端适配
   - 响应式布局
   - 触屏操作优化

## 🙏 致谢

### 功能贡献者

报告导出功能由社区贡献者 **[@baiyuxiong](https://github.com/baiyuxiong)** (baiyuxiong@163.com) 设计并实现，包括：

- 📄 多格式报告导出系统架构设计
- 🔧 Pandoc集成和格式转换实现
- 📝 Word/PDF导出功能开发
- 🛠️ 错误处理和降级策略设计
- 🧪 完整的测试和验证流程

感谢他的杰出贡献，让TradingAgents-CN拥有了专业级的报告导出能力！

---

*最后更新: 2025-07-13*
*版本: cn-0.1.7*
*功能贡献: [@baiyuxiong](https://github.com/baiyuxiong)*
