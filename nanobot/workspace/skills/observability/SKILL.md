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

### When the user asks about errors

1. **First**, use `logs_error_count` to check if there are errors
2. **If errors found**, use `logs_search` with query `"error"` to see details
3. **If you find a trace ID** in the logs, use `traces_get` to fetch the full trace
4. **Summarize findings** — don't dump raw JSON

### When the user asks "What went wrong?"

1. Use `logs_search` with query `"error"` or `"exception"`
2. Look for patterns: which service, which operation
3. If you find trace IDs, fetch them with `traces_get`
4. Explain the root cause clearly

### When the user asks about system health

1. Use `logs_error_count` for backend service
2. Use `traces_list` to see recent request flow
3. Report: "No errors in the last hour" or "Found X errors"

## Example LogsQL Queries

- `"error"` — all logs containing "error"
- `"_stream:{service=\"backend\"} AND level:error"` — backend errors only
- `"connection refused"` — logs with specific text
- `"500"` — logs with HTTP 500 status

## Response Format

- **Concise summary first**: "Found 3 errors in the backend in the last hour"
- **Key details**: Which operation failed, error message
- **Trace info if available**: "Trace shows failure in db_query step"
- **No raw JSON dumps** — summarize in plain English

## Important Rules

1. **Always check logs first** when debugging
2. **Use traces for context** — to see the full request flow
3. **Keep responses actionable** — what failed, where, why
4. **Don't overwhelm** — show top 5-10 errors, not all
