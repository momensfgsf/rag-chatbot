import google.generativeai as genai
import os

# Load API key from secrets file manually since we aren't in streamlit
import toml
try:
    secrets = toml.load(".streamlit/secrets.toml")
    api_key = secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    print("Listing available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error: {e}")
