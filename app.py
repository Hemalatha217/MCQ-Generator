import streamlit as st
from huggingface_hub import InferenceClient

# Page Config
st.set_page_config(
    page_title="AI Interview Question Generator",
    page_icon="🎤",
    layout="wide"
)

# Header
st.title("🎤 AI Interview Question Generator")
st.write("Generate interview questions for any technology or job role.")

# Input
col1, col2 = st.columns([2,1])

with col1:
    topic = st.text_area(
        "Enter Technology / Job Role",
        placeholder="Example: Python, Data Analyst, DBMS, Machine Learning..."
    )

with col2:
    level = st.selectbox(
        "Difficulty Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

generate = st.button("Generate Questions")

if generate:

    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        try:

            client = InferenceClient(
                api_key=st.secrets["HF_Token"]
            )

            prompt = f"""
Generate 10 interview questions on {topic}.

Difficulty Level: {level}

Requirements:
- Number each question.
- Include only questions.
- No answers.
- Suitable for technical interviews.
"""

            response = client.chat.completions.create(
                model="Qwen/Qwen2.5-7B-Instruct",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1500
            )

            result = response.choices[0].message.content

            st.subheader("Generated Interview Questions")
            st.write(result)

        except Exception as e:
            st.error("Error occurred")
            st.exception(e)
