# 🎯 TikTok Video Virality Analysis

An AI-powered pipeline for analyzing TikTok videos using Google's Gemini to assess viral potential and provide actionable insights.

## 🌟 Overview

This project helps content creators and marketers understand what makes TikTok videos go viral. Using Google's Gemini AI, it analyzes various aspects of videos to provide detailed insights and recommendations.

### Key Features

- 🎥 **Comprehensive Video Analysis**

  - Visual elements (text, transitions, style)
  - Content structure (hook, flow, CTA)
  - Engagement factors
  - Technical elements
  - Trend alignment

- 🤖 **Advanced AI Integration**

  - Powered by Google's Gemini
  - Natural language insights
  - Actionable recommendations

- 📊 **Data Processing**
  - Batch processing
  - Quality metrics
  - Detailed logging

## 📚 Documentation

- [Getting Started Guide](docs/getting_started.md) - Setup and basic usage
- [Project Structure](docs/project_structure.md) - Codebase organization
- [Technical Documentation](docs/) - Detailed technical docs

## 🏗️ Architecture

```
virality-chat-poc/
├── src/                  # Source code
├── tests/               # Test suite
├── scripts/             # Utility scripts
├── data/                # Data storage
├── docs/                # Documentation
└── logs/                # Log files
```

See [Project Structure](docs/project_structure.md) for detailed organization.

## 🚀 Quick Start

1. **Prerequisites**

   - Python 3.9+
   - Google Gemini API key
   - Apify account (for TikTok scraping)

2. **Installation**

   ```bash
   python scripts/setup_project.py
   ```

3. **Basic Usage**
   ```bash
   python scripts/run_pipeline.py --mode all
   ```

See [Getting Started Guide](docs/getting_started.md) for detailed instructions.

## 🔧 Development

### Testing

```bash
pytest
```

### Code Quality

```bash
black src/ tests/ scripts/
flake8 src/ tests/ scripts/
```

See [Getting Started Guide](docs/getting_started.md#development-commands) for more commands.

## 📈 Project Status

Current version: 0.1.0

- ✅ Core analysis pipeline
- ✅ Gemini AI integration
- ✅ Data processing
- ✅ Basic UI
- 🚧 Advanced analytics (in progress)
- 🚧 Trend detection (planned)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

See [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini team for the AI capabilities
- TikTok for the platform
- Open source community

## 📞 Support

- Check [Troubleshooting Guide](docs/getting_started.md#troubleshooting)
- Open an issue
- See documentation
