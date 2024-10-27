import os
import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI with API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Define prompt for the summarizer
prompt = """You are a YouTube Video summarizer. Summarize the provided transcript text into a concise summary within 250 words, highlighting key points."""

# Function to extract video ID from YouTube URL
def extract_video_id(youtube_video_url):
    if "watch?v=" in youtube_video_url:
        return youtube_video_url.split("watch?v=")[-1]
    elif "youtu.be/" in youtube_video_url:
        return youtube_video_url.split("youtu.be/")[-1]
    else:
        raise ValueError("Invalid YouTube URL format.")

# Function to retrieve transcript text from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = extract_video_id(youtube_video_url)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item["text"] for item in transcript_text])
        return transcript
    except Exception as e:
        raise e

# Function to generate summarized content based on the prompt
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit app interface
st.set_page_config(
        page_title="YouTube Summarizer",
)

st.title("YouTube Video Summarizer")

# Input for YouTube video URL
youtube_link = st.text_input("Enter YouTube URL:")

# Display video thumbnail if link is provided
if youtube_link:
    try:
        video_id = extract_video_id(youtube_link)
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    except ValueError as e:
        st.error(f"Error: {e}")

# Button to get summarized notes
if st.button("Get Summarized Notes"):
    try:
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            summary_text = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Summarized Notes")
            st.write(summary_text)
    except Exception as e:
        st.error(f"Error: {e}")
