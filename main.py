import requests
from PyPDF2 import PdfReader

# Replace with your actual API key (locally only)
API_KEY = "your_groq_api_key"


# Extract text from PDF
def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    except Exception as e:
        return f"Error reading PDF: {e}"


#  Summarization function
def summarize_text(text, style_prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": f"""
You are an AI assistant that processes documents.

{style_prompt}

Make the output clean and readable.

Text:
{text}
"""
            }
        ],
        "max_tokens": 400
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"

        result = response.json()
        return result['choices'][0]['message']['content']

    except Exception as e:
        return f"Something went wrong: {e}"


#  MAIN PROGRAM
if __name__ == "__main__":
    print("=== AI Document Processing Tool ===")

    # Input selection
    print("\nChoose input type:")
    print("1. Enter text")
    print("2. Upload PDF")

    choice = input("Enter 1 or 2: ")

    if choice == "1":
        text = input("Enter text:\n")

    elif choice == "2":
        file_path = input("Enter PDF file path: ")
        text = extract_text_from_pdf(file_path)

    else:
        print("Invalid choice")
        exit()

    # Style selection
    print("\nChoose summary style:")
    print("1. Short summary")
    print("2. Bullet points")
    print("3. Detailed explanation")

    style_choice = input("Enter 1, 2, or 3: ")

    if style_choice == "1":
        style_prompt = "Give a very short and concise summary."
    elif style_choice == "2":
        style_prompt = "Summarize in clear bullet points."
    elif style_choice == "3":
        style_prompt = "Give a detailed and well-explained summary."
    else:
        print("Invalid choice, defaulting to short summary.")
        style_prompt = "Give a short summary."

    # Final processing
    if not text.strip():
        print("No input provided.")
    else:
        summary = summarize_text(text, style_prompt)
        print("\nSummary:\n")
        print(summary)
