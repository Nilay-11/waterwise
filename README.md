# 💧 WaterWise — AI Water & Sanitation Knowledge Assistant
### 1M1B AI for Sustainability Virtual Internship (In Collaboration with IBM SkillsBuild & AICTE)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![WHO Guidelines](https://img.shields.io/badge/WHO-Guidelines%20for%20Drinking--water%20Quality-008dc9?logo=worldhealthorganization)](https://www.who.int/publications/i/item/9789241549950)
[![UN SDG 6](https://img.shields.io/badge/UN%20SDG-6%20Clean%20Water%20%26%20Sanitation-26bde2?style=flat&logo=un)](https://sdgs.un.org/goals/goal6)
[![IBM Bob / Granite](https://img.shields.io/badge/IBM-Bob%20%2F%20Granite%20LLM-0f62fe?logo=ibm)](https://www.ibm.com/products/watsonx-ai)

> **A verifiable Retrieval-Augmented Generation (RAG) decision-support system grounded in World Health Organization (WHO) and UN-Water guidelines, powered by IBM Bob & Granite Foundation Models.**

---

## 🌍 Problem Statement & SDG Alignment

**Primary UN SDG: SDG 6 (Clean Water and Sanitation)**
- **Target 6.1**: Universal access to safe drinking water (WHO Guidelines 4th Ed. & Water Safety Plans).
- **Target 6.2**: Adequate sanitation & ending open defecation (WHO/UNICEF JMP Sanitation Ladder & SBM-Grameen).
- **Target 6.3**: Improving water quality & halving untreated wastewater (UN-Water Global Wastewater Assessment).
- **Target 6.4**: Water-use efficiency & Nature-based Solutions (UNESCO WWDR).

Over 2 billion people lack safely managed drinking water. Critical guidelines from the **World Health Organization (WHO)**, **UN-Water**, and national bodies like India's **Jal Jeevan Mission** are contained within 500+ page technical publications. Frontline health workers, rural water operators, and community leaders need instant, verifiable access to water safety thresholds without the risk of generative AI hallucinations.

---

## 🏗️ Architecture & Pipeline

```text
       ┌─────────────────────────────────────────────────────────────┐
       │             AUTHORITATIVE WHO & UN CORPUS                   │
       │   • WHO Guidelines for Drinking-water Quality (4th Ed)       │
       │   • WHO / UNICEF JMP Sanitation & Hygiene Standards          │
       │   • UN-Water Global Wastewater Assessment                    │
       │   • Jal Jeevan Mission (Ministry of Jal Shakti, India)      │
       │   • UNESCO World Water Development Reports                  │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                              Document Ingestion
                           (Chunking & Indexing)
                                      │
                              Dense Vector Store
                                      │
User Question ──► Semantic Retrieval (Threshold Gate) ──► Grounded Prompt
                                                                  │
                                                       IBM Bob / Granite LLM
                                                                  │
                                      ┌───────────────────────────┴───────────────────────────┐
                                      ▼                                                       ▼
                             [Grounded Answer]                                       [Official Citations]
                    "Wastewater treatment involves..."                      • WHO Drinking-water Guidelines (Ch. 4)
                                                                            • UN-Water Wastewater Report (Ch. 3)
```

---

## 🛡️ Responsible AI & Key Features

1. **Strict WHO & UN Grounding**: Every answer is restricted to verifiable WHO/UN documentation with bracketed citations.
2. **Anti-Hallucination Guardrail ("I don't know" mode)**: Safely declines out-of-scope queries (e.g. stock prices, unrelated trivia) to avoid dispensing inaccurate medical or water treatment advice.
3. **Dynamic Knowledge Ingestion**: Ingest custom local water utility or regional circulars through the web dashboard.
4. **IBM Bob / watsonx Integration**: Powered by IBM Granite foundation models (`ibm/granite-3-8b-instruct`) with a built-in standalone fallback.

---

## 🚀 Quickstart & Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/Nilay-11/promptshiedX.git
cd promptshiedX

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run streamlit_app.py
```

---

## ☁️ Streamlit Cloud Deployment

1. Go to [share.streamlit.io](https://share.streamlit.io).
2. Select your repository: `Nilay-11/promptshiedX` (or your renamed repo).
3. Main file path: `streamlit_app.py`
4. Click **Deploy!**
