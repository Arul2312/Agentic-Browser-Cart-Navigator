# Agentic Browser Cart Navigator

An agentic AI system for autonomous Amazon shopping cart navigation and analysis. Uses OpenAI GPT-4o-mini with browser-use technology to analyze cart contents, compare against spending thresholds, and make intelligent checkout decisions.

## Features

- **Agentic AI Mode**: Autonomous Amazon cart navigation using OpenAI GPT-4o-mini
- **Manual Mode**: Human-guided navigation with AI-assisted analysis
- **Threshold Enforcement**: Configurable spending limits with conditional checkout
- **Cart Analysis**: Real-time extraction of Amazon cart contents and pricing

## Project Structure

```
Agentic-Browser-Cart-Navigator/
├── config/
│   ├── site_config.yaml        # Main configuration
│   └── settings.py             # Config loader
├── src/
│   ├── agents/
│   │   ├── agent_factory.py    # Agent creation
│   │   ├── base_agent.py       # Base agent class
│   │   ├── browser_use_agent.py # AI agent
│   │   └── manual_agent.py     # Manual agent
│   ├── core/
│   │   ├── models.py           # Data models
│   │   └── page_graph.py       # Navigation graph
│   ├── extractors/             # Data extraction
│   └── utils/                  # Utilities
├── main.py                     # Application entry point
├── requirements.txt            # Dependencies
└── README.md
```

## Installation

1. **Clone repository:**
   ```bash
   git clone https://github.com/yourusername/Agentic-Browser-Cart-Navigator.git
   cd Agentic-Browser-Cart-Navigator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

3. **Set OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

## Usage

### Agentic AI Mode (Default)
```bash
python main.py
```

### Manual Mode
1. Edit `config/site_config.yaml`:
   ```yaml
   agent_mode: "manual"
   ```
2. Run:
   ```bash
   python main.py
   ```

### Configuration
Edit `config/site_config.yaml`:
```yaml
agent_mode: "browser_use"    # "browser_use" or "manual"
price_threshold: 100.0       # Spending limit in USD
llm_provider: "openai"       # AI provider
```
