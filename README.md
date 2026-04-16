# KubeSphere Enterprise 接口自动化测试

基于 [AoMaker](https://github.com/anomalyco/aomaker) 框架的 KubeSphere Enterprise API 自动化测试项目。

## 项目结构

```
.
├── apis/                          # API 定义（由 swagger 生成）
│   ├── ks_core/                   # KubeSphere Core API
│   │   ├── apis.py                # 接口路由定义
│   │   └── models.py              # 数据模型定义
│   └── mock/                      # Mock API（测试用）
├── conf/
│   └── config.yaml                # 环境配置文件
├── data/
│   ├── api_data/                  # 测试数据
│   │   ├── _common/               # 公共数据（用户、集群配置等）
│   │   └── {module}/              # 模块级数据（按 ks_core 模块划分）
│   │       ├── _common.json       # 模块公共数据
│   │       ├── test_environment.json
│   │       └── {feature}/         # 功能级数据
│   └── scenario_data/             # 场景测试数据
├── middlewares/
│   ├── middlewares.yaml           # 中间件配置
│   └── cluster_prefix_middleware.py   # 集群前缀中间件
├── testcases/
│   ├── test_api/                  # 单接口测试
│   └── test_scenario/             # 场景测试
├── utils/                         # 公共工具
├── hooks.py                       # 全局钩子（before_all/after_all）
├── login.py                       # 登录实现
└── pytest.ini                     # pytest 配置
```

## 快速开始

### 1. 安装依赖

```bash
pip install aomaker
```

### 2. 配置环境

在 `conf/config.yaml` 中配置测试环境：

```yaml
test:
  base_url: "http://139.198.112.87:20885"
  account:
    user: "admin"
    pwd: "P@88w0rd"
```

### 3. 运行测试

```bash
# 运行所有测试
arun

# 按模块运行
arun -e test -m access_management

# 按模块运行（指定环境）
arun -e test -m identity_management
```

## 开发规范

### 测试数据

测试数据统一放在 `data/api_data/` 目录下，按模块和功能组织：

```
data/api_data/
├── _common/                    # 公共数据
│   ├── test_users.json         # 用户配置
│   ├── cluster_config.json     # 集群配置
│   └── test_labels.json        # 标签配置
└── ks_core/                    # KubeSphere Core 模块
    ├── _common.json            # 模块公共数据
    ├── test_environment.json   # 测试环境配置
    └── access_management/      # 功能目录
        ├── valid_members.json
        └── invalid_members.json
```

加载测试数据：
```python
from utils.test_data_helper import load_test_data

# 加载配置（支持嵌套字段）
users = load_test_data("_common", "test_users")
username = load_test_data("_common", "test_users", data_key="admin.username", replace_vars=False)

# 加载数据列表（用于参数化）
members = load_test_data("ks_core", "access_management", "invalid_members")
```

### 变量替换

数据文件中支持 `{{variable}}` 变量替换：
```json
{
  "username": "{{admin_user}}",
  "password": "P@88w0rd"
}
```

注意：`{{admin_user}}` 依赖 `test_users.json` 中 `admin.username` 字段已配置，否则会被当作文本直接发送。

### 集群前缀

测试涉及 Host 和 Member 多集群时，**不需要手动添加集群前缀**。通过 `cluster_prefix_middleware` 中间件自动处理：

```python
from utils.cluster_helpers import set_current_cluster, clear_current_cluster

# 设置当前集群（中间件会自动添加 /clusters/{cluster} 前缀）
set_current_cluster("member-cluster-name")
api = SomeAPI(...)
api.send()
clear_current_cluster()
```

中间件默认对所有接口添加 `/clusters/xxx` 前缀。如需排除特定接口，修改 `middlewares/cluster_prefix_middleware.py` 中的 `EXCLUDE_PATHS`：

```python
EXCLUDE_PATHS = [
    "/kapis/tenant.kubesphere.io/v1alpha3/clusters",
    "/kapis/tenant.kubesphere.io/v1beta1/workspacetemplates",
    # 更多排除的接口...
]
```

### Schema 校验

API 返回非 200 或 Status 响应时，关闭 schema 校验：
```python
api = SomeAPI(enable_schema_validation=False)
```

### 钩子函数

`hooks.py` 中定义全局初始化和清理逻辑：

- `before_all`: 测试开始前准备数据（企业空间、项目等）
- `after_all`: 测试结束后清理数据

## 测试标记

| 标记 | 说明 |
|------|------|
| `authentication` | 需要认证的用例 |
| `access_management` | 访问管理用例 |
| `multi_cluster` | 多集群用例 |
| `identity_management` | 身份管理用例 |
| `namespaced_resources` | 命名空间资源用例 |

运行特定标记的测试：
```bash
arun -e test -m access_management
```

## 测试数据初始化

项目实现了自动化的测试数据初始化机制（通过 `before_all` 钩子），无需手动准备：

- **企业空间**：自动创建 `ws-host-test`（Host）和 `ws-member-test`（Member）
- **项目**：自动创建 `host-pro1-test` 和 `mem-pro1-test`
- 资源存在则复用，不存在则创建
- 支持重试机制处理数据库锁定

## 常见问题

**Q: 变量替换不生效，`{{admin_user}}` 显示为原文**

A: 检查 `data/api_data/_common/test_users.json` 中是否正确配置了 `admin.username` 字段。

**Q: Allure 报告生成失败**

A: 确保已安装 Allure Commandline：[安装指南](https://allurereport.org/)

**Q: 数据库锁定错误**

A: 框架已内置重试机制，如仍频繁出现，可增加重试次数或等待时间。
