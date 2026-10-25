
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(
    page_title="CodePilot AI",
    page_icon="🚀",
    layout="wide"
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

You help developers:
- Explain code clearly.
- Generate functions and programs.
- Debug programming errors.
- Review code and suggest improvements.
- Refactor code for readability and efficiency.
- Explain time and space complexity.

Your answers must be:
- Technically accurate.
- Clear and structured.
- Practical and useful.
- Focused on the user's programming language.

When generating code:
1. Use correct syntax.
2. Prefer readable and maintainable code.
3. Explain important decisions.
4. Mention edge cases when relevant.

When debugging:
1. Identify the likely cause.
2. Explain why the error happens.
3. Provide corrected code.
4. Explain the fix.

Never claim that code was executed or tested unless
it actually was.
"""

if not API_KEY:
    st.error(
        "Gemma API key is missing. "
        "Add GEMMA_API_KEY to your .env file."
    )
    st.stop()

client = genai.Client(api_key=API_KEY)

# ----------------------------
# Styling
# ----------------------------

st.markdown("""
<style>
    .main {
        background-color: #0b1020;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }

    .hero {
        padding: 24px;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            #111827,
            #172554
        );
        border: 1px solid #26344d;
        margin-bottom: 24px;
    }

    .hero h1 {
        color: #f8fafc;
        font-size: 42px;
        margin-bottom: 4px;
    }

    .hero p {
        color: #94a3b8;
        font-size: 16px;
    }

    .stButton button {
        border-radius: 10px;
        font-weight: 600;
    }

    .stTextArea textarea {
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------

st.markdown("""
<div class="hero">
    <h1> CodePilot AI</h1>
    <p>
        Your intelligent coding partner.
        Explain, debug, generate, and improve code
        with Google Gemma 4.
    </p>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar
# ----------------------------

with st.sidebar:
    st.title("⚙️ Workspace")

    mode = st.selectbox(
        "Choose an AI tool",
        [
            "Explain Code",
            "Generate Code",
            "Debug Code",
            "Review Code",
            "Improve Code"
        ]
    )

    language = st.selectbox(
        "Programming Language",
        [
            "Python",
            "Java",
            "JavaScript",
            "C++",
            "TypeScript",
            "Go",
            "SQL",
            "Other"
        ]
    )

    st.divider()

    st.markdown("### Powered by")
    st.markdown("**Google Gemma 4**")

    st.caption(
        "AI inference through the hosted Gemma API."
    )

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# ----------------------------
# Session State
# ----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# Prompt Builder
# ----------------------------

def build_prompt(mode, language, code, question):

    instructions = {
        "Explain Code": """
Explain the supplied code step by step.
Describe its purpose, important variables,
control flow, and output.
""",

        "Generate Code": """
Generate clean, correct, and maintainable code
for the requested functionality.
Include a brief explanation and relevant edge cases.
""",

        "Debug Code": """
Analyze the supplied code and error.
Identify the root cause, explain the error,
and provide corrected code.
""",

        "Review Code": """
Perform a code review.
Identify bugs, readability problems,
security concerns, and performance issues.
Prioritize the most important findings.
""",

        "Improve Code": """
Refactor the supplied code.
Improve readability, maintainability,
and efficiency without changing its intended behavior.
Explain the improvements.
"""
    }

    return f"""
{SYSTEM_PROMPT}

TASK:
{instructions[mode]}

PROGRAMMING LANGUAGE:
{language}

USER REQUEST:
{question}

CODE:
```{language.lower()}
{code}
```

Respond with useful technical detail.
Use Markdown and fenced code blocks where appropriate.
"""

# ----------------------------
# Main Interface
# ----------------------------

left, right = st.columns([1, 1])

with left:
    st.subheader("💻 Your Code")

    code = st.text_area(
        "Paste your code here",
        height=350,
        placeholder="Paste your code or start writing..."
    )

    question = st.text_area(
        "What would you like CodePilot to do?",
        height=100,
        placeholder=(
            "Example: Explain this code and "
            "suggest a more efficient approach."
        )
    )

    submit = st.button(
        " Ask Gemma",
        type="primary",
        use_container_width=True
    )

with right:
    st.subheader("🤖 AI Response")

    if submit:

        if not code.strip() and not question.strip():
            st.warning(
                "Please provide code or a programming question."
            )

        else:
            prompt = build_prompt(
                mode,
                language,
                code,
                question
            )

            with st.spinner(
                "Gemma is analyzing your request..."
            ):

                try:
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.2,
                            max_output_tokens=4096
                        )
                    )

                    answer = response.text

                    if not answer:
                        answer = (
                            "Gemma returned an empty response. "
                            "Please try again."
                        )

                    st.markdown(answer)

                    st.session_state.messages.append({
                        "mode": mode,
                        "question": question,
                        "answer": answer
                    })

                    st.download_button(
                        "⬇️ Download Response",
                        data=answer,
                        file_name="codepilot_response.md",
                        mime="text/markdown"
                    )

                except Exception as e:
                    st.error(
                        "Gemma API request failed. "
                        "Check your API key, model access, "
                        "and internet connection."
                    )

                    st.caption(str(e))

    else:
        st.info(
            "Your AI-generated explanation, "
            "code, or review will appear here."
        )

# ----------------------------
# Conversation History
# ----------------------------

if st.session_state.messages:

    st.divider()

    st.subheader("🕘 Recent Activity")

    for item in reversed(st.session_state.messages[-5:]):

        with st.expander(
            f"{item['mode']} — {item['question'][:70]}"
        ):

            st.markdown(item["answer"])
