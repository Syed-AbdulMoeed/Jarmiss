from dotenv import load_dotenv
from google import genai
from llama_index.core.tools import FunctionTool

load_dotenv()

def analyze_multimodal_file(file_path: str, question: str):
    """Uploads an image, audio, or video file to Gemini and asks a specific question"""
    client = genai.Client()
    try:
        # Upload file and get response from model
        uploaded_file = client.files.upload(file=file_path)
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=[question, uploaded_file]
        )

        # Delete file
        client.files.delete(name=uploaded_file.name)
        return response.text
    
    except Exception as e:
        return f"Failed to analyze file: {e}"


ans = analyze_multimodal_file("TaskFiles/shapes.jpg", "What are the colors of the shapes to the left and right of the blue rectangle")
print(ans)  