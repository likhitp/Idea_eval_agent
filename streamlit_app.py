import streamlit as st # type: ignore
import sys
import io
import os
from contextlib import redirect_stdout
from crew import ProductDesign
from dotenv import load_dotenv

# Set environment variables from Streamlit secrets
def setup_environment():
    """Setup environment variables from .env file first, then Streamlit secrets as fallback"""
    # First try to load from .env file
    load_dotenv()
    
    # Get keys from environment (which now includes .env if it exists)
    openai_key = os.getenv("OPENAI_API_KEY")
    serper_key = os.getenv("SERPER_API_KEY")
    
    # If keys not in .env, try to get from Streamlit secrets
    if not openai_key:
        try:
            openai_key = st.secrets["OPENAI_API_KEY"]
        except:
            pass
    
    if not serper_key:
        try:
            serper_key = st.secrets["SERPER_API_KEY"]
        except:
            pass
            
    # Set the environment variables if found
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
    if serper_key:
        os.environ["SERPER_API_KEY"] = serper_key
        
    # Validate that we have both required keys
    if not openai_key or not serper_key:
        missing_keys = []
        if not openai_key:
            missing_keys.append("OPENAI_API_KEY")
        if not serper_key:
            missing_keys.append("SERPER_API_KEY")
            
        st.error(f"""
        Missing required API keys: {', '.join(missing_keys)}
        Please add them either in:
        1. A .env file in the project root:
        ```
        OPENAI_API_KEY=your-openai-key
        SERPER_API_KEY=your-serper-key
        ```
        OR
        2. .streamlit/secrets.toml:
        ```
        OPENAI_API_KEY = "your-openai-key"
        SERPER_API_KEY = "your-serper-key"
        ```
        """)
        st.stop()

# Setup environment at startup
setup_environment()

# Set page config
st.set_page_config(
    page_title="IKEA Innovation Assistant",
    page_icon="🏢",
    layout="wide"
)

# Custom CSS for IKEA branding
st.markdown("""
    <style>
    .stButton>button {
        background-color: #0051BA;
        color: white;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #003D8F;
        color: white;
    }
    .stButton>button:disabled {
        background-color: #FFDA1A !important;
        color: #333333 !important;
        cursor: not-allowed;
    }
    .title {
        color: #0051BA;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .subtitle {
        color: #333333;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .agent-conversation {
        font-family: monospace;
        white-space: pre-wrap;
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .loading-gif {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<h1 class="title">IKEA Innovation Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by AI Agents for Rapid Innovation Research</p>', unsafe_allow_html=True)

# Input section
st.markdown("### Enter Your Innovation Topic")
topic = st.text_area(
    "Describe your product concept or innovation idea in detail:",
    height=150,
    help="Enter a detailed description of your product concept, including key features, target audience, and objectives."
)

# Create a placeholder for the button
button_placeholder = st.empty()

# Run button with state handling
if button_placeholder.button("Generate Innovation Analysis", type="primary", disabled=False, key="generate_button"):
    if not topic:
        st.error("Please enter a topic before proceeding.")
    else:
        try:
            # Update button state to disabled
            button_placeholder.button("Processing...", type="primary", disabled=True, key="processing_button")
            
            # Create a progress container
            progress_container = st.empty()
            with progress_container:
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    st.info("AI agents have started working on this. It will take a few minutes.")
                    st.markdown(
                        """
                        <div class="loading-gif">
                            <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWZ5bmpuZXFsbTcydmg2YTRiY3c1N2czNWJnZTh3YzJxMGRqa3J4YyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Je0awPS61D0F5FP6QX/giphy.webp" 
                            alt="Loading..." width="700">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # Create output capture and conversation display
            output = io.StringIO()
            
            # Create a placeholder for real-time conversation
            with st.expander("View Detailed Agent Conversations", expanded=True):
                conversation_container = st.empty()
                
            # Run the analysis with output capture
            with redirect_stdout(output):
                inputs = {'topic': topic}
                crew_instance = ProductDesign()
                crew = crew_instance.crew()
                
                # Function to update conversation display
                def update_conversation():
                    current_output = output.getvalue()
                    if current_output:
                        conversation_container.text_area("", 
                            value=current_output,
                            height=600,
                            key="conversation"
                        )
                
                # Run the crew and update conversation
                results = crew.kickoff(inputs=inputs)
                update_conversation()

            # Clear the progress container
            progress_container.empty()

            # Reset button state
            button_placeholder.button("Generate Innovation Analysis", type="primary", disabled=False, key="reset_button")

            # Display the results
            st.markdown("### Analysis Results")
            
            try:
                # Get task outputs from the results
                task_outputs = results.tasks_output
                
                # Market Analysis
                st.markdown("#### 🎯 Market Analysis")
                st.markdown(task_outputs[0])
                
                # Technical Assessment
                st.markdown("#### 🔧 Technical Assessment")
                st.markdown(task_outputs[1])
                
                # Feasibility Evaluation
                st.markdown("#### 📊 Feasibility Evaluation")
                st.markdown(task_outputs[2])
                
            except Exception as e:
                st.error(f"Error displaying results: {str(e)}")
                st.error("Please check the crew output format.")

        except Exception as e:
            # Reset button state in case of error
            button_placeholder.button("Generate Innovation Analysis", type="primary", disabled=False, key="error_button")
            st.error(f"An error occurred: {str(e)}")
            st.error("Please check if the API keys are properly configured in the Streamlit secrets.")

# Footer with instructions
with st.sidebar:
    st.markdown("### How to Use")
    st.markdown("""
    1. Enter your innovation topic or product concept in the text area
    2. Click 'Generate Innovation Analysis'
    3. View the detailed agent conversations
    4. Review the comprehensive analysis reports
    5. Sample test ideas: https://docs.google.com/document/d/1qw0Bwih0KgwpgqUnNftWF-F5pqYjBj8MjT6ATKpEEZw/edit?usp=sharing
    """)
    st.markdown("### Feedback")
    st.markdown("""
    If you have ideas on how to improve this tool or have any feedback, please let me know: leo.parameshwarappa@hyperisland.se
    """)

    
    st.markdown("### About")
    st.markdown("""
    This tool leverages AI agents to perform:
    - Market Analysis
    - Technical Assessment
    - Feasibility Evaluation
    
    Perfect for rapid innovation research and concept validation.   
    """) 