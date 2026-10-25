import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

st.set_page_config(
    page_title="CodePilot AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_KEY = os.getenv("GEMMA_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["GEMMA_API_KEY"]
    except Exception:
        API_KEY = None

MODEL_NAME = "gemma-4-26b-a4b-it"


SYSTEM_PROMPT = """
You are CodePilot AI, an expert AI coding assistant.

You help developers explain code, generate functions and programs,
debug programming errors, review code, refactor code, and explain
time and space complexity.

Be technically accurate, clear, structured, practical, and focused
on the user's programming language.

When generating code:
- Use correct syntax and maintainable patterns.
- Explain important decisions.
- Mention edge cases when relevant.

When debugging:
- Identify the likely root cause.
- Explain why the error happens.
- Provide corrected code.
- Explain the fix.

Never claim code was executed or tested unless it actually was.
"""


# =========================================================
# UI STYLING
# =========================================================

st.markdown(
    """
    <style>
    :root {
        --page: #f6f8fc;
        --surface: #ffffff;
        --text: #172033;
        --muted: #64748b;
        --border: #e2e8f0;
        --accent: #4f46e5;
        --accent-hover: #4338ca;
    }

    .stApp {
        background: var(--page);
        color: var(--text);
    }

    .block-container {
        max-width: 1440px;
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
    }

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    h1, h2, h3, h4 {
        color: var(--text) !important;
        letter-spacing: -0.035em;
    }

    p, label, .stMarkdown {
        color: #475569;
    }

    [data-testid="stWidgetLabel"] p {
        color: #334155 !important;
        font-weight: 600;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] {
        background: #ffffff !important;
        color: #172033 !important;
        border: 1px solid #dbe2ea !important;
        border-radius: 10px !important;
    }

    .stTextArea textarea {
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
        font-size: 0.9rem;
        line-height: 1.55;
    }

    .stTextArea textarea:focus,
    .stTextInput input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.10) !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        background: var(--accent);
        color: #ffffff;
        border: 1px solid var(--accent);
        border-radius: 10px;
        min-height: 2.7rem;
        font-weight: 600;
        transition: background 0.15s ease, transform 0.15s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: var(--accent-hover);
        border-color: var(--accent-hover);
        color: #ffffff;
        transform: translateY(-1px);
    }

    .stButton > button:focus,
    .stDownloadButton > button:focus {
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
    }

    .hero {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 28px 30px;
        margin-bottom: 22px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.035);
    }

    .hero-label {
        color: var(--accent);
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .hero-title {
        color: var(--text);
        font-size: clamp(2rem, 4vw, 2.8rem);
        line-height: 1.12;
        font-weight: 800;
        letter-spacing: -0.055em;
        margin: 0 0 10px 0;
    }

    .hero-subtitle {
        color: var(--muted);
        font-size: 1rem;
        margin: 0;
        line-height: 1.6;
    }

    .section-label {
        color: #334155;
        font-size: 0.96rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .section-caption {
        color: #94a3b8;
        font-size: 0.82rem;
        margin-bottom: 0.8rem;
    }

    .feature-card {
        height: 100%;
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.025);
    }

    .feature-card h4 {
        color: var(--text);
        font-size: 0.98rem;
        font-weight: 700;
        margin: 0 0 7px 0;
        letter-spacing: -0.02em;
    }

    .feature-card p {
        color: var(--muted);
        font-size: 0.86rem;
        line-height: 1.5;
        margin: 0;
    }

    .response-panel {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 18px;
    }

    .stCodeBlock {
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    hr {
        border-color: var(--border);
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 1rem 2rem 1rem;
        }

        .hero {
            padding: 22px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# API CLIENT
# =========================================================

if not API_KEY:
    st.error(
        "Gemma API key is missing. Add GEMMA_API_KEY to your .env "
        "file locally or to Streamlit Secrets when deployed."
    )
    st.stop()

client = genai.Client(api_key=API_KEY)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "code_input" not in st.session_state:
    st.session_state.code_input = ""

if "question_input" not in st.session_state:
    st.session_state.question_input = ""

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "Explain Code"

if "selected_language" not in st.session_state:
    st.session_state.selected_language = "Python"

if "latest_answer" not in st.session_state:
    st.session_state.latest_answer = ""


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-label">⚡ CodePilot AI · Powered by Gemma</div>
        <div class="hero-title">Your AI coding companion.</div>
        <p class="hero-subtitle">
            Understand code. Fix bugs. Build better software.
            A focused workspace for your everyday coding challenges.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# PROMPT BUILDER
# =========================================================

def build_prompt(mode, language, code, question):
    instructions = {
        "Explain Code": """
Explain the supplied code step by step. Describe its purpose,
important variables, control flow, and output.
""",
        "Generate Code": """
Generate clean, correct, maintainable code for the requested
functionality. Include a brief explanation and relevant edge cases.
""",
        "Debug Code": """
Analyze the supplied code and error. Identify the root cause,
explain the error, and provide corrected code.
""",
        "Review Code": """
Perform a code review. Identify bugs, readability problems,
security concerns, and performance issues. Prioritize findings.
""",
        "Improve Code": """
Refactor the supplied code. Improve readability, maintainability,
and efficiency without changing intended behavior. Explain changes.
""",
    }

    return f"""
{SYSTEM_PROMPT}

TASK:
{instructions[mode]}

PROGRAMMING LANGUAGE:
{language}

USER REQUEST:
{question or "Please help with the selected task."}

CODE:
```{language.lower()}
{code}
```

Respond with useful technical detail.
Use Markdown and fenced code blocks where appropriate.
"""


# =========================================================
# EXAMPLES
# =========================================================

EXAMPLES = {
    "Explain code": {
        "mode": "Explain Code",
        "language": "Python",
        "code": """def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)""",
        "question": "Explain this factorial function step by step.",
    },
    "Debug code": {
        "mode": "Debug Code",
        "language": "Python",
        "code": """numbers = [10, 20, 30]
print(numbers[3])""",
        "question": "Find the error and provide corrected code.",
    },
    "Review code": {
        "mode": "Review Code",
        "language": "Python",
        "code": """def find_max(numbers):
    max_value = 0
    for number in numbers:
        if number > max_value:
            max_value = number
    return max_value""",
        "question": "Review this function for bugs and edge cases.",
    },
}


def load_example(example_name):
    example = EXAMPLES[example_name]
    st.session_state["selected_mode"] = example["mode"]
    st.session_state["selected_language"] = example["language"]
    st.session_state["code_input"] = example["code"]
    st.session_state["question_input"] = example["question"]


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("## ⚙️ Workspace")
    st.caption("Configure your coding assistant.")

    mode = st.selectbox(
        "AI tool",
        [
            "Explain Code",
            "Generate Code",
            "Debug Code",
            "Review Code",
            "Improve Code",
        ],
        key="selected_mode",
    )

    language = st.selectbox(
        "Programming language",
        [
            "Python",
            "Java",
            "JavaScript",
            "C++",
            "TypeScript",
            "Go",
            "SQL",
            "Other",
        ],
        key="selected_language",
    )

    st.divider()

    st.markdown("#### Model")
    st.markdown("**Google Gemma 4**")
    st.caption("Hosted Gemma API inference")

    st.divider()

    if st.button("Clear workspace", use_container_width=True):
        st.session_state.messages = []
        st.session_state.code_input = ""
        st.session_state.question_input = ""
        st.session_state.latest_answer = ""
        st.rerun()


# =========================================================
# WELCOME / EXAMPLE CARDS
# =========================================================

if (
    not st.session_state.code_input.strip()
    and not st.session_state.question_input.strip()
):
    st.markdown(
        """
        <div style="text-align:center; padding: 6px 0 18px 0;">
            <h2 style="font-size:1.8rem; margin-bottom:8px;">
                What are we working on?
            </h2>
            <p style="color:#64748b; margin:0;">
                Start with an example or paste your code below.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    example_columns = st.columns(3)
    example_names = ["Explain code", "Debug code", "Review code"]
    example_descriptions = [
        "Understand code step by step.",
        "Find the cause and fix errors.",
        "Spot bugs and improve quality.",
    ]

    for column, name, description in zip(
        example_columns, example_names, example_descriptions
    ):
        with column:
            st.markdown(
                f"""
                <div class="feature-card">
                    <h4>{name}</h4>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.button(
                f"Try {name}",
                key=f"example_{name}",
                use_container_width=True,
                on_click=load_example,
                args=(name,),
            )


# =========================================================
# MAIN WORKSPACE
# =========================================================

left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("### Your code")
    st.caption(f"Write or paste your {language} code.")

    code = st.text_area(
        "Code input",
        height=330,
        placeholder="Paste your code here...",
        key="code_input",
        label_visibility="collapsed",
    )

    st.markdown("### Instructions")
    question = st.text_area(
        "What should CodePilot do?",
        height=105,
        placeholder=(
            "For example: Explain this code, find the bug, "
            "or suggest a more efficient solution."
        ),
        key="question_input",
        label_visibility="collapsed",
    )

    submit = st.button(
        "⚡ Run with Gemma",
        type="primary",
        use_container_width=True,
    )

with right:
    st.markdown("### AI response")
    st.caption("Your explanation, code, or review will appear here.")

    if submit:
        if not code.strip() and not question.strip():
            st.warning("Add some code or describe what you want to build.")
        else:
            prompt = build_prompt(mode, language, code, question)

            with st.spinner("Gemma is thinking through your request..."):
                try:
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.2,
                            max_output_tokens=4096,
                        ),
                    )

                    answer = response.text or (
                        "Gemma returned an empty response. Please try again."
                    )

                    st.session_state.latest_answer = answer
                    st.session_state.messages.append(
                        {
                            "mode": mode,
                            "question": question or "No additional instructions",
                            "answer": answer,
                        }
                    )

                except Exception as error:
                    st.error(
                        "Gemma API request failed. Check your API key, "
                        "model access, and internet connection."
                    )
                    st.caption(str(error))

    if st.session_state.latest_answer:
        st.markdown(
            '<div class="response-panel">',
            unsafe_allow_html=True,
        )
        st.markdown(st.session_state.latest_answer)
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            "Download response",
            data=st.session_state.latest_answer,
            file_name="codepilot_response.md",
            mime="text/markdown",
            use_container_width=True,
        )
    else:
        st.markdown(
            """
            <div class="feature-card">
                <h4>Ready when you are</h4>
                <p>
                    Submit your code to get a clear explanation,
                    debugging help, code review, or an improved solution.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# RECENT ACTIVITY
# =========================================================

if st.session_state.messages:
    st.divider()
    st.markdown("### Recent activity")

    for item in reversed(st.session_state.messages[-5:]):
        title = f"{item['mode']} · {item['question'][:65]}"
        with st.expander(title):
            st.markdown(item["answer"])


# =========================================================
# FOOTER
# =========================================================

st.divider()
st.markdown(
    """
    <div style="text-align:center; color:#94a3b8; font-size:0.82rem;">
        Built with Streamlit and Google Gemma 4
        <br>
        CodePilot AI · Your coding companion
    </div>
    """,
    unsafe_allow_html=True,
)
