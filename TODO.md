# mcpie Roadmap & TODO

Inspired by HTTPie CLI features, focusing on 80-20 principle: 20% of functionality for 80% of value.

## 🎯 Phase 1: High-Impact Core Features (Immediate)

### Server Profiles & Configuration Management
- [ ] `mcpie profile save <name> <cmd_or_url>` - Save server configurations
- [ ] `mcpie profile list` - List saved profiles  
- [ ] `mcpie profile remove <name>` - Remove profiles
- [ ] `mcpie <profile_name> -- <commands>` - Use saved profiles
- [ ] Support headers/auth in profiles: `mcpie profile save api "http://api.com" -H "Auth:token"`
- [ ] Profile storage in `~/.mcpie/profiles.json`

### Enhanced Output Formatting & Filtering  
- [ ] `--format json|table|yaml` - Multiple output formats
- [ ] `--quiet` flag - Minimal output for scripting
- [ ] JSON filtering with JSONPath or jq integration
- [ ] Table formatting for list commands
- [ ] Clean vs rich output modes

### Request Validation & Dry-Run Mode
- [ ] `--dry-run` flag - Show what would be executed without running
- [ ] `--debug` flag - Show full MCP request/response details
- [ ] `--verbose` improvements - More detailed connection info
- [ ] Request validation before sending
- [ ] Better error messages with suggestions

## 🚀 Phase 2: Workflow Integration (Medium Priority)

### Session Persistence & Reuse
- [ ] `--session <name>` flag - Named session management
- [ ] `mcpie session list` - List active sessions
- [ ] `mcpie session clear <name>` - Clear specific session
- [ ] Session storage and reuse across commands
- [ ] Session timeout and cleanup

### Authentication Templates
- [ ] `--auth bearer:<token>` - Bearer token auth
- [ ] `--auth oauth2` - OAuth2 flow support
- [ ] `--auth basic:<user:pass>` - Basic auth
- [ ] Auth profiles in server configurations
- [ ] Environment variable integration for secrets

### File I/O Operations
- [ ] `--output <file>` - Export responses to files
- [ ] `--input <file>` - Import arguments from JSON/YAML files
- [ ] Bulk operations support
- [ ] Response caching options

## 🛠 Phase 3: Power User Features (Advanced)

### Command History & Replay
- [ ] Command history storage
- [ ] `mcpie history` - Show command history
- [ ] `mcpie history replay <n>` - Re-run nth command
- [ ] `--save <name>` - Save command sequences
- [ ] `mcpie run <saved_name>` - Execute saved command sequences

### Basic Plugin System
- [ ] Plugin architecture design
- [ ] Output formatter plugins
- [ ] Transport plugins (WebSocket, etc.)
- [ ] `mcpie install <plugin>` - Plugin installation
- [ ] Plugin discovery and management

### Advanced MCP Features
- [ ] Multi-server workflows
- [ ] Server health monitoring
- [ ] Connection pooling for HTTP servers
- [ ] Streaming response handling
- [ ] Resource subscription support

## 🎨 UI/UX Improvements

### HTTPie-Inspired Interface
- [ ] Consistent flag naming across commands
- [ ] Smart argument parsing and inference
- [ ] Colorized output improvements
- [ ] Progress indicators for long operations
- [ ] Intuitive error messages

### MCP-Specific Enhancements
- [ ] Schema-aware tab completion
- [ ] Multi-command workflow support
- [ ] Rich MCP protocol debugging
- [ ] Server capability discovery and caching

## 🔧 Technical Improvements

### Code Quality & Performance
- [ ] Comprehensive test suite
- [ ] Performance benchmarking
- [ ] Memory usage optimization
- [ ] Async operation improvements
- [ ] Configuration validation

### Developer Experience
- [ ] Plugin API documentation
- [ ] Development setup automation
- [ ] CI/CD improvements
- [ ] Release automation

## 📝 Documentation & Examples

- [ ] Comprehensive usage examples
- [ ] Server profile cookbook
- [ ] Integration guides (CI/CD, scripting)
- [ ] Troubleshooting guide
- [ ] Plugin development guide

---

## Implementation Notes

**Design Principles:**
- Maintain HTTPie-style simplicity and intuitiveness
- Graceful fallbacks and smart defaults
- Excellent error messages with actionable suggestions
- Consistent flag naming and behavior
- Focus on MCP-specific value-adds over generic HTTP features

**Target Users:**
- MCP server developers (testing, debugging)
- AI application developers (integration, workflows)  
- System administrators (monitoring, automation)
- Power users (scripting, bulk operations)
