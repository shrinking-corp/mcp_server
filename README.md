# Shrinking Algorithm MCP Server

This repository contains an MCP server for shrinking PlantUML (`.puml`) diagrams. It exposes one MCP tool, `shrink_diagram`, which accepts PlantUML text and returns a transformed PlantUML diagram.

The tool supports three modes:

- `kruskals` - graph-based reduction, fast and deterministic
- `evol` - evolutionary optimization, slower but may produce better results
- `preprocess` - applies preprocessing steps without running a shrinking algorithm

The server is intended to be run as a Docker-backed local MCP server over stdio. This README includes setup instructions for OpenCode and Claude Desktop.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running, or another working Docker installation
- One of the following MCP clients:
  - [OpenCode](https://opencode.ai/)
  - [Claude Desktop](https://claude.ai/download)

---

## Build the Docker Image

Run the build command from this repository root, where `Dockerfile` is located.

**macOS / Linux:**

```bash
docker build -f Dockerfile -t shrinking-mcp-server .
```

**Windows (Command Prompt):**

```cmd
docker build -f Dockerfile -t shrinking-mcp-server .
```

**Windows (PowerShell):**

```powershell
docker build -f Dockerfile -t shrinking-mcp-server .
```

To verify the image was built successfully:

```bash
docker images | grep shrinking-mcp-server
```

On Windows, if `grep` is not available, check the image list manually:

```cmd
docker images
```

---

## Configure OpenCode

OpenCode reads project configuration from `opencode.json` in the repository root. This repository already includes the required configuration:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "diagram-shrinker": {
      "type": "local",
      "command": ["docker", "run", "--rm", "-i", "shrinking-mcp-server"]
    }
  }
}
```

The MCP server name is `diagram-shrinker`. OpenCode starts it by running the Docker image built above.

After building the image, start OpenCode from this repository so it can discover the project-level `opencode.json`.

---

## Configure Claude Desktop

Locate your Claude Desktop config file:

| Platform | Path |
| -------- | ---- |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

This repository includes `claude_desktop_config.json` with the server entry you need:

```json
{
  "mcpServers": {
    "diagram-shrinker": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "shrinking-mcp-server"]
    }
  }
}
```

If your Claude Desktop config already has other servers under `mcpServers`, add the `diagram-shrinker` entry alongside them instead of replacing the whole file.

After updating the config, fully quit and reopen Claude Desktop:

- **macOS:** `Cmd+Q`, then reopen
- **Windows / Linux:** close Claude Desktop from the system tray, then reopen

After restarting, the `shrink_diagram` tool should be available.

---

## Usage

Paste the contents of a `.puml` file into your MCP client and ask it to use the tool. For example:

> Use the `shrink_diagram` tool on this PlantUML diagram with the `kruskals` algorithm.

The tool expects:

- `puml_string` - the full PlantUML diagram text
- `algorithm` - one of `kruskals`, `evol`, or `preprocess`
- `preprocess_steps` - optional list of preprocessing steps
- `algorithm_config` - optional configuration for `kruskals` or `evol`

Supported preprocessing steps are:

- `remove_empty_classes`
- `remove_isolated_classes`
- `remove_leaf_classes`
- `remove_low_degree_classes`
- `remove_random_classes`
- `remove_getters_and_setters`
- `remove_public_methods`
- `remove_private_methods`
- `remove_protected_methods`
- `remove_package_methods`
- `remove_random_methods`
- `remove_public_attributes`
- `remove_private_attributes`
- `remove_protected_attributes`
- `remove_package_attributes`
- `remove_random_attributes`
- `remove_random_edges`

---

## Troubleshooting

**Tool not appearing:**

- Make sure Docker is running
- Verify the image exists: `docker images | grep shrinking-mcp-server`
- Make sure your MCP client config uses `shrinking-mcp-server`
- Make sure the Docker image was built after the latest code changes
- Check for JSON syntax errors in `opencode.json` or `claude_desktop_config.json`

**Testing the container directly:**

```bash
docker run --rm -i shrinking-mcp-server
```

This starts the MCP server over stdio. It will wait for MCP client messages, so no normal command-line output is expected.

**OpenCode logs:**

OpenCode writes logs to:

| Platform | Path |
| -------- | ---- |
| macOS / Linux | `~/.local/share/opencode/log/` |
| Windows | `%USERPROFILE%\.local\share\opencode\log` |

Log files are named with timestamps, and OpenCode keeps the most recent 10 log files. To get more detail while debugging MCP startup issues, run OpenCode with debug logging:

```bash
opencode --log-level DEBUG
```

To print logs directly in the terminal while OpenCode is running:

```bash
opencode --print-logs
```

**Claude Desktop logs:**

Claude Desktop writes MCP server logs under the Claude logs directory. The exact log file name may vary by platform and Claude Desktop version, but it usually includes the MCP server name, `diagram-shrinker`.
