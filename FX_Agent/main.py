import os
import logging
import pytz
from datetime import datetime
from dotenv import load_dotenv

from src.data_fetcher import DataFetcher
from src.ai_insight_generator import MarketInsightAgent
from src.forecaster import FXForecaster
from src.storage_manager import StorageManager
from src.email_reporter import EmailReporter

# Configure native architecture logging to Ho Chi Minh time
tz = pytz.timezone("Asia/Ho_Chi_Minh")
os.makedirs("logs", exist_ok=True)

class GMT7Formatter(logging.Formatter):
    def converter(self, timestamp):
        dt = datetime.fromtimestamp(timestamp, tz)
        return dt.timetuple()

logger = logging.getLogger('FX_Agent_Core')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join('logs', 'execution.log'))
formatter = GMT7Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def main():
    logger.info("Initializing the FX_Agent Orchestration Frame...")
    load_dotenv()
    
    try:
        # Pipeline execution block
        fetcher = DataFetcher()
        df_fx = fetcher.fetch_fx_data()
        current_rate = df_fx['fx_rate'].iloc[-1]
        logger.info(f"Target Acquired. Spot EURVND: {current_rate}")
        
        news_context = fetcher.fetch_rss_news()
        logger.info("Extracted Vietnamese RSS News Vector.")
        
        agent = MarketInsightAgent()
        fx_trend = f"Current Spot Rate: {current_rate}"
        ai_dict = agent.get_insights(news_context, fx_trend)
        logger.info(f"LLM Llama-3-70b-8192 completed Reasoning pass.")
        
        forecaster = FXForecaster()
        forecaster.run_forecast(df_fx)
        prophet_signal = forecaster.generate_signal()
        forecaster.plot_forecast("forecast_chart.png")
        logger.info(f"Prophet Horizon finalized. Alpha Signal Generated: {prophet_signal}")
        
        storage = StorageManager()
        storage.save_daily_record(current_rate, prophet_signal, ai_dict.get('feature_engineering_suggestions', []))
        logger.info("Written structural telemetry to GitOps tracking (performance_log.csv).")
        
        reporter = EmailReporter()
        reporter.send_email(current_rate, prophet_signal, ai_dict, "forecast_chart.png")
        logger.info("Encrypted email framework distributed securely via SMTP. Full run verified.")
        
    except Exception as e:
        logger.error(f"FATAL PIPELINE INTERRUPTION: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()
