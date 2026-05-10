# CampusMate · 校园 AI 助手

一个基于 React + FastAPI + LLM 的校园问答助手 Demo。用户用自然语言提问校园相关问题（如"图书馆借阅规则""学生证怎么补办""校历查询"等），系统通过本地知识库检索 + 工具调用 + LLM 生成的方式给出回答。

> 项目定位：轻量级校园 Agent，演示前后端分离的 AI 应用架构、组件化前端工程实践、以及多模式（云端 LLM / 本地知识库）切换。

---

## 技术栈

**前端**

- React 18 + TypeScript
- Vite 构建
- TailwindCSS 工程化样式
- 组件化拆分 + 状态提升 + 受控组件

**后端**

- Python 3.11+
- FastAPI + Pydantic
- 关键词路由 + JSON 知识库
- 工具调用（校历查询、日期计算、办公时间）
- 支持 DeepSeek API / 本地数据库双模式

---

## 项目结构

```
campusmate/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── BootScreen.tsx       # 模式选择首屏
│   │   │   ├── Composer.tsx         # 输入框 + 发送按钮
│   │   │   ├── MessageBubble.tsx    # 单条消息气泡
│   │   │   ├── MessageList.tsx      # 消息列表 + 自动滚动
│   │   │   └── Sidebar.tsx          # 侧栏 + 示例问题
│   │   ├── App.tsx                  # 主壳，状态管理 + 业务逻辑
│   │   ├── main.tsx                 # createRoot 挂载入口
│   │   ├── types.ts                 # 共享类型定义
│   │   └── style.css                # Tailwind 三件套 + 全局样式
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── tsconfig.json
│   └── package.json
└── backend/
    ├── app/
    │   ├── main.py                  # FastAPI 入口
    │   ├── router.py                # 路由 + 关键词分发
    │   ├── llm.py                   # DeepSeek 调用封装
    │   ├── kb.py                    # 本地知识库检索
    │   ├── tools.py                 # 工具调用（日期/办公时间）
    │   ├── schemas.py               # Pydantic 数据模型
    │   └── config.py                # 配置加载
    └── run.py                       # 启动入口
```

---

## 核心功能

| 功能 | 说明 |
|---|---|
| 校园知识问答 | 回答图书馆借阅规则、学生证补办、选课退课、宿舍报修等问题 |
| 校历查询 | 查询开学、补退选截止、期末考试周、暑假等校历事项 |
| 办公信息查询 | 查询教务处、学生事务中心、后勤服务中心的办公时间、电话和地点 |
| 日期计算 | 计算"从今天到某个日期还有几天"或两个日期之间相差几天 |
| 双模式切换 | 用户可选择 DeepSeek 云端模式（联网生成）或本地知识库模式（无网可用） |

---

## 工程实践亮点

### 1. 前端组件化重构

项目早期所有逻辑集中在 `main.tsx`（163 行），随着功能迭代发现展示逻辑、交互逻辑、业务状态混在一起，改一处容易影响一片。后续按职责拆分为 6 个独立组件：

- **`BootScreen`** — 模式选择首屏
- **`Composer`** — 输入框，受控组件 + 提交事件
- **`MessageBubble`** — 单条消息纯展示
- **`MessageList`** — 列表容器 + ref forwarding 实现自动滚动
- **`Sidebar`** — 侧栏 + 示例问题列表
- **`App`** — 主壳，唯一状态亮点（messages / loading / mode 等）

`main.tsx` 简化到只负责 `createRoot` 挂载（5 行）。

### 2. 状态管理设计

遵循 colocation 原则，状态归属判断按"有多少组件需要读取"决定：

- **共享状态**（`messages` / `loading` / `mode` / `sessionId`）→ 提升到 App
- **局部状态**（`input`）→ 留在 Composer 内部，不污染父组件 re-render

### 3. 防重复提交三层防护

- **UI 层**：按钮 `disabled = loading || !input.trim()`
- **组件逻辑层**：`handleSubmit` 内 `if (!text || disabled) return`，拦截回车提交路径
- **业务逻辑层**：`App.send()` 入口 `if (loading) return`，兜底 Sidebar 等其他入口

### 4. async 状态更新使用函数式更新

`send` 函数是 async 流程，期间会多次 `setMessages`。使用函数式更新（`setMessages(prev => ...)`）避免 stale closure 导致的更新覆盖问题。

### 5. TailwindCSS 工程化样式

从原生 CSS（262 行 `.composer` `.bubble` `.mode-card` 等业务类）迁移到 TailwindCSS，仅保留 10 行全局样式（字体、渐变背景、滚动条、动画 keyframes）。

---

## 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt   # 或 uv sync
python run.py
```

后端默认监听 `http://127.0.0.1:8000`。

### 前端

```bash
cd frontend
npm install
npm run dev
```

前端默认监听 `http://127.0.0.1:5173`。

### 环境变量

DeepSeek 模式需要在 `backend/.env` 中配置：

```
DEEPSEEK_API_KEY=your_api_key_here
```

不配置也可使用本地模式。

---

## 已知不足 & 未来规划

| 方向 | 当前状态 | 规划 |
|---|---|---|
| 流式响应 | 一次性返回完整答案 | 改造为 SSE 流式输出，实现打字机效果 |
| 知识检索 | 关键词匹配 + JSON 知识库 | 引入向量检索（embedding + RAG） |
| 多会话历史 | sessionId 内存级、刷新即丢 | 持久化会话历史 |
| 错误处理 | 简单的 try/catch + setError | 增加重试、降级、超时处理 |
| 类型严格 | catch 块为 `any` | 切换到 `unknown` + 类型守卫 narrowing |

---

## 许可

MIT
