import streamlit as st
import requests
import json
import base64
import os
from dotenv import load_dotenv  # NEW

# === LOAD ENVIRONMENT VARIABLES ===
load_dotenv()  # NEW
#WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # NEW
WEBHOOK_URL = "https://hook.relay.app/api/v1/playbook/cmdytp9cl0n1a0om72rgb3jol/trigger/ULUcLdOiZrfdaDLDwqQRCg"


# === STREAMLIT PAGE CONFIGURATION ===
st.set_page_config(
    page_title="Smart Calendar Agent",
    page_icon="🗓️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# === CUSTOM CSS FOR A BETTER LOOK ===
st.markdown("""
<style>
/* A light, soothing background */
.stApp {
    background-color: #F0F2F6; 
    color: #333333;
}
/* Main container styling with a clean, rounded look */
.main .block-container {
    background-color: #FFFFFF;
    border-radius: 15px;
    padding: 3rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); /* Soft shadow for depth */
}
/* Header styling */
h1, h2, h3 {
    color: #2C3E50; /* Dark blue for a professional feel */
}
/* Paragraph text */
p {
    font-size: 1.1rem;
    color: #555555;
}
/* Text area styling */
.stTextArea textarea {
    background-color: #F9F9FB;
    border: 2px solid #BDC3C7; /* Subtle border */
    border-radius: 8px;
    padding: 10px;
    color: #333;
    font-size: 1rem;
}
/* Button styling */
.stButton > button {
    background-color: #3498DB; /* A nice, vibrant blue */
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    border: none;
    transition: background-color 0.3s;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.stButton > button:hover {
    background-color: #2980B9; /* Darker blue on hover */
    color: white;
}
/* Alert boxes */
.stAlert {
    border-radius: 8px;
}
.stSuccess {
    background-color: #DFF0D8;
    color: #277943;
    border-color: #D6E9C6;
}
.stError {
    background-color: #F2DEDE;
    color: #A94442;
    border-color: #EBCCD1;
}
.stWarning {
    background-color: #FCF8E3;
    color: #8A6D3B;
    border-color: #FAEBCC;
}
</style>
""", unsafe_allow_html=True)

# === APP CONTENT ===
st.title("🗓️ Smart Calendar Agent")
st.write("Hello! I'm your personal assistant for scheduling events. Just tell me what you want to do in natural language, and I'll add it to your Google Calendar.")

# Create a text area for user input
user_input = st.text_area(
    "What's on your mind? 👇",
    placeholder="e.g., Schedule a 30-minute meeting with the team on Tuesday at 10 AM.",
    height=150
)

# Use a container to hold the button and spinner
col1, col2 = st.columns([1, 4])
with col1:
    submit_button = st.button("🚀 Submit to Agent")

# Handle the button click
if submit_button:
    if not user_input:
        st.warning("⚠️ Please enter a request before submitting.")
    else:
        with st.spinner("Processing your request... Please wait a moment."):
            # Prepare the data payload
            payload = {
                "email_body": user_input
            }

            try:
                # Send the POST request to the webhook
                response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

                # Check for a successful response
                if response.status_code == 200:
                    st.success("🎉 Success! Your request has been sent to the agent. Check your calendar and email for the new event.")
                else:
                    st.error(f"❌ Oops! The agent returned an error: {response.status_code}.")
                    st.write("Please check the webhook URL and your Relay.app workflow settings.")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Failed to connect to the agent. Error: {e}")
                st.write("Please ensure the webhook URL is correct and the Relay.app workflow is active.")
