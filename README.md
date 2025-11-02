# 🤖 AI-Powered Data Analyst

This project is a web-based, conversational AI agent created for the Open Avenues "AI-Powered Data Exploration" fellowship. It's an intelligent assistant that allows users to analyze a dataset using plain English instead of complex Python code.

The agent uses Google's Gemini AI to translate natural language queries into executable pandas code, which is then run in a secure environment to generate answers, tables, and analyses in real-time.

## 🧠 Project Design & Fellowship Concepts

This project directly implements the advanced **"CodeAgent"** pattern explored in Workshop 5.

While the initial workshops explored a ReAct agent with a limited set of 9 pre-defined tools (like `filter_rows`, `aggregate_by`), this approach had limitations in chaining operations (as seen in the W5 "79.00 vs 84.77" error).

This project implements the more powerful solution: **a single-step CodeAgent.**

- **💻 Code Generation:** Instead of relying on limited tools, the agent is given a "system prompt" that teaches it to write raw, complete pandas code to answer the user's entire query in one go.
- **🧩 Safe Execution:** The generated code is run using `exec()` inside a `try...except` block, and the `print()` output is captured and displayed to the user.
- **🗂️ UI as Memory:** Instead of a complex `SimpleMemory` class (W6), the Streamlit chat interface _is_ the memory. The user can see their entire analysis history, encouraging them to ask complete, self-contained questions rather than relying on pronouns like "that" or "it."

## ✨ Features

- **🌐 Full Web UI:** Built with Streamlit for a clean, interactive user experience.
- **🗣️ Natural Language to Code:** Translates questions like "What are the top 5 majors by median salary?" into `print(df.nlargest(5, 'Median')[['Major', 'Median']])`.
- **🛡️ Secure Code Execution:** Uses a `try...except` block to catch and display any errors from the AI's code without crashing the app.
- **👀 Data Preview:** The agent is "aware" of the dataset's columns and displays the first 50 rows for user reference.

## Dataset: Recent College Graduates

This project uses the `recent-grads.csv` dataset, which was originally published by FiveThirtyEight.

- **Source:** [FiveThirtyEight's GitHub](https://github.com/fivethirtyeight/data/tree/master/college-majors)
- **Content:** Contains data on job outcomes for students who graduated from college between 2010 and 2012.
- **Key Columns:** `Major`, `Major_category`, `Employed`, `Unemployed`, `Median` (salary), `Unemployment_rate`, etc.

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone [https://github.com/YOUR_USERNAME/ai-data-analyst.git](https://github.com/YOUR_USERNAME/ai-data-analyst.git)
cd ai-data-analyst
```

(Remember to replace `YOUR_USERNAME` with your actual GitHub username!)

### 2. Create and Activate Virtual Environment

### On Windows (Git Bash / MINGW64):

```
# Create the venv
python -m venv venv

# Activate it
source venv/Scripts/activate
```

### On macOS / Linux:

```
# Create the venv
python3 -m venv venv

# Activate it
source venv/bin/activate
```

### 3. Install Dependencies

All required libraries are listed in `requirements.txt.`

```
(venv) $ pip install -r requirements.txt
```

### 4. Set Up Your API Key (⚠️CRITICAL)

This project uses Google's Gemini AI, which requires an API key. We use Streamlit's built-in secrets manager to keep it secure.

1. Get your free API key from [**Google AI Studio**](https://aistudio.google.com/).

2. In the project's root folder (ai_data_analyst/), create a new folder named .streamlit.

3. Inside that .streamlit folder, create a new file named secrets.toml.

4. Open secrets.toml and add the following line, pasting your API key inside the quotes:

```
GEMINI_API_KEY = "YOUR_API_KEY_GOES_HERE"
```

### How to Run the Agent

1. Make sure your virtual environment (venv) is active.

2. Run the Streamlit app from your terminal:

```
(venv) $ streamlit run app.py
```

3. This will automatically open the application in your web browser `(usually at http://localhost:8501).`

### 🚀 How to Use the App

1. The app will load the recent-grads.csv file and display a preview.

2. Type a question about the data into the text box labeled "Your question:".

3. Click the "Generate and Run Code" button.

4. The app will show:

- AI-Generated Code: The exact Python/pandas code the AI wrote.

- Analysis Result: The print() output from running that code (i.e., your answer).

#### Example Questions to Try:

- `Show me the Employed and Unemployed numbers for 'COMPUTER SCIENCE'`

- `What are the top 5 majors with the highest median salary?`

- `How many majors are in the 'Engineering' category?`

- `What is the average median salary for all majors?`

- `Show me the Major and Unemployment_rate for majors with an unemployment rate less than 0.05`
