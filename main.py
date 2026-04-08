import requests

API_KEY = "your_groq_api_key_here"

def summarize_text(text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": f"Summarize this:\n{text}"}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"

        result = response.json()
        return result['choices'][0]['message']['content']

    except Exception as e:
        return f"Something went wrong: {e}"


if __name__ == "__main__":
    print("=== AI Text Summarizer ===")
    text = input("Enter text to summarize:\n")

    if not text.strip():
        print("No input provided.")
    else:
        summary = summarize_text(text)
        print("\nSummary:\n")
        print(summary)
