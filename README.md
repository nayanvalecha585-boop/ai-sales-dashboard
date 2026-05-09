# 📊 AI Sales Insights Dashboard

A modular Streamlit dashboard that visualises Superstore sales data and generates AI-powered business insights using Google Gemini.

---

## 🗂️ Project Structure

```
ai-sales-dashboard/
│
├── app.py                    ← Main entry point (run this)
│
├── components/
│   ├── kpi_cards.py          ← KPI metric cards (row of numbers)
│   ├── charts.py             ← All Plotly charts
│   └── ai_insights.py        ← Gemini AI insights section
│
├── utils/
│   ├── data_loader.py        ← CSV loading + caching
│   ├── kpi_calculator.py     ← All KPI maths
│   └── gemini_client.py      ← Gemini API wrapper
│
├── data/
│   └── superstore.csv        ← ⚠️ Add your dataset here
│
├── .env                      ← ⚠️ Add your API key here (not in Git)
├── .env.example              ← Template for .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Run

### 1. Clone / download the project

```bash
git clone <your-repo-url>
cd ai-sales-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your dataset

Place your `superstore.csv` file inside the `data/` folder.  
Download the Superstore dataset from [Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final).

### 5. Add your Gemini API key

```bash
cp .env.example .env
```

Edit `.env`:
```
GEMINI_API_KEY=your_actual_key_here
```

Get a free API key at [aistudio.google.com](https://aistudio.google.com).

### 6. Run the dashboard

```bash
streamlit run app.py
```

---

## ✨ Features

| Feature | Details |
|---|---|
| KPI Cards | Sales, Profit, Orders, Margin, Customers, Avg Discount |
| Charts | Category bar, Region pie, Monthly trend, Segment bar, Sub-category, Scatter |
| Filters | Region, Category, Segment (sidebar) |
| CSV Upload | Upload your own dataset via sidebar |
| AI Insights | Gemini generates a full business report from your filtered data |
| Download | Save the AI report as a `.txt` file |

---

## 🔐 Security Notes

- Your `.env` file is listed in `.gitignore` — it will never be committed to Git.
- The Gemini API key is loaded only via environment variables, never hardcoded.

---

## 📦 Dependencies

- `streamlit` — dashboard UI
- `pandas` — data processing
- `plotly` — interactive charts
- `google-generativeai` — Gemini AI SDK
- `python-dotenv` — environment variable loading
