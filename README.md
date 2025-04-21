# MCP PanDA Analyzer

A tool for analyzing PanDA grid job failures using LLMs with Model Context Protocol (MCP).

WARNING: This is a work in progress and not yet ready for production use. 
The code is currently in a state of flux and may change significantly in the future.

## Features

- Analyze PanDA grid job logs for failure causes
- Support for multiple LLM backends (Claude, Llama, OpenAI)
- Both client and server components
- RAG-based processing for large log files
- Simple CLI interface (for now)

## Installation

### From GitHub

```bash
pip install git+https://github.com/yourusername/mcp-panda-analyzer.git
```

### With specific LLM support

```bash
# For Claude support
pip install "mcp-panda-analyzer[claude] @ git+https://github.com/yourusername/mcp-panda-analyzer.git"

# For Llama support
pip install "mcp-panda-analyzer[llama] @ git+https://github.com/yourusername/mcp-panda-analyzer.git"

# For OpenAI support
pip install "mcp-panda-analyzer[openai] @ git+https://github.com/yourusername/mcp-panda-analyzer.git"

# For all LLM backends
pip install "mcp-panda-analyzer[all] @ git+https://github.com/yourusername/mcp-panda-analyzer.git"
```

## Usage

### Running the Server

```bash
# Start the server with default settings
mcp-server --port 8000

# Use a specific LLM backend
mcp-server --port 8000 --llm openai
```

### Using the Client

```bash
# Analyze a job with default settings
mcp-agent --job-id 6610588906

# Specify LLM to use
mcp-agent --job-id 6610588906 --llm llama

# Connect to a remote server
mcp-agent --job-id 6610588906 --server http://remote-server:8000
```

## Environment Variables

Configure the LLM backends using environment variables:

- **Claude**: `ANTHROPIC_API_KEY`
- **OpenAI**: `OPENAI_API_KEY`
- **Llama**: `LLAMA_MODEL_PATH`, `LLAMA_CTX_LEN`, `LLAMA_GPU_LAYERS`

## Documentation

For more examples and advanced usage, see the [documentation](docs/README.md).

## License

Apache License 2.0
```