import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# Page config
# ---------------------------------------------------------
st.set_page_config(
    page_title="Witness Archive – ICE Raids Emotion Dashboard",
    layout="wide",
)

# ---------------------------------------------------------
# Data loading
# ---------------------------------------------------------
@st.cache_data
def load_data(csv_path: str):
    df = pd.read_csv(csv_path)

    # Parse publication date
    if "Publication Date" in df.columns:
        df["Publication Date"] = pd.to_datetime(df["Publication Date"], errors="coerce")
        df["Year"] = df["Publication Date"].dt.year
    else:
        df["Year"] = None

    # Ensure required columns exist
    for col in ["Title", "URL", "Source", "Summary", "Emotion Label", "Thematic Label"]:
        if col not in df.columns:
            df[col] = ""

    return df


DATA_PATH = "dataset_500_2015_2025_FINAL.csv"
df = load_data(DATA_PATH)

# ---------------------------------------------------------
# Sidebar – Filters
# ---------------------------------------------------------
st.sidebar.title("Filters")

# Year filter
if df["Year"].notna().any():
    min_year = int(df["Year"].min())
    max_year = int(df["Year"].max())
    year_range = st.sidebar.slider(
        "Publication year range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )
else:
    year_range = (None, None)

# Source filter
sources = sorted(df["Source"].dropna().unique().tolist())
selected_sources = st.sidebar.multiselect(
    "News source",
    options=sources,
    default=sources,
)

# Emotion filter
emotions = sorted(df["Emotion Label"].dropna().unique().tolist())
selected_emotions = st.sidebar.multiselect(
    "Emotion label",
    options=emotions,
    default=emotions,
)

# Thematic label filter
themes = sorted(df["Thematic Label"].dropna().unique().unique().tolist())
selected_themes = st.sidebar.multiselect(
    "Thematic label",
    options=themes,
    default=themes,
)

# ---------------------------------------------------------
# Apply filters
# ---------------------------------------------------------
filtered = df.copy()

if year_range[0] is not None:
    filtered = filtered[
        (filtered["Year"] >= year_range[0]) & (filtered["Year"] <= year_range[1])
    ]

if selected_sources:
    filtered = filtered[filtered["Source"].isin(selected_sources)]

if selected_emotions:
    filtered = filtered[filtered["Emotion Label"].isin(selected_emotions)]

if selected_themes:
    filtered = filtered[filtered["Thematic Label"].isin(selected_themes)]

filtered = filtered.reset_index(drop=True)

# ---------------------------------------------------------
# Header / Intro
# ---------------------------------------------------------
st.title("Witness Archive: Public Emotions on ICE Raids in Chicago (2015–2025)")

st.markdown("""
This dashboard visualizes **public emotions** expressed in news coverage 
and testimonies related to ICE raids in Chicago between **2015 and 2025**.
""")

# ---------------------------------------------------------
# KPI cards
# ---------------------------------------------------------
total_articles = len(df)
visible_articles = len(filtered)
unique_sources = filtered["Source"].nunique()
unique_years = filtered["Year"].nunique()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total articles", total_articles)
c2.metric("Visible articles", visible_articles)
c3.metric("Sources", unique_sources)
c4.metric("Years in view", unique_years)

st.markdown("---")

# ---------------------------------------------------------
# Charts
# ---------------------------------------------------------
if visible_articles == 0:
    st.warning("No articles match the current filters.")
else:
    col1, col2 = st.columns(2)

    # Emotion distribution
    with col1:
        st.subheader("Emotion distribution")
        emotion_counts = (
            filtered.groupby("Emotion Label")["Title"]
            .count()
            .reset_index(name="Count")
            .sort_values("Count", ascending=False)
        )
        fig_emotion = px.bar(
            emotion_counts,
            x="Emotion Label",
            y="Count",
            title="Number of articles per emotion"
        )
        st.plotly_chart(fig_emotion, use_container_width=True)

    # Emotion timeline
    with col2:
        st.subheader("Emotion trend over time")
        if filtered["Publication Date"].notna().any():
            timeline = (
                filtered.groupby(["Year", "Emotion Label"])["Title"]
                .count()
                .reset_index(name="Count")
            )
            fig_timeline = px.line(
                timeline,
                x="Year",
                y="Count",
                color="Emotion Label",
                markers=True,
                title="Emotion-labelled articles per year"
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.info("Timeline not available because dates are missing.")

st.markdown("---")

# ---------------------------------------------------------
# Article explorer
# ---------------------------------------------------------
st.subheader("Article Browser (Title + Link + Summary)")

max_show = st.slider(
    "Articles to display",
    min_value=5,
    max_value=100,
    value=25,
    step=5
)

for _, row in filtered.head(max_show).iterrows():
    title = row["Title"]
    url = row["URL]()
