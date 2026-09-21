import streamlit as st
from huggingface_hub import InferenceClient

# Page Config
st.set_page_config(
    page_title="MCQ Generator",
    page_icon="📝"
)

st.title("📝 AI MCQ Generator")

# Input
topic = st.text_input(
    "Enter Topic",
    placeholder="Python, DBMS, AI, Machine Learning..."
)

num_questions = st.selectbox(
    "Number of Questions",
    [5, 10, 15],
    index=0
)

if st.button("Generate MCQs"):

    if not topic.strip():
        st.warning("Please enter a topic.")

    else:
        try:

            # Read token from Streamlit Secrets
            HF_TOKEN = st.secrets["HF_TOKEN"]

            client = InferenceClient(
                api_key=HF_TOKEN
            )

            prompt = f"""
Generate {num_questions} multiple-choice questions on {topic}.

For each question:
- Give exactly 4 options (A, B, C, D)
- Mention the correct answer
- Keep questions simple and educational

Format:

Q1. Question

A)
B)
C)
D)

Answer:
"""

            response = client.chat.completions.create(
                model="Qwen/Qwen3-4B-Thinking-2507",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1500
            )

            result = response.choices[0].message.content

            st.subheader("📋 Generated MCQs")
            st.write(result)

        except Exception as e:
            st.error(f"Error: {e}")
