---
name: aomaker-guide
description: AOMaker框架使用指南 - 包含框架核心概念、单接口测试编写、场景测试编写
license: MIT
metadata:
  audience: developers
  framework: aomaker
---

# AOMaker 测试框架指南

## 框架核心概念

### 1. 目录结构
```
project/
├── apis/                    # 接口定义
│   └── xxx/
│       ├── apis.py          # 接口类定义
│       └── models.py        # 数据模型定义
├── testcases/               # 测试用例
│   └── test_api/
├── data/                    # 测试数据
│   └── api_data/
├── utils/                   # 公共工具
├── conf/                    # 配置文件
│   └── config.yaml
├── login.py                 # 登录认证
├── run.py                   # 运行入口
└── pytest.ini               # pytest配置
```

### 2. 核心组件

#### 接口定义 (apis.py)
```python
@define(kw_only=True)
@router.get("/api/users")
class GetUsersAPI(BaseAPI):
    """获取用户列表"""
    
    @define
    class QueryParams:
        offset: int = field(default=0)
        limit: int = field(default=10)
    
    query_params: QueryParams = field(factory=QueryParams)
    # 建议不写response，避免schema校验问题
    # 如需校验，确保返回结构与模型一致
```

#### 数据模型 (models.py)
```python
@define(kw_only=True)
class UserResponse:
    items: List[User] = field()
    totalItems: int = field()
```

## 单接口测试编写

### 基本模式
```python
import pytest

from apis.xxx.apis import SomeAPI

@pytest.mark.module_name
def test_api_success():
    """测试接口正常场景"""
    res = SomeAPI().send()
    assert res.cached_response.raw_response.status_code == 200
    
    data = res.cached_response.raw_response.json()
    assert "items" in data
```

### 带参数
```python
@pytest.mark.module_name
def test_api_with_params():
    """测试接口-带参数"""
    path_params = SomeAPI.PathParams(id=123)
    api = SomeAPI(path_params=path_params)
    res = api.send()
    assert res.cached_response.raw_response.status_code == 200
```

### 参数化数据驱动
```python
from utils.test_data_helper import get_test_data_list

TEST_DATA = get_test_data_list("component", "module", "data_key")

@pytest.mark.module_name
@pytest.mark.parametrize("data", TEST_DATA)
def test_api_parametrized(data):
    """参数化测试"""
    api = SomeAPI(request_body=data)
    res = api.send()
    assert res.cached_response.raw_response.status_code == 200
```

## 场景测试编写

### 测试数据准备
```python
from aomaker.storage import cache

def setup_test_data():
    """准备测试数据"""
    # 使用cache缓存，避免重复创建
    cache_key = "test_data_key"
    if cache.get(cache_key):
        return True
    
    # 创建数据
    api = CreateAPI(request_body={...})
    res = api.send()
    
    if res.cached_response.raw_response.status_code in (200, 201):
        cache.set(cache_key, True)
        return True
    return False
```

### 场景测试
```python
@pytest.mark.scenario
def test_user_workflow():
    """用户工作流场景测试"""
    # 1. 准备数据
    if not setup_test_data():
        pytest.skip("无法准备测试数据")
    
    # 2. 执行操作A
    res_a = StepAAPI().send()
    assert res_a.cached_response.raw_response.status_code == 200
    
    # 3. 执行操作B
    res_b = StepBAPI().send()
    assert res_b.cached_response.raw_response.status_code == 200
    
    # 4. 验证结果
    result = GetResultAPI().send()
    data = result.cached_response.raw_response.json()
    assert data["status"] == "success"
```

### 测试数据准备规范 (get_for_test)
每个接口如果存在依赖数据，必须统一使用 `get_for_test()` 函数：
- 能查到直接返回
- 查不到则调用创建接口

```python
def get_for_test():
    """
    查询前先调用，确保测试数据存在
    1. 先查询，如果测试数据已存在，直接返回 True
    2. 如果测试数据不存在，调用创建 API 创建测试数据
    3. 创建成功返回 True，失败返回 False
    """
    try:
        # 1. 查询现有数据
        api = ListAPI()
        res = api.send()
        
        if res.cached_response.raw_response.status_code != 200:
            return False
        
        data = res.cached_response.raw_response.json()
        
        # 2. 检查测试数据是否已存在
        for item in data.get("items", []):
            if item.get("name") == TEST_DATA_NAME:
                return True
        
        # 3. 测试数据不存在，创建它
        create_api = CreateAPI(request_body={"name": TEST_DATA_NAME, ...})
        create_res = create_api.send()
        
        if create_res.cached_response.raw_response.status_code in (200, 201):
            return True
        return False
        
    except Exception:
        return False
```

