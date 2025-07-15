import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

def create_minimal_prompt(text: str) -> str:
    """
    Create a minimal, low-token prompt for Gemini to generate up to 3 Turkish labels for the given text.
    """
    return f"Metni etiketle. En fazla 3 kısa Türkçe etiket ver. Sadece JSON liste döndür: [\"etiket1\", ...]\n\n{text}"

def test_gemini_connection() -> bool:
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            return False
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-pro')
        response = model.generate_content("Test")
        return True
    except Exception:
        return False

def generate_labels_for_text(text: str) -> List[str]:
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            raise ValueError("GEMINI_API_KEY not found in .env file")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-pro')
        prompt = create_minimal_prompt(text)
        response = model.generate_content(prompt)
        raw_response = response.text.strip()
        import ast
        try:
            labels = ast.literal_eval(raw_response)
            if isinstance(labels, list):
                return labels[:3]
            else:
                return []
        except:
            # Fallback: try to extract labels from brackets
            import re
            match = re.search(r'\[(.*?)\]', raw_response)
            if match:
                items = [x.strip().strip('"\'') for x in match.group(1).split(',') if x.strip()]
                return items[:3]
            return []
    except Exception as e:
        print(f"Error generating labels: {str(e)}")
        return []

def process_changed_json() -> List[Dict[str, Any]]:
    try:
        with open("changed.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        if not test_gemini_connection():
            raise RuntimeError("Gemini API connection failed. Please check your API key.")
        labeled_data = []
        for item in data:
            text = item.get("content", "")
            title = item.get("title", "")
            if text:
                labels = generate_labels_for_text(text)
                labeled_item = {
                    "title": title,
                    "content": text,
                    "labels": labels
                }
                labeled_data.append(labeled_item)
            else:
                labeled_item = {
                    "title": title,
                    "content": text,
                    "labels": []
                }
                labeled_data.append(labeled_item)
        with open("labeled_output.json", "w", encoding="utf-8") as f:
            json.dump(labeled_data, f, ensure_ascii=False, indent=2)
        return labeled_data
    except Exception as e:
        print(f"Error processing changed.json: {str(e)}")
        raise

if __name__ == "__main__":
    if test_gemini_connection():
        print("✅ Gemini API connection successful!")
        result = process_changed_json()
        print(f"✅ Processed {len(result)} items with labels")
    else:
        print("❌ Gemini API connection failed!") 