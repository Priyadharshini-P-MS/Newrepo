# ---------------------------------------------------------
# Article explorer (EMERGENCY FIX — SAFE VERSION)
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
    title = row.get("Title", "Untitled")
    url = row.get("URL", "")            # <-- FIXED (no crashing)
    summary = row.get("Summary", "")
    emotion = row.get("Emotion Label", "")
    theme = row.get("Thematic Label", "")
    pub_date = row.get("Publication Date", "")
    source = row.get("Source", "")

    date_text = ""
    if pd.notna(pub_date):
        try:
            date_text = str(pub_date.date())
        except:
            date_text = ""

    header = f"{title} — {source} {('('+date_text+')' if date_text else '')}"

    with st.expander(header):
        # clickable URL (safe check)
        if isinstance(url, str) and url.startswith("http"):
            st.markdown(f"[Open article]({url})")

        st.markdown("**Summary:**")
        st.write(summary)

        st.markdown(f"**Emotion:** {emotion}")
        st.markdown(f"**Theme:** {theme}")
