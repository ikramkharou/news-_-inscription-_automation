# Newsletter Discovery and Subscription Automation System

A comprehensive Python-based system that automatically discovers websites worldwide, identifies newsletter signup forms using AI-powered detection, and manages email subscriptions to newsletters.

## 🌟 Features

- **Global Website Discovery**: Automatically discovers websites using search engines, domain lists, and various discovery methods
- **AI-Powered Newsletter Detection**: Uses pattern matching and machine learning to identify newsletter signup forms
- **Automated Subscription Management**: Automatically subscribes to discovered newsletters with rate limiting and stealth techniques
- **Web-Based Interface**: Beautiful, responsive web interface for managing the entire system
- **Database Tracking**: SQLite database to track discovered websites, forms, and subscription status
- **Rate Limiting & Ethics**: Built-in rate limiting and ethical scraping practices
- **Real-time Statistics**: Live dashboard with statistics and progress tracking

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd News_inscrip

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```env
# Optional: API keys for enhanced search capabilities
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_google_cse_id
BING_API_KEY=your_bing_api_key

# Email configuration
TEST_EMAIL=your@email.com
```

### 3. Run the System

#### Option A: Web Interface (Recommended)
```bash
python web_interface.py
```
Then open your browser to: `http://localhost:5000`

#### Option B: Command Line Interface
```bash
# Run full pipeline (discover + scan + subscribe)
python main.py --full --email your@email.com

# Or run individual steps
python main.py --discover          # Discover websites
python main.py --scan             # Scan for newsletter forms
python main.py --subscribe --email your@email.com  # Subscribe to newsletters
python main.py --stats            # Show statistics
```

## 📁 Project Structure

```
News_inscrip/
├── main.py                 # Main orchestrator script
├── web_interface.py        # Flask web application
├── web_discovery.py        # Website discovery engine
├── newsletter_detector.py  # Newsletter form detection
├── email_automation.py     # Email subscription automation
├── database.py             # Database management
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── discover.html
│   ├── scan.html
│   ├── subscribe.html
│   ├── forms.html
│   └── websites.html
├── static/                 # Static assets
│   ├── css/style.css
│   └── js/main.js
└── README.md
```

## 🎯 Usage Examples

### Web Interface

1. **Dashboard**: View overall statistics and run the full pipeline
2. **Discover**: Start website discovery with customizable parameters
3. **Scan**: Analyze discovered websites for newsletter forms
4. **Subscribe**: Subscribe to found newsletters with your email
5. **Forms**: Browse and manage discovered newsletter forms
6. **Websites**: View all discovered websites

### Command Line

```bash
# Discover 2000 websites
python main.py --discover --max-websites 2000

# Scan 100 websites for newsletters
python main.py --scan --max-websites 100

# Subscribe to 25 newsletters
python main.py --subscribe --email user@example.com --max-subscriptions 25

# Run full pipeline with custom limits
python main.py --full --email user@example.com --max-websites 1500 --max-subscriptions 30
```

## 🔧 Configuration Options

Edit `config.py` to customize:

- **Discovery Settings**: Maximum websites, request delays, concurrent requests
- **Detection Settings**: Newsletter keywords, form patterns, confidence thresholds
- **Email Settings**: Test email, subscription limits
- **Rate Limiting**: Requests per hour/day, delays between requests
- **Database**: SQLite database path and settings

## 🛡️ Safety Features

- **Rate Limiting**: Built-in delays and request limits
- **Stealth Mode**: Undetected ChromeDriver for form submissions
- **Error Handling**: Comprehensive error handling and logging
- **Duplicate Prevention**: Avoids duplicate subscriptions
- **User Agent Rotation**: Rotates user agents for better stealth
- **Respectful Scraping**: Follows robots.txt and implements delays

## 📊 Database Schema

The system uses SQLite with the following tables:

- **websites**: Discovered websites with metadata
- **newsletter_forms**: Detected newsletter forms with confidence scores
- **subscriptions**: Email subscription records and status
- **search_results**: Search engine query results

## 🔍 Newsletter Detection

The system uses multiple methods to detect newsletter forms:

1. **HTML Structure Analysis**: Analyzes form elements and attributes
2. **Keyword Matching**: Searches for newsletter-related keywords
3. **Input Field Detection**: Identifies email input fields
4. **Submit Button Analysis**: Analyzes button text and attributes
5. **Form Action URL Analysis**: Checks form submission URLs
6. **Confidence Scoring**: Assigns confidence scores to detected forms

## 🚨 Important Notes

### Legal and Ethical Considerations

- **Respect robots.txt**: The system respects website robots.txt files
- **Rate Limiting**: Built-in delays prevent overwhelming servers
- **Terms of Service**: Always check and respect website terms of service
- **Email Compliance**: Ensure compliance with anti-spam laws (CAN-SPAM, GDPR)
- **Personal Use**: This tool is intended for personal newsletter subscriptions only

### Technical Limitations

- Some websites use complex JavaScript forms that may not be detected
- CAPTCHA-protected forms cannot be automated
- Email verification may be required for some subscriptions
- Some websites may block automated submissions

## 🐛 Troubleshooting

### Common Issues

1. **Chrome Driver Issues**: Install ChromeDriver or use `webdriver-manager`
2. **Rate Limiting**: Increase delays in `config.py` if getting blocked
3. **Database Errors**: Ensure SQLite is properly installed
4. **Form Detection**: Lower confidence threshold in `config.py`

### Debug Mode

Run with verbose logging:
```bash
python main.py --verbose --discover
```

## 📈 Performance Tips

- Start with smaller numbers (100-500 websites) for testing
- Use the web interface for better monitoring
- Monitor the logs for errors and adjust settings accordingly
- Consider running discovery and scanning separately for better control

## 🤝 Contributing

This is a demonstration project. For production use, consider:

- Adding proper error recovery mechanisms
- Implementing more sophisticated form detection
- Adding support for more email providers
- Enhancing the web interface with more features
- Adding comprehensive testing

## ⚖️ Disclaimer

This tool is for educational and personal use only. Users are responsible for:

- Complying with all applicable laws and regulations
- Respecting website terms of service
- Following anti-spam legislation
- Using the tool ethically and responsibly

The developers are not responsible for any misuse of this tool.

## 📞 Support

For issues or questions:

1. Check the troubleshooting section
2. Review the logs for error messages
3. Adjust configuration settings as needed
4. Ensure all dependencies are properly installed

---

**Happy Newsletter Discovery! 📧✨**
