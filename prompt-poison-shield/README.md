# Prompt Poison Shield

A browser extension that protects you from accidentally sharing sensitive data with Large Language Models (LLMs).

## Features

- **Real-time scanning**: Detects sensitive data as you type
- **Comprehensive detection**: API keys, passwords, PII, financial data, and more
- **Non-intrusive warnings**: Clear alerts that let you proceed or cancel
- **Privacy-focused**: All scanning happens locally in your browser
- **LLM-optimized**: Designed specifically for ChatGPT, Claude, Gemini, and other LLM interfaces

## Installation

1. Download all extension files
2. Create an \`icons/\` folder with three PNG icons:
   - \`icon16.png\` (16x16 pixels)
   - \`icon48.png\` (48x48 pixels)
   - \`icon128.png\` (128x128 pixels)
3. Open Chrome and go to \`chrome://extensions/\`
4. Enable "Developer mode"
5. Click "Load unpacked" and select your extension folder

## Supported Sites

- ChatGPT (chat.openai.com)
- Claude (claude.ai)
- Google Gemini (gemini.google.com)
- Perplexity (perplexity.ai)
- Poe (poe.com)

## Development

This is the MVP version. Future versions will include:
- User-configurable rules
- Whitelisting capabilities
- Team-based rule management
- Advanced ML-based detection

## Privacy

All data processing happens locally in your browser. No information is sent to external servers.

## License

MIT License - See LICENSE file for details
