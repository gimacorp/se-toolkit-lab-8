#!/usr/bin/env python3
"""Resolve environment variables into nanobot config and start the gateway."""

import json
import os
import tempfile
from pathlib import Path


def main():
    config_path = Path("/app/nanobot/config.json")
    workspace_path = Path("/app/nanobot/workspace")

    # Load base config
    with open(config_path) as f:
        config = json.load(f)

    # Resolve LLM provider (custom = Qwen Code API)
    if "providers" in config and "custom" in config["providers"]:
        api_key = os.environ.get("QWEN_CODE_API_KEY", "").strip()
        api_base = os.environ.get("LLM_API_BASE_URL", "http://localhost:42005/v1").strip()
        if api_key:
            config["providers"]["custom"]["apiKey"] = api_key
        if api_base:
            config["providers"]["custom"]["apiBase"] = api_base

    # Resolve gateway host/port
    gateway_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "18790")

    # Resolve webchat host/port
    webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765")

    # Resolve MCP server env vars
    if "tools" in config and "mcpServers" in config["tools"]:
        if "lms" in config["tools"]["mcpServers"]:
            backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL", "").strip()
            backend_key = os.environ.get("NANOBOT_LMS_API_KEY", "").strip()
            victorialogs_url = os.environ.get("VICTORIALOGS_URL", "").strip()
            victoriatraces_url = os.environ.get("VICTORIATRACES_URL", "").strip()
            if backend_url:
                config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = backend_url
            if backend_key:
                config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = backend_key
            if victorialogs_url:
                config["tools"]["mcpServers"]["lms"]["env"]["VICTORIALOGS_URL"] = victorialogs_url
            if victoriatraces_url:
                config["tools"]["mcpServers"]["lms"]["env"]["VICTORIATRACES_URL"] = victoriatraces_url

    # Write resolved config to temp directory (writable by nonroot)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config, f, indent=2)
        resolved_path = f.name

    # Start nanobot gateway
    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--config",
            resolved_path,
            "--workspace",
            str(workspace_path),
        ],
    )


if __name__ == "__main__":
    main()
