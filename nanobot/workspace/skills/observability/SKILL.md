# Observability Skill

You have access to observability tools for debugging system issues.

## Available Tools

### Log tools (VictoriaLogs)

| Tool | Purpose | Parameters |
|------|---------|------------|
| `logs_search` | Search logs using LogsQL | `query` (required), `limit` (default 10) |
| `logs_error_count` | Count errors for a service | `service` (default "backend"), `minutes` (default 60) |

### Trace tools (VictoriaTraces)

| Tool | Purpose | Parameters |
|------|---------|------------|
| `traces_list` | List recent traces for a service | `service` (default "backend"), `limit` (default 10) |
| `traces_get` | Fetch a specific trace by ID | `trace_id` (required) |

## How to Use

### When the user asks "What went wrong?" or "Check system health"

**Follow this investigation flow:**

1. **First** — Use `logs_error_count` to check if there are recent errors:
   - Query: `{"service": "backend", "minutes": 5}`
   - If count is 0, report "System looks healthy"

2. **If errors found** — Use `logs_search` to get details:
   - Query: `"error"` or `"exception"` with limit 10
   - Look for: error messages, stack traces, trace IDs

3. **If you find a trace ID** in the logs (format: hex string like `58df4e8c4a88b2c4...`):
   - Use `traces_get` to fetch the full trace
   - Look for: which span failed, error tags

4. **Summarize findings** in plain English:
   - What failed (operation/service)
   - Error message
   - Root cause if clear
   - **Don't dump raw JSON**

### When the user asks about errors

1. Use `logs_error_count` to check if there are errors
2. If errors found, use `logs_search` with query `"error"` to see details
3. If you find a trace ID in the logs, use `traces_get` to fetch the full trace
4. Summarize findings — don't dump raw JSON

### When the user asks about system health

1. Use `logs_error_count` for backend service (last 5-10 minutes)
2. Use `traces_list` to see recent request flow
3. Report: "No errors in the last hour" or "Found X errors"

## Example LogsQL Queries

- `"error"` — all logs containing "error"
- `"_stream:{service=\"backend\"} AND level:error"` — backend errors only
- `"connection refused"` — logs with specific text
- `"500"` — logs with HTTP 500 status
- `"exception"` — exception stack traces

## Response Format

**For "What went wrong?":**
```
## Investigation Summary

**Error Count:** X errors in the last 5 minutes

**Log Evidence:**
- [Brief description of error pattern from logs]

**Trace Evidence:**
- [If trace found: describe failure point]

**Root Cause:** [Your conclusion]
```

**For health checks:**
```
## Health Check [timestamp]

**Status:** 🟢 Healthy / 🔴 Issues detected

**Errors:** X errors in last N minutes

**Details:** [Brief if errors found, otherwise "System running smoothly"]
```

## Important Rules

1. **Always check logs first** when debugging
2. **Use traces for context** — to see the full request flow
3. **Keep responses actionable** — what failed, where, why
4. **Don't overwhelm** — show top 5-10 errors, not all
5. **Extract trace IDs** from logs when available (look for hex patterns)
6. **Be concise** — summarize, don't dump raw data
