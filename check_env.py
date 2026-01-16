import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Current Working Directory: {os.getcwd()}")
print("Sys Path:")
for p in sys.path:
    print(f"  {p}")

try:
    import google.generativeai as genai
    print("✅ google.generativeai IMPORTED SUCCESSFULLY")
    print(f"File: {genai.__file__}")
except ImportError as e:
    print(f"❌ FAILED to import google.generativeai: {e}")

try:
    import streamlit
    print("✅ streamlit IMPORTED SUCCESSFULLY")
except ImportError as e:
    print(f"❌ FAILED to import streamlit: {e}")
