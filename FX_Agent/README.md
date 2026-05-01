# FX_Agent Autonomous Treasury Engine

## 🌍 Platform Overview
**FX_Agent** is a production-grade, entirely autonomous MLOps platform engineered exclusively to manage foreign exchange volatility for a European Travel Outbound conglomerate operating strictly in Southeast Asia (focused strictly on the EUR/VND parity).

This repository encompasses a daily active Continuous Integration framework driving advanced LLM-Reasoning alongside hard Quantitative machine learning signals, acting natively as a "Robot CFO".

---

## 🏗 System Architecture & Agent Workflow
The ecosystem runs as a decoupled stack orchestrated independently via **GitHub Actions** tracking the Asia/Ho_Chi_Minh GMT+7 time boundaries natively:

1. **Information Ingestion (`src/data_fetcher.py`)**: Continuously scrapes Vietnamese Economic RSS feeds and YFinance matrix streams simultaneously.
2. **AI Reasoning Module (`src/ai_insight_generator.py`)**: Uses a targeted Prompt framework via `groq` querying `Llama-3-70b-8192` to process complex global macroeconomic events natively evaluating against the EUR/VND split.
3. **Quantitative Forecaster (`src/forecaster.py`)**: Re-trains a fresh Prophet model daily strictly against recent boundaries, enforcing a tight 1% depreciation constraint metric before issuing `HEDGE NOW` signals.
4. **HTML Intelligence Reporting (`src/email_reporter.py`)**: Secure SMTP rendering sends C-level visual templates directly to internal networks.
5. **GitOps Persistence (`src/storage_manager.py`)**: Writes stateful intelligence securely back to the repository autonomously preserving the artifact trails without database costs.

---

## 🔥 Key Engineering Decisions
* **Prompt Externalization**: Financial parameters are isolated logically within `prompts/financial_advisor_prompt.txt` ensuring business logic is highly modular beyond technical deployment code. This embraces standard LLMOps patterns.
* **Autonomous LLM Feature Engineering**: The `groq` pipeline utilizes structured JSON objects leveraging Chain of Thought (CoT), where the model autonomously proposes explicitly tracked metadata features to integrate securely inside the classical Prophet stack.
* **GitOps Storage Subsystem**: Deploying GitHub automations alongside `performance_log.csv` updates permits the system to trace its intelligence loop historically without relying on heavy and vulnerable containerized PostgreSQL modules.

---

## 🔒 Automated CI/CD & Secret Setup
To initialize the orchestrator:
1. Navigate to **Settings > Secrets and variables > Actions**.
2. Provision exact keys matching the operational framework context:
   - `GROQ_API_KEY`: Enterprise API Token
   - `EMAIL_PASSWORD`: Defined securely adhering to App Password protocols for Gmail SMTP logic.

*Built for elite resilience and dynamic edge strategy.*
