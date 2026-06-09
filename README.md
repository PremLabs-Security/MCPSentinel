# MCPSentinel

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License MIT"/>
  <img src="https://img.shields.io/badge/Security-Tool-red?style=for-the-badge" alt="Security Tool"/>
  <img src="https://github.com/PremLabs-Security/MCPSentinel/actions/workflows/ci.yml/badge.svg" alt="CI/CD"/>
</p>

**MCPSentinel** is a specialized security reconnaissance tool designed to detect exposed and unauthenticated Model Context Protocol (MCP) endpoints, Ollama servers, and common LLM proxies.

## 🛡️ Features

- **MCP Detection**: Scans for common MCP endpoints and validates protocol responses.
- **Ollama Scanner**: Identifies exposed Ollama instances and lists available models.
- **LLM Proxy Identification**: Detects LiteLLM, vLLM, and other OpenAI-compatible proxies.
- **Asynchronous Scanning**: High-performance scanning using `aiohttp` and `asyncio`.
- **Flexible Reporting**: Terminal-based tables and JSON export support.

## 🚀 Installation

```bash
git clone https://github.com/PremLabs-Security/MCPSentinel.git
cd MCPSentinel
pip install -e .
```

## 📖 Usage

### CLI Usage

Scan a single target:
```bash
mcpsentinel --target http://localhost:11434
```

Scan multiple targets from a file:
```bash
mcpsentinel --file targets.txt --output results.json
```

### Python API

```python
import asyncio
from mcpsentinel.scanner import Scanner

async def run_scan():
    scanner = Scanner()
    results = await scanner.scan_target("http://localhost:11434")
    print(results)

asyncio.run(run_scan())
```

## ⚠️ Ethical Use Disclaimer

This tool is intended for authorized security testing and research purposes only. Unauthorized scanning of systems you do not own or have explicit permission to test may be illegal. The authors are not responsible for any misuse of this tool.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Developed by [Pramod Jogdand](https://github.com/Prem2868) | [PremLabs-Security](https://github.com/PremLabs-Security)**
