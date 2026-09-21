import streamlit as st
from huggingface_hub import InferenceClient

# Page Config
st.set_page_config(
    page_title="MCQ Generator",
    page_icon="📝"
)

st.title("📝 AI MCQ Generator")

# User Input
topic = st.text_input(
    "Enter Topic",
    placeholder="Python, DBMS, AI, Machine Learning..."
)

num_questions = st.selectbox(
    "Number of Questions",
    [5, 10, 15],
    index=0
)

# Generate Button
if st.button("Generate MCQs"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")

    else:
        try:

            # Read token from Streamlit Secrets
            HF_TOKEN = st.secrets["HF_TOKEN"]

            client = InferenceClient(
                api_key=HF_TOKEN
            )

            prompt = f"""
Generate {num_questions} MCQs on {topic}.

For each question:
- Give 4 options (A, B, C, D)
- Mention the correct answer
- Keep questions simple

Example:

Q1. What is Python?

A) Database
B) Programming Language
C) Browser
D) Operating System

Answer: B) Programming Language
"""

            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1500
            )

            result = response.choices[0].message.content

            st.subheader("Generated MCQs")
            st.write(result)

        except Exception as e:
            st.error(str(e))
