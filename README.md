# Agentic Browser Cart Navigator 🤖🛒

An advanced agentic AI system specifically designed for autonomous Amazon shopping cart navigation using intelligent browser agents. Powered by OpenAI GPT-4o-mini and browser-use technology for smart Amazon e-commerce automation.

## ✨ Features

- **🤖 Agentic AI Navigation**: Autonomous Amazon cart navigation powered by OpenAI GPT-4o-mini
- **🌐 Browser-Use Integration**: Advanced browser automation specialized for Amazon cart workflows
- **👤 Manual Agent Mode**: Human-guided Amazon cart navigation with AI-assisted analysis
- **💰 Amazon-Specific Threshold Logic**: Smart spending limit enforcement for Amazon purchases
- **📋 Dynamic Amazon Cart Analysis**: Real-time extraction of Amazon cart contents and pricing
- **🧠 Context-Aware Amazon Navigation**: AI agents understand Amazon cart state and checkout flow
- **🔐 Amazon Authentication Handling**: Manages Amazon sign-in flows automatically
- **⚙️ Multi-Agent Amazon Architecture**: Modular design optimized for Amazon cart operations

## 🎯 Amazon Cart Use Case

This system is **specifically constrained to Amazon cart navigation** and includes:

- ✅ **Amazon Cart Analysis**: Extract items, prices, and totals from Amazon shopping carts
- ✅ **Amazon Checkout Logic**: Navigate Amazon's checkout process with threshold controls
- ✅ **Amazon Sign-in Handling**: Manage Amazon authentication requirements
- ✅ **Amazon Page Navigation**: Specialized selectors and logic for Amazon.com
- ✅ **Amazon Cart Threshold Enforcement**: Prevent overspending on Amazon purchases

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key (for agentic AI mode)
- Chrome/Chromium browser
- Access to Amazon.com

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Agentic-Browser-Cart-Navigator.git
   cd Agentic-Browser-Cart-Navigator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install browser binaries:**
   ```bash
   playwright install chromium
   ```

4. **Set up OpenAI API key (for agentic mode):**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

5. **Configure Amazon-specific settings:**
   Edit `config/site_config.yaml` to customize Amazon cart behavior

### Basic Usage

#### 🤖 Agentic AI Mode (Default)
```bash
python main.py
```
*AI agent will automatically navigate to Amazon, analyze your cart, and make checkout decisions*

#### 👤 Manual Agent Mode
1. Change `agent_mode` to `"manual"` in `config/site_config.yaml`
2. Run:
   ```bash
   python main.py
   ```
*Browser opens Amazon for manual navigation with AI-assisted cart analysis*

## 🧠 Amazon-Specialized Agent Architecture

### 🤖 Browser Use Agent (Amazon AI Navigation)
- **Amazon-Aware Navigation**: AI agent specifically trained for Amazon.com layouts
- **Cart-Focused Processing**: Understands Amazon cart structure and checkout flow
- **Amazon Element Recognition**: Recognizes Amazon-specific buttons, forms, and content
- **Dynamic Amazon Handling**: Adapts to Amazon's changing page layouts
- **Amazon Error Recovery**: Handles Amazon-specific errors and edge cases

### 👤 Manual Browser Agent (Amazon-Guided)
- **Amazon Cart Assistance**: Provides intelligent guidance during Amazon navigation
- **Real-time Amazon Analysis**: Live analysis of Amazon cart contents
- **Amazon Sign-in Support**: Helps with Amazon authentication when needed
- **Amazon-Specific Fallback**: Available when Amazon automation encounters issues

## ⚙️ Amazon Configuration

Edit `config/site_config.yaml`:

```yaml
# ============================================
# AMAZON CART SETTINGS
# ============================================
amazon:
  base_url: "https://amazon.com"

# Agent mode for Amazon navigation
agent_mode: "browser_use"  # Options: "browser_use" or "manual"
price_threshold: 100.0     # Amazon spending limit

# ============================================
# AGENTIC AI FOR AMAZON
# ============================================
openai:
  model: "gpt-4o-mini"
  temperature: 0.1
  max_tokens: 500

browser_use:
  max_actions: 20
  safety_mode: true
```

## 📊 Amazon Cart Analysis Outputs

