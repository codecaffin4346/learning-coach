import streamlit as st
from transformers import pipeline
import pandas as pd
import plotly.express as px

# ✅ Page config
st.set_page_config(page_title="Learning Coach AI", layout="wide")

# ✅ Load Hugging Face pipelines
explanation_generator = pipeline("text-generation", model="gpt2")  # lightweight model
quiz_generator = pipeline("text-generation", model="gpt2")
flashcard_generator = pipeline("text-generation", model="gpt2")

# ✅ Styling (Optional)
st.markdown("""
    <style>
        .main {background-color: #F0F2F6;}
        h1 {color: #333333;}
    </style>
""", unsafe_allow_html=True)

# ✅ Flashcards
def generate_flashcards(topic):
    prompt = f"Create 5 simple one-line flashcards on the topic: {topic}."
    response = flashcard_generator(prompt, max_length=100, num_return_sequences=1)
    return response[0]['generated_text'].split('\n')

# ✅ Quiz
def generate_quiz(topic):
    prompt = f"Generate a 3-question MCQ quiz on the topic: {topic}. Include answers."
    result = quiz_generator(prompt, max_length=250, num_return_sequences=1)
    return result[0]["generated_text"]

# ✅ Explanation
def generate_content(topic):
    prompt = f"Explain the topic '{topic}' in simple terms for a beginner."
    result = explanation_generator(prompt, max_length=200, num_return_sequences=1)
    return result[0]["generated_text"]

# ✅ Progress Chart
def subject_progress():
    st.subheader("📊 Subject Progress")
    data = pd.DataFrame({
        "Subjects": ["Math", "Science", "English", "History"],
        "Completion %": [80, 65, 90, 70]
    })
    fig = px.bar(data, x="Subjects", y="Completion %", color="Subjects", text_auto=True)
    st.plotly_chart(fig)

# ✅ Study Planner
def study_planner():
    st.subheader("🗓️ Weekly Study Planner")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days:
        st.text_input(f"Plan for {day}", key=day)

# ✅ Pomodoro Timer
def pomodoro_timer():
    st.subheader("⏱️ Pomodoro Timer (25 min focus + 5 min break)")
    if st.button("Start Timer"):
        st.info("⏳ Timer started! Focus for 25 mins!")

# ✅ Main Interface
st.title("🤖 Personal AI Learning Coach")

nav = st.sidebar.radio("Go to", ["Home", "Generate Topic", "Flashcards", "Quiz", "Study Planner", "Progress Tracker", "Pomodoro"])

if nav == "Home":
    st.markdown("""
    ### 🌟 Welcome!
    This AI-powered coach helps you learn smarter:
    - Generate flashcards, quizzes & content
    - Track your weekly progress
    - Stay consistent with Pomodoro timers
    """)

elif nav == "Generate Topic":
    topic = st.text_input("📌 Enter Topic to Learn")
    if topic:
        with st.expander("📘 Content Explanation"):
            st.write(generate_content(topic))
        with st.expander("🧠 Flashcards"):
            for fc in generate_flashcards(topic):
                st.info(fc)
        with st.expander("🧪 Quiz"):
            st.write(generate_quiz(topic))

elif nav == "Flashcards":
    topic = st.text_input("🔖 Enter topic to generate flashcards")
    if topic:
        cards = generate_flashcards(topic)
        for c in cards:
            st.success(c)

elif nav == "Quiz":
    topic = st.text_input("🧪 Enter topic for quiz")
    if topic:
        st.code(generate_quiz(topic))

elif nav == "Study Planner":
    study_planner()

elif nav == "Progress Tracker":
    subject_progress()

elif nav == "Pomodoro":
    pomodoro_timer()
