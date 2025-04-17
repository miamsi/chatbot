# chatbot_app.py
import streamlit as st
import pandas as pd
import difflib
import os

st.set_page_config(page_title="Smart FAQ Bot 🤖", layout="centered")

st.title("🤖 Smart FAQ Chatbot")
st.markdown("_Ask me anything! I'll get smarter over time._")

# Load or create faq.csv
if os.path.exists("faq.csv"):
    df = pd.read_csv("faq.csv")
else:
    df = pd.DataFrame(columns=["Question", "Answer"])
    df.to_csv("faq.csv", index=False)

# Build dictionary
faq_dict = dict(zip(df['Question'].str.lower(), df['Answer']))
questions = list(faq_dict.keys())

# Chat logic
def get_bot_response(user_input):
    user_input = user_input.strip().lower()
    if user_input in faq_dict:
        return faq_dict[user_input]
    else:
        close_matches = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.3)
        if close_matches:
            closest = close_matches[0]
            return f"Did you mean: **{closest}**?\n\n{faq_dict[closest]}"
        else:
            return None

# Chat interface
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 You:", "")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    response = get_bot_response(user_input)
    if response:
        st.markdown(f"**🤖 Bot:** {response}")
    else:
        st.warning("I don't know the answer to that yet.")
        new_answer = st.text_input("Can you teach me the answer?", "")
        if new_answer:
            # Save to memory
            faq_dict[user_input.lower()] = new_answer
            questions.append(user_input.lower())
            df = pd.concat([df, pd.DataFrame([{"Question": user_input, "Answer": new_answer}])], ignore_index=True)
            df.to_csv("faq.csv", index=False)
            st.success("Thanks! I've saved that.")

