#!/usr/bin/env python
import os
import sys
import warnings
import streamlit as st
from dotenv import load_dotenv

from crew import ProductDesign

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
            os.environ["OPENAI_API_KEY"] = openai_key
        except:
            pass
    
    if not serper_key:
        try:
            serper_key = st.secrets["SERPER_API_KEY"]
            os.environ["SERPER_API_KEY"] = serper_key
        except:
            pass
    
    # Check for required API keys
    missing_keys = []
    if not openai_key:
        missing_keys.append("OPENAI_API_KEY")
    if not serper_key:
        missing_keys.append("SERPER_API_KEY")
    
    if missing_keys:
        raise ValueError(
            f"Missing required API keys: {', '.join(missing_keys)}. "
            f"Please set them either in .env file or Streamlit secrets."
        )

# Initialize environment
setup_environment()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the IKEA product design innovation assessment crew.
    Example: Analyzing a smart modular furniture system with integrated storage and IoT capabilities.
    """
    inputs = {
        'topic': """Upcycling-as-a-Service for Used IKEA Furniture
        We are exploring the feasibility of a furniture upcycling service where customers can return their used IKEA furniture for refurbishment, redesign, or recycling. The upcycled items would either be resold or given back to the original owner after enhancement. The initiative targets eco-conscious customers and aligns with IKEA's sustainability goals. Key focus areas include promoting circular economy, minimizing waste, and creating a new revenue stream.
        Key Focus Areas:
        - Developing a scalable logistics process for furniture returns and refurbishment.
        - Leveraging modular design to ease the upcycling process.
        - Promoting customer incentives like discounts or loyalty programs for returned furniture."""
    }
    ProductDesign().crew().kickoff(inputs=inputs)

def train():
    """
    Train the crew for a given number of iterations.
    Usage: python -m product_design train <n_iterations> <output_filename>
    """
    inputs = {
        "topic": "Smart Modular Storage System"
    }
    try:
        ProductDesign().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    Usage: python -m product_design replay <task_id>
    """
    try:
        ProductDesign().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    Usage: python -m product_design test <n_iterations> <openai_model_name>
    """
    inputs = {
        "topic": "Smart Modular Storage System"
    }
    try:
        ProductDesign().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()
