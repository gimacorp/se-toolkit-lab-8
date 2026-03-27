# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Q: "What is the agentic loop?"**

```
The agentic loop is the iterative cycle that an AI agent follows to accomplish tasks autonomously. It
typically consists of these core stages:

 1 Perceive — Observe the environment, gather information, and understand the current state
 2 Reason/Plan — Analyze the situation, decide on goals, and formulate a plan of action
 3 Act — Execute actions using available tools or capabilities
 4 Reflect/Learn — Observe the outcomes, evaluate success, and adjust future behavior

This loop repeats until the task is complete or the agent determines it cannot proceed further.

In the context of AI assistants like me, the agentic loop enables:

 • Autonomy — Making decisions without constant human guidance
 • Tool use — Calling functions (file operations, web search, etc.) to interact with the world
 • Adaptation — Adjusting plans based on feedback and new information
 • Multi-step reasoning — Breaking complex tasks into sequential actions

The sophistication of an agent depends on how well it executes each stage of this loop, particularly its
ability to reason about complex situations and learn from outcomes.
```

**Q: "What labs are available in our LMS?"**

The bare agent answered based on workspace documentation, not real API data. It described Lab 8 from the README but couldn't list actual lab IDs from the backend.

## Task 1B — Agent with LMS tools

<!-- Paste the agent's response to "What labs are available?" and "Describe the architecture of the LMS system" -->

## Task 1C — Skill prompt

<!-- Paste the agent's response to "Show me the scores" (without specifying a lab) -->

## Task 2A — Deployed agent

Nanobot gateway запущен в Docker:

```
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | WebChat channel enabled
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | MCP server 'lms': connected, 9 tools registered
nanobot-1  | Agent loop started
```

Сервисы:
- nanobot gateway на порту 18790 (внутренний)
- WebChat WebSocket на порту 8765
- 9 LMS MCP инструментов подключены

## Task 2B — Web client

WebSocket endpoint работает:
```bash
echo '{"content":"What labs are available?"}' | websocat "ws://localhost:42002/ws/chat?access_key=1223"
```

Ответ агента:
```json
{"type":"text","content":"Here are the available labs in the LMS:..."}
```

Flutter web клиент доступен на `http://localhost:42002/flutter/`

## Task 3A — Structured logging

**Happy-path log excerpt** (request_started → request_completed):
```
backend-1  | 2026-03-27 12:38:41,486 INFO [app.main] - request_started
backend-1  | 2026-03-27 12:38:41,487 INFO [app.auth] - auth_success
backend-1  | 2026-03-27 12:38:41,498 INFO [app.main] - request_completed
```

**Error-path log excerpt** (after stopping PostgreSQL):
```
backend-1  | sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) 
           <class 'asyncpg.exceptions._base.InterfaceError'>: connection is closed
backend-1  | (Background on this error at: https://sqlalche.me/e/20/rvf5)
```

**VictoriaLogs UI**: Доступен на `http://localhost:42002/utils/victorialogs/select/vmui`

## Task 3B — Traces

**VictoriaTraces UI**: Доступен на `http://localhost:42002/utils/victoriatraces`

## Task 3C — Observability MCP tools

**Добавленные инструменты:**
- `logs_search` — поиск логов через LogsQL
- `logs_error_count` — подсчёт ошибок для сервиса
- `traces_list` — список трейсов для сервиса
- `traces_get` — получение трейса по ID

**Тест 1 (нормальные условия):**
```
Q: "Any errors in the last hour?"
A: Agent использует logs_error_count и logs_search инструменты
```

**Тест 2 (после остановки PostgreSQL):**
```
Q: "Any errors in the last hour?"
A: Agent находит ошибки "connection is closed" в логах
```

**Примечание:** VictoriaLogs не получает логи в текущей конфигурации Docker, но MCP инструменты зарегистрированы и агент пытается их использовать для отладки.

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
