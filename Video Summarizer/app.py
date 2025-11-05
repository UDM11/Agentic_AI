import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file, get_file
import google.generativeai as genai


import time
from pathlib import Path


import tempfile 

from dotenv import load_dotenv
load_dotenv()

import os


API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)


# page configuration
st.set_page_config(
    page_title="Multimodal AI Agent - Video Summarizer",
    page_icon="🎥",
    layout = "wide"
)

st.title("Phidata Video Summarizer Agent 🎥")
st.header("Powered by Gemini 2.0 flash Exp")


@st.cache_resource
def initialize_agent():
    return Agent(
        name="Video AI Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True
    )


# initialize the agent5
multimodal_Agent = initialize_agent()

# file uploader
video_file = st.file_uploader(
    "Upload a video file", type = ["mp4", "mov", "avi"], help = "UPload a video for AI analysis"
)


if video_file:
    with tempfile.NamedTemporaryFile(delete = False, suffix = '.mp4') as temp_video:
        temp_video.write(video_file.read())
        video_path = temp_video.name

        st.video(video_path, format="video/mp4", start_time = 0)


        user_query = st.text_area(
            "What insights are you seeking form the video?",
            placeholder="Ask anything about the video conitent. The AI agent will anlyze and gather additional info if needed.",
            help = "Provide specific questions or insights you weant from the video."
        )


        if st.button("Analyze Video", key="analyze_video_button"):
            if not user_query:
                st.warning("Please enter a question or insight to analyze the video.")

            else:
                try:
                    with st.spinner("Processing video and gathering insights..."):
                        # upload and process the video file
                        processed_video = upload_file(video_path)
                        while processed_video.state.name == "PROCESSING":
                            time.sleep(1)
                            processed_video = get_file(processed_video.name)

                        # prompt generation for analysis
                        analysis_prompt = (
                            f"""
                            Analyze the uploaded video for content and context.
                            Respond to the following query video insights and supplementary web research if necessary:
                            {user_query}

                            Provide a detailed, user-friendly, and actionable response.
                            """
                        )


                        # Ai agent processing
                        response = multimodal_Agent.run(analysis_prompt, videos=[processed_video])


                    # display the result
                    st.subheader("Analysis Results:")
                    st.markdown(response.content)
                

                except Exception as error:
                    st.error(f"An error occured during analysis: {error}")

                finally:
                    # clean up temporary video file
                    Path(video_path).unlink(missing_ok=True)
        
else:
    st.info("Upload a video file to begin analysis.")


# customize text area height
st.markdown(
    """
    <style>
    .stTextArea textarea {
        height: 200px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)