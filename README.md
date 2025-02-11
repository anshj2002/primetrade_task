A robust cryptocurrency market analysis tool that fetches real-time data from CoinMarketCap API, processes it, and generates comprehensive reports in multiple formats.

## ✨ Features

- 📊 Real-time cryptocurrency data fetching from CoinMarketCap
- 📈 Automated market analysis and reporting
- 💾 Data caching system for optimal API usage
- 📑 Multiple output formats (Excel, PDF)
- ☁️ Automatic Dropbox integration for file storage
- 🔄 Continuous updates every 5 minutes

## 🏗️ System Architecture

```
├── config.py              # Configuration and API settings
├── data_analyzer.py       # Data analysis logic
├── data_fetcher.py       # API interaction and data retrieval
└── python_script_for_dataFetch_analysis_and_update.py  # Main execution script
```

## 📋 Prerequisites

- Python 3.8 or higher
- CoinMarketCap API key
- Dropbox access token
- Required Python packages (see requirements.txt)

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/crypto-market-analytics.git
   cd crypto-market-analytics
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Add your API keys:
   ```env
   COIN_MARKET_CAP_API_KEY=your_api_key_here
   DROPBOX_ACCESS_TOKEN=your_dropbox_token_here
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the script**
   ```bash
   python python_script_for_dataFetch_analysis_and_update.py
   ```

## 📊 Generated Reports

The system automatically generates and uploads three types of reports to Dropbox:

1. **crypto_data.xlsx**
   - Raw cryptocurrency data
   - Current prices
   - Market caps
   - 24h volumes
   - Price changes

2. **crypto_analysis.xlsx**
   - Top 5 cryptocurrencies by market cap
   - Average price of top 50 cryptocurrencies
   - Highest and lowest 24h changes
   - Multiple sheets with detailed analysis

3. **crypto_analysis_report.pdf**
   - Professional PDF report
   - Visual representations
   - Key market insights
   - Timestamp of data collection

## 🔄 Update Frequency

- Data is fetched every 5 minutes
- Cache system prevents redundant API calls
- Timestamps are included in all reports

## 🛠️ Technical Details

- **Data Caching**: 5-minute cache to optimize API usage
- **Error Handling**: Robust error handling for API and file operations
- **File Management**: Automatic file overwrite in Dropbox
- **Report Generation**: Multiple formats with consistent timestamps

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- CoinMarketCap API for cryptocurrency data
- Dropbox API for cloud storage
- ReportLab for PDF generation
- Pandas for data analysis
