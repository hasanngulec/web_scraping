import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_connection():
    """Test Gemini API connection"""
    try:
        # Get API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            print("❌ GEMINI_API_KEY not found or not set properly in .env file!")
            print("Please add your Gemini API key to .env file:")
            print("GEMINI_API_KEY=your_actual_api_key_here")
            return False
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Test with a simple prompt
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Hello, this is a test message. Please respond with 'API connection successful!'")
        
        print("✅ Gemini API connection successful!")
        print(f"Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini API connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini_connection() 