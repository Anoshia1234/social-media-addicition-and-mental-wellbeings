import os
import pandas as pd
import plotly.express as px
import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & PROFESSIONAL SKY BLUE THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Social Media & Digital Wellbeing Dashboard",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #0F172A;
        }

        /* Soft Sky Blue Background */
        .stApp {
            background-color: #F0F9FF;
        }

        /* Top Executive Header Banner */
        .hero-banner {
            background: linear-gradient(135deg, #0284C7 0%, #38BDF8 55%, #0EA5E9 100%);
            padding: 30px 34px;
            border-radius: 18px;
            color: #FFFFFF;
            margin-bottom: 24px;
            box-shadow: 0 12px 28px -6px rgba(2, 132, 199, 0.28);
        }
        .hero-banner h1 {
            margin: 0;
            font-size: 2.15rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: #FFFFFF;
        }
        .hero-banner p {
            margin: 8px 0 0 0;
            font-size: 1.05rem;
            color: #E0F2FE;
            font-weight: 500;
        }

        /* KPI Cards */
        .kpi-card {
            background: #FFFFFF;
            padding: 20px 22px;
            border-radius: 14px;
            border-top: 4px solid #0EA5E9;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
            transition: transform 0.2s ease;
        }
        .kpi-card:hover {
            transform: translateY(-3px);
        }
        .kpi-label {
            font-size: 0.82rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748B;
            margin-bottom: 6px;
        }
        .kpi-val {
            font-size: 1.9rem;
            font-weight: 800;
            color: #0F172A;
            line-height: 1.1;
        }
        .kpi-note {
            font-size: 0.82rem;
            font-weight: 600;
            color: #0284C7;
            margin-top: 6px;
        }

        /* Social Media Platform Cards */
        .social-card {
            background: #FFFFFF;
            border-radius: 14px;
            padding: 18px 14px;
            text-align: center;
            border: 1px solid #BAE6FD;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.06);
        }
        .social-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #0F172A;
            margin-top: 10px;
        }
        .social-metrics {
            font-size: 0.85rem;
            color: #475569;
            margin-top: 4px;
        }
        .social-badge {
            display: inline-block;
            margin-top: 8px;
            padding: 3px 10px;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
            background-color: #FFE4E6;
            color: #E11D48;
        }

        /* Clean Section Headings */
        .section-heading {
            font-size: 1.28rem;
            font-weight: 800;
            color: #0F172A;
            margin: 28px 0 14px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #7DD3FC;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# 2. BULLETPROOF DATA LOADER & PREPROCESSOR
# -----------------------------------------------------------------------------
@st.cache_data
def load_and_clean_data(file_source):
    df = pd.read_csv(file_source)

    # Clean categorical columns safely
    cat_defaults = {
        "Gender": "Not Specified",
        "Occupation": "Other",
        "Primary_Platform": "Other",
        "Addiction_Level": "Moderate",
    }
    for col, default_val in cat_defaults.items():
        if col in df.columns:
            df[col] = df[col].fillna(default_val).astype(str).str.strip()

    # Clean numeric columns safely with median imputation
    num_cols = [
        "Age",
        "Daily_Usage_Hours",
        "Mental_Wellbeing_Score",
        "Sleep_Hours",
        "Anxiety_Score",
        "FOMO_Score",
        "Productivity_Loss_Score",
    ]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(df[col].median())

    return df


def resolve_dataset():
    candidate_paths = [
        "social_media_addiction_mental_wellbeing.csv",
        "social_media_addiction_mental_wellbeing (1).csv",
        "/content/social_media_addiction_mental_wellbeing.csv",
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            return load_and_clean_data(path)

    # Auto-scan current directory for any matching CSV
    for fname in os.listdir("."):
        if fname.lower().endswith(".csv") and "social_media" in fname.lower():
            return load_and_clean_data(fname)

    return None


df = resolve_dataset()

if df is None:
    st.warning("Dataset file repository mein auto-detect nahi hui. Neeche se CSV upload karein:")
    uploaded = st.file_uploader("Upload social_media_addiction_mental_wellbeing.csv", type=["csv"])
    if uploaded is not None:
        df = load_and_clean_data(uploaded)
    else:
        st.stop()


# -----------------------------------------------------------------------------
# 3. SIDEBAR INTERACTIVE FILTERS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎛️ Analytics Filters")
    st.caption("Filter demographics and platforms to dynamically update all insights.")

    platforms = sorted([p for p in df["Primary_Platform"].unique() if p != "Other"])
    sel_platforms = st.multiselect("Social Media Platforms", platforms, default=platforms)

    genders = sorted([g for g in df["Gender"].unique() if g != "Not Specified"])
    sel_genders = st.multiselect("Gender", genders, default=genders)

    occupations = sorted([o for o in df["Occupation"].unique() if o != "Other"])
    sel_occupations = st.multiselect("Occupation", occupations, default=occupations)

    min_age, max_age = int(df["Age"].min()), int(df["Age"].max())
    sel_age = st.slider("Age Group", min_age, max_age, (min_age, max_age))


filtered_df = df[
    (df["Primary_Platform"].isin(sel_platforms))
    & (df["Gender"].isin(sel_genders))
    & (df["Occupation"].isin(sel_occupations))
    & (df["Age"].between(sel_age[0], sel_age[1]))
]

if filtered_df.empty:
    st.warning("⚠️ Selected filters ke mutabiq koi record nahi mila. Sidebar se filters reset karein.")
    st.stop()


# -----------------------------------------------------------------------------
# 4. HERO HEADER BANNER
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-banner">
        <h1>📱 Social Media Addiction & Mental Wellbeing Analytics</h1>
        <p>Executive insights into platform dependency, gender usage patterns, and student vs. professional screen habits</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# 5. EXECUTIVE KPI SUMMARY CARDS
# -----------------------------------------------------------------------------
total_users = len(filtered_df)
avg_daily_hrs = filtered_df["Daily_Usage_Hours"].mean()
high_addiction_rate = filtered_df["Addiction_Level"].isin(["High", "Severe"]).mean() * 100
avg_wellbeing = filtered_df["Mental_Wellbeing_Score"].mean()

# Identify Most Addictive App dynamically
plat_risk = (
    filtered_df.assign(Is_High=filtered_df["Addiction_Level"].isin(["High", "Severe"]))
    .groupby("Primary_Platform")["Is_High"]
    .mean()
    .mul(100)
)
top_addictive_app = plat_risk.idxmax() if not plat_risk.empty else "N/A"
top_addictive_val = plat_risk.max() if not plat_risk.empty else 0.0

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Respondents</div>
            <div class="kpi-val">{total_users:,}</div>
            <div class="kpi-note">Filtered active sample</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card" style="border-top-color: #0284C7;">
            <div class="kpi-label">Avg. Daily Screen Time</div>
            <div class="kpi-val">{avg_daily_hrs:.2f} hrs</div>
            <div class="kpi-note">Per user daily average</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card" style="border-top-color: #F43F5E;">
            <div class="kpi-label">Highest Addiction App</div>
            <div class="kpi-val">{top_addictive_app}</div>
            <div class="kpi-note" style="color: #E11D48;">{top_addictive_val:.1f}% High/Severe users</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-card" style="border-top-color: #10B981;">
            <div class="kpi-label">Mental Wellbeing Score</div>
            <div class="kpi-val">{avg_wellbeing:.1f} / 10</div>
            <div class="kpi-note" style="color: #059669;">Overall wellbeing index</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# 6. SOCIAL MEDIA PLATFORM CARDS WITH ICONS
# -----------------------------------------------------------------------------
st.markdown('<div class="section-heading">🌐 Platform Engagement & Addiction Snapshot</div>', unsafe_allow_html=True)

platform_styles = {
    "Instagram": {"icon": "fab fa-instagram", "color": "#E1306C"},
    "TikTok": {"icon": "fab fa-tiktok", "color": "#0F172A"},
    "YouTube": {"icon": "fab fa-youtube", "color": "#FF0000"},
    "Facebook": {"icon": "fab fa-facebook", "color": "#1877F2"},
    "Twitter/X": {"icon": "fab fa-x-twitter", "color": "#0284C7"},
    "Snapchat": {"icon": "fab fa-snapchat", "color": "#D97706"},
}

present_platforms = [p for p in platform_styles if p in filtered_df["Primary_Platform"].unique()]
if present_platforms:
    p_cols = st.columns(len(present_platforms))
    for i, plat in enumerate(present_platforms):
        sub = filtered_df[filtered_df["Primary_Platform"] == plat]
        cnt = len(sub)
        hrs = sub["Daily_Usage_Hours"].mean()
        sev = sub["Addiction_Level"].isin(["High", "Severe"]).mean() * 100
        style = platform_styles[plat]

        with p_cols[i]:
            st.markdown(
                f"""
                <div class="social-card">
                    <i class="{style['icon']}" style="font-size: 2.1rem; color: {style['color']};"></i>
                    <div class="social-title">{plat}</div>
                    <div class="social-metrics"><b>{cnt}</b> Users • <b>{hrs:.1f} hrs</b>/day</div>
                    <div class="social-badge">{sev:.1f}% High/Severe Addiction</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# -----------------------------------------------------------------------------
# 7. CORE VISUALIZATIONS (ADDICTION, GENDER, STUDENTS VS PROFESSIONALS)
# -----------------------------------------------------------------------------
st.markdown('<div class="section-heading">📊 Behavioral & Demographic Visual Insights</div>', unsafe_allow_html=True)

addiction_order = ["Low", "Moderate", "High", "Severe"]
addiction_palette = {
    "Low": "#38BDF8",       # Sky Blue
    "Moderate": "#6366F1",  # Indigo
    "High": "#F97316",      # Vibrant Orange
    "Severe": "#F43F5E",    # Coral Red
}

gender_palette = {
    "Male": "#0284C7",        # Deep Sky Blue
    "Female": "#EC4899",      # Rose Pink
    "Non-binary": "#8B5CF6",  # Violet
}

chart_layout = dict(
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font=dict(family="Plus Jakarta Sans", color="#0F172A", size=12),
    title_font=dict(size=15, color="#0F172A"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=20, r=20, t=55, b=20),
)

row1_col1, row1_col2 = st.columns(2)

# CHART 1: Which App Has Highest Addiction?
with row1_col1:
    app_addiction = (
        filtered_df.groupby(["Primary_Platform", "Addiction_Level"])
        .size()
        .reset_index(name="Users")
    )
    fig1 = px.bar(
        app_addiction,
        x="Primary_Platform",
        y="Users",
        color="Addiction_Level",
        barmode="group",
        category_orders={"Addiction_Level": addiction_order},
        color_discrete_map=addiction_palette,
        title="<b>1. Addiction Severity Distribution by Social Media App</b>",
        labels={"Primary_Platform": "Social Media Platform", "Users": "Number of Users", "Addiction_Level": "Severity"},
    )
    fig1.update_layout(**chart_layout)
    st.plotly_chart(fig1, use_container_width=True)

# CHART 2: Male vs Female Daily Usage Across Apps
with row1_col2:
    gender_app = (
        filtered_df.groupby(["Primary_Platform", "Gender"])["Daily_Usage_Hours"]
        .mean()
        .reset_index()
    )
    fig2 = px.bar(
        gender_app,
        x="Primary_Platform",
        y="Daily_Usage_Hours",
        color="Gender",
        barmode="group",
        color_discrete_map=gender_palette,
        title="<b>2. Average Daily Usage (Hours): Male vs. Female</b>",
        labels={"Primary_Platform": "Social Media Platform", "Daily_Usage_Hours": "Avg. Daily Hours"},
    )
    fig2.update_layout(**chart_layout)
    st.plotly_chart(fig2, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

# CHART 3: Students vs Working Professionals Usage Hours by Gender
with row2_col1:
    occ_usage = (
        filtered_df.groupby(["Occupation", "Gender"])["Daily_Usage_Hours"]
        .mean()
        .reset_index()
    )
    fig3 = px.bar(
        occ_usage,
        x="Occupation",
        y="Daily_Usage_Hours",
        color="Gender",
        barmode="group",
        color_discrete_map=gender_palette,
        title="<b>3. Students vs. Working Professionals: Daily Screen Time</b>",
        labels={"Occupation": "Occupation Category", "Daily_Usage_Hours": "Avg. Daily Hours"},
    )
    fig3.update_layout(**chart_layout)
    st.plotly_chart(fig3, use_container_width=True)

# CHART 4: Students vs Professionals Addiction Level Breakdown
with row2_col2:
    occ_addiction = (
        filtered_df.groupby(["Occupation", "Addiction_Level"])
        .size()
        .reset_index(name="Users")
    )
    fig4 = px.bar(
        occ_addiction,
        x="Occupation",
        y="Users",
        color="Addiction_Level",
        barmode="stack",
        category_orders={"Addiction_Level": addiction_order},
        color_discrete_map=addiction_palette,
        title="<b>4. Addiction Severity Across Students & Professionals</b>",
        labels={"Occupation": "Occupation Category", "Users": "User Count", "Addiction_Level": "Severity"},
    )
    fig4.update_layout(**chart_layout)
    st.plotly_chart(fig4, use_container_width=True)


# -----------------------------------------------------------------------------
# 8. EXECUTIVE DATA SUMMARY TABLE
# -----------------------------------------------------------------------------
st.markdown('<div class="section-heading">📋 Platform Performance & Mental Wellbeing Summary</div>', unsafe_allow_html=True)

summary_df = (
    filtered_df.groupby("Primary_Platform")
    .agg(
        Total_Users=("User_ID", "count"),
        Avg_Daily_Hours=("Daily_Usage_Hours", "mean"),
        Avg_Wellbeing=("Mental_Wellbeing_Score", "mean"),
        Avg_Anxiety=("Anxiety_Score", "mean"),
        Avg_Sleep_Hrs=("Sleep_Hours", "mean"),
        High_Severe_Pct=("Addiction_Level", lambda x: x.isin(["High", "Severe"]).mean() * 100),
    )
    .round(2)
    .sort_values(by="High_Severe_Pct", ascending=False)
    .reset_index()
)

summary_df.columns = [
    "Platform",
    "Total Users",
    "Avg. Daily Usage (Hrs)",
    "Mental Wellbeing (1-10)",
    "Anxiety Score (1-10)",
    "Avg. Sleep (Hrs)",
    "High/Severe Addiction (%)",
]

st.dataframe(summary_df, use_container_width=True, hide_index=True)
