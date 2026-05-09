# 旅行Agent智能体系统

> 基于千问大模型的多Agent智能旅行规划系统

## 系统简介

这是一个**多Agent调度的智能旅行规划系统**，用户只需输入想去的目的地城市，系统将自动调度多个专业Agent完成旅行规划。

## 核心特性

- **多Agent协作**：6个专业Agent协同工作，各司其职
- **NLP能力**：内置意图识别、信息抽取、文本生成、摘要等NLP任务
- **千问大模型**：基于通义千问API，生成高质量内容
- **美观界面**：Streamlit Web界面，操作简单直观
- **完整规划**：包含景点、美食、路线等全方位旅行建议

## Agent架构

```
用户输入城市
     ↓
[主调度Agent] ← 协调整个规划流程
     ↓
[路由Agent] → 验证城市有效性
     ↓
┌────┴────┐
↓         ↓
[攻略Agent] [美食Agent] ← 并行执行
     ↓         ↓
     └────┬────┘
          ↓
     [路线Agent] → 生成3日行程
          ↓
     [总结Agent] → 整合生成完整报告
```

### Agent说明

| Agent | 功能 |
|-------|------|
| 🧠 主调度Agent | 协调各子Agent工作流程 |
| 🔍 路由Agent | 验证城市有效性，提取城市信息 |
| 📍 攻略Agent | 生成景点攻略、文化特色 |
| 🍜 美食Agent | 推荐特色美食、必吃餐厅 |
| 🗺️ 路线Agent | 规划行程路线、估算预算 |
| 📝 总结Agent | 整合内容生成完整报告 |

## NLP任务

本系统包含以下**NLP任务**：

1. **意图识别**：识别用户的旅行意图（目的地查询、行程规划、美食推荐等）
2. **信息抽取**：从用户输入中提取关键信息（城市、天数、预算、旅行类型等）
3. **文本生成**：根据模板和数据生成旅行相关内容
4. **摘要生成**：对长文本进行摘要提取

## 项目结构

```
travel-agent-system/
├── main.py                    # Streamlit主入口
├── config.py                  # 系统配置（API、提示词等）
├── requirements.txt           # 依赖列表
├── README.md                  # 项目说明
├── utils/                     # 工具模块
│   ├── __init__.py
│   ├── llm_client.py        # LLM客户端
│   └── nlp_tasks.py          # NLP任务处理
└── agents/                   # Agent模块
    ├── __init__.py
    ├── base_agent.py         # Agent基类
    ├── coordinator_agent.py   # 主调度Agent
    ├── router_agent.py       # 路由Agent
    ├── guide_agent.py         # 攻略Agent
    ├── food_agent.py          # 美食Agent
    ├── route_agent.py         # 路线Agent
    └── summary_agent.py       # 总结Agent
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API

编辑 `config.py` 文件，配置您的千问API Key：

```python
QWEN_CONFIG = {
    "api_key": "your-api-key-here",  # 替换为您的API Key
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
}
```

### 3. 运行系统

```bash
streamlit run main.py
```

### 4. 使用系统

1. 在浏览器中打开显示的地址（通常是 http://localhost:8501）
2. 在左侧输入想去的目的地城市
3. 选择旅行天数和风格
4. 点击"开始规划"按钮
5. 等待系统生成完整的旅行规划报告

## 使用示例

```
输入：想去北京旅游，3天，休闲度假风格
```

系统将生成：
- 📍 北京景点攻略（故宫、长城、颐和园等）
- 🍜 北京美食推荐（烤鸭、豆汁、炸酱面等）
- 🗓️ 3日行程安排（每日详细路线）
- 💡 实用贴士和注意事项

## API配置

系统使用千问兼容的OpenAI接口，支持以下模型：

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| qwen-turbo | 速度快，成本低 | 快速测试、开发调试 |
| qwen-plus | 效果平衡 | 生产环境推荐 |
| qwen-max | 效果最好 | 高质量需求 |

## 技术栈

- **语言**：Python 3.8+
- **Web框架**：Streamlit
- **AI模型**：通义千问（千问API）
- **NLP能力**：基于LLM的意图识别、信息抽取、文本生成、摘要

## 注意事项

1. **API Key安全**：请妥善保管您的API Key，不要泄露给他人
2. **网络连接**：确保能够正常访问千问API服务
3. **内容审核**：AI生成的内容仅供参考，请以实际情况为准
4. **城市支持**：系统内置了常用旅游城市列表，也支持LLM验证其他城市

## 扩展开发

### 添加新的Agent

1. 在 `agents/` 目录下创建新的Agent类
2. 继承 `BaseAgent` 类
3. 实现 `process` 方法
4. 在 `main.py` 中注册新Agent

### 添加新的NLP任务

1. 在 `utils/nlp_tasks.py` 中添加新的任务方法
2. 调用 `LLMClient` 与大模型交互
3. 返回处理结果

## License

MIT License

## 联系方式

如有问题或建议，请联系开发者。
