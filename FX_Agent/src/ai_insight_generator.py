import os
import json
from groq import Groq

class MarketInsightAgent:
    """The Groq/Llama-3 powered Reasoning Engine."""

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set.")
            
        self.client = Groq(api_key=api_key)
        
        with open(os.path.join("skills", "financial_advisor_prompt.txt"), "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def get_insights(self, news_context: str, fx_trend: str) -> dict:
        """Passes context to the LLM to yield strict JSON Insights & Features."""
        user_message = f"Recent News Context:\n{news_context}\n\nRecent FX Trend:\n{fx_trend}"
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            # Groq guarantees JSON response thanks to the response_format key
            return json.loads(chat_completion.choices[0].message.content)
        except Exception as e:
            print(f"[Error] Groq AI API Connection failed: {str(e)}")
            return {"actionable_insights": ["AI API Unavailable - Assuming Parity Hold"], "feature_engineering_suggestions": []}