## 常用技巧

### 1. 关闭Schema校验
当接口返回结构与模型定义不符时：
```python
# 构造时关闭
api = SomeAPI(enable_schema_validation=False)
res = api.send()
```

### 1.1 enable_schema_validation 与 response 的区别

- `enable_schema_validation=False` - 关闭 JSON Schema 校验，但 attrs 仍会尝试将响应解析为定义的 response model 类型
- `response=None` - 完全不解析响应体，直接返回原始 raw_response

**使用场景：**
- 当 List 接口返回空数据如 `{'items': None, 'totalItems': 0}` 时，attrs 解析可能失败
- 需要同时使用：`enable_schema_validation=False, response=None`

```python
# 完整关闭校验和解析
list_api = HandleListRuleGroupsAPI(
    path_params=HandleListRuleGroupsAPI.PathParams(cluster=cluster, namespace=namespace),
    enable_schema_validation=False,
    response=None  # 必须，否则 attrs 解析可能失败
)
res = list_api.send()
```

### 2. 响应Body非JSON格式处理
当接口返回404或错误响应体不是JSON格式时，需要禁用响应解析：
```python
# 方式1：设置 response=None 禁用响应体解析
api = SomeAPI(
    path_params=SomeAPI.PathParams(name="nonexistent"),
    enable_schema_validation=False,
    response=None  # 禁用响应体解析，避免JSONDecodeError
)
res = api.send()
assert res.cached_response.raw_response.status_code == 404

# 方式2：直接访问 raw_response 不调用 .json()
status_code = res.cached_response.raw_response.status_code
text = res.cached_response.raw_response.text  # 获取原始文本而非JSON
```

### 3. Update接口最佳实践
Update接口需要先GET获取当前数据，然后修改字段作为request body：
```python
# 1. GET获取当前数据
get_api = HandleGetXXXAPI(
    path_params=HandleGetXXXAPI.PathParams(name=resource_name),
    enable_schema_validation=False
)
get_res = get_api.send()
current_data = get_res.cached_response.raw_response.json()

# 2. 修改需要的字段
current_data["spec"]["rules"][0]["annotations"]["summary"] = "updated summary"

# 3. 发送Update请求
update_api = HandleUpdateXXXAPI(
    path_params=HandleUpdateXXXAPI.PathParams(name=resource_name),
    request_body=current_data,  # 使用GET返回的数据作为body
    enable_schema_validation=False
)
update_res = update_api.send()
assert update_res.cached_response.raw_response.status_code == 200
```

### 4. Patch接口最佳实践
Patch接口需要先从LIST接口获取数据，移除不必要的参数，作为request body：
```python
# 1. LIST获取数据（或GET单个资源）
list_api = HandleListXXXAPI(
    path_params=HandleListXXXAPI.PathParams(cluster=cluster)
)
list_res = list_api.send()
data = list_res.cached_response.raw_response.json()
items = data.get("items", [])
if not items:
    pytest.skip("无数据")

# 2. 获取第一个item并移除不必要的字段
import copy
patch_body = copy.deepcopy(items[0])

# 移除metadata中不需要的字段
metadata = patch_body.get("metadata", {})
metadata.pop("uid", None)
metadata.pop("resourceVersion", None)
metadata.pop("generation", None)
metadata.pop("managedFields", None)

# 移除status字段
patch_body.pop("status", None)

# 3. 修改需要更新的字段
metadata.setdefault("annotations", {})
metadata["annotations"]["kubesphere.io/alias-name"] = "new-alias"
metadata["annotations"]["kubesphere.io/description"] = "new description"

# 4. 发送Patch请求
patch_api = HandlePatchXXXAPI(
    path_params=HandlePatchXXXAPI.PathParams(name=metadata["name"]),
    request_body=patch_body,
    enable_schema_validation=False
)
patch_res = patch_api.send()
assert patch_res.cached_response.raw_response.status_code == 200
```

