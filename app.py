import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(
    page_title="MCQ Generator",
    page_icon="📝"
)

st.title("📝 AI MCQ Generator")

topic = st.text_area(
    "Enter Topic",
    placeholder="Example: Python, DBMS, Artificial Intelligence"
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

            client = InferenceClient(
                provider="auto",
                api_key="YOUR_HUGGINGFACE_TOKEN"
            )

            prompt = f"""
Generate exactly {num_questions} multiple-choice questions on {topic}.

Rules:
- Number each question.
- Give 4 options (A, B, C, D).
- Mention the correct answer.
- Avoid duplicate questions.

Format:

Question 1:
A)
B)
C)
D)

Answer:
"""

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2000
            )

            result = response.choices[0].message.content

            st.subheader("Generated MCQs")
            st.write(result)

        except Exception as e:
            st.error("Error occurred")
            st.exception(e)

           