### Agentic AI Mode (Amazon Automation)
```
🤖 Amazon Cart Analysis Completed
   Automated Amazon navigation using openai with $100.00 threshold

🛒 AMAZON CART CONTENTS
============================================================
   📋 Items Found: 3
   💰 Cart Total: $85.99

   📦 Amazon Items:
      1. Echo Dot (4th Gen)
      2. Fire TV Stick
      3. Kindle Paperwhite

   🎯 Amazon Threshold: $100.00
   📊 Status: ✅ BELOW THRESHOLD ($85.99 < $100.00)
   🚦 Action: ✅ ELIGIBLE FOR AMAZON CHECKOUT
   💡 Recommendation: You can proceed with Amazon purchase
============================================================

🤖 AI Agent: Proceeded to Amazon checkout and stopped at payment info
✅ Amazon Logic: Agent correctly followed threshold rules
```

## 🔧 Amazon-Specific Capabilities

### 🧠 Amazon Intelligence
- **Amazon Layout Understanding**: Recognizes Amazon cart, checkout, and navigation elements
- **Amazon Price Extraction**: Specialized parsing for Amazon pricing formats
- **Amazon Cart State**: Understands empty carts, item quantities, and subtotals
- **Amazon Checkout Flow**: Navigates Amazon's multi-step checkout process

### 🎯 Amazon Decision Logic
```python
# Amazon-Optimized AI Prompt
task = f"Go to Amazon.com. Click cart. List Amazon items and total. 
         If below ${threshold}, proceed to Amazon checkout until personal info. 
         If above ${threshold}, do not proceed with Amazon checkout."
```

### 🛒 Amazon Workflow

1. **Amazon Navigation**: AI agent goes to Amazon.com
2. **Amazon Cart Access**: Clicks Amazon cart icon or navigates to cart URL
3. **Amazon Authentication**: Handles Amazon sign-in if required
4. **Amazon Cart Analysis**: Extracts Amazon item names and cart total
5. **Amazon Threshold Check**: Compares total against spending limit
6. **Amazon Checkout Decision**: Proceeds or stops based on threshold
7. **Amazon Result Report**: Provides Amazon-specific recommendations

## 🛡️ Amazon Safety Features

- **Amazon Spending Control**: Never exceeds limits on Amazon purchases
- **Amazon Checkout Protection**: Stops before payment information entry
- **Amazon Session Management**: Proper handling of Amazon browser sessions
- **Amazon Error Handling**: Graceful recovery from Amazon-specific issues

## 🚀 Amazon Use Cases

### 💼 Amazon Budget Management
- **Amazon Cart Monitoring**: Track Amazon spending against budgets
- **Amazon Purchase Control**: Prevent Amazon overspending automatically
- **Amazon Cart Optimization**: AI-assisted Amazon purchase decisions

### 🧪 Amazon Automation Research
- **Amazon Agent Behavior**: Study AI navigation of Amazon interfaces
- **Amazon E-commerce Patterns**: Analyze Amazon user interaction flows
- **Amazon AI Integration**: Template for Amazon-specific automation

## ⚠️ Amazon-Specific Considerations

This system is designed exclusively for Amazon.com and includes:

- **Amazon Terms Compliance**: Respects Amazon's robots.txt and usage policies
- **Amazon Rate Limiting**: Implements appropriate delays for Amazon requests
- **Amazon Session Handling**: Manages Amazon login states properly
- **Amazon Regional Support**: Works with different Amazon country domains

## 🔒 Amazon Privacy & Security

- **Amazon Cart Privacy**: Cart contents analyzed locally, never stored
- **Amazon Credentials**: No storage of Amazon login information
- **Amazon Session Isolation**: Clean Amazon session for each run
- **Amazon Data Protection**: Complies with Amazon's data handling requirements

## 🛠️ Amazon Troubleshooting

### Amazon Navigation Issues

**Amazon Sign-in Required:**
- Manual mode: Sign in when prompted and press Enter
- Agentic mode: Agent will detect and handle appropriately

**Amazon Cart Not Loading:**
- Check connection to Amazon.com
- Verify Amazon accessibility in your region
- Try clearing browser cache for Amazon

**Amazon Element Detection Failed:**
- Amazon may have updated their layout
- Switch to manual mode for immediate use
- Report issue for Amazon selector updates

## 🤝 Contributing to Amazon Features

Help improve Amazon cart navigation capabilities:

1. Fork for Amazon-specific enhancements
2. Test changes against Amazon.com layouts
3. Ensure Amazon terms compliance
4. Submit Amazon-focused improvements

## 📄 License

MIT License - enables development of Amazon automation tools for personal use.

## ⚠️ Amazon Responsible Use

This tool is specifically for Amazon cart analysis and should be used:
- ✅ For personal Amazon budget management
- ✅ For Amazon purchase decision assistance
- ✅ In compliance with Amazon's terms of service
- ❌ Not for Amazon data scraping or commercial use

---

**🛒 Specialized for Amazon • 🤖 Powered by Agentic AI • 🌐 Enhanced with Browser-Use**