### 5. 加载测试数据
```python
from utils.test_data_helper import load_test_data, get_test_data_list

# 获取数据列表（用于参数化）
data_list = get_test_data_list("ks_core", "access_management", "invalid_members")

# 获取单个配置（需取第一个元素）
labels = load_test_data("ks_core", "multi_cluster", "test_labels")
TEST_LABEL_KEY = labels[0].get("key", "default_key") if labels else "default_key"
```

### 4. 使用cache缓存
```python
from aomaker.storage import cache

cache.set("key", value)
value = cache.get("key")
```

### 5. 配置管理 (config)
```python
from aomaker.storage import config

host = config.get("host")
env = config.get("env")
```

## 鉴权管理

### login.py 配置
在项目根目录创建 `login.py`，继承 `BaseLogin`：
```python
from aomaker.fixture import BaseLogin
from aomaker.core.http_client import HTTPClient

class Login(BaseLogin):
    def login(self):
        # self.base_url - 当前环境base_url
        # self.account - {'user': 'xxx', 'pwd': 'xxx'}
        login_data = {"username": self.account['user'], "password": self.account['pwd']}
        # ... 调用登录API
        return token
    
    def make_headers(self, token):
        return {"Authorization": f"Bearer {token}"}
```

## 并行测试

### CLI 运行
```bash
arun --mt --dist-mark mark1 mark2  # 多线程
arun --mp --dist-mark mark1 mark2  # 多进程(仅Linux/Mac)
```

### 方式二：run.py
```python
from aomaker.cli import main_run

main_run(env="test", mt=True, d_mark="mark1 mark2")
```

## 钩子函数 (hooks.py)

在主进程/线程执行，在 pytest 之前：
```python
from aomaker.aomaker import hook

@hook
def before_all():
    """全局初始化"""
    print("测试开始前执行")
```

`hooks.py` 中定义：
```python
from aomaker.aomaker import hook

@hook
def before_all():
    """全局初始化"""
    print("测试开始前执行")
```

## 请求中间件 (middlewares/)

### 创建中间件
在 `middlewares/` 目录创建 `xxx_middleware.py`：
```python
from aomaker.core.middlewares.registry import middleware, RequestType, CallNext

@middleware(name="my_middleware", priority=500, enabled=True)
def my_middleware(request: RequestType, call_next: CallNext):
    # 请求前处理
    response = call_next(request)
    # 响应后处理
    return response
```

### 配置启用
在 `middlewares/middleware.yaml` 中配置：
```yaml
my_middleware:
  enabled: true
  priority: 500
```

## 流式响应

```python
# 发送流式请求
response = API().send(stream=True)

# 处理流数据
def process_chunk(data):
    print(data)

response.process_stream(stream_mode="lines", callback=process_chunk)
```

## 多集群/企业空间支持

### 集群信息说明
- **Host集群**：只有1个，必须存在
- **Member集群**：可选，最多1个（测试环境）

### 接口分类：是否需要 `/clusters/xxx` 前缀

**不需要 `/clusters/xxx` 前缀的接口（集群管理类）：**
- 集群列表查询：`/kapis/tenant.kubesphere.io/v1alpha3/clusters`
- 集群标签管理：`/kapis/cluster.kubesphere.io/v1alpha1/labels`
- 集群验证：`/kapis/cluster.kubesphere.io/v1alpha1/clusters/validation`
- kubeconfig更新：`/kapis/cluster.kubesphere.io/v1alpha1/clusters/{cluster}/kubeconfig`
- 企业空间管理：`/kapis/tenant.kubesphere.io/v1alpha3/workspaces`
- 项目管理：`/kapis/tenant.kubesphere.io/v1alpha3/namespaces`
- 用户相关：`/kapis/iam.kubesphere.io/v1beta1/users`
- 权限管理：`/kapis/iam.kubesphere.io/v1beta1/clustermembers`

**需要 `/clusters/xxx` 前缀的接口（资源类）：**
- deployments、services、pods 等工作负载资源
- `/kapis/resources.kubesphere.io/v1alpha3/deployments?sortBy=updateTime&limit=10`
- 实际调用时需要加上集群前缀：

