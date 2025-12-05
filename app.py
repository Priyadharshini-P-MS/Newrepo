import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Witness Archive Dashboard", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("dataset_500_2015_2025_FINAL.csv")
    df["Publication Date"] = pd.to_datetime(df["Publication Date"], errors="coerce")
    df["Year"] = df["Publication Date"].dt.year
    return df

df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.title("Filters")

year_min = int(df["Year"].min())
year_max = int(df["Year"].max())
year_range = st.sidebar.slider("Year Range", year_min, year_max, (year_min, year_max))

sources = sorted(df["Source"].fillna("").unique())
selected_sources = st.sidebar.multiselect("Sources", sources, default=sources)

emotions = sorted(df["Emotion Label"].fillna("").unique())
selected_emotions = st.sidebar.multiselect("Emotions", emotions, default=emotions)

themes = sorted(df["Thematic Label"].fillna("").unique())
selected_themes = st.sidebar.multiselect("Themes", themes, default=themes)

# -----------------------------
# APPLY FILTERS
# -----------------------------
filtered = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1]) &
    (df["Source"].isin(selected_sources)) &
    (df["Emotion Label"].isin(selected_emotions)) &
    (df["Thematic Label"].isin(selected_themes))
]

# -----------------------------
# HEADER
# -----------------------------
st.title("Witness Archive: ICE Raids Dashboard (2015–2025)")

# -----------------------------
# EMOTION CHART
# -----------------------------
if len(filtered) > 0:
    emotion_counts = filtered.groupby("Emotion Label")["Title"].count().reset_index()
    fig = px.bar(emotion_counts, x="Emotion Label", y="Title", title="Emotion Distribution")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No articles match your filters.")

st.markdown("---")

# -----------------------------
# ARTICLE VIEWER
# -----------------------------
st.header("Articles (Title + Link + Summary)")

max_show = st.slider("Articles to Display", 5, 100, 20)

for _, row in filtered.head(max_show).iterrows():
    title = row["Title"]
    url = row["URL"]
    summary = row["Summary"]
    emotion = row["Emotion Label"]
    theme = row["Thematic Label"]
    source = row["Source"]
    pub = row["Publication Date"]

    date_txt = pub.date().isoformat() if pd.notna(pub) else ""

    header = f"{title} — {source} ({date_txt})"

    with st.expander(header):
        if isinstance(url, str) and url.startswith("http"):
            st.markdown(f"[Open article]({url})")

        st.markdown("### Summary")
        st.write(summary)

        st.write(f"**Emotion:** {emotion}")
        st.write(f"**Theme:** {theme}")
