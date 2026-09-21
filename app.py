import streamlit as st
from huggingface_hub import InferenceClient

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Study Notes Generator",
    page_icon="📚",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("📚 AI Study Notes Generator")
st.write("Generate easy-to-understand study notes for any topic.")

# ---------------- INPUT ----------------
col1, col2 = st.columns([2, 1])

with col1:
    topic = st.text_area(
        "Enter Topic",
        placeholder="Example: Artificial Intelligence, DBMS, Python..."
    )

with col2:
    note_level = st.selectbox(
        "Difficulty Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

generate = st.button("✨ Generate Notes")

# ---------------- GENERATION ----------------
if generate:

    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        try:

            with st.spinner("Generating Notes..."):

                client = InferenceClient(
                    provider="auto",
                    api_key=st.secrets["HF_Token"]
                )

                prompt = f"""
Create study notes on:

Topic: {topic}

Level: {note_level}

Include:

1. Definition
2. Key Concepts
3. Advantages
4. Disadvantages
5. Applications
6. Conclusion

Use simple student-friendly language.
"""

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=2000
                )

                result = response.choices[0].message.content

            st.subheader("📖 Generated Notes")
            st.write(result)

        except Exception as e:
            st.error("Error occurred")
            st.exception(e)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("📚 AI Study Notes Generator")


   

           