**Host集群：**
```
/clusters/{host-cluster-name}/kapis/resources.kubesphere.io/v1alpha3/deployments?sortBy=updateTime&limit=10
```

**Member集群：**
```
/clusters/{member-cluster-name}/kapis/resources.kubesphere.io/v1alpha3/deployments?sortBy=updateTime&limit=10
```

### 公共方法：获取集群列表

使用 `utils.cluster_helpers.get_clusters()` 获取集群信息：

```python
from utils.cluster_helpers import get_clusters

host_cluster, member_cluster = get_clusters()
# host_cluster: 必有值，host集群名称
# member_cluster: 可选值，member集群名称（没有则为None）
```

### 资源类接口自动添加集群前缀

通过中间件自动为资源类接口添加 `/clusters/{cluster}` 前缀，无需修改 API 定义：

```python
from utils.cluster_helpers import set_current_cluster, clear_current_cluster

# 设置当前集群，后续资源类接口请求会自动添加 /clusters/{cluster} 前缀
set_current_cluster(host_cluster)

try:
    # 这个请求会自动变成 /clusters/{host_cluster}/kapis/resources.kubesphere.io/v1alpha3/deployments
    res = ListDeploymentsAPI().send()
finally:
    # 清除集群设置
    clear_current_cluster()
```

**中间件工作原理：**
- 自动识别需要添加前缀的接口（deployments、services、namespaces 等）
- 从缓存读取当前集群名称，自动添加到请求路径
- 集群管理类接口（clusters、workspaces、labels 等）不受影响

### 公共方法：创建测试企业空间和项目

如需创建测试企业空间和项目，使用 `utils.cluster_helpers.setup_test_workspace_and_project()`：

```python
from utils.cluster_helpers import setup_test_workspace_and_project

success, host_cluster, member_cluster = setup_test_workspace_and_project()
# Host集群：创建企业空间 ws-host-test 和项目 host-pro1-test
# Member集群（如有）：创建企业空间 ws-member-test 和项目 mem-pro1-test
```

### 公共方法：清理测试企业空间和项目

测试结束后清理资源，使用 `utils.cluster_helpers.cleanup_test_workspace_and_project()`：

```python
from utils.cluster_helpers import cleanup_test_workspace_and_project

# 在测试结束时调用，删除测试创建的企业空间和项目
cleanup_test_workspace_and_project()
```

### 企业空间接口调用示例
```python
# Host企业空间 - 默认用例，所有环境都执行
@pytest.mark.resource
def test_host_workspace():
    """获取Host集群deployments列表"""
    host_cluster, _ = get_clusters()
    if not host_cluster:
        pytest.skip("无host集群")
    
    # 构建带集群前缀的URL
    path_params = ListDeploymentsAPI.PathParams(
        cluster=host_cluster,
        namespace="host-pro1-test"
    )
    api = ListDeploymentsAPI(path_params=path_params)
    api.query_params = api.QueryParams(sortBy="updateTime", limit=10)
    res = api.send()
    assert res.cached_response.raw_response.status_code == 200

# Member企业空间 - 多集群用例，只在多集群环境执行
@pytest.mark.resource
@pytest.mark.multi_cluster
def test_member_workspace():
    """获取Member集群deployments列表"""
    _, member_cluster = get_clusters()
    if not member_cluster:
        pytest.skip("无member集群")
    
    path_params = ListDeploymentsAPI.PathParams(
        cluster=member_cluster,
        namespace="mem-pro1-test"
    )
    api = ListDeploymentsAPI(path_params=path_params)
    res = api.send()
    assert res.cached_response.raw_response.status_code == 200
```

### 多集群标签使用规范

**标签定义：**
- `@pytest.mark.resource` - 资源类接口用例（Host集群，必执行）
- `@pytest.mark.multi_cluster` - 多集群用例（Member集群，可选执行）

**执行策略：**
```bash
# 单集群环境 - 只执行Host集群用例
pytest -m resource test_deployments.py

# 多集群环境 - 执行全部用例
pytest -m "resource or multi_cluster" test_deployments.py

# 只执行多集群用例
pytest -m multi_cluster test_deployments.py
```

## 集群前缀中间件

