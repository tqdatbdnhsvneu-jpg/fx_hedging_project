import yfinance as yf
import feedparser
import pandas as pd

class DataFetcher:
    """Handles raw data ingestion from Yahoo Finance and Vietnamese news publishers."""

    def __init__(self):
        self.news_urls = [
            "https://cafef.vn/tai-chinh-ngan-hang.rss",
            "https://vneconomy.vn/tai-chinh.rss"
        ]

    def fetch_fx_data(self, ticker: str = "EURVND=X", period: str = "2y") -> pd.DataFrame:
        """Fetches and cleans the history of EURVND=X."""
        df = yf.download(ticker, period=period)
        df.reset_index(inplace=True)
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]
            
        df = df[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'fx_rate'})
        df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)
        
        # Forward fill empty dates (like weekends) to maintain consistent time series parity
        full_dates = pd.DataFrame({'ds': pd.date_range(start=df['ds'].min(), end=df['ds'].max(), freq='D')})
        df = pd.merge(full_dates, df, on='ds', how='left')
        df['fx_rate'] = df['fx_rate'].ffill()
        return df

    def fetch_rss_news(self) -> str:
        """Scrapes Top-15 articles from financial RSS feeds to generate LLM context."""
        import requests
        news_context = []
        for url in self.news_urls:
            try:
                response = requests.get(url, timeout=10)
                feed = feedparser.parse(response.content)
                for entry in feed.entries[:15]:
                    title = entry.get('title', 'No Title')
                    summary = entry.get('summary', '')
                    news_context.append(f"Title: {title}\nSummary: {summary}\n")
            except requests.RequestException as e:
                print(f"[Warning] Failed to fetch {url} due to {str(e)}")
        return "\n".join(news_context)
