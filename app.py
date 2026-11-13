import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Social Media Addiction & Mental Wellbeing Dashboard",
    page_icon="🧠",
    layout="wide"
)

# 2. Custom CSS for Modern UI, Colors, Fonts & Cards
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    /* Main Background & Font */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0b1120;
        border-right: 1px solid #334155;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    /* Headers Styling */
    h1 {
        color: #38bdf8 !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    h2, h3 {
        color: #7dd3fc !important;
        font-weight: 600 !important;
    }

    /* KPI Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid #38bdf8;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease-in-out;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        border-color: #818cf8;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    /* Custom Insight Box */
    .insight-box {
        background: rgba(15, 23, 42, 0.8);
        border-left: 5px solid #38bdf8;
        padding: 20px;
        border-radius: 8px;
        margin-top: 10px;
        color: #e2e8f0;
        line-height: 1.7;
    }
</style>
""", unsafe_allow_html=True)

# 3. Data Loading & Cleaning (Error-Free)
@st.cache_data
def load_data():
    df = pd.read_csv('social_media_addiction_mental_wellbeing.csv')
    # Numeric columns median fill
    num_cols = df.select_dtypes(include=[np.number]).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    # Categorical columns mode fill
    cat_cols = df.select_dtypes(include=['object', 'string']).columns
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ CSV file 'social_media_addiction_mental_wellbeing.csv'")
    st.stop()

# 4. Title and Description
st.title("Social Media Addiction & Mental Wellbeing Analytics")
st.markdown("<p style='color:#cbd5e1; font-size:1.1rem;'>Analyzing the behavioral and psychological impacts of daily social media usage across demographics.</p>", unsafe_allow_html=True)

# 5. Sidebar Filters
st.sidebar.header("🎛️ Filter Options")
selected_gender = st.sidebar.multiselect(
    "Select Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)
selected_addiction = st.sidebar.multiselect(
    "Select Addiction Level",
    options=df['Addiction_Level'].unique(),
    default=df['Addiction_Level'].unique()
)

filtered_df = df[
    (df['Gender'].isin(selected_gender)) &
    (df['Addiction_Level'].isin(selected_addiction))
]

# Handle Empty Filter Selection Safely
if filtered_df.empty:
    st.warning("⚠️ Selected filters ke liye koi data available nahi hai. Please sidebar se kam az kam ek option select karein.")
    st.stop()

# 6. Top 4 KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Total Users Analyzed", f"{len(filtered_df):,}")
col2.metric("⏱️ Avg Daily Usage (Hrs)", f"{filtered_df['Daily_Usage_Hours'].mean():.2f}")
col3.metric("😰 Avg Anxiety Score", f"{filtered_df['Anxiety_Score'].mean():.2f}")
col4.metric("😴 Avg Sleep Quality", f"{filtered_df['Sleep_Quality_Score'].mean():.2f}")

st.markdown("---")

# 7. Interactive Visualizations (Dark Theme Matched)
st.subheader("📊 Interactive Visualizations & Analytics")

chart_template = "plotly_dark"
color_palette = ["#38bdf8", "#818cf8", "#f472b6", "#34d399", "#fbbf24"]

c1, c2 = st.columns(2)

with c1:
    st.markdown("**1. Daily Usage Hours Distribution (Univariate)**")
    fig1 = px.histogram(
        filtered_df,
        x="Daily_Usage_Hours",
        nbins=20,
        title="Daily Usage Hours Spread",
        color_discrete_sequence=['#38bdf8'],
        template=chart_template
    )
    fig1.update_layout(paper_bgcolor="rgba(30,41,59,0.5)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown("**2. Addiction Levels Breakdown (Univariate)**")
    fig2 = px.pie(
        filtered_df,
        names="Addiction_Level",
        title="Addiction Level Proportions",
        hole=0.45,
        color_discrete_sequence=color_palette,
        template=chart_template
    )
    fig2.update_layout(paper_bgcolor="rgba(30,41,59,0.5)")
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    st.markdown("**3. Daily Usage vs. Anxiety Score (Bivariate)**")
    fig3 = px.scatter(
        filtered_df,
        x="Daily_Usage_Hours",
        y="Anxiety_Score",
        color="Addiction_Level",
        title="Usage Hours vs Anxiety",
        color_discrete_sequence=color_palette,
        template=chart_template
    )
    fig3.update_layout(paper_bgcolor="rgba(30,41,59,0.5)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.markdown("**4. Mental Wellbeing by Primary Platform (Comparison)**")
    fig4 = px.box(
        filtered_df,
        x="Primary_Platform",
        y="Mental_Wellbeing_Score",
        color="Primary_Platform",
        title="Wellbeing Across Platforms",
        color_discrete_sequence=color_palette,
        template=chart_template
    )
    fig4.update_layout(paper_bgcolor="rgba(30,41,59,0.5)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

# 8. Interactive Correlation Heatmap
st.markdown("**5. Correlation Heatmap of Psychological Factors**")
num_cols = ['Daily_Usage_Hours', 'FOMO_Score', 'Anxiety_Score', 'Depression_Score', 'Sleep_Quality_Score']
corr_matrix = filtered_df[num_cols].corr().round(2)

fig5 = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale="Blues",
    title="Psychological Factors Correlation Matrix",
    template=chart_template
)
fig5.update_layout(paper_bgcolor="rgba(30,41,59,0.5)", height=450)
st.plotly_chart(fig5, use_container_width=True)

# 9. Raw Data Section
if st.checkbox("📂 Show Raw Filtered Dataset"):
    st.dataframe(filtered_df, use_container_width=True)

# 10. Findings Section
st.markdown("---")
st.subheader("💡 Key Findings & Insights")
st.markdown("""
<div class="insight-box">
    <ul>
        <li><b>High Screen Time Correlation:</b> Extended daily usage hours show a direct positive correlation with elevated anxiety and FOMO scores.</li>
        <li><b>Platform Disparities:</b> Average mental wellbeing scores fluctuate noticeably depending on the user's primary social platform choice.</li>
        <li><b>Sleep Disruption:</b> Severe addiction tiers experience lower average sleep quality due to late-night engagement patterns.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
