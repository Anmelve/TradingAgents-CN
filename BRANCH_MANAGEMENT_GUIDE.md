# 🌳 分支管理指南 - 立即行动方案

## 🎯 当前状况

您的项目现在有多个分支，功能开发主要在 `feature/tushare-integration` 分支上，包含了v0.1.6的所有功能。

## 🚀 立即行动方案（推荐）

### 方案A: 简化合并（推荐）

#### 步骤1: 发布v0.1.6正式版
```bash
# 1. 确保当前分支的所有更改都已提交
git add .
git commit -m "完成v0.1.6所有功能和文档"

# 2. 推送当前分支
git push origin feature/tushare-integration

# 3. 切换到main分支
git checkout main

# 4. 合并功能分支
git merge feature/tushare-integration

# 5. 创建版本标签
git tag -a v0.1.6 -m "TradingAgents-CN v0.1.6正式版"

# 6. 推送到远程
git push origin main --tags
```

#### 步骤2: 清理分支
```bash
# 删除已合并的功能分支
git branch -d feature/tushare-integration
git push origin --delete feature/tushare-integration

# 如果有其他已合并的功能分支，也可以删除
```

#### 步骤3: 建立新的开发流程
```bash
# 为下一版本创建开发分支
git checkout -b feature/v0.1.7
git push origin feature/v0.1.7
```

### 方案B: 保守合并（如果担心丢失代码）

#### 步骤1: 备份当前工作
```bash
# 创建备份分支
git checkout -b backup/v0.1.6-$(date +%Y%m%d)
git push origin backup/v0.1.6-$(date +%Y%m%d)

# 回到工作分支
git checkout feature/tushare-integration
```

#### 步骤2: 逐步合并
```bash
# 切换到main分支
git checkout main
git pull origin main

# 创建合并分支
git checkout -b release/v0.1.6
git merge feature/tushare-integration

# 测试无问题后合并到main
git checkout main
git merge release/v0.1.6
git tag v0.1.6
git push origin main --tags
```

## 🔧 分支管理最佳实践

### 1. 简化的分支模型
```
main (生产版本)
├── feature/v0.1.7 (下一版本开发)
├── feature/specific-feature (特定功能)
└── hotfix/urgent-fix (紧急修复)
```

### 2. 分支命名规范
- **功能分支**: `feature/功能名称` 或 `feature/v版本号`
- **修复分支**: `hotfix/问题描述`
- **备份分支**: `backup/描述-日期`

### 3. 版本发布流程
1. 在功能分支完成开发
2. 合并到main分支
3. 创建版本标签
4. 删除功能分支
5. 创建下一版本的功能分支

## 🛠️ 实用命令

### 检查分支状态
```bash
# 查看所有分支
git branch -a

# 查看当前分支
git branch --show-current

# 查看分支关系
git log --oneline --graph --all -10

# 查看未提交的更改
git status
```

### 分支操作
```bash
# 创建并切换到新分支
git checkout -b 新分支名

# 切换分支
git checkout 分支名

# 合并分支
git merge 源分支名

# 删除本地分支
git branch -d 分支名

# 删除远程分支
git push origin --delete 分支名
```

### 版本管理
```bash
# 创建标签
git tag -a v0.1.6 -m "版本描述"

# 推送标签
git push origin --tags

# 查看标签
git tag -l

# 删除标签
git tag -d 标签名
git push origin --delete 标签名
```

## 🎯 我的具体建议

基于您的项目情况，我建议：

### 立即执行（今天）
1. **提交当前所有更改**
2. **使用方案A发布v0.1.6**
3. **清理旧的功能分支**

### 短期规划（本周）
1. **建立标准的分支管理流程**
2. **创建v0.1.7开发分支**
3. **更新项目文档**

### 长期维护
1. **每个版本使用一个功能分支**
2. **定期清理已合并的分支**
3. **保持main分支的稳定性**

## 🚨 注意事项

### 执行前检查
- [ ] 确保所有重要更改都已提交
- [ ] 备份重要的工作分支
- [ ] 确认团队成员了解分支变更

### 安全措施
```bash
# 创建备份
git checkout -b backup/before-cleanup-$(date +%Y%m%d)

# 检查工作目录
git status

# 确认分支状态
git branch -a
```

## 📞 如果遇到问题

### 常见问题解决
1. **合并冲突**: 手动解决冲突后继续合并
2. **推送失败**: 先拉取远程更改再推送
3. **分支删除失败**: 确保分支已完全合并

### 紧急恢复
```bash
# 如果操作出错，可以恢复到备份分支
git checkout backup/分支名

# 或者使用reflog恢复
git reflog
git checkout HEAD@{n}
```

---

**建议**: 先使用方案A的步骤1-3发布v0.1.6，然后再考虑分支清理。这样可以确保您的工作成果得到保存，同时简化分支结构。