在 `middlewares/cluster_prefix_middleware.py` 中实现，通过 `set_current_cluster(cluster_name)` 设置当前集群，自动为指定路径添加 `/clusters/{cluster}` 前缀。

### 中间件配置

`middlewares/middlewares.yaml` 中启用：
```yaml
cluster_prefix:
    priority: 100
    enabled: true
```

### 使用方式

```python
from utils.cluster_helpers import set_current_cluster, clear_current_cluster

set_current_cluster("member-cluster-name")
api = SomeAPI(...)
api.send()
clear_current_cluster()
```

### 配置路径规则

默认所有接口都加前缀，只有在 `EXCLUDE_PATHS` 中配置的接口才排除（使用 `{workspace}` 作为通配符）。

后续如有新接口不需要前缀，添加到 `EXCLUDE_PATHS` 即可。

## 多集群测试规范

### 测试环境类型

| 环境类型 | 集群情况 | 说明 |
|---------|---------|------|
| 单集群 | 只有 host 集群 | 只执行 host 集群用例 |
| 多集群 | host + 1 个 member 集群 | 执行 host + member 集群用例 |

### 标签定义

| 标签 | 说明 | 示例 |
|-----|------|------|
| `@pytest.mark.xxx_module` | 模块级标记，按功能分 | `@pytest.mark.alerting_management` |
| `@pytest.mark.multi_cluster` | 多集群用例（只在多集群环境执行） | Member 集群验证 |
| `@pytest.mark.scenario` | 场景测试 | 业务流验证 |

**模块标签命名**（按功能模块，不是按组件）：
- `@pytest.mark.alerting_management` - 告警管理
- `@pytest.mark.whizard_monitoring` - 监控
- `@pytest.mark.ks_core` - ks-core 通用
- `@pytest.mark.whizard_logging` - 日志
- `@pytest.mark.notification` - 通知管理
- 等等...

**完整模块列表见：** `conf/labels.yaml`

### 运行策略

```bash
# 单集群环境 - 排除多集群用例，其他全跑（包含场景）
arun -e dev -m "not multi_cluster"

# 多集群环境 - 全部跑
arun -e dev

# 运行单个模块（单集群）
arun -e dev -m "alerting_management and not multi_cluster"

# 运行单个模块（多集群）
arun -e dev -m alerting_management
```

### Member 集群测试要点

在涉及集群的接口测试中，必须补充 member 集群的验证用例：

1. **验证数据隔离** - 确保 member 集群返回的是 member 集群的数据，而非 host 集群数据
2. **验证接口可用性** - 在 member 集群下 CRUD 操作正常

**fixture 声明**：
```python
@pytest.fixture(scope="module")
def member_cluster():
    """获取 member 集群（多集群环境）"""
    _, member = get_clusters()
    if not member:
        pytest.skip("无 member 集群，单集群环境跳过")
    return member
```

**测试类声明**：
```python
@pytest.mark.alerting_management
@pytest.mark.multi_cluster
class TestListClusterRuleGroupsMember:
    """Member 集群 - 查询集群规则组列表"""
```

### 测试用例组织

每个涉及集群的 API，需要包含以下测试：
1. Host 集群基础测试（成功、异常、边界）
2. Host 与 Member 集群数据差异验证
3. Member 集群 CRUD 操作

**Global 接口不需要多集群测试**（不区分集群）

## 注意事项

1. **不要使用print** - 按框架风格，使用日志或直接assert
2. **统一使用公共方法加载数据** - 使用 `utils/test_data_helper.py`
3. **处理异常场景** - API返回非200时，可能需要关闭schema校验
4. **测试数据放到JSON文件** - 放在 `data/api_data/` 目录下
5. **必须实现 get_for_test()** - 每个接口存在依赖数据时，统一使用该函数准备数据
6. **区分接口类型**：
   - 集群管理类接口（labels、clusters、workspaces等）**不需要** `/clusters/xxx` 前缀
   - 资源类接口（deployments、services、pods等）**需要** `/clusters/xxx` 前缀
7. **多集群测试必须补充** - 每个集群级 API 都需要 member 集群的验证用例
8. **Global 接口不需要多集群测试** - 全局 API（globalrulegroups、globalalerts）不区分集群
