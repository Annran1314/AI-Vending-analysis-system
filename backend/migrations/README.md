# 数据库迁移说明

本目录包含数据库迁移脚本，用于管理数据库结构的变更。

## 迁移步骤

1. **初始化数据库迁移**
   ```bash
   flask db init
   ```

2. **生成迁移脚本**
   ```bash
   flask db migrate -m "描述迁移内容"
   ```

3. **应用迁移**
   ```bash
   flask db upgrade
   ```

4. **回滚迁移**
   ```bash
   flask db downgrade
   ```

## 迁移历史

### 2024-01-01-initial-migration
- 创建用户表 (users)
- 创建产品表 (products)
- 创建报告表 (reports)
- 设置外键关系
- 创建索引