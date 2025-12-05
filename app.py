# ---------------------------------------------------------
# ARTICLE VIEWER (FIXED INDENTATION)
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

    # Date formatting
    date_text = ""
    if isinstance(pub_date, pd.Timestamp):
        date_text = pub_date.date().isoformat()

    # Header of expander
    header = f"{title} — {source} {f'({date_text})' if date_text else ''}"

    with st.expander(header):
        # CLICKABLE LINK
        if isinstance(url, str) and url.startswith("http"):
            st.markdown(f"[Open full article]({url})")

        st.markdown("### Summary")
        st.write(summary)

        st.markdown(f"**Emotion:** {emotion}")
        st.markdown(f"**Theme:** {theme}")
