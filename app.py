import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Witness Archive – ICE Raids Dashboard",
    layout="wide",
)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("dataset_500_2015_2025_FINAL.csv")

    # Parse date column
    if "Publication Date" in df.columns:
        df["Publication Date"] = pd.to_datetime(df["Publication Date"], errors="coerce")
        df["Year"] = df["Publication Date"].dt.year
    else:
        df["Year"] = None

    return df

df = load_data()

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.title("Filters")

# Year filter
if df["Year"].notna().any():
    year_min = int(df["Year"].min())
    year_max = int(df["Year"].max())
    year_range = st.sidebar.slider("Year Range", year_min, year_max, (year_min, year_max))
else:
    year_range = (None, None)

# Sources
sources = sorted(df["Source"].fillna("").unique())
selected_sources = st.sidebar.multiselect("Sources", sources, default=sources)

# Emotions
emotions = sorted(df["Emotion Label"].fillna("").unique())
selected_emotions = st.sidebar.multiselect("Emotions", emotions, default=emotions)

# Themes
themes = sorted(df["Thematic Label"].fillna("").unique())
selected_themes = st.sidebar.multiselect("Themes", themes, default=themes)

# ---------------------------------------------------------
# FILTER APPLY
# ---------------------------------------------------------
filtered = df.copy()

if year_range[0] is not None:
    filtered = filtered[
        (filtered["Year"] >= year_range[0]) & (filtered["Year"] <= year_range[1])
    ]

filtered = filtered[filtered["Source"].isin(selected_sources)]
filtered = filtered[filtered["Emotion Label"].isin(selected_emotions)]
filtered = filtered[filtered["Thematic Label"].isin(selected_themes)]

# ---------------------------------------------------------
# HEADER + DESCRIPTION
# ---------------------------------------------------------
st.title("Witness Archive Dashboard – ICE Raids in Chicago")
st.markdown("""
This dashboard visualizes **public emotions, themes, and media reporting**
on ICE raids in Chicago from **2015–2025**.
""")

# ---------------------------------------------------------
# KPIs
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Articles", len(df))
col2.metric("Filtered Articles", len(filtered))
col3.metric("Sources", filtered["Source"].nunique())
col4.metric("Years", filtered["Year"].nunique())

st.markdown("---")

# ---------------------------------------------------------
# EMOTION DISTRIBUTION CHART
# ---------------------------------------------------------
if len(filtered) > 0:
    emotion_counts = filtered.groupby("Emotion Label")["Title"].count().reset_index()
    fig_emotion = px.bar(
        emotion_counts,
        x="Emotion Label",
        y="Title",
        title="Emotion Distribution"
    )
    st.plotly_chart(fig_emotion, use_container_width=True)
else:
    st.warning("No articles match your filter selection.")

st.markdown("---")

# ---------------------------------------------------------
# ARTICLE VIEWER (NO QUOTES VERSION)
# ---------------------------------------------------------
st.header("Articles (Title + Link + Summary)")

max_show = st.slider("Articles to display", 5, 100, 20)

for _, row in filtered.head(max_show).iterrows():
    title = row.get("Title", "Untitled")
    url = row.get("URL", "")
    summary = row.get("Summary", "")
    emotion = row.get("Emotion Label", "")
    theme = row.get("Thematic Label", "")
    source = row.get("Source", "")
    pub_date = row.get("Publication Date", "")

    # Clean date text
    date_text = ""
    if isinstance(pub_date, pd.Timestamp):
        date_text = pub_date.date().isoformat()

    header = f"{title} — {source} {f'({date_text})' if date_text else ''}"

    with st.expander(header):
