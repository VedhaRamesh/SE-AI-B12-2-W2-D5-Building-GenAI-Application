
import os
import re

import streamlit as st
from dotenv import load_dotenv

from breakfast import stream_breakfast_ideas


# Load API configuration from .env
load_dotenv()

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Healthy Breakfast AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Custom styling
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            135deg,
            #f5fff8 0%,
            #f4f7ff 100%
        );
    }

    .main-title {
        font-size: 2.7rem;
        font-weight: 800;
        color: #176b4d;
        text-align: center;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #53665d;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }

    .breakfast-card {
        background: white;
        border: 1px solid #dcefe4;
        border-radius: 16px;
        padding: 20px;
        min-height: 150px;
        box-shadow: 0 4px 14px rgba(25, 80, 55, 0.07);
        margin-bottom: 16px;
    }

    .breakfast-number {
        color: #18845b;
        font-weight: 700;
        font-size: 0.9rem;
    }

    .breakfast-name {
        color: #173d2d;
        font-size: 1.15rem;
        font-weight: 700;
        margin: 8px 0;
    }

    .breakfast-description {
        color: #4d5c54;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Application heading
# --------------------------------------------------
st.markdown(
    '<div class="main-title">🥗 Healthy Breakfast AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Discover five healthy breakfast ideas tailored to your taste."
    "</div>",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Sidebar: configuration and preferences
# --------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    st.subheader("🔐 API Configuration")

    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    langsmith_key = os.getenv("LANGSMITH_API_KEY", "").strip()

    tracing_enabled = (
        os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
    )

    if openai_key:
        st.success("OpenAI API key loaded from .env")
    else:
        st.error("OPENAI_API_KEY is missing from .env")

    if tracing_enabled and langsmith_key:
        st.info("LangSmith tracing is enabled")
    else:
        st.caption("LangSmith tracing is disabled")

    st.divider()

    st.subheader("🍽️ Your Preferences")

    diet = st.selectbox(
        "Dietary preference",
        [
            "Vegetarian",
            "Vegan",
            "High-protein",
            "Non-vegetarian",
        ],
    )

    cuisine = st.selectbox(
        "Preferred cuisine",
        [
            "South Indian",
            "North Indian",
            "International",
            "Any cuisine",
        ],
    )

    priority = st.selectbox(
        "Health priority",
        [
            "Balanced nutrition",
            "High protein",
            "High fiber",
            "Quick preparation",
            "Lower added sugar",
        ],
    )

    st.caption("API keys are loaded from your local .env file.")

# --------------------------------------------------
# Parse the five numbered ideas
# --------------------------------------------------
def parse_ideas(text: str) -> list[tuple[str, str]]:
    """Extract numbered breakfast titles and descriptions."""

    pattern = re.compile(
        r"(?m)^\s*(?:\*\*)?([1-5])[.)]\s+"
        r"(?:\*\*)?(.+?)(?:\*\*)?\s*[—–-]\s*(.+?)\s*$"
    )

    ideas = []

    for match in pattern.finditer(text):
        number, title, description = match.groups()

        if int(number) != len(ideas) + 1:
            continue

        ideas.append(
            (
                title.strip().strip("*"),
                description.strip().strip("*"),
            )
        )

    return ideas


# --------------------------------------------------
# Session state
# --------------------------------------------------
if "ideas" not in st.session_state:
    st.session_state.ideas = []

if "last_preferences" not in st.session_state:
    st.session_state.last_preferences = None

# --------------------------------------------------
# Generate button
# --------------------------------------------------
left, center, right = st.columns([1, 2, 1])

with center:
    generate_clicked = st.button(
        "✨ Generate My 5 Breakfast Ideas",
        type="primary",
        use_container_width=True,
    )

# --------------------------------------------------
# Stream the AI response
# --------------------------------------------------
if generate_clicked:
    if not openai_key:
        st.error("Please configure OPENAI_API_KEY in your .env file.")

    elif tracing_enabled and not langsmith_key:
        st.error(
            "Enter your LangSmith API key or disable tracing in .env."
        )

    else:
        try:
            # Configure LangSmith tracing.
            if tracing_enabled:
                os.environ["LANGSMITH_API_KEY"] = langsmith_key
                os.environ["LANGSMITH_TRACING"] = "true"
                os.environ["LANGSMITH_PROJECT"] = "healthy-breakfast-ai"
            else:
                os.environ["LANGSMITH_TRACING"] = "false"
                os.environ.pop("LANGSMITH_API_KEY", None)

            # Stream text into a temporary placeholder.
            response_placeholder = st.empty()

            with st.spinner("🥑 Preparing your breakfast ideas..."):
                response = response_placeholder.write_stream(
                    stream_breakfast_ideas(
                        api_key=openai_key,
                        diet=diet,
                        cuisine=cuisine,
                        priority=priority,
                    )
                )

            # Remove the temporary text after streaming completes.
            response_placeholder.empty()

            # Parse the completed response.
            ideas = parse_ideas(response)

            if len(ideas) != 5:
                st.error(
                    "The AI response did not contain exactly five "
                    "recognizable ideas. Please try generating again."
                )
            else:
                st.session_state.ideas = ideas
                st.session_state.last_preferences = (
                    diet,
                    cuisine,
                    priority,
                )

                st.success("Your five breakfast ideas are ready!")

        except ValueError as exc:
            st.error(str(exc))

        except Exception:
            st.error(
                "Unable to generate ideas. Check your API key, "
                "account access, network connection, and model "
                "availability, then try again. "
                "Check the terminal for technical details."
            )

# --------------------------------------------------
# Display the five breakfast cards
# --------------------------------------------------
if st.session_state.ideas:
    st.divider()
    st.subheader("🍳 Your Breakfast Collection")

    previous_preferences = st.session_state.last_preferences

    if previous_preferences:
        st.caption(
            f"Diet: {previous_preferences[0]} · "
            f"Cuisine: {previous_preferences[1]} · "
            f"Priority: {previous_preferences[2]}"
        )

    cards = st.columns(2)

    for index, (title, description) in enumerate(
        st.session_state.ideas
    ):
        with cards[index % 2]:
            st.markdown(
                f"""
                <div class="breakfast-card">
                    <div class="breakfast-number">
                        BREAKFAST #{index + 1}
                    </div>
                    <div class="breakfast-name">
                        {title}
                    </div>
                    <div class="breakfast-description">
                        {description}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if st.button("🔄 Clear Results"):
        st.session_state.ideas = []
        st.session_state.last_preferences = None
        st.rerun()

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "🥗 Nutrition information is general guidance. "
    "Adjust ingredients to your individual needs."
)
