# Stock Broker Scraper & Dashboard

這是一個自動化的股票券商進出明細爬蟲系統。
**🔗 [點此查看即時看板 (Streamlit)](https://stocktool-forfamilyuse.streamlit.app/)**

透過 GitHub Actions 定時爬取券商公開資料，並透過 Streamlit 提供數據看板，方便監控特定券商的進出流向。

## Tech Stack

* **Language**: Python 3.13
* **Scraping**: `BeautifulSoup4`, `requests`
* **Data Processing**: `Pandas`
* **Dashboard**: `Streamlit`
* **Automation**: `GitHub Actions` (Scheduled at 18:30 TW daily)

## Project Structure

```text
├── .github/workflows/    # CI/CD 設定 (自動化爬蟲)
├── data/                 # 存放爬蟲產出的 CSV
├── app.py                # Streamlit 前端網頁
├── scraper.py            # 爬蟲核心邏輯
├── brokers.json          # 設定檔：定義股票代碼與對應券商 URL
└── requirements.txt      # 相依套件列表
```