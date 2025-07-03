# mcpie - MCP Client for Humans

Interactive command-line tool for MCP (Model Context Protocol) servers with short commands and rich output.

Like **httpie** for HTTP, but for MCP servers! 🥧

## Features

- Interactive REPL with tab completion and command history
- Short aliases: `ls`, `r list`, `t call add 5 3`, `p get name`
- Rich tables and syntax-highlighted JSON output
- Both STDIO and SSE transport support
- Smart argument parsing (JSON, key=value, or interactive prompting)

## Installation

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) then:

```bash
uv sync
```

```bash
uv tool install .
```

From pypi:

```bash
uv tool install mcpie-cli
```

```bash
uvx mcpie-cli
```

## Quick Start

```bash
# Start interactive client
mcpie "python server.py"           # STDIO transport
mcpie "http://localhost:8000"      # SSE transport

# Inside the REPL
mcp> discover                     # See everything available
mcp> ls                          # List resources
mcp> t call add 5 3              # Call tool with smart parsing
mcp> r read config://app         # Read resource
mcp> help                        # Show all commands
```

## Commands

**Discovery:**
- `discover` - Show all capabilities
- `ls` - List resources (alias for `r list`)

**Resources:** `r list`, `r read <uri>`, `r templates`
**Tools:** `t list`, `t call <name> [args]`, `t inspect <name>`
**Prompts:** `p list`, `p get <name> [args]`, `p inspect <name>`
**Server:** `s info`, `s ping`, `s capabilities`

## Examples

```bash
# Different argument formats
t call add 5 3                        # Auto-mapped to parameters
t call add '{"a": 5, "b": 3}'         # JSON format
t call add                             # Interactive prompting

# With headers/env vars
mcpie -H "Authorization:token" http://localhost:8000
mcpie -e "API_KEY:secret" "python server.py"
```

That's it! Type `help` in the REPL for more details.
