import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import logging

class FXForecaster:
    """Automated Machine Learning specific to FX exchange rate tracking."""

    def __init__(self):
        # Suppress verbose debug logs from Prophet for clean CLI execution
        logging.getLogger('cmdstanpy').setLevel(logging.WARNING)
        logging.getLogger('prophet').setLevel(logging.WARNING)
        self.model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
        self.forecast_df = None

    def run_forecast(self, df: pd.DataFrame, horizon: int = 30) -> pd.DataFrame:
        """Trains the internal model and creates a trajectory matrix."""
        df_p = df.rename(columns={'fx_rate': 'y'})
        self.model.fit(df_p)
        future = self.model.make_future_dataframe(periods=horizon)
        self.forecast_df = self.model.predict(future)
        return self.forecast_df

    def generate_signal(self) -> str:
        """Evaluates forward depreciation dynamics to trigger a signal."""
        if self.forecast_df is None:
            raise ValueError("Must execute run_forecast() before pulling signals.")
        
        # The T-0 baseline (the last actual known historical spot rate date)
        last_actual_rate = self.forecast_df['yhat'].iloc[-31]
        
        # The T+30 projection limit
        future_rate = self.forecast_df['yhat'].iloc[-1]
        
        # Depreciate by 1% constraint: If the rate falls below 99% of current rate.
        # Less FX_Rate value = weaker EUR => less VND per EUR bought
        if future_rate < (last_actual_rate * 0.99):
            return "HEDGE NOW"
        return "HOLD"

    def plot_forecast(self, output_path: str = "forecast_chart.png"):
        """Compiles the model output trajectory internally locally."""
        fig = self.model.plot(self.forecast_df)
        plt.title("EUR vs VND 30-Day Forecast Engine Trajectory")
        plt.xlabel("Prophet Time Horizon")
        plt.ylabel("Exchange Rate Magnitude")
        fig.savefig(output_path, bbox_inches='tight')
        plt.close(fig)
