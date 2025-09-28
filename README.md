[中文](README.md) | [English](README.EN.md)

# Python Web 微服务项目示例

集成了常见的web项目组件，提供基本的web功能
- 定时任务:
  - [xxl-job](https://github.com/xuxueli/xxl-job)   
  - [pyxxl](https://github.com/fcfangcc/pyxxl)      
- 配置中心: [Nacos](https://github.com/nacos-group/nacos-sdk-python)
- 数据库: [MySQL / sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)
- Web框架: [FastAPI](https://github.com/fastapi/fastapi)
- 日志（集成trace id链路追踪）: [loguru](https://github.com/Delgan/loguru)
- 三方通知组件: [企业微信](https://developer.work.weixin.qq.com/document/path/99110)

# 项目结构

```
root/
├── app/                         # 核心应用代码目录
│   ├── common/                  # 通用模块
│   │   ├── const.py             # 系统字典/常量
│   │   ├── logger.py            # 系统日志配置
│   │   └── utils/               # 工具类集合
│   ├── config/                  # 系统配置模块
│   │   ├── db/                  # 数据库访问层和数据存储
│   │   ├── trace_/              # 链路追踪配置类
│   │   ├── nacos_config.py      # nacos配置中心类
│   │   └── xxl_job_config.py    # xxl-job 配置类
│   ├── nacos_/                  # nacos配置中心业务模块
│   │   └── controller.py        # nacos对外暴露接口（手动刷新配置使用）
│   ├── demo_business/           # demo 业务模块
│   │   ├── controller.py        # demo 业务对外暴露接口
│   │   └── service.py           # demo 业务逻辑实现
│   ├── web/                     # Web服务模块
│   │   └── server.py            # Web 服务启动入口
│   └── xxl_job/                 # XXL-JOB任务调度
│       ├── tasks/               # 具体任务实现
│       └── scheduler_server.py  # xxl-job任务调度服务启动入口
├── docker/                      # Docker配置文件
├── log/                         # 日志文件目录
├── xx_log/                      # xxl-job日志文件目录
├── config_prod.yaml             # 生产环境配置文件（仅仅只是连接nacos的配置文件，具体的业务配置均在nacos中）
├── config_uat.yaml              # uat环境配置文件（与config_prod.yaml用法一致）
├── config_test.yaml             # test环境配置文件（与config_prod.yaml用法一致）
└── requirements.txt             # 项目依赖包列表
```
# 目录详解

## [app](app) (核心应用目录)
```
这是项目的根应用目录，包含所有核心业务逻辑模块。
```

### [common](app/common) (通用模块)
```
包含项目的基础组件，如枚举类、工具类、日志等
```

子目录说明:
- `utils`: 工具类集合
  - [wechat_msg_util.py](app/common/utils/wechat_msg_util.py): 企微消息工具类

### [config](app/config) (系统配置模块)
```
包含项目的各种基本配置，，如数据库连接、Nacos配置、XXL-JOB配置等。
```

子目录说明:
- `db`: 数据库相关配置集合
  - [db_mysql.py](app/config/db/db_mysql.py): 企微消息工具类
- `trace_`: 链路追踪配置集合
  - [trace_config.py](app/config/trace_/trace_id_config.py): web请求链路追踪中间件
  - [request_context.py](app/config/trace_/request_context.py): 请求上下文对象
- [nacos_config.py](app/config/nacos_config.py): Nacos配置类
- [xxl_job_config.py](app/config/xxl_job_config.py): XXL-JOB配置类

### [demo_business](app/demo_business) (示例业务模块)
```
为展示项目结构的示例模块，可参考示例模块自行拓展。
```

子目录说明：（参考mvc框架）
- [controller.py](app/demo_business/controller.py): 示例业务统一对外暴露接口（RESTful API）
- [service.py](app/demo_business/service.py):  示例业务统具体业务实现

### [nacos_](app/nacos_) (nacos业务模块)
```
因没使用nacos官方自带的自动监听配置刷新逻辑，故自行实现手动刷新逻辑
（官方的逻辑里涉及到了多进程逻辑，使用起来不是很方便）
```

子目录说明：（参考mvc框架）
- [controller.py](app/demo_business/controller.py): nacos提供的对外刷新接口（RESTful API）


### [web](app/web) (Web服务模块)
```
提供RESTful API接口。
```

子目录说明:
- [server.py](app/web/server.py): Web服务器入口，使用FastAPI框架

### [xxl_job](app/xxl_job) (任务调度模块)
```
集成XXL-JOB分布式任务调度平台。
```

子目录说明:
- `tasks`: 具体任务实现
  - [config_task.py](app/xxl_job/tasks/config_task.py): 系统配置定时任务（例如nacos的刷新）
- [scheduler_server.py](app/xxl_job/scheduler_server.py): 调度服务器，负责注册和执行任务

## [docker](docker) (Docker配置)
```
包含Docker镜像构建所需的配置文件。
```

文件说明：
- [dockerfile-server](docker/dockerfile-server): Web服务 Docker镜像构建文件
- [dockerfile-job](docker/dockerfile-job): XXL-JOB调度服务 Docker镜像构建文件

## [log](log) (日志文件)
```
存放项目运行时生成的日志文件，按日期命名。
```

## [xxl_log](xxl_log) (xxl-job日志文件)
```
存放xxl-job运行时生成的日志文件，按日期命名。
```

## 配置文件

### [config_prod.yaml](config_prod.yaml)
```
生产环境配置文件，配置了Nacos配置中心的相关参数。
```

### [config_uat.yaml](config_uat.yaml)
```
UAT环境配置文件，配置了Nacos配置中心的相关参数。
```

### [config_test.yaml](config_test.yaml)
```
TEST环境配置文件，配置了Nacos配置中心的相关参数。
```