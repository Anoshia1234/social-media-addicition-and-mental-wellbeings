import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Social Media & Mental Wellbeing Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('social_media_addiction_mental_wellbeing.csv')
    df.fillna(df.median(numeric_only=True), inplace=True)
    for col in df.select_dtypes(include=['object']).columns:
        df[col].fillna(df[col].mode()[0], inplace=True)
    return df

df = load_data()

# Title and Description
st.title("Social Media Addiction & Mental Wellbeing Analytics")
st.markdown("This dashboard analyzes the behavioral and psychological impacts of social media usage on individuals.")

# Sidebar Filters
st.sidebar.header("Filter Options")
selected_gender = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
selected_addiction = st.sidebar.multiselect("Select Addiction Level", options=df['Addiction_Level'].unique(), default=df['Addiction_Level'].unique())

filtered_df = df[(df['Gender'].isin(selected_gender)) & (df['Addiction_Level'].isin(selected_addiction))]

# 4 Key Numbers at the Top
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Users Analyzed", len(filtered_df))
col2.metric("Avg Daily Usage (Hrs)", f"{filtered_df['Daily_Usage_Hours'].mean():.2f}")
col3.metric("Avg Anxiety Score", f"{filtered_df['Anxiety_Score'].mean():.2f}")
col4.metric("Avg Sleep Quality", f"{filtered_df['Sleep_Quality_Score'].mean():.2f}")

st.markdown("---")

# 5 Graphs (Including Plotly)
st.subheader("📊 Interactive Visualizations & Analytics")

c1, c2 = st.columns(2)

with c1:
    st.markdown("**1. Daily Usage Hours Distribution (Univariate)**")
    fig1 = px.histogram(filtered_df, x="Daily_Usage_Hours", nbins=20, title="Daily Usage Hours Spread", color_discrete_sequence=['teal'])
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown("**2. Addiction Levels Breakdown (Univariate)**")
    fig2 = px.pie(filtered_df, names="Addiction_Level", title="Addiction Level Proportions", hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    st.markdown("**3. Daily Usage vs. Anxiety Score (Bivariate)**")
    fig3 = px.scatter(filtered_df, x="Daily_Usage_Hours", y="Anxiety_Score", color="Addiction_Level", title="Usage Hours vs Anxiety")
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.markdown("**4. Mental Wellbeing by Primary Platform (Comparison)**")
    fig4 = px.box(filtered_df, x="Primary_Platform", y="Mental_Wellbeing_Score", color="Primary_Platform", title="Wellbeing Across Platforms")
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("**5. Correlation Heatmap of Psychological Factors**")
plt.figure(figsize=(8, 4))
num_cols = ['Daily_Usage_Hours', 'FOMO_Score', 'Anxiety_Score', 'Depression_Score', 'Sleep_Quality_Score']
sns.heatmap(filtered_df[num_cols].corr(), annot=True, cmap='Blues', fmt='.2f')
st.pyplot(plt)

# Raw Data Checkbox
if st.checkbox("Show Raw Filtered Dataset"):
    st.dataframe(filtered_df)

# Findings Section
st.markdown("---")
st.subheader("💡 Key Findings & Insights")
st.markdown("""
- **High Screen Time Correlation:** Extended daily usage hours show a direct positive correlation with elevated anxiety scores.
- **Platform Disparities:** Average mental wellbeing scores fluctuate significantly depending on the user's primary social platform choice.
- **Sleep Disruption:** Severe addiction tiers experience lower average sleep quality due to late-night engagement patterns.
""")
