# frontend/streamlit_app.py

import requests
import streamlit as st

BACKEND_URL = "http://localhost:8000"


# ─── Session State Initialization ────────────────────────────────────────────

def _init_state() -> None:
    """Initialize all session state keys with default values."""
    defaults = {
        "topics": [],
        "suggestions": [],
        "history": [],       # stored locally in session state
        "feedback": [],      # stored locally in session state
        "fact_summary": "",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


# ─── API Helpers ──────────────────────────────────────────────────────────────

def _api_post(path: str, payload: dict) -> tuple:
    """POST to the FastAPI backend and return (data, error)."""
    try:
        response = requests.post(f"{BACKEND_URL}{path}", json=payload, timeout=60)
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as exc:
        return None, str(exc)


def _parse_interests(raw_interests: str) -> list:
    """Convert comma-separated interests string to a list of strings."""
    return [item.strip() for item in raw_interests.split(",") if item.strip()]


# ─── Feedback (local only — no /feedback endpoint in backend) ────────────────

def _save_feedback(suggestion: str, rating: str) -> None:
    """Save feedback locally in session state (no backend endpoint for feedback)."""
    entry = {"suggestion": suggestion, "rating": rating}
    st.session_state.feedback.insert(0, entry)
    st.toast("Feedback saved!")


# ─── Tab 1: Generate ─────────────────────────────────────────────────────────

def render_generate_tab() -> None:
    st.subheader("Conversation Starter Generator")

    description = st.text_area(
        "Event description",
        value="AI for Sustainable Cities",
        height=120,
        placeholder="Describe the event, panel, meetup, or networking session.",
    )
    interests = st.text_input(
        "Your interests (comma separated)",
        value="climate change, urban planning",
        placeholder="Example: climate change, urban planning",
    )

    if st.button("Generate conversation starters", type="primary", use_container_width=True):
        payload = {
            "description": description,
            "interests": _parse_interests(interests),
        }
        with st.spinner("Generating starters using DistilBERT + GPT-2..."):
            # POST /generate-conversation → ConversationResponse {topics, suggestions}
            data, error = _api_post("/generate-conversation", payload)

        if error:
            st.error("Backend is not reachable. Start FastAPI on http://localhost:8000 and try again.")
            st.caption(error)
        else:
            st.session_state.topics = data.get("topics", [])
            st.session_state.suggestions = data.get("suggestions", [])

            # Save to local history in session state
            history_entry = {
                "description": description,
                "interests": _parse_interests(interests),
                "topics": st.session_state.topics,
                "suggestions": st.session_state.suggestions,
            }
            st.session_state.history.insert(0, history_entry)

    # Display results
    if st.session_state.topics:
        st.markdown("**Detected themes**")
        st.write(", ".join(st.session_state.topics))

    if st.session_state.suggestions:
        st.markdown("**Generated starters**")
        for index, suggestion in enumerate(st.session_state.suggestions, start=1):
            with st.container(border=True):
                st.write(suggestion)
                col_up, col_down = st.columns(2)
                if col_up.button("👍 Thumbs up", key=f"up_{index}", use_container_width=True):
                    _save_feedback(suggestion, "positive")
                if col_down.button("👎 Thumbs down", key=f"down_{index}", use_container_width=True):
                    _save_feedback(suggestion, "negative")


# ─── Tab 2: Fact Check ────────────────────────────────────────────────────────

def render_fact_check_tab() -> None:
    st.subheader("Fact Check")
    st.caption("Verify a topic using the Wikipedia API.")

    query = st.text_input("Topic to verify", value="blockchain in healthcare")

    if st.button("Check facts", type="primary", use_container_width=True):
        with st.spinner("Checking Wikipedia..."):
            # POST /fact-check → FactCheckResponse {summary}
            data, error = _api_post("/fact-check", {"query": query})

        if error:
            st.error("Fact-checking needs the backend to be running.")
            st.caption(error)
        else:
            st.session_state.fact_summary = data.get("summary", "")

    if st.session_state.fact_summary:
        st.info(st.session_state.fact_summary)


# ─── Tab 3: Conversation History ─────────────────────────────────────────────

def render_history_tab() -> None:
    st.subheader("Conversation History")
    st.caption("All conversation starters generated in this session.")

    # History stored locally in session state (no /history endpoint in backend)
    if not st.session_state.history:
        st.caption("No generated conversations yet. Go to Generate tab to create some.")
        return

    for item in st.session_state.history:
        with st.container(border=True):
            st.markdown(f"**Event:** {item.get('description', 'Untitled event')}")
            interests_list = item.get("interests", [])
            if interests_list:
                st.caption("Interests: " + ", ".join(interests_list))
            themes = item.get("topics", [])
            if themes:
                st.caption("Themes: " + ", ".join(themes))
            for suggestion in item.get("suggestions", []):
                st.write(f"- {suggestion}")


# ─── Tab 4: Feedback History ──────────────────────────────────────────────────

def render_feedback_tab() -> None:
    st.subheader("Feedback History")
    st.caption("All thumbs up / thumbs down feedback given in this session.")

    # Feedback stored locally in session state (no /feedback endpoint in backend)
    if not st.session_state.feedback:
        st.caption("No feedback submitted yet. Rate some suggestions in the Generate tab.")
        return

    for item in st.session_state.feedback:
        with st.container(border=True):
            rating = item.get("rating", "")
            icon = "👍" if rating == "positive" else "👎"
            st.markdown(f"**{icon} {rating.title()}**")
            st.write(item.get("suggestion", ""))


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    st.set_page_config(
        page_title="Personalized Networking Assistant",
        page_icon="🤝",
        layout="wide",
    )
    _init_state()

    st.title("🤝 Personalized Networking Assistant")
    st.caption("Generate tailored conversation starters for professional networking events.")

    tabs = st.tabs(["🧠 Generate", "✅ Fact Check", "📜 Conversation History", "👍 Feedback History"])
    with tabs[0]:
        render_generate_tab()
    with tabs[1]:
        render_fact_check_tab()
    with tabs[2]:
        render_history_tab()
    with tabs[3]:
        render_feedback_tab()


if __name__ == "__main__":
    main()