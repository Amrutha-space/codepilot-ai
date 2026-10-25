# CodePilot AI — Use AI to Understand Code, Not Only to Write It!

### Your intelligent coding partner, powered by Google Gemma 4

We use AI to write code—why not understand it with the same AI?

**CodePilot AI** is a lightweight, AI-powered coding assistant designed to help developers understand, generate, debug, review, and improve code.

Built using Streamlit and Google's hosted Gemma API, CodePilot AI provides an interactive developer workspace for everyday programming tasks.

## Features

- **Explain Code:** Understand code with clear, step-by-step explanations.
- **Generate Code:** Create functions and programs from natural-language prompts.
- **Debug Code:** Identify errors and receive corrected code with explanations.
- **Review Code:** Find bugs, readability issues, security concerns, and potential performance improvements.
- **Improve Code:** Refactor code for better readability, maintainability, and efficiency.
- **Multi-language Support:** Work with Python, Java, JavaScript, C++, TypeScript, Go, SQL, and more.
- **Download Responses:** Export AI-generated explanations and code as Markdown files.

## Tech Stack

- Python
- Streamlit
- Google Gen AI SDK
- Google Gemma 4 (`gemma-4-26b-a4b-it`)

## Architecture

```text
User
  ↓
Streamlit Interface
  ↓
Google Gen AI SDK
  ↓
Gemma API
  ↓
AI-Generated Response
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Amrutha-space/codepilot-ai.git
cd codepilot-ai
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root and add your API key:

```env
GEMMA_API_KEY=your_api_key_here
```

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

Replace `your_api_key_here` with your actual key. Never share your API key or commit your `.env` file to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

## Security

- The API key is read from the `GEMMA_API_KEY` environment variable, with Streamlit secrets as a fallback.
- The `.env` file and `.streamlit/secrets.toml` should remain private.
- The project `.gitignore` excludes these sensitive files.

## Future Improvements

- Multi-turn conversational context
- Monaco code editor integration
- Streaming AI responses
- Secure code execution sandbox
- GitHub repository integration
- Automated unit test generation
- File upload and project-level code analysis

## Author

**ANNEPU AMRUTHA — Cracked Engineer**

Built as a hackathon project to explore practical applications of Google's Gemma models and AI-powered developer tools.
