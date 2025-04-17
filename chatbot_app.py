import streamlit as st
import pandas as pd
import os
from rapidfuzz import process

st.set_page_config(page_title="Smart FAQ Bot 🤖", layout="centered")

st.title("🤖 Smart FAQ Chatbot")
st.markdown("_Tanya apa pun! Aku akan semakin pintar seiring waktu._")

# Load atau buat faq.csv
if os.path.exists("faq.csv"):
    df = pd.read_csv("faq.csv")
else:
    df = pd.DataFrame(columns=["Question", "Answer"])
    df.to_csv("faq.csv", index=False)

# Siapkan dictionary
faq_dict = dict(zip(df['Question'].str.lower(), df['Answer']))
questions = list(faq_dict.keys())

# Fungsi pencocokan fuzzy
def find_best_match(query, choices, threshold=60):
    result = process.extractOne(query, choices, score_cutoff=threshold)
    return result[0] if result else None

# Logika chatbot
def get_bot_response(user_input):
    user_input = user_input.strip().lower()
    if user_input in faq_dict:
        return faq_dict[user_input]
    else:
        closest = find_best_match(user_input, questions)
        if closest:
            return f"Did you mean: **{closest}**?\n\n{faq_dict[closest]}"
        else:
            return None

# Antarmuka pengguna
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 You:", "")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    response = get_bot_response(user_input)
    if response:
        st.markdown(f"**🤖 Bot:** {response}")
    else:
        st.warning("Aku belum tahu jawabannya.")
        new_answer = st.text_input("Bantu ajarkan jawabannya?", key="teach")
        if new_answer:
            faq_dict[user_input.lower()] = new_answer
            questions.append(user_input.lower())
            df = pd.concat([df, pd.DataFrame([{"Question": user_input, "Answer": new_answer}])], ignore_index=True)
            df.to_csv("faq.csv", index=False)
            st.success("Terima kasih! Aku sudah simpan jawabannya.")
