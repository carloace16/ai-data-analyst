import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import io  # We need this to capture the output of `exec`
import sys # We need this to redirect the output

# --- Page Configuration ---
# Set the page to a wide layout for better data display
st.set_page_config(layout="wide")
st.title("🤖 AI-Powered Data Analyst")

# --- Google Gemini Configuration ---
try:
    # Get the API key from Streamlit's secret management
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # --- THIS IS THE FINAL FIX ---
    # Using the correct model name from your key's available list
    model = genai.GenerativeModel('models/gemini-pro-latest') 
    # --- END OF FIX ---
    
except KeyError:
    # This error happens if "GEMINI_API_KEY" isn't in secrets.toml
    st.error("GEMINI_API_KEY not found. Please set it in your .streamlit/secrets.toml file.")
    st.stop() # Stop the app if the key is missing
except Exception as e:
    # Catch any other errors during initialization
    st.error(f"Error configuring Google Gemini: {e}")
    st.stop()

# --- Data Loading ---
DATA_FILE = "recent-grads.csv"

# Use Streamlit's caching to load the data only once
@st.cache_data
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        st.error(f"Error: Data file not found at '{filepath}'")
        st.write("Please make sure `recent-grads.csv` is in the same folder as `app.py`.")
        return None

# Load the dataframe
df = load_data(DATA_FILE)

# --- Main App UI ---
# Only proceed if the data was successfully loaded
if df is not None:
    st.header("Chat with your data")
    st.write("Ask a question in plain English, and the AI will generate Python code to answer it.")

    # Get the list of column names for the AI prompt
    # This helps the AI know what fields it can work with
    column_names = df.columns.to_list()

    # --- Chat Input ---
    user_query = st.text_area("Your question:", placeholder="e.g., 'What are the top 5 majors with the highest median salary?'")

    if st.button("Generate and Run Code"):
        if user_query:
            # Show a spinner while the AI is working
            with st.spinner("🤖 AI is thinking..."):
                try:
                    # This is the "System Prompt" - our detailed instructions to the AI
                    system_prompt = f"""
                    You are an expert Python data analyst. Your task is to help a user analyze a pandas DataFrame.
                    The user will ask a question in plain English.
                    You will respond with a single, complete, runnable Python code snippet that uses the DataFrame to answer a question.
                    
                    Here are the rules you MUST follow:
                    1.  The DataFrame is already loaded and is named `df`.
                    2.  Your response must be ONLY the Python code. Do not include any text like "Here is the code:" or "```python" or any explanations.
                    
                    3.  You MUST use the `print()` function to output the final answer (e.g., `print(df.head())`, `print(f"Total majors: {len(df)}")`).
                    
                    4.  The pandas library is already imported as `pd`.
                    5.  Do not include any code for loading the data (e.g., `pd.read_csv`). The data is already in the `df` variable.
                    
                    Here is the list of available columns in the DataFrame `df`:
                    {column_names}
                    
                    Here is an example of a good response:
                    User Query: "How many majors are there in total?"
                    Your Response:
                    print(f"There are {len(df)} majors in total.")
                    
                    Here is another example:
                    User Query: "Show me the top 5 majors by median salary."
                    Your Response:
                    print(df.nlargest(5, 'Median')[['Major', 'Median']])
                    """
                    
                    # Combine the system prompt with the user's specific query
                    full_prompt = f"{system_prompt}\n\nUser Query: \"{user_query}\"\nYour Response:"
                    
                    # Call the Gemini API to generate the code
                    response = model.generate_content(full_prompt)
                    
                    # Clean the AI's response
                    generated_code = response.text.strip().replace("```python", "").replace("```", "")
                    
                    # Display the AI-generated code
                    st.subheader("AI-Generated Code:")
                    st.code(generated_code, language="python")
                    
                    # --- THIS IS THE "MAGIC" PART ---
                    st.subheader("Analysis Result:")
                    
                    # Create a "fake" console to capture the print() output
                    output_capture = io.StringIO()
                    sys.stdout = output_capture
                    
                    try:
                        # Execute the AI's code. This is the "danger zone".
                        # We pass `df` into the execution scope
                        exec(generated_code, {'df': df, 'pd': pd})
                        
                        # Get the captured output
                        result = output_capture.getvalue()
                        
                        # Display the result
                        if result:
                            st.text(result)
                        else:
                            st.warning("The code ran successfully, but produced no output.")
                            
                    except Exception as e_exec:
                        # This catches any error *from the AI's code*
                        st.error(f"Error executing the generated code:\n\n{e_exec}")
                    finally:
                        # Always reset the system output back to normal
                        sys.stdout = sys.__stdout__
                    # --- END OF THE NEW PART ---
                    
                except Exception as e_api:
                    # This catches errors from the AI API call
                    st.error(f"An error occurred while contacting the AI: {e_api}")
        else:
            st.warning("Please enter a question.")

    # --- Data Preview ---
    st.subheader("Data Preview (first 50 rows)")
    st.dataframe(df.head(50))

else:
    st.warning("Could not load data. The app cannot proceed.")

# --- Sidebar ---
st.sidebar.title("About")
st.sidebar.info(
    "This project is a conversational AI agent that can "
    "translate natural language queries into data analysis code."
    "\n\n"
    "Built for the Open Avenues Fellowship."
)

