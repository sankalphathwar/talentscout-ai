import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
import google.generativeai as genai
from textblob import TextBlob

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Gemini API Key

# Streamlit Page Config
st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main-title {
        font-size: 30px;
        font-weight: bold;
        color: #2C3E50;
        text-align: center;
    }
    .stButton>button {
        background-color: #3498DB;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 8px 15px;
        border: none;
    }
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        border-radius: 8px;
        padding: 10px;
        border: 1px solid #BDC3C7;
    }
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Page Title
st.markdown('<p class="main-title">🤖 TalentScout Hiring Assistant</p>', unsafe_allow_html=True)
st.write("🚀 **AI-powered hiring assistant** - Streamline your interview process!")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to generate technical interview questions
def generate_tech_questions(tech_stack):
    if not tech_stack.strip():
        return "⚠ Please provide a valid tech stack."
    
    prompt = f"Generate 3-5 technical interview questions for a candidate proficient in {tech_stack}."
    
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(prompt)
        return response.text if response.text else "⚠ Unable to generate questions."
    
    except Exception as e:
        return f"⚠ Error: {str(e)}"

# Function to analyze sentiment of responses
def analyze_sentiment(response_text):
    analysis = TextBlob(response_text)
    return "Positive 😊" if analysis.sentiment.polarity > 0 else "Negative 😞" if analysis.sentiment.polarity < 0 else "Neutral 😐"

# Candidate Form
with st.form("candidate_form"):
    st.subheader("📝 Candidate Information")

    col1, col2 = st.columns(2)

    with col1:
        full_name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)

    with col2:
        desired_position = st.text_input("Desired Position")
        location = st.text_input("Current Location")
        tech_stack = st.text_area("Tech Stack (e.g., Python, Django, MySQL)")

    submit_button = st.form_submit_button("Submit")

if submit_button:
    if full_name and email and phone and tech_stack:
        st.success(f"Generating questions for {desired_position} role...")

        # Generate technical questions
        tech_questions = generate_tech_questions(tech_stack)

        # Save data to session state
        st.session_state.messages.append({
            "name": full_name, "email": email, "phone": phone, "experience": experience,
            "position": desired_position, "location": location, "tech_stack": tech_stack,
            "questions": tech_questions
        })

        # Display questions
        st.subheader("📌 Technical Interview Questions")
        st.write(tech_questions)

        # Sentiment Analysis
        st.subheader("📊 Sentiment Analysis of Responses")
        candidate_response = st.text_area("Candidate's Answer (Optional)")
        if candidate_response:
            sentiment_result = analyze_sentiment(candidate_response)
            st.write(f"Sentiment: {sentiment_result}")

    else:
        st.warning("⚠ Please fill out all required fields.")

# Display previous conversations
if st.session_state.messages:
    st.subheader("🗂️ Previous Conversations")
    df = pd.DataFrame(st.session_state.messages)
    st.dataframe(df)
