# stock-profile

## 一、模块职责说明


| 模块              | 职责                                                   |
| ----------------- | ------------------------------------------------------ |
| **models/**       | 定义 ORM 模型，与数据库表结构对应                      |
| **schemas/**      | 定义 Pydantic 数据模型，用于请求/响应数据验证          |
| **repositories/** | 封装数据库 CRUD 操作，隔离 SQLAlchemy 逻辑             |
| **routes/**       | API 层，处理 HTTP 请求，调用 repository/service 层逻辑 |
| **modules/**      | 存放数据计算逻辑（指标、AI 分析、估值模型等）          |
| **core/**         | 核心配置、日志、全局常量                               |
| **utils/**        | 通用工具函数                                           |
| **reports/**      | 报表生成模块（导出 PDF、HTML、Excel 等）               |

## 二、服务运行

### 1、docker方式

```a
docker run -d -p 3000:3000 -e NEXT_PUBLIC_API_BASE=http://1.1.1.1:8000/api --name frontend stock-profile-frontend:v1.0
```
