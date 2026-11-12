# Social Media Addiction & Mental Wellbeing Analysis

An end-to-end Exploratory Data Analysis (EDA) and interactive web application examining the correlation between daily social media consumption and psychological health metrics (anxiety, depression, sleep quality, and overall mental wellbeing).

## 📊 Dataset Overview
- **Source:** Kaggle (`social_media_addiction_mental_wellbeing.csv`)
- **Rows:** 1,500
- **Columns:** 30
- **Description:** Captures individual behavioral habits (screen time, late-night usage, FOMO scores) alongside mental wellness evaluations.

## 🚀 Key Features & Project Workflow
1. **Data Cleaning & Preprocessing:** Handled missing values using median/mode imputation, verified uniqueness of user IDs, and analyzed statistical outliers using IQR rules.
2. **Exploratory Data Analysis (EDA):** Conducted univariate distributions, bivariate scatter plots, and correlation heatmaps in a Jupyter/Colab notebook.
3. **Interactive Streamlit Dashboard:** Built with custom sidebar filters, key performance indicators (KPIs), Plotly visualizations, and a raw data inspection toggle.

## 🔗 Live Links
- **Live Streamlit Dashboard:** [View App Here](https://your-streamlit-app-link.streamlit.app)
- **Google Slides Presentation:** [View Slides Here](https://docs.google.com/presentation/d/your-presentation-link/edit?usp=sharing)

## 🛠️ Installation & Local Setup
Clone the repository and run the application locally:
```bash
git clone [https://github.com/your-username/social-media-wellbeing-analysis.git](https://github.com/your-username/social-media-wellbeing-analysis.git)
cd social-media-wellbeing-analysis
pip install -r requirements.txt
streamlit run app.py
